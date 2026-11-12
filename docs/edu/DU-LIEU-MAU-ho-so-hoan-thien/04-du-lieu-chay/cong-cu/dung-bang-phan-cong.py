"""Dựng bảng phân công (Excel, ảnh) và phiếu in từ đầu ra thật của chương trình.

Đầu vào : phan-cong-exampanel.csv, phan-cong-thu-cong.csv và dau-vao.json trong một thư mục chạy.
Đầu ra  : bang-phan-cong-*.xlsx, bang-phan-cong-*.png, phieu-in-<mã GV>.png (ghi vào thư mục đích).
Không tự gõ số: mọi ô lấy từ CSV do chương trình ExamPanel xuất.

Dùng:  python dung-bang-phan-cong.py <thư mục chạy> <thư mục đích> [mã GV ...]
"""
import csv
import json
import sys
from pathlib import Path

import xlsxwriter
from PIL import Image, ImageDraw, ImageFont

FONT = "C:/Windows/Fonts/arial.ttf"
FONT_B = "C:/Windows/Fonts/arialbd.ttf"
EXAMS = ["GK1", "CK1", "GK2", "CK2"]
EXAM_NAME = {"GK1": "Giữa kỳ 1", "CK1": "Cuối kỳ 1", "GK2": "Giữa kỳ 2", "CK2": "Cuối kỳ 2"}
EXAM_BG = {"GK1": (222, 235, 247), "CK1": (189, 215, 238), "GK2": (226, 239, 218), "CK2": (198, 224, 180)}
COLS = [(g, s) for g in (10, 11, 12) for s in ("VL", "CN")]
ROWS = [("Đề", "setter", 1), ("Đề", "setter", 2), ("P.Biện", "reviewer", 1)]
INK = (30, 30, 30)
MUTED = (110, 110, 110)


def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def load(path):
    cells = {}
    with open(path, encoding="utf8", newline="") as f:
        for r in csv.DictReader(f):
            cells[(r["exam"], int(r["grade"]), r["subject"], r["role"], int(r["slot"]))] = r["teacher"]
    return cells


def cell(cells, exam, col, row):
    g, s = col
    _, role, slot = row
    return cells.get((exam, g, s, role, slot), "")


def exams_in(cells):
    return [e for e in EXAMS if any(k[0] == e for k in cells)]


def seat_counts(cells, info):
    c = {code: 0 for code in info}
    for t in cells.values():
        c[t] = c.get(t, 0) + 1
    return c


def write_xlsx(cells, out, title, counts_pair=None, idle=()):
    wb = xlsxwriter.Workbook(str(out))
    ws = wb.add_worksheet("Phan cong")
    head = wb.add_format({"bold": True, "align": "center", "valign": "vcenter", "border": 1, "bg_color": "#F2F2F2"})
    body = wb.add_format({"align": "center", "valign": "vcenter", "border": 1})
    ws.merge_range(0, 0, 0, 8, title, wb.add_format({"bold": True, "font_size": 13}))
    ws.write(2, 0, "Kỳ thi", head)
    ws.write(2, 1, "Vai trò", head)
    for i, (g, s) in enumerate(COLS):
        ws.write(2, 2 + i, f"Khối {g} - {'Vật lí' if s == 'VL' else 'Công nghệ'}", head)
    r = 3
    for e in exams_in(cells):
        for row in ROWS:
            ws.write(r, 0, EXAM_NAME[e], body)
            ws.write(r, 1, row[0], body)
            for i, col in enumerate(COLS):
                ws.write(r, 2 + i, cell(cells, e, col, row), body)
            r += 1
    ws.set_column(0, 1, 14)
    ws.set_column(2, 7, 18)
    if idle:
        ws.write(r + 1, 0, f"Không có vị trí nào trong bảng này: {', '.join(idle)} ({len(idle)} giáo viên).")
    if counts_pair:
        w2 = wb.add_worksheet("So luot")
        for i, h in enumerate(("Mã GV", "Thủ công (số vị trí)", "ExamPanel (số vị trí)")):
            w2.write(0, i, h, head)
        for j, code in enumerate(counts_pair[0], 1):
            w2.write(j, 0, code, body)
            w2.write(j, 1, counts_pair[0][code], body)
            w2.write(j, 2, counts_pair[1][code], body)
        w2.set_column(0, 2, 22)
    wb.close()


def draw_matrix(cells, out, title, note):
    exams = exams_in(cells)
    cw, rh, lw, hh = 118, 44, 190, 44
    w = lw + cw * len(COLS) + 40
    h = 110 + hh * 2 + rh * 3 * len(exams) + 80
    im = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(im)
    d.text((20, 18), title, font=font(24, True), fill=INK)
    y0 = 70
    d.rectangle([20, y0, 20 + lw, y0 + hh * 2], outline=INK)
    d.text((30, y0 + 30), "Kỳ thi / khối", font=font(18, True), fill=INK)
    for gi, g in enumerate((10, 11, 12)):
        x = 20 + lw + gi * 2 * cw
        d.rectangle([x, y0, x + 2 * cw, y0 + hh], outline=INK)
        d.text((x + cw - 14, y0 + 10), str(g), font=font(20, True), fill=INK)
        for si, s in enumerate(("VL", "CN")):
            xx = x + si * cw
            d.rectangle([xx, y0 + hh, xx + cw, y0 + hh * 2], fill=(252, 228, 214) if s == "VL" else (255, 242, 204), outline=INK)
            d.text((xx + cw // 2 - 12, y0 + hh + 10), s, font=font(18, True), fill=INK)
    y = y0 + hh * 2
    for e in exams:
        bg = EXAM_BG[e]
        for ri, row in enumerate(ROWS):
            d.rectangle([20, y, 20 + lw, y + rh], fill=bg, outline=INK)
            if ri == 1:
                d.text((40, y + 10), e, font=font(20, True), fill=INK)
            d.text((130, y + 12), row[0], font=font(18), fill=INK)
            for ci, col in enumerate(COLS):
                x = 20 + lw + ci * cw
                d.rectangle([x, y, x + cw, y + rh], fill=bg, outline=INK)
                v = cell(cells, e, col, row)
                if v:
                    d.text((x + cw // 2 - 22, y + 12), v, font=font(18, True), fill=INK)
            y += rh
    d.text((20, y + 14), note, font=font(15), fill=MUTED)
    im.save(out)


def teacher_info(run_dir):
    inp = json.loads((run_dir / "dau-vao.json").read_text(encoding="utf8"))
    return {t["code"]: t for t in inp["teachers"]}


def draw_slip(cells, info, code, out, year):
    mine = []
    for (e, g, s, role, slot), t in cells.items():
        if t != code:
            continue
        mates = sorted({u for (e2, g2, s2, r2, sl2), u in cells.items() if (e2, g2, s2) == (e, g, s) and u != code})
        mine.append((EXAMS.index(e), g, s, role, e, mates))
    mine.sort()
    w, rowh = 900, 36
    h = 250 + rowh * (len(mine) + 1)
    im = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(im)
    d.rectangle([10, 10, w - 10, h - 10], outline=INK, width=2)
    d.text((40, 30), "PHIẾU THÔNG BÁO NHIỆM VỤ RA ĐỀ", font=font(26, True), fill=INK)
    d.text((40, 70), f"Năm học {year}", font=font(18), fill=MUTED)
    d.text((40, 110), f"Mã giáo viên: {code}", font=font(22, True), fill=INK)
    d.text((40, 145), f"Phân hiệu: {info[code]['campus']}   ·   Tổng số lượt nhiệm vụ: {len(mine)}", font=font(18), fill=INK)
    y = 190
    for x, label in ((40, "Kỳ"), (200, "Khối"), (300, "Môn"), (460, "Vai trò"), (620, "Cùng ban")):
        d.text((x, y), label, font=font(17, True), fill=INK)
    d.line([40, y + 28, w - 40, y + 28], fill=INK)
    y += 36
    for _, g, s, role, e, mates in mine:
        d.text((40, y), EXAM_NAME[e], font=font(17), fill=INK)
        d.text((200, y), str(g), font=font(17), fill=INK)
        d.text((300, y), "Vật lí" if s == "VL" else "Công nghệ", font=font(17), fill=INK)
        d.text((460, y), "Ra đề" if role == "setter" else "Phản biện", font=font(17), fill=INK)
        d.text((620, y), ", ".join(mates), font=font(17), fill=INK)
        y += rowh
    im.save(out)


def main():
    run_dir, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    codes = sys.argv[3:]
    out_dir.mkdir(parents=True, exist_ok=True)
    info = teacher_info(run_dir)
    plan = load(run_dir / "phan-cong-exampanel.csv")
    manual = load(run_dir / "phan-cong-thu-cong.csv")
    tag = run_dir.name
    n = len(info)
    scope = "cả năm" if len(exams_in(plan)) == 4 else exams_in(plan)[0]
    cm, cp = seat_counts(manual, info), seat_counts(plan, info)
    pair = (cm, cp)
    idle_m = [c for c in info if cm[c] == 0]
    idle_p = [c for c in info if cp[c] == 0]
    write_xlsx(plan, out_dir / f"bang-phan-cong-exampanel-{tag}.xlsx", f"Bảng phân công do ExamPanel đề xuất ({n} giáo viên, {scope})", pair, idle_p)
    write_xlsx(manual, out_dir / f"bang-phan-cong-thu-cong-{tag}.xlsx", f"Bảng phân công thủ công đã số hoá ({n} giáo viên, {scope})", pair, idle_m)
    note = "Nguồn: phan-cong-exampanel.csv, đầu ra của chương trình ExamPanel (seed 42, 8 lượt, 200000 vòng)."
    draw_matrix(plan, out_dir / f"bang-phan-cong-exampanel-{tag}.png", f"Phương án ExamPanel · {n} giáo viên · {scope}", note)
    draw_matrix(manual, out_dir / f"bang-phan-cong-thu-cong-{tag}.png", f"Bảng thủ công đã số hoá · {n} giáo viên · {scope}",
                "Nguồn: phan-cong-thu-cong.csv, số hoá từ bảng trong biên bản họp Tổ, tên thay bằng mã. "
                + (f"Không có vị trí: {', '.join(idle_m)} ({len(idle_m)} giáo viên)." if idle_m else ""))
    for c in codes:
        draw_slip(plan, info, c, out_dir / f"phieu-in-{c}-{tag}.png", "2026–2027")
    print("xong", tag, len(plan), len(manual))


if __name__ == "__main__":
    main()

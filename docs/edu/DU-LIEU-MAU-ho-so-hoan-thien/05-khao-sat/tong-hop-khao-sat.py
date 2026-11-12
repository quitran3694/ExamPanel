"""Tổng hợp khảo sát: bảng theo câu, biểu đồ phân bố, trích nhận xét.

Dùng cho cả dữ liệu thật lẫn dữ liệu minh hoạ. Mọi số do script tính, không gõ tay.

Dùng:
  python tong-hop-khao-sat.py <ket-qua.csv> [--gui <so-gui-phieu.csv>] [--chon P01,P05,...] [--out <thư mục>]

Tệp CSV: cột ma, q1..q6 (1–5), y_kien_tot, y_kien_cai_thien.
Nếu dòng đầu của CSV bắt đầu bằng "DỮ LIỆU MINH HOẠ" thì dòng đó được bỏ qua khi đọc,
tên tệp ra có hậu tố -DU-LIEU-MINH-HOA và biểu đồ có chú thích cùng nội dung.
"""
import argparse
import csv
import statistics
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

LABEL = "DỮ LIỆU MINH HOẠ, không phải số liệu thực địa"
QUESTIONS = [
    ("q1", "Bảng phân công rõ ràng, dễ hiểu"),
    ("q2", "Phân công công bằng giữa các giáo viên"),
    ("q3", "Tiết kiệm thời gian hơn xếp bằng bảng tính"),
    ("q4", "Phần mềm và phiếu in dễ sử dụng"),
    ("q5", "Sẵn sàng tiếp tục dùng cho các kỳ sau"),
    ("q6", "Tin cậy kết quả phân công"),
]
# Thang đỏ cam – xám – xanh, phân biệt được cả khi in đen trắng nhờ độ đậm khác nhau.
COLORS = {1: (178, 24, 43), 2: (239, 138, 98), 3: (200, 200, 200), 4: (103, 169, 207), 5: (33, 102, 172)}


def font(size, bold=False):
    return ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf", size)


def read_csv(path):
    text = Path(path).read_text(encoding="utf8").splitlines()
    minh_hoa = text[0].startswith("DỮ LIỆU MINH HOẠ")
    if minh_hoa:
        text = text[1:]
    return list(csv.DictReader(text)), minh_hoa


def summarize(rows):
    out = []
    for key, label in QUESTIONS:
        vals = [int(r[key]) for r in rows]
        counts = {k: vals.count(k) for k in range(1, 6)}
        out.append({
            "key": key, "label": label, "n": len(vals), "counts": counts,
            "mean": statistics.mean(vals),
            "sd": statistics.stdev(vals) if len(vals) > 1 else 0.0,
            "agree": 100.0 * (counts[4] + counts[5]) / len(vals),
        })
    return out


def markdown(stats, rows, sent, minh_hoa):
    lines = []
    if minh_hoa:
        lines += [LABEL, ""]
    lines += ["# Tổng hợp khảo sát ý kiến về bảng phân công ra đề", ""]
    if sent:
        lines += [f"- Phiếu gửi: {sent}. Phiếu trả lời: {len(rows)}. Không phản hồi: {sent - len(rows)}. "
                  f"Tỉ lệ trả lời: {100.0 * len(rows) / sent:.1f}%.", ""]
    lines += ["| Câu | Nội dung | n | Mức 1 | Mức 2 | Mức 3 | Mức 4 | Mức 5 | Trung bình | Độ lệch chuẩn | Đồng ý (4–5) |",
              "| :-: | :-- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |"]
    for i, s in enumerate(stats, 1):
        c = s["counts"]
        lines.append(f"| {i} | {s['label']} | {s['n']} | {c[1]} | {c[2]} | {c[3]} | {c[4]} | {c[5]} | "
                     f"{s['mean']:.2f} | {s['sd']:.2f} | {s['agree']:.1f}% |")
    allv = [int(r[k]) for r in rows for k, _ in QUESTIONS]
    agree = 100.0 * sum(1 for v in allv if v >= 4) / len(allv)
    lines += ["", f"Trung bình chung 6 câu: {statistics.mean(allv):.2f}. Tỉ lệ đồng ý chung (4–5): {agree:.1f}%.",
              "Độ lệch chuẩn là độ lệch mẫu (chia n − 1).", ""]
    return "\n".join(lines)


def chart(stats, n, minh_hoa, path):
    left, bar_w, bar_h, gap = 410, 580, 34, 22
    w = left + bar_w + 150
    h = 130 + len(stats) * (bar_h + gap) + 90
    im = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(im)
    d.text((20, 18), "Phân bố mức độ đồng ý theo từng câu", font=font(24, True), fill=(30, 30, 30))
    d.text((20, 54), f"n = {n} phiếu trả lời. Thang 1 (rất không đồng ý) đến 5 (rất đồng ý).", font=font(16), fill=(90, 90, 90))
    lx = left
    for k in range(1, 6):
        d.rectangle([lx, 88, lx + 18, 106], fill=COLORS[k])
        d.text((lx + 24, 88), f"Mức {k}", font=font(15), fill=(60, 60, 60))
        lx += 95
    y = 124
    for i, s in enumerate(stats, 1):
        d.text((20, y + 6), f"{i}. {s['label']}", font=font(16), fill=(30, 30, 30))
        x = left
        for k in range(1, 6):
            seg = bar_w * s["counts"][k] / s["n"]
            if seg > 0:
                d.rectangle([x, y, x + seg, y + bar_h], fill=COLORS[k])
                if seg > 22:
                    d.text((x + seg / 2 - 5, y + 8), str(s["counts"][k]), font=font(15, True),
                           fill="white" if k in (1, 5) else (30, 30, 30))
            x += seg
        d.text((left + bar_w + 14, y + 6), f"TB {s['mean']:.2f}", font=font(16, True), fill=(30, 30, 30))
        y += bar_h + gap
    if minh_hoa:
        d.text((20, h - 34), LABEL, font=font(14), fill=(110, 110, 110))
    im.save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ket_qua")
    ap.add_argument("--gui")
    ap.add_argument("--chon", default="")
    ap.add_argument("--out")
    a = ap.parse_args()
    rows, minh_hoa = read_csv(a.ket_qua)
    out = Path(a.out) if a.out else Path(a.ket_qua).parent
    out.mkdir(parents=True, exist_ok=True)
    sfx = "-DU-LIEU-MINH-HOA" if minh_hoa else ""
    sent = len(read_csv(a.gui)[0]) if a.gui else None
    stats = summarize(rows)
    md = markdown(stats, rows, sent, minh_hoa)
    (out / f"tong-hop-khao-sat{sfx}.md").write_text(md, encoding="utf8")
    with open(out / f"tong-hop-khao-sat{sfx}.csv", "w", encoding="utf8", newline="") as f:
        w = csv.writer(f)
        if minh_hoa:
            f.write(LABEL + "\n")
        w.writerow(["cau", "noi_dung", "n", "muc1", "muc2", "muc3", "muc4", "muc5", "trung_binh", "do_lech_chuan", "ti_le_dong_y_4_5"])
        for i, s in enumerate(stats, 1):
            c = s["counts"]
            w.writerow([i, s["label"], s["n"], c[1], c[2], c[3], c[4], c[5], f"{s['mean']:.2f}", f"{s['sd']:.2f}", f"{s['agree']:.1f}"])
    chart(stats, len(rows), minh_hoa, out / f"bieu-do-khao-sat{sfx}.png")
    if a.chon:
        chosen = [c.strip() for c in a.chon.split(",") if c.strip()]
        by = {r["ma"]: r for r in rows}
        lines = ([LABEL, ""] if minh_hoa else []) + ["# Nhận xét tiêu biểu (ẩn danh)", ""]
        for c in chosen:
            r = by[c]
            lines.append(f"- **{c}**: tốt: “{r['y_kien_tot']}”" +
                         ("" if r["y_kien_cai_thien"].startswith("Chưa có") else f" Cần cải thiện: “{r['y_kien_cai_thien']}”"))
        (out / f"nhan-xet-tieu-bieu{sfx}.md").write_text("\n".join(lines) + "\n", encoding="utf8")
    print(md)


if __name__ == "__main__":
    main()

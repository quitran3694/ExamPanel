"""Bảng thống kê 19 giáo viên (mã hoá) và sơ đồ 19 → 17 → 12, dựng từ đầu vào mã hoá.

Nguồn: dau-vao.json của lượt 17 giáo viên (17 người tham gia ban ra đề) cùng ghi chú của đầu vào
về 2 cán bộ quản lí (GV18, GV19), không tham gia ban ra đề.
Dùng:  python tao-bang-19gv.py <dau-vao-17gv.json> <thư mục đích>
"""
import csv
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

EXAMS = ["GK1", "CK1", "GK2", "CK2"]
SUBJ = {"VL": "Vật lí", "CN": "Công nghệ"}


def font(size, bold=False):
    return ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf", size)


def main():
    inp = json.loads(Path(sys.argv[1]).read_text(encoding="utf8"))
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    in12 = 12
    for i, t in enumerate(inp["teachers"], 1):
        un = t["unavailable"]
        if not un:
            st = "Tham gia đủ 4 kỳ"
        elif len(un) == 3:
            st = "Nghỉ thai sản, chỉ tham gia CK2"
        else:
            st = "Hợp đồng ký muộn, tham gia từ CK1"
        grades = "/".join(str(g) for g in t["grades"]) if t.get("grades") else "chưa xác định"
        rows.append([t["code"], t["campus"], "/".join(SUBJ[s] for s in t["setter"]), grades, st, "Có" if i <= in12 else "Không"])
    for code in ("GV18", "GV19"):
        rows.append([code, "—", "—", "—", "Cán bộ quản lí, không tham gia ban ra đề", "Không"])
    head = ["Mã GV", "Phân hiệu", "Môn ra đề", "Khối dạy", "Tình trạng tham gia ra đề", "Có vị trí trong bảng thủ công"]
    with open(out / "thong-ke-19-giao-vien.csv", "w", encoding="utf8", newline="") as f:
        w = csv.writer(f)
        w.writerow(head)
        w.writerows(rows)

    widths = [90, 100, 130, 130, 440, 260]
    rh = 34
    W = sum(widths) + 40
    H = 120 + rh * (len(rows) + 1) + 50
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.text((20, 18), "Thống kê chuyên môn: 19 giáo viên Tổ Vật lí – Công nghệ (đã mã hoá)", font=font(24, True), fill=(30, 30, 30))
    n12 = sum(1 for r in rows if r[5] == "Có")
    n17 = sum(1 for r in rows if r[4].split(",")[0] != "Cán bộ quản lí")
    d.text((20, 56), f"{len(rows)} người, {n17} tham gia ban ra đề. Bảng thủ công của Tổ chỉ phân công cho GV01–GV12 (có mặt ở GK1)", font=font(18), fill=(90, 90, 90))
    y = 100
    x = 20
    d.rectangle([20, y, W - 20, y + rh], fill=(242, 242, 242), outline=(30, 30, 30))
    for wd, h in zip(widths, head):
        d.text((x + 8, y + 7), h, font=font(16, True), fill=(30, 30, 30))
        x += wd
    for r in rows:
        y += rh
        fill = (255, 247, 230) if r[5] == "Không" else "white"
        d.rectangle([20, y, W - 20, y + rh], fill=fill, outline=(160, 160, 160))
        x = 20
        for wd, v in zip(widths, r):
            d.text((x + 8, y + 7), v, font=font(16), fill=(30, 30, 30))
            x += wd
    d.text((20, y + rh + 14), "Nguồn: dau-vao.json (17 giáo viên) và ghi chú đầu vào về 2 cán bộ quản lí. Khối dạy của GV13–GV17 chưa xác định.", font=font(14), fill=(110, 110, 110))
    im.save(out / "thong-ke-19-giao-vien.png")
    print(len(rows), n17, n12)


if __name__ == "__main__":
    main()

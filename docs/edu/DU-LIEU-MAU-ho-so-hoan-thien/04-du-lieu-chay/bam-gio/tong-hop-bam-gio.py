"""Tổng hợp nhật ký bấm giờ: thời lượng từng bước, tổng từng lần, trung bình, so với cách thủ công.

Mọi số tính từ giờ bắt đầu và kết thúc trong CSV. Không gõ tay.
Dùng:  python tong-hop-bam-gio.py <nhat-ky.csv> [--thu-cong "khoảng 1 ngày, ít nhất 3 lần sửa"]
Nếu dòng đầu CSV bắt đầu bằng "DỮ LIỆU MINH HOẠ" thì dòng đó được bỏ qua khi đọc,
tên tệp ra có hậu tố -DU-LIEU-MINH-HOA và nhãn được ghi ở dòng đầu tệp .md.
"""
import argparse
import csv
import statistics
from collections import OrderedDict
from datetime import datetime
from pathlib import Path

LABEL = "DỮ LIỆU MINH HOẠ, không phải số liệu thực địa"
STEPS = ["Nhập dữ liệu", "Kiểm tra khả thi", "Chạy tối ưu", "Rà và khoá ô", "Xuất và in"]


def minutes(a, b):
    f = "%H:%M"
    return int((datetime.strptime(b, f) - datetime.strptime(a, f)).total_seconds() // 60)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nhat_ky")
    ap.add_argument("--thu-cong", default="khoảng 1 ngày, ít nhất 3 lần sửa (ước lượng của tác giả, chưa bấm giờ)")
    a = ap.parse_args()
    text = Path(a.nhat_ky).read_text(encoding="utf8").splitlines()
    minh_hoa = text[0].startswith("DỮ LIỆU MINH HOẠ")
    rows = list(csv.DictReader(text[1:] if minh_hoa else text))
    sessions = OrderedDict()
    for r in rows:
        key = (r["lan"], r["lan_ghi"], r["ngay"])
        sessions.setdefault(key, []).append(r)
    L = []
    if minh_hoa:
        L += [LABEL, ""]
    L += ["# Nhật ký bấm giờ lập phương án bằng ExamPanel", ""]
    totals, per_step = [], {s: [] for s in STEPS}
    for (lan, ten, ngay), items in sessions.items():
        L += [f"## Lần {lan}: {ten} ({ngay})", "", "| Bước | Bắt đầu | Kết thúc | Phút | Ghi chú |", "| :-- | :-: | :-: | :-: | :-- |"]
        total = 0
        for it in items:
            m = minutes(it["bat_dau"], it["ket_thuc"])
            total += m
            per_step[it["buoc"]].append(m)
            L.append(f"| {it['buoc']} | {it['bat_dau']} | {it['ket_thuc']} | {m} | {it['ghi_chu']} |")
        L += ["", f"Tổng: **{total} phút** (từ {items[0]['bat_dau']} đến {items[-1]['ket_thuc']}).", ""]
        totals.append(total)
    L += ["## Bảng tóm tắt", "", "| Bước | " + " | ".join(f"Lần {k[0]} ({k[1]})" for k in sessions) + " | Trung bình |",
          "| :-- |" + " :-: |" * (len(sessions) + 1)]
    for s in STEPS:
        L.append(f"| {s} | " + " | ".join(str(v) for v in per_step[s]) + f" | {statistics.mean(per_step[s]):.1f} |")
    L.append("| **Tổng (phút)** | " + " | ".join(f"**{t}**" for t in totals) + f" | **{statistics.mean(totals):.1f}** |")
    L += ["", f"Trung bình {statistics.mean(totals):.1f} phút mỗi lần, thấp nhất {min(totals)}, cao nhất {max(totals)}.",
          f"Cách thủ công bằng Excel: {a.thu_cong}.", ""]
    out = "\n".join(L)
    sfx = "-DU-LIEU-MINH-HOA" if minh_hoa else ""
    Path(a.nhat_ky).with_name(f"tong-hop-bam-gio{sfx}.md").write_text(out, encoding="utf8")
    print(out)


if __name__ == "__main__":
    main()

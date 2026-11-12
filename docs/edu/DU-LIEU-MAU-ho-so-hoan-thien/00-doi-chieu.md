# Đối chiếu: số trong slide, poster, video và tệp nguồn

Đường dẫn tính từ thư mục này. Số "minh hoạ" lấy từ tệp có hậu tố `-DU-LIEU-MINH-HOA`.
Toàn bộ số đo so sánh dùng dữ liệu 17 giáo viên đủ điều kiện, 60 vị trí, 4 kỳ × 3 khối.

## Số do chương trình tính (17 giáo viên)

Tệp nguồn chung: `04-du-lieu-chay/ca-nam-17gv/site3_comparison.md` (đầu vào `dau-vao.json`, điểm `site3_scores.json`, nhật ký `nhat-ky-lenh.log`).

| Số trong hồ sơ | Nơi dùng | Dòng trong tệp nguồn |
| :-- | :-- | :-- |
| 527,43 → 52,53 điểm phạt mềm; giảm 90,04% | slide 10; poster ô 4; video cảnh 5 | dòng **Tổng**, dòng Tỉ lệ giảm |
| Dồn việc S9: 9 trường hợp → 1; phạt 45 → 5 | slide 10, 11; poster ô 4, ô 5 | dòng S9 |
| Cân bằng khối lượng S8: phạt 333,43 → 23,53 | slide 10, 11; poster ô 5 | dòng S8 |
| Độc lập cơ sở S3: phạt 32 → 0 | slide 10; poster ô 4 | dòng S3 |
| Ràng buộc cứng: thủ công 6 vi phạm (1 vượt số việc trong kỳ, 1 vượt hạn mức, 4 thiếu hạn mức tối thiểu); ExamPanel 0 | slide 10, 11; poster ô 4, ô 5 | mục vi phạm ràng buộc cứng |
| Chênh lệch lượt việc nhóm Vật lí 6 → 3 | slide 11; poster ô 5 | dòng Max–Min |
| GV Công nghệ duy nhất nhận 12/60 lượt | slide 11 | bảng khối lượng, dòng GV12 |
| 60/60 vị trí, 17 giáo viên | slide 10; poster ô 4 | dòng Quy mô |
| Thời gian tìm phương án 650 ms (bản release; lần chạy chậm nhất trong 3 lần đo 439, 583, 650 ms) | slide 10; poster ô 4 | dòng "thời gian chạy" trong `04-du-lieu-chay/ca-nam-17gv/site3_comparison.md` (lần chạy lưu lại: 583 ms) |
| Phương án phân công ExamPanel cho 17 giáo viên | slide 3 ô 5 | `03-minh-chung/bang-phan-cong/bang-phan-cong-exampanel-ca-nam-17gv.{png,xlsx}` |
| Bảng thủ công 17 giáo viên, 5 người không có vị trí (GV13–GV17) | không dùng trực tiếp trong slide | `03-minh-chung/bang-phan-cong/bang-phan-cong-thu-cong-ca-nam-17gv.{png,xlsx}` (có chú thích dưới bảng và trang "So luot") |

Câu trung thực, ghi ở chú thích slide 10, poster ô 4, ghi chú slide 3, 10 và kịch bản video cảnh 5: **bảng thủ công của Tổ chỉ phân công cho 12 giáo viên có mặt ở GK1** (GV13 nghỉ thai sản vắng GK1, CK1, GK2; GV14–GV17 hợp đồng muộn vắng GK1), nên một phần chênh lệch đến từ đó. Hồ sơ không dùng số −72,8% hay các số của lượt 12 giáo viên.

## Số từ minh chứng thật

| Số trong hồ sơ | Nơi dùng | Tệp nguồn |
| :-- | :-- | :-- |
| 19 giáo viên, 17 tham gia ban ra đề (trừ 2 cán bộ quản lí) | slide 2, 3; poster ô 1; video cảnh 5 | `03-minh-chung/thong-ke-19-giao-vien.csv`, `.png`; `03-minh-chung/trich-bien-ban-hop-to-6-10-2026-bang-phan-cong-da-che-ten.png` |
| Tổ thống nhất 100% bảng phân công | slide 3, 11 | `03-minh-chung/trich-bien-ban-hop-to-6-10-2026-ket-luan-thong-nhat-da-che-ten.png` |
| Quyết định 3726/QĐ-UBND, 19/8/2026 | slide 3 | `03-minh-chung/quyet-dinh-3726-QD-UBND-trang1.png` |
| Quyết định 95/QĐ-TTGDTXĐN, 19/10/2026 | slide 3 | `03-minh-chung/quyet-dinh-95-QD-TTGDTXDN-trang1-da-che-ten.png` |

**Điều cần chủ dự án kiểm tra:** slide 3 và slide 11 ghi mốc họp Tổ là 6/10/2026 (theo quyết định của chủ dự án). Biên bản gốc `THÁNG 9-BB NHÓM LÍ.docx` ghi họp ngày 26/9/2026. Ba ảnh trích biên bản không hiển thị ngày, nhưng trang đầu biên bản có ngày 26/9. Cần xác nhận 6/10 là cuộc họp nào, hoặc sửa mốc cho khớp biên bản.

## Số minh hoạ (khảo sát và bấm giờ)

| Số trong hồ sơ | Nơi dùng | Tệp nguồn |
| :-- | :-- | :-- |
| Trung bình 46,3 phút; 49, 43, 47 phút; thấp nhất 43, cao nhất 49 | slide 11; poster ô 5; video cảnh 6 | `04-du-lieu-chay/bam-gio/tong-hop-bam-gio-DU-LIEU-MINH-HOA.md` |
| Thủ công khoảng 1 ngày, sửa ít nhất 3 lần | slide 2, 11; poster ô 1, 5; video cảnh 1 | Ước lượng của tác giả, chưa bấm giờ |
| 16/19 phiếu trả lời | slide 11; poster ô 5; video cảnh 6 | `05-khao-sat/tong-hop-khao-sat-DU-LIEU-MINH-HOA.md` |
| Trung bình chung 4,21/5; 85,4% đồng ý (mức 4–5) | slide 11; poster ô 5; video cảnh 6 | cùng tệp, dòng "Trung bình chung 6 câu" |

## Lệnh chạy

```
cargo run -q --release -p exam-panel-service --example site_comparison -- <dau-vao.json> <thu-muc-ra>
python 04-du-lieu-chay/cong-cu/dung-bang-phan-cong.py 04-du-lieu-chay/ca-nam-17gv 03-minh-chung/bang-phan-cong GV03 GV12 GV16
python 04-du-lieu-chay/cong-cu/tao-bang-19gv.py 04-du-lieu-chay/ca-nam-17gv/dau-vao.json 03-minh-chung
python 05-khao-sat/tong-hop-khao-sat.py 05-khao-sat/ket-qua-khao-sat-DU-LIEU-MINH-HOA.csv --gui 05-khao-sat/so-gui-phieu-DU-LIEU-MINH-HOA.csv --chon P02,P07,P08,P10,P12,P15
python 04-du-lieu-chay/bam-gio/tong-hop-bam-gio.py 04-du-lieu-chay/bam-gio/nhat-ky-bam-gio-DU-LIEU-MINH-HOA.csv
```

`04-du-lieu-chay/cong-cu/site_comparison_xuat_phan_cong.rs.txt` là bản sao chương trình đo, thêm bước ghi hai tệp CSV phân công. Nó dùng cùng thư viện lõi, không đổi thuật toán. Hai tệp CSV phân công do bản sao này xuất. Tệp điểm và báo cáo (`site3_comparison.md`, `site3_scores.json`) do ví dụ `site_comparison` gốc chạy sau cùng. Thời gian chạy thay đổi giữa các lần (439, 583, 650 ms), điểm không đổi vì seed cố định.

Trường `_ghi_chu` trong `dau-vao.json` đã được sửa một cụm chữ (bỏ số đối chiếu cũ). Dữ liệu giáo viên và bảng thủ công không đổi.

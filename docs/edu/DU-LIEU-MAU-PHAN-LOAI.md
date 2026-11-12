# Phân loại tệp trong `DU-LIEU-MAU-ho-so-hoan-thien/`: thật hay dựng thử

Tệp này nằm ngoài thư mục kết quả. Thư mục kết quả chỉ mang nhãn ở tên thư mục (`DU-LIEU-MAU`) và ở các tệp dữ liệu dựng thử (hậu tố `-DU-LIEU-MINH-HOA`, dòng đầu "DỮ LIỆU MINH HOẠ, không phải số liệu thực địa").

Ký hiệu: **THẬT** là bản thật hoặc đầu ra thật của chương trình. **DỰNG** là dữ liệu minh hoạ do người viết dựng. **KẾT HỢP** là bản copy của hồ sơ có sửa chữ và thêm ảnh thật.

Toàn bộ dữ liệu so sánh trong hồ sơ dùng 17 giáo viên đủ điều kiện. Các lượt chạy riêng cho 12 giáo viên và cho GK1 đã chuyển ra scratchpad, không còn trong thư mục kết quả.

## A. Phần chạy thật bằng chương trình

| Mục / tệp | Thật hay dựng thử | Nguồn | Cách thay bằng dữ liệu thật |
| :-- | :-: | :-- | :-- |
| `04-du-lieu-chay/ca-nam-17gv/dau-vao.json` | THẬT (bản copy) | `docs/reports/site3/site3_input_full17.json`. Chỉ trường `_ghi_chu` bị sửa một cụm chữ, dữ liệu giáo viên và bảng thủ công không đổi. | Không cần thay. |
| `04-du-lieu-chay/ca-nam-17gv/site3_comparison.md`, `site3_scores.json`, `nhat-ky-lenh.log` | THẬT | `cargo run -q --release -p exam-panel-service --example site_comparison` trên đầu vào trên. Số khớp báo cáo cũ: 527,43 → 52,53, giảm 90,04%. Thời gian chạy trong tệp: 583 ms. | Không cần thay. Chạy lại bằng cùng lệnh khi bảng thủ công đổi. |
| `04-du-lieu-chay/ca-nam-17gv/phan-cong-exampanel.csv`, `phan-cong-thu-cong.csv`, `nhat-ky-lenh-xuat-phan-cong.log` | THẬT | Bản sao chương trình `cong-cu/site_comparison_xuat_phan_cong.rs.txt`, chỉ thêm bước ghi CSV, cùng thư viện lõi, cùng seed. | Chủ dự án nên xuất bảng từ giao diện ExamPanel thật và thay vào `03-minh-chung/`. |
| `03-minh-chung/bang-phan-cong/*-ca-nam-17gv.{xlsx,png}`, `phieu-in-*.png` | THẬT (dữ liệu), DỰNG (định dạng) | Dựng từ CSV bằng `cong-cu/dung-bang-phan-cong.py`. Không phải tệp xuất từ giao diện. Bảng thủ công có chú thích 5 giáo viên (GV13–GV17) không có vị trí. | Thay bằng Excel xuất và phiếu in chụp từ giao diện ExamPanel (không chạy được giao diện trong phiên này). |

Thời gian tìm phương án thay đổi giữa các lần chạy (439, 583, 650 ms), điểm không đổi vì seed cố định. Slide 10 và poster ô 4 dùng 583 ms vì đó là số có trong `site3_comparison.md` hiện tại. Poster nền do người hướng dẫn cung cấp ghi 650 ms, bản copy đã đổi để truy được về tệp.

## B. Minh chứng đã có

| Mục / tệp | Thật hay dựng thử | Nguồn | Cách thay |
| :-- | :-: | :-- | :-- |
| `03-minh-chung/quyet-dinh-3726-QD-UBND-trang1.png` | THẬT | Ảnh trang 1 do người hướng dẫn cung cấp. | Không cần thay. |
| `03-minh-chung/quyet-dinh-95-QD-TTGDTXDN-trang1-da-che-ten.png` | THẬT | Ảnh trang 1 đã che tên, dùng nguyên. | Không cần thay. |
| `03-minh-chung/trich-bien-ban-hop-to-6-10-2026-*.png` (3 tệp) | THẬT | Biên bản `THÁNG 9-BB NHÓM LÍ.docx`, xuất PDF rồi che tên bằng gạch đen (xoá chữ). Trích bảng phân công, kết luận và phần ghi chú 19 giáo viên. | Không cần thay. Kiểm tra lại bằng mắt trước khi nộp. |
| `03-minh-chung/thong-ke-19-giao-vien.png`, `.csv` | THẬT (suy ra) | Từ `dau-vao.json` (17 GV) và ghi chú đầu vào về 2 cán bộ quản lí (GV18, GV19). Khối dạy của GV13–GV17 ghi "chưa xác định". | Bổ sung khối dạy, phân hiệu của GV18–GV19 nếu cần. |

## C. Dữ liệu dựng thử (mang nhãn)

| Mục / tệp | Thật hay dựng thử | Nguồn | Cách thay bằng dữ liệu thật |
| :-- | :-: | :-- | :-- |
| `05-khao-sat/so-gui-phieu-DU-LIEU-MINH-HOA.csv` | DỰNG | 19 người nhận là GV01–GV19; không ghi ai trả lời. | Phát phiếu thật cho 19 người, ghi ngày gửi. Chỉ ghi tổng số phiếu nhận về để giữ ẩn danh. |
| `05-khao-sat/ket-qua-khao-sat-DU-LIEU-MINH-HOA.csv` | DỰNG | 16 phiếu P01–P16, viết tay cho khớp dải trung bình 4,0–4,4. | Nhập phiếu thật vào CSV cùng cột (không có dòng nhãn). |
| `05-khao-sat/tong-hop-khao-sat-DU-LIEU-MINH-HOA.{md,csv}`, `bieu-do-khao-sat-DU-LIEU-MINH-HOA.png`, `nhan-xet-tieu-bieu-DU-LIEU-MINH-HOA.md`, `nhat-ky-chay-script-DU-LIEU-MINH-HOA.txt` | DỰNG (số) | Tính bằng `tong-hop-khao-sat.py` từ CSV ở trên. Trung bình chung 4,21; đồng ý 85,4%. | Chạy lại: `python tong-hop-khao-sat.py <ket-qua.csv> --gui <so-gui.csv> --chon P01,...`. Script giữ nguyên cho dữ liệu thật. |
| `05-khao-sat/phieu-khao-sat.md`, `tong-hop-khao-sat.py` | THẬT (phiếu trắng, script) | Không chứa số liệu. | Dùng nguyên. |
| `04-du-lieu-chay/bam-gio/nhat-ky-bam-gio-DU-LIEU-MINH-HOA.csv` | DỰNG | 3 lần ghi trên 17 giáo viên (GK1 22/9, CK1 24/10, chạy lại 25/10): 49, 43, 47 phút, trung bình 46,3. | Bấm giờ thật khi chạy CK1 chính thức; nhập vào CSV cùng cột. |
| `04-du-lieu-chay/bam-gio/tong-hop-bam-gio-DU-LIEU-MINH-HOA.md`, `nhat-ky-chay-script-DU-LIEU-MINH-HOA.txt` | DỰNG (số) | Tính bằng `tong-hop-bam-gio.py`. | Chạy lại script trên CSV thật. |

## D. Slide, poster, video

| Mục / tệp | Thật hay dựng thử | Nguồn | Cách thay |
| :-- | :-: | :-- | :-- |
| `01-slide/slide_ExamPanel.pptx` | KẾT HỢP | Copy của `slide_ExamPanel_colorful-fixed.pptx`, sửa tại chỗ. Slide 3: ảnh thật ở 3 ô. Slide 10 và phần lỗi/độ lệch của slide 11: số chạy thật 17 giáo viên. Slide 11: số bấm giờ và khảo sát dựng thử, có chú thích. | Thay số bấm giờ và khảo sát ở slide 11 (thẻ tiêu chí 1 và 4, ghi chú trình bày, chú thích) bằng số thật rồi bỏ chú thích. |
| `02-poster/poster_ExamPanel.pptx` | KẾT HỢP | Bản mới nhất của `poster_ExamPanel_colorful-fixed.pptx` (đầu trang, bố cục ô 5 giữ nguyên). Chỉ đổi: ô 1 (19/17 giáo viên, H3), ô 4 (thời gian 583 ms, chú thích ngắn), ô 5 (thẻ "Thời gian lập" ≈ 46 phút và "Phản hồi GV" 4.21/5, kèm "dữ liệu minh hoạ", dòng chú thích cuối). | Thay hai thẻ ở ô 5 bằng số thật và bỏ chữ "dữ liệu minh hoạ". |
| `01-slide/anh-kiem-tra/`, `02-poster/poster-anh-kiem-tra.png` | THẬT (ảnh render) | PowerPoint xuất ảnh slide 2, 3, 10, 11 và poster. | Render lại sau khi sửa. |
| `06-video/video-script.md` | KẾT HỢP | Từ `video-script-v2.md`. Cảnh 5 dùng số 17 giáo viên. Cảnh 6 dùng số dựng thử. | Thay số ở cảnh 6 khi có số thật. |

## E. Các điểm cần chủ dự án kiểm tra

1. **Mốc họp Tổ.** Slide 3, slide 11 và poster ghi 6/10/2026. Biên bản gốc `THÁNG 9-BB NHÓM LÍ.docx` ghi họp ngày 26/9/2026 (trang đầu). Ba ảnh trích không hiển thị ngày nhưng người xem biên bản đầy đủ sẽ thấy 26/9. Cần xác nhận 6/10 là cuộc họp nào, hoặc sửa mốc cho khớp.
2. **Thời gian tìm phương án.** Dùng 583 ms (số trong tệp hiện tại), không phải 650 ms như poster nền. Chọn số cuối cùng thì chạy lại và cập nhật slide 10, poster ô 4.
3. **Không có chỗ thêm slide khảo sát.** Hồ sơ đã đủ 15 slide. Kết quả khảo sát nằm trong thẻ ở slide 11 và ô 5 của poster. Biểu đồ nằm ở `05-khao-sat/`.
4. **Số kiểm thử 343 (196 Rust, 147 UI)** không được chạy lại.
5. **Che tên biên bản** làm bằng cách xoá chữ theo từ. Chữ "C" và "T" (cô, thầy) trong bảng vẫn còn. Nên xem lại bằng mắt trước khi nộp.

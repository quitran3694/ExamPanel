# Đo so sánh: phương án thủ công đã số hoá và ExamPanel

> Tệp do `crates/service/examples/site_comparison.rs` sinh từ `docs/reports/site3/site3_input_full17.json`; mọi con số do chương trình in ra. Giáo viên chỉ có mã GV01…, không có tên thật.

- Quy mô: 17 giáo viên, 4 phân hiệu, 4 kỳ × 3 khối, 60 vị trí trong phương án thủ công.
- Kiểm tra khả thi trước khi giải: **KHẢ THI** (0 lỗi, 12 cảnh báo).
  - Cảnh báo: `forced_placement` {"exam": String("GK1"), "grade": Number(10), "position": Number(0), "role": String("setter"), "subject": String("CN"), "teacher_name": String("Giáo viên GV12")}
  - Cảnh báo: `forced_placement` {"exam": String("GK1"), "grade": Number(11), "position": Number(0), "role": String("setter"), "subject": String("CN"), "teacher_name": String("Giáo viên GV12")}
  - Cảnh báo: `forced_placement` {"exam": String("GK1"), "grade": Number(12), "position": Number(0), "role": String("setter"), "subject": String("CN"), "teacher_name": String("Giáo viên GV12")}
  - Cảnh báo: `forced_placement` {"exam": String("CK1"), "grade": Number(10), "position": Number(0), "role": String("setter"), "subject": String("CN"), "teacher_name": String("Giáo viên GV12")}
  - Cảnh báo: `forced_placement` {"exam": String("CK1"), "grade": Number(11), "position": Number(0), "role": String("setter"), "subject": String("CN"), "teacher_name": String("Giáo viên GV12")}
  - Cảnh báo: `forced_placement` {"exam": String("CK1"), "grade": Number(12), "position": Number(0), "role": String("setter"), "subject": String("CN"), "teacher_name": String("Giáo viên GV12")}
  - Cảnh báo: `forced_placement` {"exam": String("GK2"), "grade": Number(10), "position": Number(0), "role": String("setter"), "subject": String("CN"), "teacher_name": String("Giáo viên GV12")}
  - Cảnh báo: `forced_placement` {"exam": String("GK2"), "grade": Number(11), "position": Number(0), "role": String("setter"), "subject": String("CN"), "teacher_name": String("Giáo viên GV12")}
  - Cảnh báo: `forced_placement` {"exam": String("GK2"), "grade": Number(12), "position": Number(0), "role": String("setter"), "subject": String("CN"), "teacher_name": String("Giáo viên GV12")}
  - Cảnh báo: `forced_placement` {"exam": String("CK2"), "grade": Number(10), "position": Number(0), "role": String("setter"), "subject": String("CN"), "teacher_name": String("Giáo viên GV12")}
  - Cảnh báo: `forced_placement` {"exam": String("CK2"), "grade": Number(11), "position": Number(0), "role": String("setter"), "subject": String("CN"), "teacher_name": String("Giáo viên GV12")}
  - Cảnh báo: `forced_placement` {"exam": String("CK2"), "grade": Number(12), "position": Number(0), "role": String("setter"), "subject": String("CN"), "teacher_name": String("Giáo viên GV12")}

## Phương án thủ công: vi phạm ràng buộc cứng

| Mã vi phạm | Số lần |
| :--- | :---: |
| `max_tasks_per_exam_exceeded` | 1 |
| `quota_exceeded` | 1 |
| `quota_unmet` | 4 |

## So sánh điểm phạt mềm S1–S10 (càng thấp càng tốt)

Tham số tối ưu: seed 42, R = 8, 200000 vòng/lần chạy; thời gian chạy 2434 ms.

| Quy tắc | Thủ công (đơn vị) | Thủ công (phạt) | ExamPanel (đơn vị) | ExamPanel (phạt) |
| :--- | :---: | :---: | :---: | :---: |
| S1 Tần suất phản biện | 6.00 | 60.00 | 0.00 | 0.00 |
| S2 Cân bằng vai trò | 1.00 | 3.00 | 0.00 | 0.00 |
| S3 Độc lập cơ sở | 8.00 | 32.00 | 0.00 | 0.00 |
| S4 Đa dạng cặp ra đề | 0.00 | 0.00 | 0.00 | 0.00 |
| S5 Đa dạng quan hệ phản biện | 1.00 | 6.00 | 0.00 | 0.00 |
| S6 Ra đề liên tiếp | 8.00 | 16.00 | 0.00 | 0.00 |
| S7 Xoay vòng khối | 0.00 | 0.00 | 0.00 | 0.00 |
| S8 Cân bằng khối lượng | 41.68 | 333.43 | 2.94 | 23.53 |
| S9 Dồn việc trong kỳ | 9.00 | 45.00 | 1.00 | 5.00 |
| S10 Thiếu môn phản biện | 8.00 | 32.00 | 6.00 | 24.00 |
| **Tổng** | | **527.43** | | **52.53** |

**Tỉ lệ giảm điểm phạt mềm: 90.04%.**

Vi phạm ràng buộc cứng của phương án ExamPanel: không có.

## Khối lượng nhiệm vụ theo giáo viên (số vị trí, đếm trực tiếp từ bảng phân công)

| Mã GV | Thủ công | ExamPanel |
| :--- | :---: | :---: |
| GV01 | 5 | 3 |
| GV02 | 5 | 3 |
| GV03 | 4 | 3 |
| GV04 | 4 | 3 |
| GV05 | 4 | 4 |
| GV06 | 4 | 4 |
| GV07 | 4 | 3 |
| GV08 | 4 | 3 |
| GV09 | 4 | 3 |
| GV10 | 4 | 3 |
| GV11 | 6 | 3 |
| GV12 | 12 | 12 |
| GV13 | 0 | 1 |
| GV14 | 0 | 3 |
| GV15 | 0 | 3 |
| GV16 | 0 | 3 |
| GV17 | 0 | 3 |

Max–Min nhóm Vật lí (loại giáo viên chỉ ra đề Công nghệ; tính cả giáo viên chưa được giao vị trí nào): thủ công 6 − 0 = 6; ExamPanel 4 − 1 = 3.

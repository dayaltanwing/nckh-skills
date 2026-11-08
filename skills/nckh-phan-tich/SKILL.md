---
name: nckh-phan-tich
description: Phân tích dữ liệu định lượng cho khoa học xã hội bằng R (ưu tiên) hoặc Python, theo script tái lập được: làm sạch dữ liệu khảo sát, thống kê mô tả, độ tin cậy (alpha, omega), EFA/CFA, bất biến đo lường, t-test/ANOVA, tương quan, hồi quy, trung gian/điều tiết, SEM, xử lý dữ liệu thiếu; xuất bảng và hình chuẩn APA 7. Dùng khi người dùng muốn phân tích dữ liệu, chạy thống kê, kiểm định giả thuyết, hoặc hỏi về kết quả SPSS/R/Python.
---

# Phân tích định lượng

Đọc `../nckh/references/nguyen-tac.md` trước. Bốn nguyên tắc chi phối skill này:
- **4**: chỉ kiểm định theo kế hoạch đã viết; phần còn lại là khám phá.
- **5**: báo cáo đầy đủ.
- **6**: dữ liệu thô chỉ đọc.
- **8**: mọi thứ là script.

Chi tiết gói và mẫu code nằm trong `references/r-goi-y.md`.

## Trước khi chạy bất cứ thứ gì

1. Đọc kế hoạch phân tích trong `nckh/de-cuong.md`. Chưa có thì dừng lại, đề nghị viết kế hoạch ngắn trước (giả thuyết → phân tích → tiêu chí). Nếu người dùng đã thu và đã xem dữ liệu, vẫn viết kế hoạch, nhưng ghi trung thực vào nhật ký rằng kế hoạch được viết sau khi đã xem dữ liệu.
2. Đọc `nckh/cong-cu/codebook.csv` nếu có.
3. **Quyền riêng tư**: kiểm tra dữ liệu có cột định danh không (họ tên, email, SĐT, mã HS). Có thì đề nghị người dùng tự xoá hoặc mã hoá cột đó trong bản gốc trước khi bạn đọc nội dung (nguyên tắc 6). Khi khám phá cấu trúc, xem tên cột và vài thống kê tổng hợp, không in toàn bộ dữ liệu ra chat.
4. Kiểm tra R/Python và các gói đã cài chưa. Gói nào thiếu thì đưa lệnh cài cho người dùng.

## Chuỗi script (`nckh/phan-tich/`)

Mỗi bước một file, đánh số thứ tự. Mỗi file đọc đầu vào từ bước trước và ghi đầu ra ra file. Có `00-chay-tat-ca.R` để chạy lại toàn bộ.

| File | Việc làm | Đầu ra |
|---|---|---|
| `01-lam-sach.R` | Đọc `du-lieu/raw/`, đổi tên biến theo codebook, mã hoá ngược item đảo chiều, gắn nhãn giá trị thiếu, loại phiếu theo tiêu chí **đã định trước** (attention check, thời gian quá nhanh, trả lời thẳng hàng), ghi số phiếu bị loại ở từng bước | `du-lieu/clean/`, `ket-qua/loai-phieu.csv` |
| `02-mo-ta.R` | Đặc điểm mẫu, mô tả từng biến, mẫu hình dữ liệu thiếu, phân phối (độ lệch, độ nhọn) | Bảng 1 |
| `03-thang-do.R` | α và ω, CFA từng thang đo (chỉ số độ phù hợp, hệ số tải), giá trị hội tụ/phân biệt (AVE, HTMT), bất biến đo lường nếu so sánh nhóm | Bảng thang đo |
| `04-tuong-quan.R` | Ma trận tương quan kèm M, SD, α trên đường chéo | Bảng 2 |
| `05-gia-thuyet.R` | Đúng các phân tích trong kế hoạch, mỗi giả thuyết một khối có chú thích `# H1` | Bảng kết quả chính |
| `06-do-vung.R` | Kiểm tra độ vững: chạy lại không có biến kiểm soát, cách xử lý thiếu khác, loại ngoại lai | Phụ lục |
| `07-kham-pha.R` | Phân tích ngoài kế hoạch, **gắn nhãn khám phá** | Phụ lục |

Đặt `set.seed()` ở đầu các script có bootstrap/mô phỏng. Script cuối ghi `sessionInfo()` ra `ket-qua/phien-ban.txt`.

## Mặc định có lý do

- **Dữ liệu thiếu**: dùng FIML (lavaan `missing = "fiml"`) hoặc multiple imputation (`mice`). Chỉ xoá theo danh sách (listwise) khi tỉ lệ thiếu rất nhỏ, và ghi lý do.
- **Thang Likert trong CFA**: biến 5 mức trở xuống thì cân nhắc ước lượng WLSMV (khai báo `ordered`). Từ 5 mức trở lên và phân phối gần chuẩn thì có thể dùng MLR. Nêu lựa chọn cho người dùng chọn.
- **Trung gian**: kiểm định hiệu ứng gián tiếp bằng bootstrap khoảng tin cậy (≥ 5000 lần), không dùng các bước Baron & Kenny làm tiêu chí.
- **Ngưỡng độ phù hợp CFA** (CFI/TLI ≥ .90–.95, RMSEA ≤ .06–.08, SRMR ≤ .08): trình bày là quy ước tham khảo (Hu & Bentler, 1999), không phải luật cứng.
- **Kiểm định bội**: nếu kế hoạch có nhiều kiểm định cùng họ, áp dụng Holm hoặc FDR.

## Đọc kết quả cho người dùng

Với mỗi giả thuyết, giải thích bằng tiếng Việt thường:
- Có được ủng hộ không.
- Độ lớn hiệu ứng có ý nghĩa thực tiễn không. Đừng chỉ nhìn p.
- Giới hạn diễn giải: không nói nhân quả với dữ liệu cắt ngang.

⛔ Diễn giải cuối cùng là của người dùng (nguyên tắc 3).

## Viết kết quả kiểu APA 7

Mẫu câu: `Career adaptability predicted career decision self-efficacy, β = .42, 95% CI [.33, .51], p < .001.` Bảng APA: số thập phân thống nhất, bỏ số 0 đứng đầu với giá trị không thể vượt quá 1 (p, r, β chuẩn hoá). Xuất bảng ra `.csv` và `.tex` để `nckh-viet-bai` đưa vào bản thảo Prism. Hình: `ggplot2`, `theme_classic()`, lưu `.pdf` cho LaTeX.

Mỗi con số đưa vào bản thảo phải đến từ file trong `ket-qua/` (nguyên tắc 2). Không gõ lại số bằng tay từ chat.

## Python (khi người dùng muốn)

Bộ tương đương: `pandas`, `pingouin` (tin cậy, kiểm định), `statsmodels` (hồi quy), `factor_analyzer` (EFA), `semopy` (CFA/SEM). Lưu ý cho người dùng: hệ sinh thái SEM/tâm trắc của R (`lavaan`, `semTools`, `psych`) đầy đủ và được reviewer quen hơn.

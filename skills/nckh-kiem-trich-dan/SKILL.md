---
name: nckh-kiem-trich-dan
description: Kiểm tra trích dẫn và tài liệu tham khảo trước khi nộp. Đối chiếu từng mục BibTeX với Crossref (DOI có thật không, tiêu đề/năm có khớp không, bài có bị rút không), kiểm tra mọi \cite trong .tex đều có trong .bib và ngược lại, kiểm tra khẳng định được trích có được thẻ đọc ủng hộ không. Dùng khi người dùng muốn kiểm tra tài liệu tham khảo, citation, DOI, hoặc trước khi nộp bài.
---

# Kiểm tra trích dẫn

Đọc `../nckh/references/nguyen-tac.md` trước. Đây là "hàng rào bảo vệ" của bộ skill, giống guard hook trong super-board: nó chặn lỗi nặng nhất trong nghiên cứu có dùng AI, là **trích dẫn bịa hoặc sai** (nguyên tắc 1). Chạy nó sau mỗi lần viết và trước mỗi lần nộp.

## Tầng 1: tài liệu có thật và đúng không (script)

Chạy từ thư mục gốc của đề tài (nơi có thư mục `nckh/`). Script nằm trong thư mục của skill này chứ không nằm trong đề tài, nên phải ghi đủ đường dẫn tới nó:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/kiem_trich_dan.py" nckh/tai-lieu/tai-lieu.bib --tex nckh/ban-thao/main.tex
```

Phần đầu của đường dẫn script là thư mục chứa file SKILL.md này. Nếu trong lệnh trên vẫn còn một biến chưa được thay bằng đường dẫn thật, hãy tự thay (cài theo dự án thì là `.claude/skills/nckh-kiem-trich-dan`).

Script làm các việc sau:
- Báo khoá bị trùng trong `.bib`. Hai mục cùng khoá thì `\cite` có thể trỏ nhầm bài.
- Với mục có DOI: hỏi Crossref; so tiêu đề (độ giống), năm, tác giả đầu; kiểm tra có thông báo rút bài/đính chính không.
- Với mục không có DOI: tìm trên Crossref theo tiêu đề và tác giả, đề xuất DOI nếu tìm được bản khớp cao.
- Với `--tex`: liệt kê khoá được `\cite` nhưng không có trong `.bib` (lỗi), và khoá có trong `.bib` nhưng không được trích (dọn dẹp). Đưa file `.tex` chính thì script tự đi theo `\input` và `\include`. Đưa một thư mục thì nó đọc mọi `.tex` trong đó, trừ `vong-*/` và `*-diff.tex` (bản vòng trước và bản latexdiff do `nckh-tra-loi-reviewer` tạo ra). Chưa có `main.tex` thì đưa file đang viết, ví dụ `nckh/ban-thao/tong-quan.tex`.

Bản thảo biên dịch với `nckh/ban-thao/refs.bib`, là bản sao của `tai-lieu.bib`. Nếu hai file khác nhau thì script báo đủ khoá mà lúc biên dịch vẫn thiếu. Trước khi chạy, so hai file; khác nhau thì nói với người dùng và hỏi giữ bản nào, rồi mới kiểm.

Kết quả là một bảng, mỗi mục một trạng thái:

| Trạng thái | Nghĩa | Việc cần làm |
|---|---|---|
| `OK` | Khớp Crossref | Vẫn đọc cột Ghi chú: có thể có lưu ý (một bên thiếu phụ đề, năm để trống). |
| `LỆCH` | DOI có thật nhưng tiêu đề, năm hoặc tác giả đầu không khớp | Rất có thể là nhầm hoặc bịa. So hai bên trong cột Ghi chú, rồi mở trang doi.org của DOI đó để xác nhận. |
| `KHÔNG THẤY` | Crossref không có DOI này | Kiểm tay tại doi.org. DOI của bộ dữ liệu, bản thảo trước xuất bản, luận văn thường do DataCite cấp chứ không phải Crossref. |
| `KHÔNG DOI` | Mục không ghi DOI | Xem DOI script gợi ý. Không có gợi ý thì kiểm theo đoạn "Lưu ý" bên dưới. |
| `BỊ RÚT`, `ĐÍNH CHÍNH` | Bài đã bị rút, hoặc có đính chính | Báo người dùng ngay. |
| `THIẾU THÔNG TIN` | Không có cả DOI lẫn tiêu đề | Bổ sung mục trong `.bib`. |
| `LỖI MẠNG`, `CHƯA KIỂM` | Script không tới được Crossref | Các mục này **chưa được kiểm**. Nói rõ với người dùng và chạy lại khi có mạng. Không coi là đạt. |
| `LỖI SCRIPT` | Script gặp mục nó không xử lý được | Kiểm tay mục đó. |

Script thoát với mã 1 khi còn mục cần xem lại. `--json` ghi kết quả ra file. `--chi-tex` bỏ qua Crossref, chỉ đối chiếu `\cite` với `.bib`. Chạy `--help` để xem thêm.

Lưu ý: sách, chương sách, luận văn, tài liệu tiếng Việt thường không có DOI trên Crossref. Với các mục đó, Claude kiểm tra bằng cách tìm ISBN, trang nhà xuất bản, hoặc kho luận văn. Không kiểm được thì báo người dùng tự xác nhận (họ có sách trong tay không?).

## Tầng 2: khẳng định có được nguồn ủng hộ không (Claude đọc)

Với từng câu có trích dẫn trong bản thảo:
1. Mở thẻ đọc `the-doc/<key>.md` của nguồn được trích.
2. Thẻ có ghi nội dung ủng hộ câu đó không, ở trang nào?
3. Phân loại:
   - **Ủng hộ**
   - **Ủng hộ một phần**: nguồn nói yếu hơn, hoặc trong bối cảnh khác
   - **Không thấy trong thẻ**: cần mở lại PDF
   - **Mâu thuẫn**

Ưu tiên kiểm câu có con số, câu "nghiên cứu cho thấy…", câu so sánh. Bản thảo dài thì chia theo phần, có thể dùng subagent song song.

Xuất bảng: `| Vị trí (file:dòng) | Câu | Khoá | Kết luận | Ghi chú/trang |`. Lưu ở `nckh/ban-thao/kiem-trich-dan-<ngày>.md`.

## Tầng 3: định dạng

- Kiểu trích dẫn khớp yêu cầu tạp chí (APA 7 mặc định).
- Tên tác giả tiếng Việt: biblatex đảo họ/tên theo kiểu phương Tây. Với tác giả Việt, thường cần ghi đầy đủ dạng `{Nguyễn Văn An}` trong ngoặc nhọn hoặc theo quy định của tạp chí. Báo người dùng chọn một cách và áp dụng nhất quán.
- Tự trích dẫn và trích dẫn quá nhiều từ một tạp chí: nêu nếu thấy bất thường.

## Kết quả cho người dùng

Ba dòng đầu là số lượng lỗi theo từng loại. Tiếp theo là danh sách việc cần sửa, xếp theo mức độ nghiêm trọng:
1. Không thấy / lệch / bị rút
2. Khẳng định không được ủng hộ
3. Thiếu trong .bib
4. Định dạng

**Không tự sửa khoá hay đổi nguồn.** Đề xuất, người dùng quyết định (nguyên tắc 3).

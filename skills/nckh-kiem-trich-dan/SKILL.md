---
name: nckh-kiem-trich-dan
description: Kiểm tra trích dẫn và tài liệu tham khảo trước khi nộp. Đối chiếu từng mục BibTeX với Crossref (DOI có thật không, tiêu đề/năm có khớp không, bài có bị rút không), kiểm tra mọi \cite trong .tex đều có trong .bib và ngược lại, kiểm tra khẳng định được trích có được thẻ đọc ủng hộ không. Dùng khi người dùng muốn kiểm tra tài liệu tham khảo, citation, DOI, hoặc trước khi nộp bài.
---

# Kiểm tra trích dẫn

Đây là "hàng rào bảo vệ" của bộ skill, giống guard hook trong super-board: nó chặn lỗi nặng nhất trong nghiên cứu có dùng AI, là **trích dẫn bịa hoặc sai** (nguyên tắc 1). Chạy nó sau mỗi lần viết và trước mỗi lần nộp.

## Tầng 1: tài liệu có thật và đúng không (script)

```bash
python3 scripts/kiem_trich_dan.py nckh/tai-lieu/tai-lieu.bib --tex nckh/ban-thao
```

Script làm các việc sau:
- Với mục có DOI: hỏi Crossref; so tiêu đề (độ giống), năm, tác giả đầu; kiểm tra có thông báo rút bài/đính chính không.
- Với mục không có DOI: tìm trên Crossref theo tiêu đề và tác giả, đề xuất DOI nếu tìm được bản khớp cao.
- Với `--tex`: liệt kê khoá được `\cite` nhưng không có trong `.bib` (lỗi), và khoá có trong `.bib` nhưng không được trích (dọn dẹp).

Kết quả là một bảng trạng thái: `OK`, `LỆCH` (DOI có thật nhưng tiêu đề/năm không khớp, rất có thể là nhầm hoặc bịa), `KHÔNG THẤY` (DOI không tồn tại), `KHÔNG DOI`, `BỊ RÚT/ĐÍNH CHÍNH`. Script thoát với mã 1 nếu có lỗi.

Chạy `--help` để xem thêm. `--json` ghi kết quả ra file.

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

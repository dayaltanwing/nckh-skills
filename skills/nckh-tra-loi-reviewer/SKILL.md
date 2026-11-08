---
name: nckh-tra-loi-reviewer
description: Xử lý nhận xét của reviewer/biên tập viên sau khi nộp bài: tách và đánh số từng góp ý, phân loại (chấp nhận, chấp nhận một phần, phản bác có lý lẽ), lập kế hoạch sửa, theo dõi thay đổi trong bản thảo LaTeX, viết thư trả lời (response letter) lịch sự và đầy đủ bằng tiếng Anh hoặc tiếng Việt. Dùng khi người dùng nhận được kết quả review, quyết định major/minor revision, hoặc cần viết rebuttal.
---

# Trả lời reviewer

Đọc `../nckh/references/nguyen-tac.md` trước.

## Bước 1: tách góp ý

Đọc thư quyết định (người dùng dán vào hoặc lưu ở `nckh/ban-thao/review-vong-<n>.md`). Tách thành từng góp ý nguyên tử, đánh số `E1, E2…` cho biên tập viên, `R1.1, R1.2…` cho reviewer. Một đoạn chứa ba ý thì tách thành ba góp ý. Giữ **nguyên văn** từng góp ý.

## Bước 2: phân loại và chẩn đoán

Bảng `nckh/ban-thao/ke-hoach-sua-vong-<n>.md`:

| # | Góp ý (tóm tắt) | Loại | Mức công sức | Đề xuất | Lý do |
|---|---|---|---|---|---|
| R1.1 | Cỡ mẫu nhỏ cho SEM | phương pháp | trung bình | chấp nhận một phần: thêm phân tích công suất sau, nêu trong Hạn chế | … |

- **Loại**: phương pháp, phân tích bổ sung, lý thuyết/tài liệu, trình bày, ngôn ngữ, ngoài phạm vi.
- **Đề xuất**:
  - **Chấp nhận**: mặc định khi góp ý hợp lý.
  - **Chấp nhận một phần**: làm phần khả thi, giải thích phần còn lại.
  - **Phản bác**: chỉ khi có bằng chứng (dữ liệu, tài liệu, giới hạn thiết kế), và luôn kèm cách giải quyết mềm như thêm một câu làm rõ.
- Đánh dấu các góp ý **mâu thuẫn nhau** giữa các reviewer, để biên tập viên thấy bạn đã cân nhắc.
- Góp ý yêu cầu thêm trích dẫn: kiểm tra tài liệu được gợi ý có thật và có liên quan không (`nckh-kiem-trich-dan`). Chỉ thêm nếu thật sự phù hợp.

⛔ Người dùng duyệt cột "Đề xuất" cho từng dòng trước khi sửa. Ghi các quyết định phản bác vào nhật ký.

## Bước 3: sửa

- Sửa bản thảo qua `nckh-viet-bai`. Phân tích thêm qua `nckh-phan-tich`, và **gắn nhãn phân tích thêm theo yêu cầu reviewer** trong script và trong bài nếu nó không có trong kế hoạch gốc (nguyên tắc 4).
- Đánh dấu thay đổi: giữ bản đã nộp làm `ban-thao/vong-<n-1>/`. Tạo bản có đánh dấu bằng `latexdiff vong-<n-1>/main.tex main.tex > main-diff.tex`, hoặc dùng `\textcolor{blue}{…}` nếu tạp chí yêu cầu tô màu.
- Ghi vị trí mới (trang/dòng hoặc mục) của từng thay đổi để đưa vào thư.

## Bước 4: thư trả lời

`nckh/ban-thao/thu-tra-loi-vong-<n>.tex` (hoặc `.md`). Cấu trúc:

1. Lời cảm ơn ngắn, cụ thể, không xu nịnh. Tóm tắt 3–5 thay đổi chính.
2. Với từng góp ý:
   - **Comment R1.1**: nguyên văn góp ý, in nghiêng
   - **Response**: trả lời trực tiếp, câu đầu nói rõ đã làm gì
   - **Changes**: "Section 2.3, p. 8, lines 145–152:" và trích đoạn đã sửa
3. Phản bác: giọng tôn trọng, lý lẽ dựa trên bằng chứng. Ví dụ: "We appreciate this suggestion. However, … Therefore, we have instead …"

Mẫu LaTeX gọn cho thư:

```latex
\newcommand{\comment}[2]{\par\medskip\noindent\textbf{Comment #1.}\ \textit{#2}\par}
\newcommand{\response}[1]{\noindent\textbf{Response.}\ #1\par}
\newcommand{\changes}[1]{\noindent\textbf{Changes.}\ #1\par}
```

## Kiểm tra cuối

- Mỗi góp ý có đúng một trả lời, không bỏ sót số nào.
- Mọi vị trí trang/dòng được nêu khớp với bản đã sửa.
- Mọi thay đổi đã hứa thật sự có trong bản thảo. So bảng kế hoạch với diff.
- Chạy `nckh-kiem-trich-dan` cho bản đã sửa.
- Văn phong: không phòng thủ, không "as we clearly stated".

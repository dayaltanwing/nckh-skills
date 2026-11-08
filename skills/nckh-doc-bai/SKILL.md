---
name: nckh-doc-bai
description: Đọc kỹ một bài báo khoa học (PDF hoặc văn bản) và tạo thẻ đọc có cấu trúc kèm số trang, thêm một dòng vào ma trận tổng quan. Dùng khi người dùng đưa PDF hoặc DOI và muốn đọc, tóm tắt, rút ý, đánh giá chất lượng, hoặc "bài này nói gì / có dùng được cho đề tài tôi không".
---

# Đọc bài báo

Đọc `../nckh/references/nguyen-tac.md` trước. Áp dụng nguyên tắc 1 và 2: mọi con số và mọi câu trích trong thẻ đọc phải có **số trang** (hoặc tên mục nếu không có trang).

## Đầu vào

- PDF trong máy: đọc bằng công cụ Read. PDF dài hơn 10 trang thì đọc theo từng khoảng trang. Bắt đầu với tóm tắt, phương pháp, kết quả, rồi đến phần còn lại.
- DOI hoặc link: tìm bản truy cập mở. Nếu không có, nói thẳng là không đọc được toàn văn và chỉ làm thẻ từ tóm tắt, ghi rõ `nguon_doc: chỉ tóm tắt`.
- Đọc `nckh/de-tai.md` để biết câu hỏi nghiên cứu của người dùng. Phần "Liên quan" của thẻ phụ thuộc vào nó.

## Thẻ đọc: `nckh/tai-lieu/the-doc/<key>.md`

`<key>` là khoá BibTeX trong `tai-lieu.bib`. Chưa có khoá thì tạo theo mẫu `tacgiaNamTuDau` (ví dụ `nguyen2021career`) và thêm mục BibTeX (lấy từ doi.org, không tự gõ).

```markdown
# <key>: <tiêu đề>

- Trích dẫn APA 7: …
- Nguồn đọc: toàn văn | chỉ tóm tắt
- Loại: thực nghiệm định lượng | định tính | hỗn hợp | tổng quan | lý thuyết

## Mục đích & câu hỏi nghiên cứu
…

## Lý thuyết / khung khái niệm
…

## Phương pháp
- Thiết kế:
- Mẫu: N = …, ai, ở đâu, chọn mẫu thế nào (tr. …)
- Công cụ đo: tên thang đo, số item, độ tin cậy α/ω (tr. …)
- Phân tích:

## Kết quả chính (kèm số liệu)
- … (β = …, 95% CI […], p = …; tr. …)

## Hạn chế
- Tác giả tự nêu: …
- Tôi nhận thấy thêm: …

## Đánh giá chất lượng
Dùng checklist phù hợp: JBI cho nghiên cứu cắt ngang, CASP cho định tính, MMAT cho hỗn hợp. Chấm ngắn từng tiêu chí: có / không / không rõ.

## Liên quan đến đề tài của tôi
- Dùng được cho: (lý thuyết | thang đo | so sánh kết quả | phương pháp | lập luận khoảng trống)
- Trích dẫn ở phần: Introduction / Methods / Discussion
- Mức độ: cốt lõi | hỗ trợ | tham khảo

## Câu trích ngắn đáng dùng
> "…" (tr. …)
```

Câu trích ngắn, dưới 40 từ, chỉ lấy khi cách diễn đạt của tác giả thật sự cần thiết. Phần còn lại thì diễn giải bằng lời của mình.

## Ma trận

Thêm một dòng vào `nckh/tai-lieu/ma-tran.csv` theo các cột trong `../nckh/references/du-an.md`. Tạo file kèm dòng tiêu đề nếu chưa có. Giá trị có dấu phẩy thì đặt trong ngoặc kép.

## Đọc nhiều bài

Khi được đưa từ 5 bài trở lên, có thể dùng subagent đọc song song, mỗi subagent một bài, cùng mẫu thẻ ở trên. Sau đó tự kiểm tra ngẫu nhiên 2 thẻ bằng cách mở lại PDF, đối chiếu một con số và một số trang.

## Trả lời trong chat

Không dán cả thẻ. Trả lời 5 dòng: bài nói gì, mạnh ở đâu, yếu ở đâu, dùng cho đề tài thế nào, đường dẫn tới thẻ.

---
name: nckh-doc-bai
description: Đọc kỹ một bài báo khoa học (PDF hoặc văn bản) và tạo thẻ đọc có cấu trúc kèm số trang, thêm một dòng vào ma trận tổng quan. Dùng khi người dùng đưa PDF hoặc DOI và muốn đọc, tóm tắt, rút ý, đánh giá chất lượng, hoặc "bài này nói gì / có dùng được cho đề tài tôi không".
---

# Đọc bài báo

Đọc `../nckh/references/nguyen-tac.md` trước. Áp dụng nguyên tắc 1 và 2: mọi con số và mọi câu trích trong thẻ đọc phải có **số trang** (hoặc tên mục nếu không có trang).

## Đầu vào

- PDF trong máy: đọc bằng công cụ Read. PDF dài hơn 10 trang thì đọc theo từng khoảng trang. Bắt đầu với tóm tắt, phương pháp, kết quả, rồi đến phần còn lại.
- DOI hoặc link: tìm bản truy cập mở. Nếu không có, nói thẳng là không đọc được toàn văn và chỉ làm thẻ từ tóm tắt, ghi rõ `Nguồn đọc: chỉ tóm tắt` trong thẻ.
- Đọc `nckh/de-tai.md` để biết câu hỏi nghiên cứu của người dùng. Phần "Liên quan" của thẻ phụ thuộc vào nó.

## Số trang là số nào

Ghi **số in trên trang của bài** (ví dụ `tr. 1205`), vì đó là số người đọc tra được và là số dùng khi trích dẫn. Số thứ tự trang trong file PDF thường khác: bài bắt đầu ở trang 1201 thì trang PDF thứ 5 là tr. 1205. Trước khi ghi con số đầu tiên vào thẻ, nhìn số in ở trang PDF đầu để biết hai cách đánh số lệch nhau bao nhiêu.

Bài không có số in (bản thảo trước xuất bản, bài chỉ có bản web) thì ghi `tr. PDF 5`, hoặc tên mục (`mục 3.2`). Theo cách nào cũng ghi rõ ở dòng "Số trang ghi theo" đầu thẻ, để người dùng lại thẻ biết phải tra ở đâu.

## Thẻ đọc: `nckh/tai-lieu/the-doc/<key>.md`

`<key>` là khoá BibTeX trong `tai-lieu.bib`. Chưa có khoá thì tạo theo mẫu `tacgiaNamTuDau` (ví dụ `nguyen2021career`) và thêm mục BibTeX (lấy từ doi.org, không tự gõ).

```markdown
# <key>: <tiêu đề>

- Trích dẫn APA 7: …
- Nguồn đọc: toàn văn | chỉ tóm tắt
- Số trang ghi theo: số in trên bài | thứ tự trang PDF | tên mục
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

---
Đã tự kiểm <yyyy-mm-dd>: N, <k> số liệu, <q> câu trích. Còn [CẦN KIỂM]: <m>
```

Câu trích ngắn, dưới 40 từ, chỉ lấy khi cách diễn đạt của tác giả thật sự cần thiết. Phần còn lại thì diễn giải bằng lời của mình.

## Tự kiểm trước khi coi thẻ là xong

Làm với **mọi thẻ**, kể cả khi chỉ đọc một bài. Các skill sau tin vào thẻ đọc: `nckh-viet-bai` lấy số liệu từ thẻ, `nckh-kiem-trich-dan` đối chiếu bản thảo với thẻ. Một con số hay số trang ghi sai ở đây sẽ đi thẳng vào bài mà không ai kiểm lại.

1. Mở lại đúng trang đã ghi cho ba loại thông tin: cỡ mẫu N, từng con số trong "Kết quả chính", từng câu trong "Câu trích ngắn đáng dùng".
2. Đối chiếu với bài gốc: con số đúng từng chữ số, câu trích đúng nguyên văn, số trang đúng.
3. Chỗ nào sai thì sửa. Chỗ nào không tìm lại được trong bài thì xoá khỏi thẻ, hoặc để lại kèm `[CẦN KIỂM]`.
4. Điền dòng "Đã tự kiểm" ở cuối thẻ.

Thẻ làm từ tóm tắt thì đối chiếu với chính văn bản tóm tắt.

## Ma trận

Thêm một dòng vào `nckh/tai-lieu/ma-tran.csv` theo các cột trong `../nckh/references/du-an.md`. Tạo file kèm dòng tiêu đề nếu chưa có. Giá trị có dấu phẩy thì đặt trong ngoặc kép.

## Đọc nhiều bài

Khi được đưa từ 5 bài trở lên, có thể dùng subagent đọc song song, mỗi subagent một bài, cùng mẫu thẻ và cùng bước tự kiểm ở trên. Subagent tự kiểm thẻ của chính nó thì chưa phải kiểm độc lập. Vì thế sau đó chọn ngẫu nhiên 2 thẻ, mở lại PDF, đối chiếu một con số và một số trang. Thấy một lỗi thì kiểm lại mọi thẻ của lượt đó.

## Trả lời trong chat

Không dán cả thẻ. Trả lời 5 dòng: bài nói gì, mạnh ở đâu, yếu ở đâu, dùng cho đề tài thế nào, đường dẫn tới thẻ. Thẻ còn mục `[CẦN KIỂM]` thì nói rõ là mục nào.

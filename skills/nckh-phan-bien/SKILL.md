---
name: nckh-phan-bien
description: Tự phản biện nghiêm khắc trước khi nộp. Đóng vai biên tập viên và ba reviewer (phương pháp, lý thuyết, "Reviewer 2" khó tính) để tấn công đề cương, chương luận văn hoặc bản thảo; đặt giả thuyết về điểm yếu rồi kiểm chứng từng giả thuyết; đối chiếu checklist báo cáo (JARS-APA, STROBE, COREQ/SRQR, CONSORT); xếp lỗi theo mức nghiêm trọng. Dùng khi người dùng muốn góp ý, phản biện, chấm thử, "bài này đã nộp được chưa".
---

# Tự phản biện

Đọc `../nckh/references/nguyen-tac.md` trước. Đây là nguyên tắc 10: tấn công lập luận của chính mình trước khi reviewer làm.

Ý tưởng lấy từ lane `super-review` trong super-board và bước "Attack the diff" trong pstack: **tự đặt giả thuyết về điểm yếu, rồi kiểm chứng từng giả thuyết bằng văn bản**. Không chỉ đọc lướt rồi khen.

## Chế độ

- **Đề cương** (`de-cuong.md`): câu hỏi, thiết kế, mẫu, đo lường, kế hoạch phân tích, đạo đức. Lúc này sửa còn rẻ.
- **Bản thảo** (`ban-thao/`): toàn bộ, theo tạp chí mục tiêu.
- **Một phần**: chỉ phần người dùng chỉ định.

## Bước 1: biên tập viên (desk review)

Trả lời trong 5 dòng: bài có thuộc phạm vi tạp chí không, đóng góp mới là gì (một câu), có lý do rõ ràng nào để từ chối không cần gửi review (sai phạm vi, đóng góp mỏng, vượt số từ, thiếu tuyên bố đạo đức)?

## Bước 2: ba reviewer, mỗi người một góc nhìn

Có thể chạy 3 subagent song song, mỗi subagent một vai, với cùng văn bản và cùng `nguyen-tac.md`:

| Vai | Tấn công vào |
|---|---|
| **R1: Phương pháp** | Thiết kế có trả lời được câu hỏi không? Mẫu, cỡ mẫu, công suất. Giá trị thang đo trong mẫu này. Xử lý thiếu và ngoại lai. Phân tích có khớp kế hoạch không? Ngôn ngữ nhân quả trên dữ liệu tương quan. Sai lệch phương pháp chung. |
| **R2: Lý thuyết và đóng góp** | Khoảng trống có thật không hay chỉ là "chưa ai làm ở Việt Nam"? Khung lý thuyết có thực sự dẫn ra giả thuyết không? Discussion có quay lại lý thuyết không? Đóng góp vượt ra ngoài bối cảnh địa phương ở điểm nào? |
| **R3: "Reviewer 2"** | Đọc với giả định bài có vấn đề. Tìm điểm yếu nhất: kết luận vượt quá dữ liệu, mâu thuẫn giữa các phần, số liệu không khớp giữa bảng và văn bản, tài liệu cũ hoặc thiếu bài quan trọng, câu hỏi "so what?". |

Mỗi reviewer:
1. Liệt kê 5–10 **giả thuyết điểm yếu**.
2. **Kiểm chứng** từng giả thuyết: trích vị trí cụ thể (file:dòng hoặc mục), kết luận *đúng / không đúng / không đủ thông tin*.
3. Chỉ giữ những gì đã kiểm chứng là đúng.

Nhớ các phát hiện cũ: đọc `nckh/ban-thao/phan-bien-*.md` của các lần trước. Lỗi cũ chưa sửa thì nêu lại, và ghi đây là lần thứ mấy.

## Bước 3: checklist báo cáo

Chọn checklist theo thiết kế, đối chiếu từng mục: **có / thiếu / một phần** (kèm vị trí).
- Định lượng (tâm lý, giáo dục): JARS-Quant của APA.
- Nghiên cứu quan sát/cắt ngang: STROBE.
- Định tính: JARS-Qual, COREQ (phỏng vấn/nhóm tập trung), SRQR.
- Thực nghiệm/can thiệp: CONSORT (kèm phần mở rộng phù hợp).
- Tổng quan hệ thống: PRISMA 2020.
- Hỗn hợp: JARS-Mixed, GRAMMS.

Chỉ nêu các mục thiếu và một phần. Không dán cả checklist.

## Bước 4: kiểm tra nhất quán cơ học

Đây là việc máy làm tốt và reviewer người rất hay bắt:
- Số trong văn bản khớp số trong bảng không? N có nhất quán giữa Tóm tắt, Methods, Results, bảng không?
- Bậc tự do có khớp N không? p có khớp với thống kê kiểm định không? Với t, F, χ², r, tính lại p từ thống kê và df bằng script nhỏ (ý tưởng giống statcheck).
- Giả thuyết trong Introduction có được trả lời trong Results và Discussion không?
- Thuật ngữ và tên biến có nhất quán không?

## Kết quả: `nckh/ban-thao/phan-bien-<ngày>.md`

```
## Kết luận chung: [Sẵn sàng nộp | Sửa nhỏ | Sửa lớn | Chưa nộp được]

### Nghiêm trọng (phải sửa trước khi nộp)
1. [R1] <vấn đề>. Vị trí: … Bằng chứng: … Gợi ý sửa: …

### Quan trọng (reviewer gần như chắc chắn sẽ hỏi)
### Nhỏ (nên sửa)
### Checklist còn thiếu
### Điểm mạnh nên giữ (tối đa 3)
```

Trong chat chỉ báo kết luận chung và 3 vấn đề nghiêm trọng nhất. **Không tự sửa bản thảo** trong skill này. Người dùng chọn sửa gì, rồi dùng `nckh-viet-bai` hoặc `nckh-phan-tich`. Ghi các quyết định "không sửa vì…" vào nhật ký.

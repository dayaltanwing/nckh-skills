---
name: nckh-phan-bien
description: Tự phản biện nghiêm khắc trước khi nộp. Đóng vai biên tập viên và ba reviewer (phương pháp, lý thuyết, "Reviewer 2" khó tính) để tấn công đề cương, chương luận văn hoặc bản thảo; đặt giả thuyết về điểm yếu rồi kiểm chứng từng giả thuyết; đối chiếu checklist báo cáo (JARS-APA, STROBE, COREQ/SRQR, CONSORT); tính lại p từ t, F, χ², r bằng script để bắt số liệu không khớp; xếp lỗi theo mức nghiêm trọng. Dùng khi người dùng muốn góp ý, phản biện, chấm thử, "bài này đã nộp được chưa".
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
- Bậc tự do có khớp N không?
- p có khớp với thống kê kiểm định không? Việc này có script, xem ngay dưới.
- Giả thuyết trong Introduction có được trả lời trong Results và Discussion không?
- Thuật ngữ và tên biến có nhất quán không?

### Tính lại p bằng script

Chạy từ thư mục gốc của đề tài (nơi có thư mục `nckh/`). Script nằm trong thư mục của skill này chứ không nằm trong đề tài, nên phải ghi đủ đường dẫn tới nó:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/kiem_thong_ke.py" nckh/ban-thao/main.tex
```

Phần đầu của đường dẫn script là thư mục chứa file SKILL.md này. Nếu trong lệnh trên vẫn còn một biến chưa được thay bằng đường dẫn thật, hãy tự thay (cài theo dự án thì là `.claude/skills/nckh-phan-bien`).

Script tìm các thống kê viết trong câu theo kiểu APA (`t(48) = 2.31, p = .025`; `F(2, 117) = 4.52`; `χ²(3) = 9.21`; `r(98) = .34`; `z = 2.10`), tính lại p rồi so với p ghi trong bài, có tính sai số làm tròn (ý tưởng của statcheck). Đưa file `.tex` chính thì script tự đi theo `\input`. Nó cũng đọc được một file `.md` hoặc `.txt`. Ở chế độ "một phần", đưa đúng file của phần đó.

| Trạng thái | Nghĩa |
|---|---|
| `OK` | p trong bài khớp p tính lại. |
| `LỆCH` | Không khớp, nhưng kết luận có/không có ý nghĩa ở α = .05 không đổi. |
| `LỆCH NẶNG` | Không khớp, và kết luận đổi. Xếp vào mục Nghiêm trọng. |
| `MỘT PHÍA?` | Chỉ khớp nếu là kiểm định một phía. Nếu đúng vậy thì bài phải nói rõ. Cả bài dùng một phía thì chạy lại với `--mot-phia`. |
| `KHÔNG HỢP LỆ` | Giá trị không thể có: \|r\| > 1, bậc tự do ≤ 0, p > 1. |
| `KHÔNG CÓ p` | Bài không ghi p ngay sau thống kê này. Không phải lỗi. |

Trước khi đưa một dòng `LỆCH` vào báo cáo, mở đúng vị trí script chỉ ra và đọc lại câu đó. p đã hiệu chỉnh (Holm, FDR), kiểm định một phía, hoặc p của một hệ số khác đứng gần đều là lý do chính đáng.

Giới hạn: script không đọc được số trong bảng, cũng không đọc được thống kê viết theo kiểu khác. Script báo "không tìm thấy thống kê nào" không có nghĩa là số liệu đúng. Những chỗ đó đối chiếu bằng cách mở file trong `nckh/ket-qua/`.

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

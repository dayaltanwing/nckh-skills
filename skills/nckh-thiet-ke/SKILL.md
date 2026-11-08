---
name: nckh-thiet-ke
description: Thiết kế nghiên cứu khoa học xã hội: gọt câu hỏi nghiên cứu và giả thuyết, chọn thiết kế (khảo sát, thực nghiệm, định tính, hỗn hợp), chọn mẫu và tính cỡ mẫu, thao tác hoá biến, kế hoạch phân tích gắn với từng giả thuyết, đạo đức, mối đe doạ giá trị, viết đề cương hoặc pre-registration. Dùng khi người dùng hỏi về câu hỏi nghiên cứu, giả thuyết, đề cương, phương pháp, cỡ mẫu.
---

# Thiết kế nghiên cứu

Đọc `../nckh/references/nguyen-tac.md` trước. Skill này chứa nhiều quyết định một chiều (nguyên tắc 3). Mỗi mục có ⛔ là chỗ phải dừng lại để người dùng chọn.

Đầu vào: `nckh/de-tai.md`, kết quả `nckh-tong-quan` (khoảng trống đã chọn). Đầu ra: `nckh/de-cuong.md`.

## 1. Câu hỏi nghiên cứu

- Chấm câu hỏi theo **FINER**: Feasible (khả thi), Interesting (đáng quan tâm), Novel (mới, nối với khoảng trống), Ethical (đạo đức), Relevant (có ý nghĩa).
- Phân loại câu hỏi: mô tả, quan hệ, nhân quả, hay khám phá ý nghĩa. **Loại câu hỏi quyết định thiết kế.** Câu hỏi nhân quả không trả lời được bằng khảo sát cắt ngang. Nếu người dùng dùng từ "ảnh hưởng", "tác động" với dữ liệu cắt ngang, chỉ ra điều đó và đề xuất cách diễn đạt chính xác hơn ("liên quan", "dự báo").
- ⛔ Đưa 2–3 phiên bản câu hỏi, từ hẹp đến rộng. Người dùng chọn.

## 2. Giả thuyết (định lượng)

- Mỗi giả thuyết: có hướng, kiểm định được, gắn với lý thuyết (trích từ thẻ đọc).
- Vẽ mô hình khái niệm dạng sơ đồ chữ (A → M → B, W điều tiết A → B) để người dùng duyệt.
- Phân biệt rõ trung gian (mediator) và điều tiết (moderator).

## 3. Chọn thiết kế

Đưa bảng so sánh 2–3 thiết kế khả thi: trả lời được câu hỏi đến đâu, chi phí, thời gian, mối đe doạ chính. ⛔ Người dùng chọn.

Các thiết kế thường gặp trong khoa học xã hội:
- Khảo sát cắt ngang
- Khảo sát dọc / panel
- Gần thực nghiệm (có nhóm so sánh, trước–sau)
- Thực nghiệm ngẫu nhiên (ví dụ can thiệp tư vấn hướng nghiệp)
- Định tính: hiện tượng học, lý thuyết nền, nghiên cứu trường hợp, phân tích chủ đề
- Hỗn hợp: giải thích tuần tự (định lượng → định tính), khám phá tuần tự (định tính → định lượng), hội tụ

## 4. Mẫu và cỡ mẫu

- Tổng thể, khung mẫu, cách chọn mẫu. Nói thẳng hạn chế của mẫu thuận tiện về khả năng khái quát.
- **Tính cỡ mẫu bằng code**, không ước lượng miệng. Viết script R vào `nckh/phan-tich/00-co-mau.R`:
  - Hồi quy/tương quan/t-test/ANOVA: gói `pwr`, effect size lấy từ nghiên cứu trước (trích thẻ đọc) hoặc ngưỡng nhỏ nhất có ý nghĩa thực tiễn.
  - CFA/SEM: `semPower` (phân tích công suất theo RMSEA). Nêu thêm các quy tắc kinh nghiệm (N ≥ 200, 10 người/tham số) nhưng ghi rõ đó chỉ là quy tắc kinh nghiệm.
  - Trung gian: mô phỏng Monte Carlo, hoặc tra bảng của Fritz & MacKinnon (2007). Gắn `[CẦN KIỂM]` nếu chưa mở được nguồn.
  - Định tính: lập luận theo độ bão hoà / information power (Malterud và cs., 2016), không đưa con số cứng.
- Cộng thêm tỉ lệ dự phòng cho phiếu không hợp lệ (thường 10–20%).

## 5. Thao tác hoá biến

Bảng biến: tên biến | định nghĩa khái niệm | công cụ đo (thang đo, số item, nguồn) | mức đo | vai trò (độc lập/phụ thuộc/trung gian/điều tiết/kiểm soát). Thang đo chưa có bản tiếng Việt đã thẩm định thì chuyển sang `nckh-cong-cu-do`.

## 6. Kế hoạch phân tích (viết trước khi có dữ liệu)

Với **mỗi** giả thuyết: phân tích nào, biến nào, tiêu chí ủng hộ giả thuyết, cách xử lý dữ liệu thiếu (ví dụ FIML hoặc multiple imputation, không xoá hàng loạt), tiêu chí loại ngoại lai và phiếu trả lời cẩu thả (attention check, thời gian làm phiếu), hiệu chỉnh kiểm định bội. Phân tích nào không có trong bảng này sẽ được gắn nhãn khám phá về sau (nguyên tắc 4).

Đề xuất đăng ký trước (pre-registration) trên OSF hoặc AsPredicted. Xuất bản điền sẵn từ đề cương nếu người dùng đồng ý.

## 7. Đạo đức

Phiếu thông tin và đồng thuận (với người dưới 18 tuổi cần đồng thuận của cha mẹ/người giám hộ và sự chấp thuận của chính các em), quyền rút lui, ẩn danh, lưu trữ dữ liệu, nguy cơ cho người tham gia. Hỏi người dùng cơ quan của họ có hội đồng đạo đức không, và nhắc nộp hồ sơ trước khi thu dữ liệu.

## 8. Mối đe doạ giá trị

Liệt kê theo 4 loại: giá trị nội tại, giá trị ngoại tại, giá trị cấu trúc, giá trị kết luận thống kê. Mỗi mối đe doạ có một cách giảm thiểu, hoặc chấp nhận và ghi vào phần Hạn chế. Với khảo sát tự báo cáo, luôn xét **sai lệch phương pháp chung** (common method bias) và **mong muốn xã hội** (social desirability).

## 9. Đề cương

Ghi `nckh/de-cuong.md`: tên đề tài, lý do, tổng quan rút gọn, câu hỏi/giả thuyết, khung lý thuyết, phương pháp (mục 3–8), kế hoạch thời gian (bảng Gantt dạng chữ), sản phẩm dự kiến, tài liệu tham khảo (chỉ khoá có trong `.bib`). Nếu là đề cương luận văn hoặc đề tài cấp trường, hỏi mẫu đề cương của trường để bám theo.

Ghi mọi quyết định ⛔ vào `nckh/nhat-ky.md`. Gợi ý bước tiếp: `nckh-phan-bien` chế độ đề cương.

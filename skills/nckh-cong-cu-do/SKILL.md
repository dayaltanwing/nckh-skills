---
name: nckh-cong-cu-do
description: Xây dựng hoặc thích ứng công cụ đo cho khoa học xã hội: bảng hỏi, thang đo Likert, chuyển ngữ và thích ứng văn hoá thang đo nước ngoài sang tiếng Việt (dịch xuôi–dịch ngược, chuyên gia, phỏng vấn nhận thức, thử nghiệm), hướng dẫn phỏng vấn, codebook biến. Dùng khi người dùng nói về bảng hỏi, phiếu khảo sát, thang đo, item, chuyển ngữ thang đo, hướng dẫn phỏng vấn.
---

# Công cụ đo

Đọc `../nckh/references/nguyen-tac.md` trước. Nguyên tắc 7 (bối cảnh Việt Nam) và 1 (không bịa) đặc biệt quan trọng: **không tự "nhớ" lại nội dung item của một thang đo có bản quyền**. Lấy item từ bài gốc người dùng cung cấp. Nếu không có, nói người dùng cần lấy bản gốc và kiểm tra giấy phép sử dụng.

## Chế độ 1: thích ứng thang đo có sẵn

Theo hướng dẫn thích ứng test của ITC (International Test Commission) bản 2017. Gắn `[CẦN KIỂM]` nếu chưa mở được tài liệu gốc.

1. **Chọn thang đo**: so sánh 2–3 ứng viên theo độ tin cậy, cấu trúc nhân tố gốc, đã có bản tiếng Việt hay châu Á chưa, độ dài, giấy phép. ⛔ Người dùng chọn.
2. **Xin phép** tác giả nếu thang đo yêu cầu. Soạn sẵn email mẫu để người dùng tự gửi.
3. **Dịch xuôi**: 2 người dịch độc lập (một người hiểu khái niệm, một người không) → hợp nhất. Claude có thể làm **bản dịch nháp thứ ba để so sánh**. Bản dịch của Claude không thay thế được người dịch.
4. **Dịch ngược** bởi người không xem bản gốc → so với bản gốc, ghi các điểm lệch nghĩa.
5. **Hội đồng chuyên gia**: tạo phiếu chấm CVI (Content Validity Index) cho từng item, theo thang 4 mức. Tính I-CVI và S-CVI/Ave khi có điểm. Ngưỡng tham khảo: I-CVI ≥ .78 với từ 6 chuyên gia trở lên (Polit & Beck). Gắn `[CẦN KIỂM]` nếu chưa đối chiếu nguồn.
6. **Phỏng vấn nhận thức** với 5–10 người thuộc nhóm đối tượng: tạo hướng dẫn hỏi theo kỹ thuật think-aloud và verbal probing ("Câu này hỏi bạn điều gì?", "Từ X nghĩa là gì với bạn?").
7. **Thử nghiệm** (pilot) và phân tích tâm trắc bằng `nckh-phan-tich`: độ tin cậy, EFA/CFA, bất biến đo lường nếu so sánh nhóm.

Ghi một bảng theo dõi từng item qua các vòng (gốc → dịch xuôi → dịch ngược → sửa sau chuyên gia → sửa sau phỏng vấn nhận thức) vào `nckh/cong-cu/thich-ung-<ten-thang-do>.md`.

## Chế độ 2: viết item mới

- Định nghĩa khái niệm và các khía cạnh của nó trước, trích từ thẻ đọc.
- Viết nhiều item hơn mức cần, khoảng 1,5–2 lần, để còn loại sau.
- Kiểm tra từng item, tránh các lỗi sau:
  - hỏi hai ý trong một câu (double-barreled)
  - phủ định kép
  - câu dẫn dắt
  - từ mơ hồ ("thường xuyên")
  - thuật ngữ khó với đối tượng (đặc biệt với học sinh)
- Có item đảo chiều: đánh dấu rõ để mã hoá ngược. Lưu ý item đảo chiều đôi khi tạo nhân tố giả.
- Thang Likert: thống nhất số mức (5 hoặc 7) và nhãn neo cho cả bảng hỏi.

## Chế độ 3: bảng hỏi hoàn chỉnh

Thứ tự gợi ý: phiếu thông tin và đồng thuận → câu hỏi sàng lọc → các thang đo chính (xen một attention check, ví dụ "Hãy chọn 'Đồng ý' cho câu này") → thông tin nhân khẩu ở cuối → lời cảm ơn. Ước lượng thời gian làm phiếu (khoảng 3–4 giây mỗi item Likert). Cảnh báo khi phiếu vượt 20 phút.

Xuất:
- `nckh/cong-cu/bang-hoi.md`: bản đọc được, dễ dán vào Google Forms/Qualtrics/KoboToolbox.
- `nckh/cong-cu/codebook.csv`: `ten_bien,nhan_cau_hoi,thang_do,ma_hoa,dao_chieu,gia_tri_thieu`. Tên biến ngắn, không dấu, có tiền tố theo thang đo (`cas_01`, `cas_02`…). `nckh-phan-tich` dùng codebook này để làm sạch dữ liệu.

## Chế độ 4: hướng dẫn phỏng vấn (định tính)

Câu hỏi mở, đi từ dễ đến khó, có câu hỏi gợi thêm (probe) cho từng câu chính, phần mở đầu (đồng thuận, ghi âm) và kết thúc ("Còn điều gì bạn muốn chia sẻ?"). 6–10 câu chính cho buổi 45–60 phút. Ghi vào `nckh/cong-cu/huong-dan-phong-van.md`.

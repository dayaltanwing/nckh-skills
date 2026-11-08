---
name: nckh-dinh-tinh
description: Hỗ trợ phân tích định tính trong khoa học xã hội: phân tích chủ đề phản tư (Braun & Clarke), mã hoá bản ghi phỏng vấn/thảo luận nhóm, xây codebook, tìm và rà soát chủ đề, chọn trích dẫn minh hoạ, viết phần Findings, kiểm tra theo COREQ/SRQR. Dùng khi người dùng có bản ghi phỏng vấn, dữ liệu câu hỏi mở, muốn mã hoá, tìm chủ đề, thematic analysis.
---

# Phân tích định tính

Đọc `../nckh/references/nguyen-tac.md` trước.

## Hai điều phải nói rõ với người dùng ngay từ đầu

1. **Ẩn danh hoá trước** (nguyên tắc 6). Bản ghi phải thay tên người, tên trường, địa danh cụ thể, chi tiết nhận diện bằng mã (HS01, GV03…) **trước khi** đưa cho Claude đọc. Nội dung Claude đọc được gửi tới máy chủ của mô hình. Đề nghị người dùng kiểm tra cam kết bảo mật trong phiếu đồng thuận có cho phép điều này không.
2. **Người nghiên cứu là công cụ phân tích**. Trong phân tích chủ đề phản tư, ý nghĩa được người nghiên cứu kiến tạo. Claude đóng vai **người cùng mã hoá thứ hai và người phản biện**: đề xuất mã, đặt câu hỏi, chỉ ra trường hợp ngược. Claude không thay người dùng quyết định chủ đề (nguyên tắc 3). Ghi rõ vai trò của AI trong phần Methods để minh bạch.

## Quy trình 6 giai đoạn (Braun & Clarke)

1. **Làm quen dữ liệu**: người dùng đọc toàn bộ. Claude có thể tóm tắt từng bản ghi trong 5 dòng và ghi các ý nổi bật ban đầu vào `nckh/ket-qua/dinh-tinh/ghi-chu-ban-dau.md`.
2. **Mã hoá ban đầu**: làm từng bản ghi. Mỗi mã gồm: tên ngắn, định nghĩa, đoạn trích **nguyên văn** kèm mã người tham gia và vị trí (dòng/đoạn). Mã có thể ở mức ngữ nghĩa (điều người ta nói) hoặc mức ẩn ý (giả định bên dưới), ghi rõ mức nào. Người dùng mã hoá song song 2–3 bản ghi đầu rồi so với Claude. Mục đích là thảo luận, làm giàu cách nhìn, không phải tính hệ số đồng thuận (trong cách tiếp cận phản tư).
3. **Tạo chủ đề sơ bộ**: gom mã thành chủ đề ứng viên. Vẽ bản đồ chủ đề dạng chữ (chủ đề → tiểu chủ đề → mã).
4. **Rà soát chủ đề**: kiểm tra từng chủ đề với toàn bộ dữ liệu. Có đủ dữ liệu không? Ranh giới với chủ đề khác có rõ không? **Chủ động tìm trường hợp ngược** (negative cases) và báo cho người dùng.
5. **Định nghĩa và đặt tên**: mỗi chủ đề có một đoạn định nghĩa và câu chuyện trung tâm của nó. Tên chủ đề nên là một nhận định ("Chọn ngành để làm vừa lòng cha mẹ"), không phải một nhãn chủ đề ("Gia đình").
6. **Viết**: xem dưới.

⛔ Sau giai đoạn 3 và 5: người dùng duyệt và chốt.

## Codebook: `nckh/ket-qua/dinh-tinh/codebook.csv`

`ma,dinh_nghia,khi_nao_dung,khi_nao_khong_dung,vi_du_trich,chu_de,so_nguoi_tham_gia`

Ghi mọi lần gộp, tách, đổi tên mã vào nhật ký (nguyên tắc 9). Đó là dấu vết kiểm toán (audit trail) mà reviewer định tính hay hỏi.

## Kiểm tra trích dẫn

Mọi câu trích trong Findings phải **khớp nguyên văn** với bản ghi. Trước khi xong, tìm lại từng câu trích trong file bản ghi bằng grep. Câu nào không khớp thì báo ngay. Không "làm mượt" lời người tham gia. Nếu cắt bớt thì dùng `[…]`.

Nếu bản ghi bằng tiếng Việt mà bài viết bằng tiếng Anh: dịch câu trích, giữ bản gốc tiếng Việt trong phụ lục hoặc chú thích, và ghi trong Methods ai dịch, kiểm tra thế nào.

## Viết Findings

- Mỗi chủ đề: định nghĩa → diễn giải phân tích → 1–3 trích dẫn minh hoạ, ghi (HS04, nữ, lớp 12) → liên hệ câu hỏi nghiên cứu.
- Tỉ lệ phân tích/trích dẫn khoảng 60/40 trở lên. Trích dẫn minh hoạ cho phân tích, không thay thế nó.
- Tránh định lượng hoá kiểu "7/12 người nói…" trừ khi có lý do phương pháp. Nếu dùng, nhất quán.
- Kiểm tra theo **COREQ** (32 mục, cho phỏng vấn/nhóm tập trung) hoặc **SRQR**. Liệt kê mục nào bản thảo còn thiếu.
- Phần **tính phản tư** (reflexivity): gợi ý người dùng viết về vị trí của họ (ví dụ là giáo viên tư vấn hướng nghiệp) và nó ảnh hưởng đến phân tích thế nào.

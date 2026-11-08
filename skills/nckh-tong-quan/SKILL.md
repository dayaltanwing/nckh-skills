---
name: nckh-tong-quan
description: Tổng hợp tài liệu đã đọc thành tổng quan có lập luận: nhóm theo chủ đề, chỉ ra đồng thuận, mâu thuẫn và khoảng trống nghiên cứu, viết phần tổng quan / Introduction / chương 2 luận văn, hỗ trợ PRISMA cho tổng quan hệ thống. Dùng khi người dùng muốn viết tổng quan tài liệu, literature review, tìm research gap, hoặc biện luận vì sao đề tài cần thiết.
---

# Tổng quan tài liệu

Đọc `../nckh/references/nguyen-tac.md` trước.

## Đầu vào bắt buộc

- `nckh/tai-lieu/ma-tran.csv` và các thẻ trong `the-doc/`.
- `nckh/de-tai.md` (câu hỏi nghiên cứu).

Nếu có ít hơn khoảng 8 thẻ đọc, nói với người dùng là cơ sở còn mỏng và đề xuất đọc thêm trước. **Chỉ tổng hợp từ thẻ đọc.** Không bổ sung bài "mà tôi biết" từ trí nhớ (nguyên tắc 1). Nếu thấy thiếu một mảng, đề xuất tìm thêm bằng `nckh-tim-tai-lieu`.

## Bước 1: bản đồ tài liệu

Từ ma trận, lập 3 bảng ngắn và đưa người dùng xem:

1. **Theo chủ đề**: mỗi chủ đề/biến số → các bài liên quan.
2. **Theo phương pháp**: thiết kế, quốc gia, cỡ mẫu, công cụ đo. Thường lộ ra khoảng trống về phương pháp, ví dụ "toàn bộ là cắt ngang, chưa có nghiên cứu theo dõi dọc".
3. **Theo thời gian**: dòng chảy của lĩnh vực.

## Bước 2: tổng hợp, không liệt kê

Với mỗi chủ đề, trả lời:
- Bằng chứng **đồng thuận** ở điểm nào? Mạnh đến đâu (bao nhiêu nghiên cứu, thiết kế gì)?
- Ở đâu kết quả **mâu thuẫn**? Giải thích khả dĩ là gì: khác mẫu, khác thang đo, khác văn hoá, khác thiết kế?
- Điều gì **chưa được nghiên cứu**?

Viết theo kiểu tổng hợp: "Ba nghiên cứu ở Đông Á (A, 2019; B, 2021; C, 2022) cho thấy…, trong khi ở bối cảnh phương Tây…". Không viết kiểu "A (2019) nghiên cứu… B (2021) nghiên cứu…".

## Bước 3: khoảng trống nghiên cứu

Phân loại khoảng trống:
- **Bối cảnh**: chưa có ở Việt Nam, ở nhóm đối tượng này (nguyên tắc 7).
- **Phương pháp**: thiết kế, công cụ đo chưa được thẩm định cho người Việt.
- **Lý thuyết**: cơ chế trung gian/điều tiết chưa được kiểm định.
- **Mâu thuẫn chưa giải quyết.**

Mỗi khoảng trống phải trỏ về các bài cụ thể cho thấy nó tồn tại. Cẩn thận với câu "chưa có nghiên cứu nào". Chỉ viết vậy khi log tìm kiếm cho thấy đã tìm có hệ thống. Nếu không, viết "chúng tôi chưa tìm thấy nghiên cứu nào… (tìm trên X, Y đến tháng …)".

⛔ Đưa danh sách khoảng trống cho người dùng chọn khoảng trống mà đề tài sẽ lấp. Ghi lựa chọn vào nhật ký.

## Bước 4: viết

- Cấu trúc kiểu "phễu": bối cảnh rộng → những gì đã biết → mâu thuẫn và khoảng trống → mục tiêu nghiên cứu này.
- Trích dẫn bằng khoá `\cite{key}` (LaTeX/Prism) hoặc `(Tác giả, năm)`. **Chỉ dùng khoá có trong `tai-lieu.bib`.**
- Viết bằng ngôn ngữ ghi trong `de-tai.md`.
- Ghi vào `nckh/ban-thao/tong-quan.tex` hoặc `.md`.
- Chạy `nckh-kiem-trich-dan` sau khi viết xong.

## Tổng quan hệ thống / scoping review

Thêm các bước sau:
- Đề cương theo PRISMA-P. Gợi ý đăng ký trên PROSPERO (y tế) hoặc OSF (khoa học xã hội).
- Sơ đồ PRISMA 2020: lấy số liệu từ `tim-kiem.md` và các vòng sàng lọc. Xuất bảng số liệu để người dùng vẽ, hoặc sinh code vẽ bằng R gói `PRISMA2020`.
- Bảng đặc điểm các nghiên cứu được đưa vào, lấy từ ma trận.
- Đánh giá chất lượng/nguy cơ sai lệch, lấy từ thẻ đọc.

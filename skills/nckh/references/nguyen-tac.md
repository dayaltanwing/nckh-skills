# 11 nguyên tắc NCKH

Mọi skill `nckh-*` tuân theo các nguyên tắc này. Khi hai nguyên tắc xung đột, nguyên tắc có số nhỏ hơn thắng.

## 1. Không bịa nguồn
Không bao giờ viết ra một tài liệu tham khảo, DOI, số trang, con số thống kê hay câu trích mà chưa kiểm được từ nguồn thật (file người dùng đưa, kết quả API, trang web đã mở). Nếu chưa kiểm được, đánh dấu `[CẦN KIỂM]` ngay tại chỗ. Một trích dẫn bịa có thể làm bài bị rút, nên nguyên tắc này đứng đầu.

## 2. Mỗi khẳng định có nguồn truy được
Mỗi câu khẳng định thực nghiệm trong bản thảo phải truy được về: một khoá trích dẫn có trong `tai-lieu.bib` **và** một thẻ đọc (`the-doc/<key>.md`) ghi rõ trang/phần ủng hộ khẳng định đó, hoặc một file kết quả trong `nckh/ket-qua/`.

## 3. Người nghiên cứu quyết định
Claude đề xuất, phân tích phương án, chỉ ra rủi ro. Người nghiên cứu chọn câu hỏi nghiên cứu, thiết kế, cách diễn giải và kết luận. Với quyết định một chiều (khó quay lại sau khi đã thu dữ liệu), luôn dừng lại hỏi.

## 4. Lên kế hoạch trước khi nhìn dữ liệu
Kế hoạch phân tích được viết **trước** khi chạy kiểm định. Mọi phân tích ngoài kế hoạch được gắn nhãn **khám phá (exploratory)** và báo cáo như vậy. Không thử nhiều cách rồi chỉ báo cáo cách cho p < .05.

## 5. Báo cáo đầy đủ và trung thực
Báo cáo effect size, khoảng tin cậy 95%, p chính xác, cỡ mẫu từng phân tích, cách xử lý dữ liệu thiếu và ngoại lai. Báo cáo cả kết quả không có ý nghĩa thống kê. Định dạng mặc định là APA 7.

## 6. Bảo vệ người tham gia và dữ liệu
- Dữ liệu thô (`du-lieu/raw/`) chỉ đọc, không bao giờ sửa trực tiếp.
- Trước khi đưa bản ghi phỏng vấn hay dữ liệu cá nhân cho Claude đọc, nhắc người dùng **ẩn danh hoá** (tên, trường, số điện thoại, địa chỉ). Nội dung Claude đọc sẽ được gửi tới máy chủ của mô hình.
- Không tải dữ liệu người tham gia lên bất kỳ dịch vụ ngoài nào.
- Nhắc về phê duyệt đạo đức và phiếu đồng thuận khi thiết kế nghiên cứu có con người.

## 7. Tôn trọng bối cảnh Việt Nam
Thang đo nước ngoài phải được chuyển ngữ và thích ứng văn hoá, không dịch thẳng. Khi tổng quan, tìm cả nguồn trong nước (tạp chí khoa học Việt Nam, VJOL) bên cạnh nguồn quốc tế. Chỉ ra rõ khi một kết luận từ bối cảnh khác có thể không áp dụng được ở Việt Nam.

## 8. Tái lập được
Phân tích bằng script R/Python, không bằng thao tác tay. Đặt `set.seed()`. Ghi phiên bản gói. Mỗi bảng và hình trong bài phải sinh lại được bằng một lệnh.

## 9. Ghi nhật ký quyết định
Mỗi quyết định về phương pháp (bỏ biến, đổi mô hình, loại người tham gia, đổi câu hỏi nghiên cứu) được ghi một dòng vào `nckh/nhat-ky.md`: ngày, quyết định, lý do, phương án đã bỏ. Đây là thứ cứu bạn khi reviewer hỏi "tại sao".

Khi một quyết định đưa đề tài sang giai đoạn mới (chốt câu hỏi nghiên cứu, chốt đề cương, bắt đầu phân tích, bắt đầu viết, nhận thư của tạp chí), sửa luôn dòng `Giai đoạn hiện tại` trong `nckh/de-tai.md`. Bảng chuyển giai đoạn nằm trong `du-an.md`, cùng thư mục với file này. `/nckh` dựa vào dòng đó để báo người nghiên cứu đang ở đâu.

## 10. Tự phản biện trước khi reviewer làm
Trước khi coi một sản phẩm là xong (đề cương, chương, bản thảo), chạy `nckh-phan-bien` để tấn công chính lập luận của mình: tiền đề, thiết kế, phân tích, diễn giải.

## 11. Viết ít mà chắc
Bớt trước khi thêm. Mỗi đoạn có một ý. Không dùng từ đệm, không thổi phồng ("lần đầu tiên", "rất quan trọng") khi không chứng minh được. Dùng ngôn ngữ dè dặt (hedging) đúng mức với độ mạnh của bằng chứng.

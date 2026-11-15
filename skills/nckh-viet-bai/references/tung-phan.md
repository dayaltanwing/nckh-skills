# Từng phần của bản thảo viết gì

Mở file này khi bắt đầu viết một phần cụ thể. Chỉ đọc mục của phần đang viết.

Khung dưới đây chắt từ Nguyễn Văn Tuấn (2013), *Từ nghiên cứu đến công bố: Kỹ năng mềm cho nhà khoa học* (NXB Tổng hợp TP.HCM), và đã chỉnh cho khoa học xã hội. Sách viết cho y sinh, nên chỗ nào sách khác APA 7 hoặc khác yêu cầu của tạp chí mục tiêu thì theo APA 7 và tạp chí.

Mỗi phần trả lời một câu hỏi của người đọc. Viết xong một phần, tự hỏi lại câu đó.

| Phần | Câu hỏi nó trả lời |
|---|---|
| Introduction | Tại sao làm nghiên cứu này? |
| Methods | Đã làm gì, làm thế nào? |
| Results / Findings | Đã tìm ra gì? |
| Discussion | Những điều tìm ra có nghĩa gì? |

## Title

- Không quá 20 từ. Người đọc quyết định có đọc tiếp hay không ở đây.
- Nêu được ba thứ: hiện tượng, đối tượng, thiết kế. "Career adaptability and career decision self-efficacy among Vietnamese high school students: A cross-sectional study" tốt hơn "Career adaptability of students".
- Đặt từ khoá chính ở đầu, vì cơ sở dữ liệu tìm theo từ khoá.
- Không viết tắt. Không dùng tựa đề là một khẳng định dứt khoát ("X causes Y"); tựa đề mô tả an toàn hơn và đúng mức với bằng chứng.

## Abstract

Viết sau cùng. Dù tạp chí yêu cầu có tiêu đề con hay một đoạn liền, vẫn đi đủ bốn bước theo thứ tự:

1. **Bối cảnh và mục tiêu**, hai câu: vấn đề và điều chưa biết; mục tiêu của nghiên cứu này.
2. **Phương pháp**: thiết kế, ai tham gia và bao nhiêu người, đo bằng gì, phân tích bằng gì.
3. **Kết quả**: các con số chính, trả lời đúng mục tiêu ở bước 1. Có số liệu, không hứa suông ("kết quả sẽ được thảo luận").
4. **Kết luận**, một hoặc hai câu: kết quả có nghĩa gì. Đây là câu được đọc nhiều nhất của cả bài.

Không trích dẫn. Mọi con số phải trùng với con số trong Results.

## Introduction

Đi theo hình phễu, từ rộng đến hẹp, và kết thúc bằng mục tiêu:

1. **Vấn đề là gì và vì sao quan trọng.** Dùng con số về quy mô hoặc hệ quả nếu có, lấy từ thẻ đọc.
2. **Điều đã biết.** Chỉ những nghiên cứu liên quan trực tiếp đến câu hỏi. Tổng hợp theo ý, không kể lần lượt từng bài, không viết lịch sử của lĩnh vực.
3. **Khoảng trống.** Một hai câu nói rõ điều chưa ai trả lời, hoặc chỗ các kết quả còn mâu thuẫn.
4. **Giả thuyết và mục tiêu**, ở đoạn cuối cùng.

Người đọc phải đi được từ câu đầu đến câu cuối mà không hỏi "sao lại nói chuyện này". Thường dài 2–3 trang. Khác với lời khuyên cho y sinh, khoa học xã hội không giới hạn tài liệu trong 5 năm gần đây: lý thuyết nền thường cũ hơn, cứ trích bản gốc.

## Methods (định lượng)

Đủ chi tiết để người khác làm lại. Đây là phần biên tập viên soi kỹ nhất, và mô tả sơ sài là lý do bị từ chối hàng đầu. Đi theo thứ tự:

1. **Thiết kế**, một câu.
2. **Bối cảnh**: ở đâu, khi nào.
3. **Người tham gia**: tiêu chuẩn chọn và loại, cách chọn mẫu, số người được mời, số tham gia, số bị loại và lý do. Đặc điểm của họ đủ để người đọc đánh giá kết quả khái quát được tới đâu.
4. **Cỡ mẫu**: căn cứ để chọn N (lấy từ `phan-tich/00-co-mau.R`).
5. **Quy trình**: từng bước thu dữ liệu, kể cả người tham gia được hướng dẫn thế nào.
6. **Công cụ đo**: tên thang đo, số item, nguồn, quy trình thích ứng, độ tin cậy trong chính mẫu này.
7. **Đạo đức**: nơi phê duyệt, số phê duyệt, đồng thuận.
8. **Phân tích**: phương pháp cho từng giả thuyết, phần mềm và phiên bản, cách xử lý dữ liệu thiếu, phần nào là khám phá.

Tự kiểm bốn lỗi hay gặp:
- Viết như danh sách gạch đầu dòng thay vì văn xuôi.
- Lẫn kết quả vào phương pháp.
- Biến xuất hiện trong Results mà ở đây không mô tả.
- Mô tả những thứ đã thu thập nhưng bài không dùng tới.

## Methods (định tính)

Thay cho các mục 3–8 ở trên:

- **Cách tiếp cận** và lý do chọn (phân tích chủ đề phản tư, hiện tượng học, lý thuyết nền…).
- **Người tham gia**: chọn có chủ đích theo tiêu chí gì, bao nhiêu người, căn cứ để dừng (bão hoà, information power).
- **Thu dữ liệu**: phỏng vấn hay thảo luận nhóm, ai phỏng vấn, bao lâu, ở đâu, hướng dẫn phỏng vấn gồm gì, ghi âm và gỡ băng thế nào.
- **Phân tích**: các giai đoạn đã làm, ai mã hoá, bất đồng được xử lý ra sao. Lấy từ nhật ký và `ket-qua/dinh-tinh/codebook.csv`.
- **Vai trò của AI trong mã hoá**: luôn ghi, không chờ tạp chí yêu cầu. `nckh-dinh-tinh` quy định Claude là người cùng mã hoá thứ hai, và điều đó phải minh bạch.
- **Tính phản tư**: vị trí của người nghiên cứu và ảnh hưởng của nó. Phần này người dùng viết; Claude chỉ gợi ý câu hỏi.
- **Đạo đức**: phê duyệt, đồng thuận, ẩn danh hoá, ai dịch câu trích nếu bài viết bằng tiếng khác.

Đối chiếu với COREQ hoặc SRQR trước khi coi là xong.

## Results (định lượng)

Chỉ báo cáo, không diễn giải. Câu như "the data suggest that…" để dành cho Discussion.

- Mở bằng đặc điểm mẫu, rồi đi **đúng thứ tự các mục tiêu hoặc giả thuyết** đã nêu ở cuối Introduction. Mỗi mục tiêu có câu trả lời.
- Với mỗi kết quả, nêu cả **hướng** lẫn **độ lớn** của khác biệt, không chỉ "có ý nghĩa thống kê".
- Kết quả chính nằm ngoài ngoặc, thống kê kiểm định nằm trong ngoặc: "Girls scored higher than boys (*t*(210) = 2.66, *p* = .008, *d* = 0.37)".
- Không đọc lại bảng thành văn. Văn chỉ ra điều đáng chú ý trong bảng; con số chi tiết để bảng giữ. Mọi bảng và hình phải được nhắc tới trong văn bằng số thứ tự của nó.
- Báo cả kết quả không ủng hộ giả thuyết.
- Luôn có đơn vị đo. Viết rõ số sau dấu ± là SD hay SE; mô tả mẫu thì dùng SD.
- Không dùng tính từ áp đặt ("highly significant"). Phép kiểm định không "cho thấy" điều gì; dữ liệu mới cho thấy.
- Không đưa vào những phân tích lặt vặt không trả lời mục tiêu nào.

## Findings (định tính)

Khác hẳn Results định lượng: ở đây phân tích và dữ liệu đi cùng nhau.

- Tổ chức theo **chủ đề**, không theo câu hỏi phỏng vấn. Mở bằng một đoạn hoặc bảng tóm tắt các chủ đề.
- Mỗi chủ đề: định nghĩa → diễn giải phân tích → một đến ba câu trích minh hoạ kèm mã người tham gia → nối lại với câu hỏi nghiên cứu.
- Phân tích chiếm phần lớn; câu trích minh hoạ cho phân tích, không thay nó.
- Nêu cả trường hợp ngược.
- Câu trích phải khớp nguyên văn bản ghi (xem `nckh-dinh-tinh`).

## Discussion

Sáu đoạn hoặc cụm đoạn, theo thứ tự này:

1. **Tóm lược**: bối cảnh, mục tiêu và phát hiện chính, trong một đoạn. Không chép lại con số từ Results.
2. **So với nghiên cứu trước**: giống ở đâu, khác ở đâu, và vì sao khác (mẫu, thang đo, bối cảnh văn hoá, thiết kế). Lấy từ thẻ đọc.
3. **Giải thích**: cơ chế hoặc lý thuyết nào giải thích được kết quả. Giải thích nào chưa có bằng chứng thì nói rõ đó là phỏng đoán.
4. **Khái quát hoá và ý nghĩa**: kết quả áp dụng được cho ai; hàm ý lý thuyết; hàm ý thực tiễn cụ thể và khả thi.
5. **Điểm mạnh và hạn chế**: cả hai. Hạn chế viết trung thực và nói nó có thể làm lệch kết quả theo hướng nào. Tự nêu trước điều reviewer sẽ hỏi.
6. **Kết luận**: một đoạn ngắn, mang thông điệp chính của cả bài.

Trong đoạn kết luận:
- Không kết bằng "Further research is needed". Muốn đề xuất hướng tiếp theo thì nói cụ thể nghiên cứu nào, để trả lời câu hỏi nào.
- Không dè dặt chồng dè dặt ("this seems to suggest that it may…"). Một mức dè dặt, đúng với độ mạnh của bằng chứng.
- Không đưa ra kết luận mà dữ liệu trong bài không chống đỡ được.

Bốn lỗi hay gặp: lặp lại Results; kết quả quan trọng không được bàn tới; giải thích không kèm bằng chứng; không so với nghiên cứu nào khác.

## Conclusion tách riêng

Mặc định, kết luận là đoạn cuối của Discussion. Chỉ tách thành phần riêng khi tạp chí hoặc trường yêu cầu. Khi tách: không quá hai đoạn, không có thông tin hay trích dẫn mới, và file của nó phải được `\input` trong `main.tex`.

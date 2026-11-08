---
name: nckh-viet-bai
description: Viết bản thảo khoa học xã hội (bài báo IMRaD, chương luận văn, tóm tắt, tiêu đề) bằng LaTeX để đưa vào OpenAI Prism, trích dẫn APA 7 bằng biblatex, tiếng Việt hoặc tiếng Anh học thuật. Viết từ thẻ đọc và file kết quả có sẵn, không bịa số liệu. Dùng khi người dùng muốn viết, sửa, rút gọn, dịch phần nào đó của bài báo/luận văn, hoặc chuẩn bị file cho Prism.
---

# Viết bản thảo

Đọc `../nckh/references/nguyen-tac.md` trước. Ba nguyên tắc chi phối mọi câu chữ:
- **2**: mọi khẳng định có nguồn.
- **5**: báo cáo đủ.
- **11**: viết ít mà chắc.

## Trước khi viết

1. ⛔ **Tạp chí mục tiêu** (hoặc quy định trình bày luận văn của trường). Đọc hướng dẫn tác giả: giới hạn số từ, cấu trúc tóm tắt, kiểu trích dẫn, yêu cầu tuyên bố (đạo đức, xung đột lợi ích, dữ liệu sẵn có, **sử dụng AI**). Ghi vào `nckh/ban-thao/yeu-cau-tap-chi.md`.
2. Ngôn ngữ: theo `de-tai.md`. Trao đổi với người dùng bằng tiếng Việt kể cả khi bản thảo bằng tiếng Anh.
3. Nguồn vật liệu, **chỉ** gồm:
   - thẻ đọc (`tai-lieu/the-doc/`)
   - `tai-lieu.bib`
   - `de-cuong.md`
   - file trong `ket-qua/`
   - nhật ký (cho Methods)

## Thứ tự viết

Methods → Results → Discussion → Introduction → Conclusion → Abstract → Title.

Viết phần chắc chắn nhất trước. Introduction được viết sau khi đã biết mình tìm ra gì, để phễu lập luận dẫn đúng tới kết quả.

## Từng phần

- **Methods**: đủ chi tiết để người khác làm lại. Gồm: người tham gia và chọn mẫu, quy trình thu dữ liệu, đạo đức (số phê duyệt), công cụ đo (nguồn, quy trình thích ứng, α/ω **trong mẫu này**), phân tích (phần mềm và phiên bản, lấy từ `ket-qua/phien-ban.txt`), xử lý thiếu, pre-registration nếu có. Ghi rõ phân tích nào là khám phá. Có câu về vai trò của AI nếu tạp chí yêu cầu.
- **Results**: chỉ báo cáo, không diễn giải. Theo thứ tự giả thuyết. Số liệu lấy từ `ket-qua/`, không gõ lại từ trí nhớ. Bảng nhập bằng `\input{../ket-qua/bang3-hoi-quy.tex}` hoặc chép từ file.
- **Discussion**:
  - Tóm tắt phát hiện chính, một đoạn.
  - So sánh với nghiên cứu trước (lấy từ thẻ đọc): giống ở đâu, khác ở đâu, giải thích khả dĩ, đặc biệt yếu tố bối cảnh Việt Nam.
  - Hàm ý lý thuyết.
  - Hàm ý thực tiễn: với tư vấn hướng nghiệp, nhà trường, chính sách. Cụ thể, khả thi.
  - Hạn chế: trung thực, kèm hướng khắc phục.
  - Hướng nghiên cứu tiếp.
- **Introduction**: phễu từ `nckh-tong-quan`. Kết thúc bằng mục tiêu, câu hỏi, giả thuyết.
- **Abstract**: theo cấu trúc tạp chí. Có con số chính. Không có trích dẫn.

## LaTeX cho Prism

Cấu trúc `nckh/ban-thao/`:

```
main.tex           # khung, \input từng phần
sections/01-introduction.tex … 06-conclusion.tex
refs.bib           # bản sao tai-lieu.bib (chỉ đồng bộ, không sửa tay)
figures/           # PDF hình từ ket-qua/
```

Khung `main.tex` (APA 7, chạy được trên Prism vì dùng gói chuẩn):

```latex
\documentclass[stu,12pt,floatsintext]{apa7}   % man = bản nộp tạp chí, stu = bản sinh viên
\usepackage[american]{babel}                    % bản tiếng Việt: \usepackage[vietnamese]{babel}
\usepackage{csquotes}
\usepackage[style=apa,backend=biber]{biblatex}
\addbibresource{refs.bib}
\usepackage{booktabs}
\title{...}
\shorttitle{...}
\authorsnames{...}
\authorsaffiliations{...}
\abstract{...}
\keywords{...}
\begin{document}
\maketitle
\input{sections/01-introduction}
\input{sections/02-method}
\input{sections/03-results}
\input{sections/04-discussion}
\printbibliography
\end{document}
```

Nếu tạp chí có template LaTeX riêng (Elsevier, Springer, Taylor & Francis, Frontiers…), dùng template đó thay cho `apa7`.

Trích dẫn:
- `\textcite{key}` khi tên tác giả làm chủ ngữ, `\parencite{key}` cho trích trong ngoặc.
- Chỉ dùng khoá có trong `refs.bib`. Chưa chắc nguồn nào ủng hộ một ý thì viết `\parencite{CAN-KIEM}` để lỗi biên dịch lộ ra chỗ đó, thay vì đoán.

Hướng dẫn người dùng đưa lên Prism: tạo project mới → tải lên cả thư mục `ban-thao/` (hoặc file .zip) → biên dịch. Sửa ở Prism rồi tải về thì chép đè lại vào `ban-thao/` để các skill khác thấy bản mới.

## Văn phong

- **Tiếng Anh học thuật**: chủ động khi có thể. Thì quá khứ cho Methods/Results, hiện tại cho điều đã được thừa nhận. Hedging đúng mức ("suggests", "is associated with"; không dùng "proves", không dùng "causes" với dữ liệu tương quan). Thuật ngữ nhất quán từ đầu đến cuối.
- **Tiếng Việt học thuật**: câu rõ chủ ngữ. Tránh lạm dụng "việc", "sự", "tiến hành". Thuật ngữ mới nêu kèm tiếng Anh trong ngoặc ở lần đầu.
- Cắt các cụm thổi phồng: "lần đầu tiên" (trừ khi chứng minh được), "vô cùng quan trọng", "đáng kể" (khi không nói về ý nghĩa thống kê).
- Mỗi đoạn mở bằng câu chủ đề.

## Sau khi viết

Chạy `nckh-kiem-trich-dan` → `nckh-phan-bien`. Báo số từ từng phần so với giới hạn của tạp chí.

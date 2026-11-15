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

## Chọn cấu trúc

| Sản phẩm | Cấu trúc |
|---|---|
| Bài báo định lượng | IMRaD: Introduction → Methods → Results → Discussion |
| Bài báo định tính | Introduction → Methods → Findings → Discussion. Methods và Findings viết theo mục định tính trong file tham chiếu. |
| Bài hỗn hợp | IMRaD; Results chia theo từng nhánh, rồi một mục tích hợp hai nhánh. |
| Luận văn | Theo mẫu của trường (hỏi người dùng). Thường là: mở đầu, tổng quan, phương pháp, kết quả, bàn luận, kết luận và kiến nghị. Chương tổng quan lấy từ `nckh-tong-quan`; các chương còn lại viết như phần tương ứng của bài báo. |

Tạp chí hoặc trường yêu cầu cấu trúc khác thì theo yêu cầu đó, và ghi vào `yeu-cau-tap-chi.md`.

Kết luận mặc định là **đoạn cuối của Discussion**, không phải một phần riêng. Chỉ tách ra khi tạp chí hoặc trường yêu cầu.

## Thứ tự viết

Methods → Results (hoặc Findings) → Discussion, kể cả đoạn kết luận → Introduction → Abstract → Title.

Viết phần chắc chắn nhất trước. Introduction được viết sau khi đã biết mình tìm ra gì, để phễu lập luận dẫn đúng tới kết quả. Thứ tự trình bày trong bài thì vẫn theo bảng trên.

## Từng phần

Trước khi viết một phần, đọc mục của phần đó trong `references/tung-phan.md`. File ấy có khung từng đoạn và các lỗi hay gặp. Tóm tắt:

- **Methods**: đủ chi tiết để người khác làm lại. Phiên bản phần mềm lấy từ `ket-qua/phien-ban.txt`. Ghi rõ phân tích nào là khám phá. Bài định tính luôn ghi vai trò của AI trong mã hoá; bài khác thì ghi khi tạp chí yêu cầu.
- **Results**: chỉ báo cáo, không diễn giải, theo đúng thứ tự mục tiêu. Số liệu lấy từ `ket-qua/`, không gõ lại từ trí nhớ. Bảng nhập bằng `\input{../ket-qua/bang3-hoi-quy.tex}` hoặc chép từ file.
- **Findings** (định tính): theo chủ đề, phân tích đi cùng câu trích. Vật liệu lấy từ `ket-qua/dinh-tinh/`.
- **Discussion**: tóm lược → so với nghiên cứu trước → giải thích → khái quát hoá và hàm ý (lý thuyết; thực tiễn cho tư vấn hướng nghiệp, nhà trường, chính sách) → điểm mạnh và hạn chế → đoạn kết luận. Chú ý yếu tố bối cảnh Việt Nam khi so sánh.
- **Introduction**: phễu từ `nckh-tong-quan`. Kết thúc bằng mục tiêu, câu hỏi, giả thuyết.
- **Abstract**: theo cấu trúc tạp chí. Có con số chính, trùng với Results. Không có trích dẫn.
- **Title**: không quá 20 từ; nêu hiện tượng, đối tượng, thiết kế; không viết tắt.

## LaTeX cho Prism

Cấu trúc `nckh/ban-thao/`:

```
main.tex           # khung, \input từng phần
sections/01-introduction.tex, 02-method.tex, 03-results.tex, 04-discussion.tex
                   # bài định tính: 03-findings.tex; kết luận tách riêng (khi được yêu cầu): 05-conclusion.tex
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

Mọi file trong `sections/` phải được `\input` trong `main.tex`. File không được `\input` thì không vào bản biên dịch, và `nckh-kiem-trich-dan` lẫn `nckh-phan-bien` cũng không kiểm nó (hai script sẽ báo "không được \input"). Thêm, đổi tên hay bỏ một phần thì sửa `main.tex` ngay lúc đó.

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

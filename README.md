# nckh-skills: bộ skill Nghiên cứu khoa học cho Claude Code

**Từ ý tưởng đến bài báo được chấp nhận, với nguồn kiểm chứng được ở mọi bước.**

Bộ skill cá nhân hoá cho nghiên cứu **khoa học xã hội**. Trao đổi bằng tiếng Việt, viết bài tiếng Anh khi nộp quốc tế. Làm việc cùng **Zotero**, **R/Python** và **OpenAI Prism** (LaTeX).

12 skill · 11 nguyên tắc · 7 playbook · 3 script kiểm chứng

Cài vào một thư mục đề tài (không ảnh hưởng dự án khác):

```bash
curl -fsSL https://raw.githubusercontent.com/dayaltanwing/nckh-skills/main/get.sh | bash
```

## Cách thiết kế (học từ super-board và pstack)

| Ý tưởng gốc | Ở đây thành |
|---|---|
| pstack: `poteto-mode`, một cửa trước chọn đúng playbook | `/nckh`: đọc trạng thái đề tài, chọn playbook, gọi đúng skill |
| pstack: bộ principles mọi skill phải theo | `nguyen-tac.md`: 11 nguyên tắc, đứng đầu là **không bịa nguồn** |
| pstack: playbooks (feature, bug-fix…) | 7 playbook: đề tài mới, tổng quan, định lượng, định tính, viết, trả lời reviewer, quay lại |
| super-board: trạng thái nằm trên board, không nằm trong phiên chat | Thư mục `nckh/`: đề tài, nhật ký quyết định, thẻ đọc, kết quả |
| super-board: lane Build → QA → Review | Viết → Kiểm trích dẫn → Phản biện |
| super-board: guard hooks chặn lỗi nguy hiểm | `nckh-kiem-trich-dan`: script đối chiếu Crossref chặn trích dẫn bịa/sai/bị rút |
| super-review: tự đặt giả thuyết điểm yếu rồi kiểm chứng, nhớ phát hiện cũ | `nckh-phan-bien`: 3 reviewer giả lập, kiểm chứng từng giả thuyết, nhớ lỗi chưa sửa |
| pstack: `show-me-your-work` (nhật ký quyết định) | `nckh/nhat-ky.md`: mọi quyết định phương pháp, để trả lời reviewer "tại sao" |

## Các skill

**Bạn gõ: cửa trước**

| Skill | Việc làm |
|---|---|
| `/nckh` | Trạng thái đề tài, khởi tạo dự án, chọn playbook. Không biết bắt đầu từ đâu thì gõ lệnh này. |

**Theo giai đoạn**

| Giai đoạn | Skill | Việc làm |
|---|---|---|
| Tổng quan | `/nckh-tim-tai-lieu` | Chuỗi tìm Boolean Anh–Việt, tìm trên OpenAlex bằng script, log PRISMA, xuất BibTeX cho Zotero |
| | `/nckh-doc-bai` | Thẻ đọc có số trang, đánh giá chất lượng, thêm dòng vào ma trận tổng quan |
| | `/nckh-tong-quan` | Tổng hợp theo chủ đề, đồng thuận/mâu thuẫn, khoảng trống nghiên cứu, viết theo phễu |
| Thiết kế | `/nckh-thiet-ke` | Câu hỏi (FINER), giả thuyết, thiết kế, cỡ mẫu bằng code, kế hoạch phân tích, đạo đức, đề cương |
| | `/nckh-cong-cu-do` | Thích ứng thang đo (ITC: dịch xuôi–ngược, CVI, phỏng vấn nhận thức), bảng hỏi, codebook, hướng dẫn phỏng vấn |
| Phân tích | `/nckh-phan-tich` | Chuỗi script R tái lập được: làm sạch → thang đo (α, ω, CFA) → giả thuyết → độ vững; bảng APA cho LaTeX |
| | `/nckh-dinh-tinh` | Phân tích chủ đề Braun & Clarke, codebook, trường hợp ngược, kiểm câu trích nguyên văn, COREQ |
| Viết & nộp | `/nckh-viet-bai` | IMRaD bằng LaTeX `apa7` + biblatex cho Prism, chỉ dùng số liệu từ file kết quả |
| | `/nckh-kiem-trich-dan` | Đối chiếu Crossref, `\cite` ↔ `.bib`, khẳng định ↔ thẻ đọc |
| | `/nckh-phan-bien` | Biên tập viên + 3 reviewer, checklist JARS/STROBE/COREQ, tính lại p bằng script để bắt số liệu không khớp |
| | `/nckh-tra-loi-reviewer` | Tách góp ý, kế hoạch sửa, latexdiff, thư trả lời |

## Cài vào một dự án

Bộ skill **chỉ được cài vào từng thư mục đề tài** (`<đề tài>/.claude/skills/`). Các dự án Claude Code khác của bạn không bị ảnh hưởng.

**Cách nhanh nhất.** Mở Terminal trong thư mục đề tài và chạy:

```bash
curl -fsSL https://raw.githubusercontent.com/dayaltanwing/nckh-skills/main/get.sh | bash
```

Hoặc nói với Claude trong phiên làm việc của đề tài đó: *"Cài bộ skill từ github.com/dayaltanwing/nckh-skills vào dự án này."*

**Cập nhật** lên bản mới nhất: chạy lại đúng lệnh trên.

**Gỡ** khỏi dự án:

```bash
curl -fsSL https://raw.githubusercontent.com/dayaltanwing/nckh-skills/main/get.sh | bash -s -- --go
```

**Từ bản clone của repo:**
- `./install.sh` cài vào thư mục hiện tại; `./install.sh "<đề tài>"` cài vào thư mục khác.
- `./install.sh --go` để gỡ.
- `./install.sh --link "<đề tài>"`: sửa skill ở bản clone là đề tài thấy ngay.
- `--global` cài cho mọi dự án. Chỉ dùng khi bạn thật sự muốn.
- Script từ chối cài khi bạn đang ở thư mục home, vì cài ở đó cũng là cài cho mọi dự án.

**Dạng plugin** (Claude Code chạy trong Terminal). Trong thư mục đề tài, chạy lần lượt hai lệnh sau:

```bash
claude plugin marketplace add dayaltanwing/nckh-skills --scope project
```

```bash
claude plugin install nckh@nckh-skills --scope project
```

Ở dạng plugin, tên skill có thêm tiền tố: `/nckh:nckh`, `/nckh:nckh-tim-tai-lieu`…

Cần có: Claude Code, Python 3.9+ (cho 3 script, không cần cài thêm gói nào). Cho phân tích: R (khuyến nghị) với các gói trong `skills/nckh-phan-tich/references/r-goi-y.md`, hoặc Python.

## Bắt đầu

Mở Claude Code trong thư mục đề tài:

```
/nckh khoi-tao                         # 5 câu hỏi, tạo thư mục nckh/
/nckh tôi muốn viết tổng quan về ...   # tự chọn playbook
/nckh                                  # tôi đang ở đâu, làm gì tiếp?
```

## Dự án trông như thế nào

```
de-tai-cua-ban/
└── nckh/
    ├── de-tai.md        nhat-ky.md       de-cuong.md
    ├── tai-lieu/        tai-lieu.bib, tim-kiem.md, ma-tran.csv, the-doc/
    ├── cong-cu/         bang-hoi.md, codebook.csv
    ├── du-lieu/         raw/ (chỉ đọc), clean/
    ├── phan-tich/       01-lam-sach.R …
    ├── ket-qua/         bảng, hình
    └── ban-thao/        main.tex, sections/, refs.bib → đưa lên Prism
```

## Làm việc với công cụ của bạn

- **Zotero**: Better BibTeX, auto-export collection ra `nckh/tai-lieu/tai-lieu.bib`. BibTeX do skill tìm được thì nhập ngược lại qua File → Import.
- **R/Python**: mọi phân tích là script trong `nckh/phan-tich/`, chạy lại được bằng một lệnh.
- **OpenAI Prism**: tải thư mục `nckh/ban-thao/` lên Prism để biên tập và biên dịch. Sửa xong thì tải về, chép đè lại để skill thấy bản mới.

## Giới hạn cần biết

- Claude không thay thế người dịch, hội đồng chuyên gia, hay người nghiên cứu khi diễn giải. Các bước ⛔ trong skill là chỗ bạn quyết định.
- Script tìm và kiểm dựa vào OpenAlex/Crossref. Sách, luận văn, tạp chí Việt Nam không có DOI cần kiểm tay.
- OpenAlex giới hạn số lượt tìm mỗi ngày. Dùng thường xuyên thì lấy khoá API miễn phí tại openalex.org/settings/api (hạn mức gấp 10) và đặt vào biến môi trường `OPENALEX_API_KEY`.
- Script tính lại p chỉ đọc thống kê viết trong câu theo kiểu APA (`t(48) = 2.31, p = .025`). Số trong bảng vẫn phải đối chiếu với file kết quả.
- Dữ liệu người tham gia: ẩn danh hoá trước khi cho Claude đọc (nguyên tắc 6).
- Kiểm tra quy định của tạp chí và trường về việc dùng AI, và khai báo theo yêu cầu.

## Sửa và cập nhật bộ skill

Repo này là bản gốc. Muốn sửa một skill:
1. Clone repo về máy.
2. Sửa file trong `skills/`.
3. Commit và push.

Hoặc nhờ Claude trong thư mục bản clone làm giúp. Các dự án đã cài sẽ nhận bản mới khi chạy lại lệnh cài.

Sửa script thì chạy bộ kiểm thử trước khi push. Nó không gọi mạng và không cần cài thêm gì:

```bash
python3 -m unittest discover -s tests
```

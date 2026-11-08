---
name: nckh-tim-tai-lieu
description: Tìm tài liệu khoa học cho một đề tài khoa học xã hội. Xây chuỗi tìm kiếm Boolean, tìm trên OpenAlex/Crossref bằng script có sẵn, ghi log tìm kiếm cho PRISMA, loại trùng, xuất BibTeX để nhập vào Zotero. Dùng khi người dùng muốn tìm bài báo, tìm tài liệu, literature search, "có nghiên cứu nào về…".
---

# Tìm tài liệu

Đọc `../nckh/references/nguyen-tac.md` trước. Nguyên tắc 1 (không bịa nguồn) là trung tâm của skill này: **mọi bài bạn đưa ra phải đến từ kết quả tìm kiếm thật**, không phải từ trí nhớ.

## 1. Tách khái niệm, xây chuỗi tìm

Dùng khung **PEO** (Population, Exposure, Outcome) hoặc **PICo** (Population, phenomenon of Interest, Context) cho khoa học xã hội.

Mỗi khái niệm có một cột từ đồng nghĩa, bằng tiếng Anh và tiếng Việt:

| Khái niệm | Tiếng Anh | Tiếng Việt |
|---|---|---|
| P | "high school students" OR adolescen* OR "secondary school" | học sinh THPT, học sinh trung học |
| E/I | "career decision*" OR "career choice" OR "career indecision" | chọn nghề, quyết định nghề nghiệp |
| O/Co | Vietnam* OR "Southeast Asia" | Việt Nam |

Chuỗi = các từ trong một cột nối bằng `OR`, các cột nối với nhau bằng `AND`. Đưa bảng này cho người dùng duyệt trước khi tìm.

## 2. Tìm

**OpenAlex** (miễn phí, phủ rộng, có tóm tắt). Dùng script đi kèm:

```bash
python3 scripts/tim_openalex.py "career decision AND adolescents AND Vietnam" --tu-nam 2015 --so-luong 50 --bib nckh/tai-lieu/ung-vien.bib
```

Script in bảng (tác giả, năm, tiêu đề, tạp chí, số trích dẫn, DOI, link truy cập mở) và tuỳ chọn xuất BibTeX lấy từ doi.org. Chạy `--help` để xem đủ tuỳ chọn (lọc theo loại bài, sắp xếp theo trích dẫn).

**Nguồn người dùng tự tìm** (cần đăng nhập hoặc chặn bot). Đưa họ chuỗi tìm đã chuyển sang cú pháp từng nơi:
- Scopus: `TITLE-ABS-KEY(...)`
- Web of Science: `TS=(...)`
- Google Scholar: chuỗi rút gọn, xem 100 kết quả đầu
- ERIC (giáo dục), APA PsycInfo (tâm lý) nếu trường có quyền truy cập
- Nguồn Việt Nam: vjol.info.vn, tạp chí của các trường ĐH Sư phạm, ĐHQG (nguyên tắc 7)

**Lần theo trích dẫn** (snowballing): với 3–5 bài trụ cột, xem danh sách tài liệu tham khảo của chúng (lùi) và các bài trích dẫn chúng (tiến, dùng `cited_by` của OpenAlex: `--trich-dan-boi <OpenAlex ID>`).

## 3. Ghi log (bắt buộc)

Mỗi lần tìm, thêm một dòng vào `nckh/tai-lieu/tim-kiem.md`:

```
| 2026-11-08 | OpenAlex | <chuỗi tìm> | lọc: 2015–2026, article | 47 kết quả |
```

Không có log thì không vẽ được sơ đồ PRISMA và không trả lời được reviewer khi họ hỏi "tìm thế nào".

## 4. Loại trùng và sàng lọc sơ bộ

- Loại trùng theo DOI, rồi theo tiêu đề đã chuẩn hoá (chữ thường, bỏ dấu câu).
- Đề xuất danh sách ưu tiên đọc: bài tổng quan/meta-analysis gần đây, bài trích dẫn nhiều, bài ở bối cảnh Việt Nam/châu Á, bài dùng thang đo người dùng định dùng.
- Với tổng quan hệ thống: tiêu chí đưa vào/loại ra phải được người dùng chốt **trước** khi sàng lọc. Ghi vào nhật ký.

## 5. Đưa vào Zotero

Gộp BibTeX đã duyệt vào `nckh/tai-lieu/tai-lieu.bib`. Hướng dẫn người dùng: Zotero → File → Import → chọn file `.bib`. Nếu họ dùng Better BibTeX, khoá trích dẫn sẽ được giữ nguyên.

Chiều ngược lại: người dùng export collection từ Zotero ra `.bib` (Better BibTeX, có auto-export) vào `nckh/tai-lieu/tai-lieu.bib` để các skill khác dùng.

## Đầu ra

- Bảng bài ứng viên đã xếp ưu tiên (tối đa 30 dòng trong chat; phần còn lại nằm trong file).
- File `.bib` ứng viên.
- Dòng log mới trong `tim-kiem.md`.
- Gợi ý bước tiếp: `nckh-doc-bai` với 5 bài đứng đầu.

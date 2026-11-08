# Cấu trúc thư mục `nckh/` của một dự án

`/nckh khoi-tao` tạo cấu trúc này trong thư mục đề tài. Mọi skill `nckh-*` đọc và ghi vào đây. Trạng thái nằm trong file, không nằm trong trí nhớ của cuộc trò chuyện.

```
nckh/
├── de-tai.md              # nguồn sự thật duy nhất: chủ đề, câu hỏi NC, giả thuyết, sản phẩm, hạn chót
├── nhat-ky.md             # nhật ký quyết định (bảng)
├── de-cuong.md            # đề cương / kế hoạch nghiên cứu (nckh-thiet-ke)
├── tai-lieu/
│   ├── tai-lieu.bib       # BibTeX, đồng bộ với Zotero (import/export)
│   ├── tim-kiem.md        # log mỗi lần tìm: ngày, nguồn, chuỗi tìm, số kết quả (cho PRISMA)
│   ├── ma-tran.csv        # ma trận tổng quan, mỗi bài một dòng
│   └── the-doc/<key>.md   # thẻ đọc cho từng bài, tên file = khoá BibTeX
├── cong-cu/               # bảng hỏi, hướng dẫn phỏng vấn, codebook biến
├── du-lieu/
│   ├── raw/               # dữ liệu gốc, CHỈ ĐỌC
│   └── clean/             # dữ liệu đã làm sạch, sinh từ script
├── phan-tich/             # script R/Python, đánh số theo thứ tự chạy: 01-lam-sach.R, 02-mo-ta.R…
├── ket-qua/               # bảng, hình, output do script sinh ra
└── ban-thao/              # file .tex cho Prism, refs.bib, thư trả lời reviewer
```

## Mẫu `de-tai.md`

```markdown
# <Tên đề tài>

- Sản phẩm: <bài báo cho tạp chí X | luận văn ThS | …>
- Hạn chót: <yyyy-mm-dd>
- Ngôn ngữ sản phẩm: <Việt | Anh>
- Hướng tiếp cận: <định lượng | định tính | hỗn hợp>
- Giai đoạn hiện tại: <tổng quan | thiết kế | thu dữ liệu | phân tích | viết | phản hồi reviewer>

## Câu hỏi nghiên cứu
1. …

## Giả thuyết (nếu có)
- H1: …

## Khung lý thuyết
…
```

## Mẫu `nhat-ky.md`

```markdown
| Ngày | Quyết định | Lý do | Phương án đã bỏ | Skill |
|---|---|---|---|---|
| 2026-11-08 | Khởi tạo đề tài | — | — | nckh |
```

## Mẫu cột `ma-tran.csv`

`key,tac_gia,nam,quoc_gia,boi_canh,ly_thuyet,thiet_ke,mau_n,cong_cu_do,ket_qua_chinh,han_che,lien_quan_den_rq,ghi_chu`

`.gitignore` gợi ý: `nckh/du-lieu/` (không đẩy dữ liệu người tham gia lên GitHub).

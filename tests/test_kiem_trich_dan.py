"""Kiểm thử kiem_trich_dan.py. Không gọi mạng: câu trả lời của Crossref được giả lập.

Chạy từ thư mục gốc của repo:  python3 -m unittest discover -s tests
"""
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from contextlib import redirect_stdout
from unittest import mock

import _nap

TIEU_DE = "Career adaptability of Vietnamese high school students"


def ban_ghi(family="Nguyễn", given="Văn An", title=TIEU_DE, year=2020, **them):
    """Một bản ghi Crossref tối thiểu (phần `message`)."""
    msg = {
        "title": [title] if title else [],
        "issued": {"date-parts": [[year]]},
        "author": [{"family": family, "given": given}],
    }
    msg.update(them)
    return msg


def muc_bib(author="Nguyễn, Văn An", title=TIEU_DE, year="2020", doi="10.1234/abc", **them):
    m = {"khoa": "x2020", "loai": "article", "title": title, "author": author, "year": year, "doi": doi}
    m.update(them)
    return {k: v for k, v in m.items() if v is not None}


class CoSo(unittest.TestCase):
    def setUp(self):
        self.k = _nap.nap("kiem_trich_dan")

    def kiem(self, muc, crossref):
        """Chạy kiem_muc với Crossref trả về `crossref` (None = DOI không tồn tại)."""
        self.k.lay_json = lambda url: None if crossref is None else {"message": crossref}
        return self.k.kiem_muc(muc)

    def assertTrangThai(self, kq, mong_doi):
        self.assertEqual(kq["trang_thai"], mong_doi, kq["ghi_chu"])


class TacGiaDau(CoSo):
    """Mục 1: tên tác giả Việt Nam không được bị báo oan là LỆCH."""

    def test_ten_tay(self):
        kq = self.kiem(muc_bib(author="Braun, Virginia and Clarke, Victoria"), ban_ghi("Braun", "Virginia"))
        self.assertTrangThai(kq, "OK")

    def test_ten_tay_khong_dau_phay(self):
        kq = self.kiem(muc_bib(author="Virginia Braun and Victoria Clarke"), ban_ghi("Braun", "Virginia"))
        self.assertTrangThai(kq, "OK")

    def test_ten_viet_theo_thu_tu_viet(self):
        kq = self.kiem(muc_bib(author="Nguyễn Văn An"), ban_ghi("Nguyễn", "Văn An"))
        self.assertTrangThai(kq, "OK")

    def test_ten_viet_trong_ngoac_nhon(self):
        kq = self.kiem(muc_bib(author="{Nguyễn Văn An} and {Trần Thị Bình}"), ban_ghi("Nguyễn", "Văn An"))
        self.assertTrangThai(kq, "OK")

    def test_tap_chi_dao_ho_ten(self):
        # Tạp chí đăng ký "An" là họ; .bib ghi đúng họ là Nguyễn.
        kq = self.kiem(muc_bib(author="Nguyen, Van An"), ban_ghi("An", "Nguyen Van"))
        self.assertTrangThai(kq, "OK")

    def test_bib_dao_ho_ten(self):
        # .bib (lấy từ doi.org) ghi "An" là họ; Crossref bản khác ghi họ Nguyễn.
        kq = self.kiem(muc_bib(author="An, Nguyễn Văn"), ban_ghi("Nguyễn", "Văn An"))
        self.assertTrangThai(kq, "OK")

    def test_ten_viet_tat(self):
        kq = self.kiem(muc_bib(author="Nguyen, V. A."), ban_ghi("An", "Nguyễn Văn"))
        self.assertTrangThai(kq, "OK")

    def test_crossref_ghi_ca_ten_vao_o_ho(self):
        kq = self.kiem(muc_bib(author="Nguyễn Văn An"), {**ban_ghi(), "author": [{"family": "Nguyen Van An"}]})
        self.assertTrangThai(kq, "OK")

    def test_khong_dau_va_co_dau_la_mot(self):
        kq = self.kiem(muc_bib(author="Do, Thi Hoa"), ban_ghi("Đỗ", "Thị Hoa"))
        self.assertTrangThai(kq, "OK")

    def test_dau_viet_bang_lenh_latex(self):
        for ten in (r"Nguy{\~{\^e}}n, Văn An", r"Nguy\~{\^e}n, V. A.", r"{Nguy{\~{\^{e}}}n V{\u{a}}n An}"):
            with self.subTest(ten=ten):
                self.assertTrangThai(self.kiem(muc_bib(author=ten), ban_ghi("Nguyễn", "Văn An")), "OK")

    def test_chu_dac_biet_bang_lenh_latex(self):
        cap = [(r"{\DJ}{\~{\^o}}, Thị Hoa", "Đỗ"), (r"M{\"u}ller, Hans", "Müller"), (r"S{\o}rensen, Lars", "Sørensen"),
               (r"Wei{\ss}, Anna", "Weiß"), (r"Garc{\'\i}a, Juan", "García"), (r"{\L}ukasz, Jan", "Łukasz")]
        for ten, ho in cap:
            with self.subTest(ten=ten):
                self.assertTrangThai(self.kiem(muc_bib(author=ten), ban_ghi(ho, "X")), "OK")

    def test_to_chuc(self):
        cr = {**ban_ghi(), "author": [{"name": "World Health Organization"}]}
        self.assertTrangThai(self.kiem(muc_bib(author="{World Health Organization}"), cr), "OK")

    def test_and_trong_ngoac_khong_tach_tac_gia(self):
        cr = {**ban_ghi(), "author": [{"name": "Barnes and Noble"}]}
        self.assertTrangThai(self.kiem(muc_bib(author="{Barnes and Noble} and Smith, John"), cr), "OK")

    def test_ho_kep(self):
        self.assertTrangThai(self.kiem(muc_bib(author="García, Juan"), ban_ghi("García-López", "Juan")), "OK")
        self.assertTrangThai(self.kiem(muc_bib(author="Ludwig van Beethoven"), ban_ghi("van Beethoven", "Ludwig")), "OK")

    def test_tac_gia_khac_han_van_bi_bao(self):
        kq = self.kiem(muc_bib(author="Smith, John"), ban_ghi("Jones", "Mary"))
        self.assertTrangThai(kq, "LỆCH")
        self.assertIn("tác giả đầu", kq["ghi_chu"])

    def test_tac_gia_viet_khac_han_van_bi_bao(self):
        kq = self.kiem(muc_bib(author="Trần Thị Bình"), ban_ghi("Lê", "Văn Cường"))
        self.assertTrangThai(kq, "LỆCH")

    def test_chi_tac_gia_thu_hai_khop_thi_van_bao(self):
        kq = self.kiem(muc_bib(author="Clarke, Victoria and Braun, Virginia"), ban_ghi("Braun", "Virginia"))
        self.assertTrangThai(kq, "LỆCH")

    def test_lay_tac_gia_co_sequence_first(self):
        cr = {**ban_ghi(), "author": [{"family": "Clarke", "given": "V", "sequence": "additional"},
                                      {"family": "Braun", "given": "V", "sequence": "first"}]}
        self.assertTrangThai(self.kiem(muc_bib(author="Braun, Virginia"), cr), "OK")

    def test_khong_co_tac_gia_thi_bo_qua(self):
        self.assertTrangThai(self.kiem(muc_bib(author=None), ban_ghi()), "OK")
        self.assertTrangThai(self.kiem(muc_bib(), {**ban_ghi(), "author": []}), "OK")


class Nam(CoSo):
    """Mục 2: năm không phải số không được làm script hỏng."""

    def test_nam_khong_phai_so(self):
        for nam in ("n.d.", "in press", "đang in", ""):
            with self.subTest(nam=nam):
                kq = self.kiem(muc_bib(year=nam), ban_ghi(year=2021))
                self.assertTrangThai(kq, "OK")

    def test_nam_khong_phai_so_co_ghi_chu_nam_crossref(self):
        kq = self.kiem(muc_bib(year="in press"), ban_ghi(year=2021))
        self.assertIn("2021", kq["ghi_chu"])

    def test_nam_co_hau_to(self):
        self.assertTrangThai(self.kiem(muc_bib(year="2020a"), ban_ghi(year=2020)), "OK")

    def test_truong_date_cua_biblatex(self):
        self.assertTrangThai(self.kiem(muc_bib(year=None, date="2020-05-03"), ban_ghi(year=2020)), "OK")

    def test_lech_mot_nam_la_binh_thuong(self):
        # Bản online và bản in thường lệch nhau một năm.
        self.assertTrangThai(self.kiem(muc_bib(year="2020"), ban_ghi(year=2021)), "OK")

    def test_crossref_ghi_nam_dang_chuoi(self):
        cr = {**ban_ghi(), "issued": {"date-parts": [["2020"]]}}
        self.assertTrangThai(self.kiem(muc_bib(year="2020"), cr), "OK")
        cr = {**ban_ghi(), "issued": {"date-parts": [[None]]}, "created": {"date-parts": [[2020, 5, 1]]}}
        self.assertTrangThai(self.kiem(muc_bib(year="2014"), cr), "LỆCH")

    def test_lech_nhieu_nam_thi_bao(self):
        kq = self.kiem(muc_bib(year="2015"), ban_ghi(year=2020))
        self.assertTrangThai(kq, "LỆCH")
        self.assertIn("2015", kq["ghi_chu"])
        self.assertIn("2020", kq["ghi_chu"])


class TieuDe(CoSo):
    def test_khac_tieu_de_thi_bao(self):
        kq = self.kiem(muc_bib(), ban_ghi(title="Thermal conductivity of doped silicon nanowires"))
        self.assertTrangThai(kq, "LỆCH")
        self.assertIn("tiêu đề", kq["ghi_chu"])

    def test_khac_hoa_thuong_dau_cau(self):
        self.assertTrangThai(self.kiem(muc_bib(title="{Career} adaptability of {Vietnamese} high-school students."), ban_ghi()), "OK")

    def test_crossref_tach_phu_de(self):
        chinh, phu = "Thematic analysis", "A practical guide to understanding and doing qualitative research well"
        cr = {**ban_ghi(title=chinh), "subtitle": [phu]}
        kq = self.kiem(muc_bib(title=f"{chinh}: {phu}"), cr)
        self.assertTrangThai(kq, "OK")
        self.assertEqual(kq["ghi_chu"], "")   # khớp đầy đủ, không cần lưu ý

    def test_mot_ben_thieu_phu_de(self):
        chinh = "Using thematic analysis in psychology"
        dai = chinh + ": A step-by-step guide for beginners in the social and health sciences"
        for bib, cr in ((dai, chinh), (chinh, dai)):
            kq = self.kiem(muc_bib(title=bib), ban_ghi(title=cr))
            self.assertTrangThai(kq, "OK")
            self.assertIn("phụ đề", kq["ghi_chu"])   # vẫn nói cho người dùng biết hai tiêu đề không y hệt

    def test_trung_vai_tu_dau_khong_du_de_coi_la_khop(self):
        cr = ban_ghi(title="Career adaptability and life satisfaction among older workers in three countries")
        self.assertTrangThai(self.kiem(muc_bib(title="Career adaptability"), cr), "LỆCH")

    def test_the_html_trong_tieu_de_crossref(self):
        cr = ban_ghi(title="Career adaptability of <i>Vietnamese</i> high school students &amp; teachers")
        self.assertTrangThai(self.kiem(muc_bib(title="Career adaptability of Vietnamese high school students & teachers"), cr), "OK")

    def test_crossref_khong_co_tieu_de(self):
        kq = self.kiem(muc_bib(), ban_ghi(title=None))
        self.assertTrangThai(kq, "OK")
        self.assertIn("tiêu đề", kq["ghi_chu"])


class TrangThai(CoSo):
    def test_doi_khong_ton_tai(self):
        self.assertTrangThai(self.kiem(muc_bib(), None), "KHÔNG THẤY")

    def test_doi_co_tien_to_url(self):
        url = []
        self.k.lay_json = lambda u: url.append(u) or {"message": ban_ghi()}
        self.k.kiem_muc(muc_bib(doi="https://doi.org/10.1234/ABC"))
        self.assertTrue(url[0].endswith("/works/10.1234/ABC"), url[0])

    def test_bi_rut(self):
        cr = {**ban_ghi(), "updated-by": [{"type": "retraction"}]}
        self.assertTrangThai(self.kiem(muc_bib(), cr), "BỊ RÚT")

    def test_dinh_chinh(self):
        cr = {**ban_ghi(), "updated-by": [{"type": "correction"}]}
        self.assertTrangThai(self.kiem(muc_bib(), cr), "ĐÍNH CHÍNH")

    def test_khong_doi_co_ban_khop(self):
        self.k.lay_json = lambda u: {"message": {"items": [{"title": [TIEU_DE], "DOI": "10.9999/tim-duoc"}]}}
        kq = self.k.kiem_muc(muc_bib(doi=None))
        self.assertTrangThai(kq, "KHÔNG DOI")
        self.assertIn("10.9999/tim-duoc", kq["ghi_chu"])

    def test_khong_doi_khong_co_ban_khop(self):
        self.k.lay_json = lambda u: {"message": {"items": [{"title": ["Something else entirely"], "DOI": "10.9/x"}]}}
        kq = self.k.kiem_muc(muc_bib(doi=None))
        self.assertTrangThai(kq, "KHÔNG DOI")
        self.assertNotIn("10.9/x", kq["ghi_chu"])

    def test_khong_doi_nam_khong_phai_so(self):
        url = []
        self.k.lay_json = lambda u: url.append(u) or {"message": {"items": []}}
        self.assertTrangThai(self.k.kiem_muc(muc_bib(doi=None, year="n.d.")), "KHÔNG DOI")

    def test_thieu_thong_tin(self):
        self.assertTrangThai(self.k.kiem_muc(muc_bib(doi=None, title=None)), "THIẾU THÔNG TIN")


class DocBib(CoSo):
    def test_cac_kieu_gia_tri(self):
        muc = self.k.doc_bib('''
            @comment{bo qua}
            @string{jpsp = "Journal"}
            @Article{braun2006,
              title = {Using {thematic} analysis},
              author = "Braun, Virginia and Clarke, Victoria",
              year = 2006,
              DOI = {10.1191/1478088706qp063oa},
            }
            @book{le2019, title={Sách}, author={Lê Văn C}, year={2019}}
        ''')
        self.assertEqual([m["khoa"] for m in muc], ["braun2006", "le2019"])
        self.assertEqual(muc[0]["loai"], "article")
        self.assertEqual(muc[0]["title"], "Using {thematic} analysis")
        self.assertEqual(muc[0]["author"], "Braun, Virginia and Clarke, Victoria")
        self.assertEqual(muc[0]["year"], "2006")
        self.assertEqual(muc[0]["doi"], "10.1191/1478088706qp063oa")


class DongLenh(unittest.TestCase):
    """Chạy script như người dùng chạy, ở chế độ không gọi mạng (--chi-tex)."""

    def setUp(self):
        self._tam = tempfile.TemporaryDirectory()
        self.d = self._tam.name
        self.addCleanup(self._tam.cleanup)
        self.bib = _nap.ghi(self.d, "tai-lieu.bib", "\n".join(
            "@article{%s, title={T %s}, author={A, B}, year={2020}}" % (k, k) for k in ("a2020", "b2020", "c2020")))

    def chay(self, tex, *them):
        kq_json = os.path.join(self.d, "kq.json")
        ma, out, err = _nap.chay("kiem_trich_dan", self.bib, "--chi-tex", "--tex", tex, "--json", kq_json, *them)
        self.assertEqual(err, "")
        with open(kq_json, encoding="utf-8") as f:
            return ma, out, json.load(f)

    def test_du_khoa(self):
        tex = _nap.ghi(self.d, "bt/main.tex", r"\textcite{a2020} và \parencite[xem][tr.~5]{b2020, c2020}.")
        ma, out, kq = self.chay(tex)
        self.assertEqual((ma, kq["thieu_trong_bib"], kq["khong_duoc_trich"]), (0, {}, []))

    def test_thieu_va_thua(self):
        tex = _nap.ghi(self.d, "bt/main.tex", "Dòng 1\n\\parencite{a2020}\n\\cite{khong-co}\n")
        ma, out, kq = self.chay(tex)
        self.assertEqual(ma, 1)
        self.assertEqual(kq["thieu_trong_bib"], {"khong-co": ["main.tex:3"]})
        self.assertEqual(kq["khong_duoc_trich"], ["b2020", "c2020"])

    def test_chu_thich_latex_khong_tinh(self):
        tex = _nap.ghi(self.d, "bt/main.tex", "% \\cite{cu1}\n\\cite{a2020} 50\\% mẫu \\cite{b2020} % \\cite{cu2}\n  %\\cite{cu3}\n")
        ma, out, kq = self.chay(tex)
        self.assertEqual(kq["thieu_trong_bib"], {})
        self.assertEqual(kq["khong_duoc_trich"], ["c2020"])

    def test_nocite_sao(self):
        tex = _nap.ghi(self.d, "bt/main.tex", "\\nocite{*}\n\\cite{a2020}\n")
        ma, out, kq = self.chay(tex)
        self.assertEqual((ma, kq["thieu_trong_bib"], kq["khong_duoc_trich"]), (0, {}, []))

    def test_cac_lenh_cite_cua_biblatex(self):
        tex = _nap.ghi(self.d, "bt/main.tex",
                       "\\Cite{a2020} \\Citeauthor{b2020} \\Textcite{c2020} \\citeyear*{d1} \\autocite{d2} \\footcite{d3}\n"
                       "\\parencites[xem][5]{d4}[10]{d5}{d6} \\fullcite{d7}\n")
        ma, out, kq = self.chay(tex)
        self.assertEqual(sorted(kq["thieu_trong_bib"]), ["d1", "d2", "d3", "d4", "d5", "d6", "d7"])
        self.assertEqual(kq["khong_duoc_trich"], [])

    def test_lenh_cau_hinh_khong_phai_trich_dan(self):
        tex = _nap.ghi(self.d, "bt/main.tex",
                       "\\setcitestyle{authoryear,round}\n\\citestyle{apa}\n\\DeclareCiteCommand{\\mycite}\n"
                       "\\defcitealias{a2020}{Bài I}\n\\citetalias{a2020} \\citep{b2020} \\citet*{c2020}\n")
        ma, out, kq = self.chay(tex)
        self.assertEqual((ma, kq["thieu_trong_bib"], kq["khong_duoc_trich"]), (0, {}, []))

    def test_xuong_dong_roi_chu_thich(self):
        # "\\\\%" là lệnh xuống dòng (\\\\) rồi tới chú thích, không phải dấu phần trăm thật.
        tex = _nap.ghi(self.d, "bt/main.tex", "a \\\\% \\cite{cu}\n\\cite{a2020}\\cite{b2020}\\cite{c2020}\n")
        ma, out, kq = self.chay(tex)
        self.assertEqual(kq["thieu_trong_bib"], {})

    def test_danh_sach_khoa_ngat_dong(self):
        tex = _nap.ghi(self.d, "bt/main.tex", "Dòng 1\nXem \\parencite[xem][tr.~5]{a2020,\n  b2020,%\n  thieu}\n\\textcite\n{c2020}\n")
        ma, out, kq = self.chay(tex)
        self.assertEqual(kq["thieu_trong_bib"], {"thieu": ["main.tex:2"]})
        self.assertEqual(kq["khong_duoc_trich"], [])

    def test_file_chinh_di_theo_input(self):
        tex = _nap.ghi(self.d, "bt/main.tex", "\\input{sections/01-intro}\n\\include{sections/02-method.tex}\n% \\input{sections/bo}\n")
        _nap.ghi(self.d, "bt/sections/01-intro.tex", "Mở đầu\n\\parencite{a2020}\n\\input{sections/con}\n")
        _nap.ghi(self.d, "bt/sections/02-method.tex", "\\textcite{thieu1}\n")
        _nap.ghi(self.d, "bt/sections/con.tex", "\\cite{b2020}\n")
        _nap.ghi(self.d, "bt/sections/bo.tex", "\\cite{khong-doc}\n")
        _nap.ghi(self.d, "bt/khong-lien-quan.tex", "\\cite{khong-doc-2}\n")
        ma, out, kq = self.chay(tex)
        self.assertEqual(kq["thieu_trong_bib"], {"thieu1": ["sections/02-method.tex:1"]})
        self.assertEqual(kq["khong_duoc_trich"], ["c2020"])

    def test_input_vong_lap_khong_treo(self):
        tex = _nap.ghi(self.d, "bt/main.tex", "\\input{a}\n\\cite{a2020}\n")
        _nap.ghi(self.d, "bt/a.tex", "\\input{main}\n\\cite{b2020}\n")
        ma, out, kq = self.chay(tex)
        self.assertEqual(kq["khong_duoc_trich"], ["c2020"])

    def test_input_khong_tim_thay_thi_canh_bao(self):
        tex = _nap.ghi(self.d, "bt/main.tex", "\\input{sections/mat}\n\\cite{a2020}\\cite{b2020}\\cite{c2020}\n")
        ma, out, kq = self.chay(tex)
        self.assertEqual(ma, 0)
        self.assertIn("sections/mat", out)
        self.assertTrue(kq["canh_bao"])

    def test_thu_muc_bo_qua_ban_vong_truoc_va_latexdiff(self):
        _nap.ghi(self.d, "bt/main.tex", "\\input{sections/01}\n\\cite{a2020}\n")
        _nap.ghi(self.d, "bt/sections/01.tex", "\\cite{b2020}\n")
        _nap.ghi(self.d, "bt/vong-1/main.tex", "\\cite{da-bo-o-vong-1}\n")
        _nap.ghi(self.d, "bt/main-diff.tex", "\\cite{chi-co-trong-diff}\n")
        ma, out, kq = self.chay(os.path.join(self.d, "bt"))
        self.assertEqual(kq["thieu_trong_bib"], {})
        self.assertEqual(kq["khong_duoc_trich"], ["c2020"])
        self.assertIn("vong-1", out)  # nói rõ đã bỏ qua gì

    def test_khoa_trung_trong_bib(self):
        bib = _nap.ghi(self.d, "trung.bib", "@article{a2020, title={Một}}\n@book{b2020, title={Hai}}\n@article{a2020, title={Ba}}\n")
        kq_json = os.path.join(self.d, "kq.json")
        ma, out, err = _nap.chay("kiem_trich_dan", bib, "--chi-tex", "--json", kq_json)
        with open(kq_json, encoding="utf-8") as f:
            kq = json.load(f)
        self.assertEqual(ma, 1)
        self.assertEqual(kq["khoa_trung"], ["a2020"])
        self.assertIn("a2020", out)

    def test_bib_co_bom_va_khong_phai_utf8(self):
        bib = os.path.join(self.d, "la.bib")
        with open(bib, "wb") as f:
            f.write(b"\xef\xbb\xbf@article{a2020, title={Caf\xe9}, author={M\xfcller, H}}\n")
        ma, out, err = _nap.chay("kiem_trich_dan", bib, "--chi-tex")
        self.assertEqual((ma, err), (0, ""))
        self.assertIn("1 mục", out)

    def test_in_duoc_tieng_viet_khi_bang_ma_khong_phai_utf8(self):
        # Giả lập Windows: đầu ra bị chuyển hướng với bảng mã không chứa chữ Việt.
        bib = _nap.ghi(self.d, "trung.bib", "@article{a2020, title={Một}}\n@article{a2020, title={Hai}}\n")
        ma, out, err = _nap.chay("kiem_trich_dan", bib, "--chi-tex", env={"PYTHONIOENCODING": "ascii"})
        self.assertEqual((ma, err), (1, ""))
        self.assertIn("Khoá trùng", out)

    def test_khong_doc_duoc_bib(self):
        ma, out, err = _nap.chay("kiem_trich_dan", os.path.join(self.d, "khong-co.bib"))
        self.assertEqual(ma, 2)

    def test_khong_doc_duoc_tex(self):
        ma, out, err = _nap.chay("kiem_trich_dan", self.bib, "--chi-tex", "--tex", os.path.join(self.d, "khong-co"))
        self.assertEqual(ma, 2)
        self.assertIn("khong-co", err)


class NhanLoi(unittest.TestCase):
    """Lỗi phải được gọi đúng tên: lỗi trong script không phải là lỗi mạng."""

    def chay_main(self, loi):
        k = _nap.nap("kiem_trich_dan")
        with tempfile.TemporaryDirectory() as d:
            bib = _nap.ghi(d, "t.bib", "@article{a, title={T}, doi={10.1/x}}\n")

            def hong(m):
                raise loi
            k.kiem_muc = hong
            k.time.sleep = lambda s: None
            out = io.StringIO()
            with mock.patch.object(sys, "argv", ["kiem_trich_dan.py", bib]), redirect_stdout(out):
                with self.assertRaises(SystemExit) as thoat:
                    k.main()
        return thoat.exception.code, out.getvalue()

    def test_loi_mang(self):
        ma, out = self.chay_main(urllib.error.URLError("Tunnel connection failed: 403 Forbidden"))
        self.assertEqual(ma, 1)
        self.assertIn("LỖI MẠNG", out)

    def test_het_thoi_gian_cho_cung_la_loi_mang(self):
        import socket
        ma, out = self.chay_main(socket.timeout("timed out"))
        self.assertIn("LỖI MẠNG", out)

    def test_mat_mang_thi_dung_som(self):
        k = _nap.nap("kiem_trich_dan")
        goi = []

        def hong(m):
            goi.append(m["khoa"])
            raise urllib.error.URLError("no route")
        k.kiem_muc = hong
        k.time.sleep = lambda s: None
        muc = [{"khoa": f"k{i}", "loai": "article", "doi": "10.1/x"} for i in range(10)]
        out = io.StringIO()
        with redirect_stdout(out):
            kq = k.kiem_tat_ca(muc)
        self.assertEqual(goi, ["k0", "k1", "k2"])                      # không gọi tiếp sau 3 lỗi liên tiếp
        self.assertEqual([x["trang_thai"] for x in kq], ["LỖI MẠNG"] * 3 + ["CHƯA KIỂM"] * 7)
        self.assertIn("7 mục CHƯA KIỂM", out.getvalue())

    def test_loi_mang_le_te_khong_lam_dung(self):
        k = _nap.nap("kiem_trich_dan")

        def luc_duoc_luc_khong(m):
            if int(m["khoa"][1:]) % 2:
                raise urllib.error.URLError("chập chờn")
            return {"khoa": m["khoa"], "loai": "article", "doi": "", "trang_thai": "OK", "ghi_chu": ""}
        k.kiem_muc = luc_duoc_luc_khong
        k.time.sleep = lambda s: None
        with redirect_stdout(io.StringIO()):
            kq = k.kiem_tat_ca([{"khoa": f"k{i}", "loai": "article"} for i in range(10)])
        self.assertEqual([x["trang_thai"] for x in kq], ["OK", "LỖI MẠNG"] * 5)

    def test_loi_trong_script_khong_goi_la_loi_mang(self):
        ma, out = self.chay_main(ValueError("invalid literal for int()"))
        self.assertEqual(ma, 1)
        self.assertNotIn("LỖI MẠNG", out)
        self.assertIn("LỖI SCRIPT", out)
        self.assertIn("ValueError", out)


if __name__ == "__main__":
    unittest.main()

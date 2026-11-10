"""Kiểm thử tim_openalex.py. Không gọi mạng: câu trả lời của OpenAlex và doi.org được giả lập.

Chạy từ thư mục gốc của repo:  python3 -m unittest discover -s tests
"""
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
import urllib.parse
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

import _nap


def bai(i, doi="", ten="Savickas", tieu_de=None, **them):
    """Một bài như OpenAlex trả về."""
    w = {
        "id": f"https://openalex.org/W{i}",
        "display_name": tieu_de or f"Bài số {i}",
        "publication_year": 2012,
        "type": "article",
        "doi": f"https://doi.org/{doi}" if doi else None,
        "cited_by_count": 10 * i,
        "authorships": [{"author": {"display_name": ten}}],
        "primary_location": {"source": {"display_name": "Journal of Vocational Behavior"}},
        "open_access": {"oa_url": "https://example.org/pdf" if i % 2 else None},
    }
    w.update(them)
    return w


def bibtex_gia(doi):
    return " @article{Savickas_2012, title={Bài %s}, DOI={%s}, author={Savickas, Mark L.}, year={2012} }" % (doi, doi)


class CoSo(unittest.TestCase):
    def setUp(self):
        self.o = _nap.nap("tim_openalex")
        self.o.time.sleep = lambda s: None
        self.url = []
        self._tam = tempfile.TemporaryDirectory()
        self.d = self._tam.name
        self.addCleanup(self._tam.cleanup)

    def tra_ve(self, ket_qua, tong=None):
        def lay(url):
            self.url.append(url)
            return {"meta": {"count": len(ket_qua) if tong is None else tong}, "results": ket_qua}
        self.o.lay_json = lay

    def chay(self, *doi_so, env=None):
        """Chạy như dòng lệnh. Trả về (mã thoát, stdout, stderr)."""
        out, err = io.StringIO(), io.StringIO()
        ma = 0
        moi_truong = {k: v for k, v in os.environ.items() if k != "OPENALEX_API_KEY"}
        moi_truong.update(env or {})
        with mock.patch.object(sys, "argv", ["tim_openalex.py", *doi_so]), mock.patch.dict(os.environ, moi_truong, clear=True):
            with redirect_stdout(out), redirect_stderr(err):
                try:
                    self.o.chay()
                except SystemExit as e:
                    ma = e.code
        return ma, out.getvalue(), err.getvalue()


class TimKiem(CoSo):
    def test_bang_ket_qua(self):
        self.tra_ve([bai(1, "10.1/a"), bai(2)], tong=137)
        ma, out, err = self.chay("career AND Vietnam", "--tu-nam", "2015")
        self.assertEqual((ma, err), (0, ""))
        self.assertIn("# OpenAlex: 137 kết quả khớp, hiển thị 2", out)
        self.assertIn("| 1 | Savickas | 2012 | Bài số 1 | Journal of Vocational Behavior | 10 | 10.1/a | có |", out)
        self.assertIn("| 2 | Savickas | 2012 | Bài số 2 | Journal of Vocational Behavior | 20 |  |  |", out)

    def test_tham_so_gui_di(self):
        self.tra_ve([])
        self.chay("career", "--tu-nam", "2015", "--den-nam", "2020", "--loai", "review", "--sap-xep", "trich-dan", "--so-luong", "40")
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.url[0]).query)
        self.assertEqual(q["search"], ["career"])
        self.assertEqual(q["per-page"], ["40"])
        self.assertEqual(q["sort"], ["cited_by_count:desc"])
        self.assertEqual(q["filter"], ["from_publication_date:2015-01-01,to_publication_date:2020-12-31,type:review"])

    def test_trich_dan_boi(self):
        self.tra_ve([])
        self.chay("--trich-dan-boi", "W2741809807")
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.url[0]).query)
        self.assertEqual(q["filter"], ["cites:W2741809807"])
        self.assertNotIn("search", q)

    def test_can_chuoi_tim(self):
        ma, out, err = self.chay()
        self.assertEqual(ma, 2)

    def test_qua_200_thi_noi_ro(self):
        self.tra_ve([bai(i) for i in range(1, 4)], tong=900)
        ma, out, err = self.chay("career", "--so-luong", "300")
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.url[0]).query)
        self.assertEqual(q["per-page"], ["200"])
        self.assertIn("chỉ lấy được 200 bài", out)
        ma, out, err = self.chay("career", "--so-luong", "200")
        self.assertNotIn("chỉ lấy được", out)

    def test_so_luong_khong_hop_le(self):
        self.assertEqual(self.chay("career", "--so-luong", "0")[0], 2)

    def test_khoa_api_duoc_gui_nhung_khong_bi_in_ra(self):
        self.tra_ve([bai(1)])
        ma, out, err = self.chay("career", env={"OPENALEX_API_KEY": "bi-mat-123"})
        self.assertIn("api_key=bi-mat-123", self.url[0])
        self.assertNotIn("bi-mat-123", out + err)
        self.assertIn("# Truy vấn: https://api.openalex.org/works?", out)

    def test_khong_co_khoa_thi_khong_gui(self):
        self.tra_ve([bai(1)])
        self.chay("career")
        self.assertNotIn("api_key", self.url[0])

    def test_du_lieu_thieu_khong_lam_hong(self):
        self.tra_ve([{"id": None, "display_name": None, "authorships": [{"author": {"display_name": None}}, {"author": None}, {}],
                      "primary_location": None, "open_access": None, "doi": None, "cited_by_count": None},
                     {"authorships": None}])
        ma, out, err = self.chay("career")
        self.assertEqual((ma, err), (0, ""))
        self.assertIn("| 1 |  | ", out)

    def test_tieu_de_co_gach_dung_va_xuong_dong(self):
        self.tra_ve([bai(1, tieu_de="Phần A | phần B\n  dòng hai")])
        ma, out, err = self.chay("career")
        dong = [d for d in out.splitlines() if d.startswith("| 1 |")]
        self.assertEqual(len(dong), 1)
        self.assertIn("Phần A \\| phần B dòng hai", dong[0])
        self.assertEqual(dong[0].replace("\\|", "").count("|"), 9)      # đúng 8 cột

    def test_tom_tat(self):
        self.assertEqual(self.o.tom_tat({"Career": [0], "is": [2], "adaptability": [1], "key.": [3]}), "Career adaptability is key.")
        self.assertEqual(self.o.tom_tat(None), "")
        self.tra_ve([bai(1, abstract_inverted_index={"Tóm": [0], "tắt": [1], "a|b": [2]})])
        ma, out, err = self.chay("career", "--tom-tat")
        self.assertIn("_Tóm tắt a\\|b…_", out)

    def test_ghi_json(self):
        self.tra_ve([bai(1, "10.1/a")])
        f = os.path.join(self.d, "kq.json")
        self.chay("career", "--json", f)
        with open(f, encoding="utf-8") as fh:
            kq = json.load(fh)
        self.assertEqual((kq[0]["openalex"], kq[0]["doi"], kq[0]["nam"]), ("W1", "10.1/a", 2012))


class LoiMang(CoSo):
    def loi(self, loi, **kw):
        def lay(url):
            raise loi
        self.o.lay_json = lay
        return self.chay("career", **kw)

    def test_bi_tu_choi_thi_noi_cach_dat_khoa(self):
        for ma_http in (401, 403):
            ma, out, err = self.loi(urllib.error.HTTPError("https://api.openalex.org/works?api_key=bi-mat", ma_http, "Forbidden", {}, None),
                                    env={"OPENALEX_API_KEY": "bi-mat"})
            self.assertEqual(ma.count("OPENALEX_API_KEY"), 1)
            self.assertIn(f"HTTP {ma_http}", ma)
            self.assertNotIn("bi-mat", ma + out + err)
            self.assertNotIn("Lỗi mạng", ma)

    def test_goi_qua_nhieu(self):
        ma, out, err = self.loi(urllib.error.HTTPError("u", 429, "Too Many Requests", {}, None))
        self.assertIn("quá nhiều", ma)

    def test_mat_mang(self):
        ma, out, err = self.loi(urllib.error.URLError("Tunnel connection failed: 403 Forbidden"))
        self.assertIn("Lỗi mạng", ma)
        self.assertNotIn("OPENALEX_API_KEY", ma)


class GhiBib(CoSo):
    def setUp(self):
        super().setUp()
        self.bib = os.path.join(self.d, "ung-vien.bib")
        self.o.lay_bibtex = bibtex_gia

    def doc(self):
        with open(self.bib, encoding="utf-8") as f:
            return f.read()

    def khoa(self):
        return [m[1] for m in __import__("re").findall(r"@(\w+)\{([^,]+),", self.doc())]

    def test_khoa_trung_duoc_doi(self):
        self.tra_ve([bai(1, "10.1/a"), bai(2, "10.1/b"), bai(3, "10.1/c")])
        ma, out, err = self.chay("career", "--bib", self.bib)
        self.assertEqual(self.khoa(), ["Savickas_2012", "Savickas_2012a", "Savickas_2012b"])
        self.assertIn("Đã ghi thêm BibTeX của 3 bài", out)

    def test_khong_ghi_de_file_da_co(self):
        _nap.ghi(self.d, "ung-vien.bib", "@article{savickas_2012, title={Mục có sẵn}, doi = {10.9/CU}}")   # không có dòng trống cuối
        self.tra_ve([bai(1, "10.1/a"), bai(2, "10.9/cu")])
        ma, out, err = self.chay("career", "--bib", self.bib)
        self.assertIn("Mục có sẵn", self.doc())
        self.assertEqual(self.khoa(), ["savickas_2012", "Savickas_2012a"])       # khoá trùng (không kể hoa thường) được đổi
        self.assertIn("của 1 bài", out)
        self.assertIn("1 bài đã có trong file", out)
        self.assertIn("}\n @article{Savickas_2012a", self.doc())                  # mục mới bắt đầu ở dòng mới

    def test_chay_lai_khong_them_ban_trung(self):
        self.tra_ve([bai(1, "10.1/a"), bai(2, "10.1/b")])
        self.chay("career", "--bib", self.bib)
        truoc = self.doc()
        ma, out, err = self.chay("career", "--bib", self.bib)
        self.assertEqual(self.doc(), truoc)
        self.assertIn("của 0 bài", out)
        self.assertIn("2 bài đã có trong file", out)

    def test_doi_trung_trong_cung_mot_lan_tim(self):
        self.tra_ve([bai(1, "10.1/a"), bai(2, "10.1/A")])
        self.chay("career", "--bib", self.bib)
        self.assertEqual(self.khoa(), ["Savickas_2012"])

    def test_bai_khong_doi_va_bai_khong_lay_duoc(self):
        def lay(doi):
            if doi.endswith("hong"):
                raise urllib.error.HTTPError("u", 404, "Not Found", {}, None)
            if doi.endswith("html"):
                return "<html>không phải BibTeX</html>"
            return bibtex_gia(doi)
        self.o.lay_bibtex = lay
        goc = self.o.MAU_DAU_MUC

        def lay_that(doi):                      # dùng đúng phép kiểm của script với câu trả lời giả
            muc = lay(doi)
            if not goc.match(muc):
                raise ValueError("doi.org không trả về BibTeX")
            return muc
        self.o.lay_bibtex = lay_that
        self.tra_ve([bai(1, "10.1/a"), bai(2), bai(3, "10.1/hong"), bai(4, "10.1/html")])
        ma, out, err = self.chay("career", "--bib", self.bib)
        self.assertEqual(self.khoa(), ["Savickas_2012"])
        self.assertIn("của 1 bài", out)
        self.assertIn("1 bài không có DOI", out)
        self.assertIn("KHÔNG lấy được BibTeX của 2 bài", out)
        self.assertIn("- 10.1/hong:", out)
        self.assertIn("- 10.1/html:", out)
        self.assertNotIn("hong", self.doc())      # file .bib không bị chèn dòng báo lỗi

    def test_khong_co_gi_de_ghi_thi_khong_tao_file(self):
        self.tra_ve([bai(1)])
        self.chay("career", "--bib", self.bib)
        self.assertFalse(os.path.exists(self.bib))

    def test_het_bang_chu_cai_thi_danh_so(self):
        da_dung = {"k"} | {"k" + c for c in "abcdefghijklmnopqrstuvwxyz"}
        self.assertEqual(self.o.dat_khoa_rieng("@article{K, title={x}}", da_dung), "@article{K2, title={x}}")
        self.assertEqual(self.o.dat_khoa_rieng("@article{K, title={x}}", da_dung), "@article{K3, title={x}}")

    def test_lay_bibtex_kiem_cau_tra_loi(self):
        o = _nap.nap("tim_openalex")

        class TraLoi:
            def __init__(self, nd):
                self.nd = nd

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                return self.nd.encode("utf-8")
        yeu_cau = []

        def mo(req, timeout):
            yeu_cau.append(req)
            return TraLoi(" @article{Braun_2006, title={Using thematic analysis}, DOI={10.1191/1478088706qp063oa} }\n")
        with mock.patch.object(o.urllib.request, "urlopen", mo):
            self.assertTrue(o.lay_bibtex("10.1191/1478088706qp063oa").startswith("@article{Braun_2006"))
        self.assertEqual(yeu_cau[0].full_url, "https://doi.org/10.1191/1478088706qp063oa")
        self.assertEqual(yeu_cau[0].get_header("Accept"), "application/x-bibtex; charset=utf-8")
        with mock.patch.object(o.urllib.request, "urlopen", lambda req, timeout: TraLoi("<!DOCTYPE html><html></html>")):
            with self.assertRaises(ValueError):
                o.lay_bibtex("10.1/x")


class DongLenhThat(unittest.TestCase):
    def test_help_va_bang_ma(self):
        ma, out, err = _nap.chay("tim_openalex", "--help", env={"PYTHONIOENCODING": "ascii"})
        self.assertEqual((ma, err), (0, ""))
        self.assertIn("không ghi đè", out)


if __name__ == "__main__":
    unittest.main()

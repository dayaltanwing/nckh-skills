"""Kiểm thử kiem_thong_ke.py.

Chạy từ thư mục gốc của repo:  python3 -m unittest discover -s tests
"""
import json
import os
import tempfile
import unittest

import _nap

# (loại, giá trị, df1, df2, p đúng). p đúng lấy từ scipy 1.18 (stats.t.sf, f.sf, chi2.sf, norm.sf);
# t, r, z là p hai phía.
P_CHUAN = [
    ("t", 1.0, 1, None, 0.5000000000000001),
    ("t", 2.0, 4.7, None, 0.10557218220343964),
    ("t", 2.228, 10, None, 0.05001177181711132),
    ("t", 2.31, 48, None, 0.025232937459841107),
    ("t", 0.5, 48, None, 0.6193596576930802),
    ("t", 3.5, 120, None, 0.0006538077398618747),
    ("t", 8.0, 29, None, 8.012575649631688e-09),
    ("t", 1.96, 1000, None, 0.050273184955748736),
    ("t", 2.1, 45.3, None, 0.04132841726446314),
    ("t", 40.0, 5, None, 1.8411962171772954e-07),
    ("F", 5.34, 1, 48, 0.0251823524093857),
    ("F", 4.52, 2, 117, 0.012856768788707262),
    ("F", 35.2, 3, 196, 3.038646879596168e-18),
    ("F", 3.3, 1.82, 105.6, 0.04516302300542716),
    ("F", 1.2, 12, 1000, 0.2777905856504157),
    ("F", 0.3, 5, 10, 0.9019579816310673),
    ("F", 60.0, 2, 20, 3.5401331746414338e-09),
    ("chi2", 3.84, 1, None, 0.05004352124870519),
    ("chi2", 9.21, 3, None, 0.02662527433636976),
    ("chi2", 51.3, 24, None, 0.0009645273079392715),
    ("chi2", 1254.31, 350, None, 5.083179991452409e-102),
    ("chi2", 0.5, 2, None, 0.7788007830714049),
    ("chi2", 90.0, 100, None, 0.7531979655998298),
    ("chi2", 30.0, 7.5, None, 0.00014301587882904854),
    ("chi2", 150.0, 10, None, 3.727485055062505e-27),
    ("r", 0.34, 98, None, 0.0005382497694072949),
    ("r", 0.5, 28, None, 0.004899933667068085),
    ("r", 0.1, 10, None, 0.7571581091015624),
    ("r", 0.9, 500, None, 1.9328268277478186e-182),
    ("r", 0.999, 3, None, 3.7954974373400645e-05),
    ("z", 1.96, 1, None, 0.04999579029644087),
    ("z", 2.1, 1, None, 0.035728841125633085),
    ("z", 0.5, 1, None, 0.6170750774519738),
    ("z", 5.0, 1, None, 5.733031437583866e-07),
    ("z", 8.0, 1, None, 1.244192114854348e-15),
]


class CoSo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k = _nap.nap("kiem_thong_ke")

    def kiem(self, van_ban, la_tex=True, **tuy_chon):
        return self.k.kiem_van_ban("x.tex", van_ban.split("\n"), la_tex, **tuy_chon)

    def mot(self, van_ban, la_tex=True, **tuy_chon):
        """Văn bản chỉ có một thống kê: trả về kết quả của nó."""
        kq = self.kiem(van_ban, la_tex, **tuy_chon)
        self.assertEqual(len(kq), 1, f"{van_ban!r} -> {kq}")
        return kq[0]

    def assertTrangThai(self, van_ban, mong_doi, loai=None, la_tex=True, **tuy_chon):
        kq = self.mot(van_ban, la_tex, **tuy_chon)
        self.assertEqual(kq["trang_thai"], mong_doi, f"{van_ban!r} -> {kq}")
        if loai:
            self.assertEqual(kq["loai"], loai, van_ban)
        return kq


class SoHoc(CoSo):
    def test_khop_scipy(self):
        for loai, gt, df1, df2, chuan in P_CHUAN:
            with self.subTest(loai=loai, gt=gt, df1=df1, df2=df2):
                self.assertAlmostEqual(self.k.tinh_p(loai, gt, df1, df2) / chuan, 1.0, delta=1e-7)

    def test_bac_tu_do_rat_lon(self):
        # p đúng lấy từ scipy. Trước khi có nhánh xấp xỉ, df = 1e15 cho sai số 40–60%.
        chuan = [("t", 2.0, 1e9, None, 0.045500264166313246), ("t", 2.0, 1e15, None, 0.04550026389635871),
                 ("t", 5.0, 1e12, None, 5.73303143855025e-07),
                 ("F", 4.0, 1, 1e12, 0.04550026389662835), ("F", 2.6, 3, 1e12, 0.05033109786045144),
                 ("F", 1.6, 20, 1e10, 0.04329831618054975), ("F", 0.4, 1e12, 5, 0.9714568766731589),
                 ("F", 2.5, 1e12, 5, 0.15085496391552888), ("F", 1.0, 1e9, 1e9, 0.4999999999999981),
                 ("F", 1.001, 1e9, 1e9, 1.4718529529567575e-56)]
        for loai, gt, df1, df2, p in chuan:
            with self.subTest(loai=loai, gt=gt, df1=df1, df2=df2):
                self.assertAlmostEqual(self.k.tinh_p(loai, gt, df1, df2) / p, 1.0, delta=1e-5)
        self.assertGreater(self.k.p_f(0.999, 1e9, 1e9), 0.999999)

    def test_gia_tri_bien(self):
        k = self.k
        self.assertEqual(k.p_t(0, 10), 1.0)
        self.assertEqual(k.p_f(0, 2, 10), 1.0)
        self.assertEqual(k.p_chi2(0, 3), 1.0)
        self.assertEqual(k.p_z(0), 1.0)
        self.assertEqual(k.p_r(1.0, 10), 0.0)
        self.assertEqual(k.p_t(-2.31, 48), k.p_t(2.31, 48))
        for p in (k.p_t(1e6, 3), k.p_f(1e9, 2, 5), k.p_chi2(1e6, 4), k.p_z(60)):
            self.assertTrue(0.0 <= p < 1e-12, p)


class CachViet(CoSo):
    """Cùng một thống kê, nhiều cách viết: đều phải đọc ra được."""

    def test_t(self):
        for vb in ("The effect was significant, t(48) = 2.31, p = .025.",
                   r"$t(48) = 2.31$, $p = .025$",
                   r"\textit{t}(48) = 2.31, \textit{p} = .025",
                   r"\emph{t}\,(48)~=~2.31, \emph{p}\,=\,.025",
                   r"{\it t}(48)=2.31,{\it p}=.025",
                   r"($t(48) = \num{2.31}$, $p = 0.025$)",
                   "t (48) = 2.31; p = .025",
                   "t(48) = 2.31, P = .025",
                   "t(48) = 2.31, p-value = 0.025",
                   "t(48) = 2.31, 95% CI [0.12, 0.85], d = 0.65, p = .025",
                   "t(48) = 2.31, 95% CI [0.12, 0.85], Cohen's d = 0.65, Hedges' g = 0.64, BF10 = 2.4, p = .025",
                   "t(48) = 2.31, two-tailed p = .025",
                   "t(48) = 2.31, partial eta squared = .10, odds ratio = 2.1, p = .025",
                   "t(48) = 2.31,\n   p = .025",
                   "t(48) = 2.31 with p = .025",
                   "t(48) = 2,31 với mức ý nghĩa p = 0,025"):
            with self.subTest(vb=vb):
                self.assertTrangThai(vb, "OK", "t")

    def test_t_am(self):
        for vb in ("t(48) = -2.31, p = .025", "t(48) = \u22122.31, p = .025", r"$t(48) = -2.31$, $p = .025$",
                   r"\textit{t}(48) = $-$2.31, \textit{p} = .025", "t(48) = \u20132.31, p = .025"):
            with self.subTest(vb=vb):
                self.assertTrangThai(vb, "OK", "t")

    def test_f(self):
        for vb in (r"$F(2, 117) = 4.52$, $p = .013$, $\eta^2_p = .07$",
                   r"\textit{F}(2, 117) = 4.52, \textit{MSE} = 1.20, \textit{p} = .013",
                   "F(2,117)=4.52, p=.013",
                   "F(2; 117) = 4.52, p = .013",
                   r"$F(1.82, 105.6) = 3.30$, $p = .045$",
                   r"$\Delta F(1, 196) = 5.20$, $p = .024$",
                   "ΔF(1, 196) = 5.20, p = .024",
                   "F(2, 2,455) = 3.10, p = .045"):
            with self.subTest(vb=vb):
                self.assertTrangThai(vb, "OK", "F")

    def test_chi_binh_phuong(self):
        for vb in (r"$\chi^2(3) = 9.21$, $p = .027$",
                   r"$\chi^{2}(3, N = 210) = 9.21$, $p = .027$",
                   r"$\chi^2$(3, \textit{N} = 1,210) = 9.21, \textit{p} = .027",
                   "χ²(3) = 9.21, p = .027",
                   "χ2(3) = 9.21, p = .027",
                   "χ^2 (3) = 9.21, p = .027",
                   "chi-square(3) = 9.21, p = .027",
                   "Chi-squared (3) = 9.21, p = .027",
                   "X2(3) = 9.21, p = .027",
                   r"$\Delta\chi^2(3) = 9.21$, $p = .027$",
                   r"$\chi^2_{\text{diff}}(3) = 9.21$, $p = .027$",
                   "Wald χ²(3) = 9.21, p = .027",
                   "χ²(350) = 1,254.31, p < .001"):
            with self.subTest(vb=vb):
                self.assertTrangThai(vb, "OK", "chi2")

    def test_r_va_z(self):
        self.assertTrangThai(r"$r(98) = .34$, $p < .001$", "OK", "r")
        self.assertTrangThai("r(98) = -.34, p < .001", "OK", "r")
        self.assertTrangThai("r(98) = 0.20, p = .046", "OK", "r")
        self.assertTrangThai(r"$z = 2.10$, $p = .036$", "OK", "z")
        self.assertTrangThai("Z = -2.10, p = .036", "OK", "z")

    def test_dau_so_sanh(self):
        for vb in ("t(48) = 2.31, p < .05", r"t(48) = 2.31, $p < .05$", r"t(48) = 2.31, \textit{p} \textless{} .05",
                   r"t(48) = 2.31, $p \leq .05$", "t(48) = 2.31, p ≤ .05", "t(48) = 2.31, p <= .05",
                   "t(48) = 0.50, p > .05", r"t(48) = 0.50, $p \geq .05$", "t(48) = 0.50, p >= .10",
                   "t(48) = 0.50, ns", "t(48) = 0.50, n.s.", r"$t(48) = 0.50$, \textit{ns}"):
            with self.subTest(vb=vb):
                self.assertTrangThai(vb, "OK", "t")

    def test_p_dang_khoa_hoc(self):
        for vb in ("t(29) = 8.00, p = 8.0e-9", r"$t(29) = 8.00$, $p = 8.0 \times 10^{-9}$", "t(29) = 8.00, p = 8.0 × 10^-9"):
            with self.subTest(vb=vb):
                self.assertTrangThai(vb, "OK", "t")
        self.assertTrangThai("t(29) = 8.00, p = 8.0e-4", "LỆCH")

    def test_dau_phay_thap_phan(self):
        for vb in ("t(48) = 2,31; p = 0,025", "t(48) = 2,310; p = 0,025", "t(48) = 2,31; Sig. = 0,025",
                   "t(48) = 2,31, p < 0,05", "F(2, 117) = 4,52; p = 0,013", "r(98) = 0,34; p < 0,001"):
            with self.subTest(vb=vb):
                self.assertTrangThai(vb, "OK")
        self.assertTrangThai("χ2(350) = 1.254,31; p < 0,001", "OK", "chi2")
        self.assertTrangThai("t(48) = 2,31; p = 0,250", "LỆCH NẶNG")

    def test_dau_phay_hang_nghin_trong_van_ban_tieng_anh(self):
        # 2,310 trong bài tiếng Anh là hai nghìn ba trăm mười, không phải 2.310.
        kq = self.mot("Model fit was poor, χ²(900) = 2,310, p < .001, CFI = .82, RMSEA = .09.")
        self.assertEqual(kq["trang_thai"], "OK")
        self.assertTrangThai("t(1,203) = 2.50, p = .013", "OK", "t")

    def test_bac_tu_do_le(self):
        self.assertTrangThai("Welch's t(45.3) = 2.10, p = .041", "OK", "t")

    def test_markdown_va_van_ban_thuong(self):
        for vb in ("*t*(48) = 2.31, *p* = .025", "_t_(48) = 2.31, _p_ = .025", "**F**(2, 117) = 4.52, **p** = .013",
                   "t(48) = 2.31, p &lt; .05", "χ²(3) = 9.21, _p_ = .027", "`t(48) = 2.31, p = .025`",
                   "t(48)\u00a0=\u00a02.31, p\u00a0=\u00a0.025"):
            with self.subTest(vb=vb):
                self.assertTrangThai(vb, "OK", la_tex=False)

    def test_dau_phan_tram_trong_van_ban_thuong_khong_phai_chu_thich(self):
        with tempfile.TemporaryDirectory() as d:
            f = _nap.ghi(d, "a.md", "Có 50% mẫu là nữ; t(48) = 2.31, p = .025\n")
            ban_thao, _ = self.k.doc_ban_thao(f)
            self.assertEqual(self.k.kiem_van_ban(*ban_thao[0])[0]["trang_thai"], "OK")


class KhongDocNham(CoSo):
    """Những thứ trông giống mà không phải: không được đọc nhầm."""

    def test_eta_binh_phuong_rieng_phan_khong_phai_p(self):
        for vb in (r"$F(2, 117) = 4.52$, $\eta^2_p = .07$", r"$F(2, 117) = 4.52$, $\eta_p^2 = .07$",
                   r"$F(2, 117) = 4.52$, $\eta^{2}_{p} = .07$", r"$F(2, 117) = 4.52$, $\eta^2_\text{p} = .07$",
                   r"$F(2, 117) = 4.52$, $\eta^2_{\mathrm{p}} = .07$", "F(2, 117) = 4.52, ηp² = .07",
                   "F(2, 117) = 4.52, η2p = .07"):
            with self.subTest(vb=vb):
                self.assertTrangThai(vb, "KHÔNG CÓ p", "F")

    def test_p_dung_sau_eta(self):
        kq = self.assertTrangThai(r"$F(2, 117) = 4.52$, $\eta_p^2 = .07$, $p = .013$", "OK", "F")
        self.assertEqual(kq["p_ghi"], "p = .013")

    def test_p_da_hieu_chinh_khong_dem_ra_so(self):
        for vb in (r"$t(48) = 2.31$, $p_{\text{Holm}} = .075$", r"$t(48) = 2.31$, $p_{adj} = .075$",
                   "t(48) = 2.31, padj = .075", "t(48) = 2.31, p_FDR = .075"):
            with self.subTest(vb=vb):
                self.assertTrangThai(vb, "KHÔNG CÓ p", "t")

    def test_chu_trong_tu_khac(self):
        for vb in ("cost(48) = 2.31, p = .9", "Heart(48) = 2.31, p = .9", "CDF(2, 117) = 4.52, p = .9",
                   "size = 2.10, p = .9", r"$\beta = 0.42$, $p < .001$", "t = 2.31, p = .025", "r = .34, p < .001",
                   "χ2/df = 2.31, p = .9"):
            with self.subTest(vb=vb):
                self.assertEqual(self.kiem(vb), [])

    def test_chu_thich_latex(self):
        self.assertEqual(self.kiem(self.k.bo_chu_thich("% t(48) = 2.31, p = .9")), [])
        dong = self.k.bo_chu_thich("Có 50\\% nữ, t(48) = 2.31 % ghi chú: p = .9")
        self.assertTrangThai(dong, "KHÔNG CÓ p")
        self.assertTrangThai(self.k.bo_chu_thich("Có 50\\% nữ, t(48) = 2.31, p = .025 % p = .9"), "OK")

    def test_p_cua_cau_sau_khong_thuoc_thong_ke_nay(self):
        self.assertTrangThai("We found t(48) = 0.52. The other effect was significant, p = .003.", "KHÔNG CÓ p")
        self.assertTrangThai("t(48) = 0.52.\n\nĐoạn mới có p = .003.", "KHÔNG CÓ p")
        # Dòng trống là hết đoạn, kể cả khi đoạn sau bắt đầu bằng chữ thường.
        for vb in ("t(48) = 0.52.\n\np = .003", "t(48) = 0.52\n\np = .003", "t(48) = 0.52.\n  \n(p = .003)"):
            with self.subTest(vb=vb):
                self.assertTrangThai(vb, "KHÔNG CÓ p")

    def test_dau_cham_truoc_chu_thuong_khong_phai_het_cau(self):
        # Dấu chấm của chữ viết tắt ("est.", "vs.") không kết thúc câu, nên p đứng sau vẫn thuộc thống kê này.
        self.assertTrangThai("t(48) = 2.31 (est. 95% CI [0.1, 0.9]), p = .025", "OK")
        self.assertTrangThai("t(48) = 2.31 vs. p = .025", "OK")

    def test_p_cua_thong_ke_dung_sau(self):
        kq = self.kiem("t(48) = 0.52 and F(1, 48) = 5.34, p = .025")
        self.assertEqual([(x["loai"], x["trang_thai"]) for x in kq], [("t", "KHÔNG CÓ p"), ("F", "OK")])

    def test_p_cua_he_so_khac_trong_cung_cau(self):
        for vb in ("The main effect was not significant, F(1, 196) = 0.85, but the slope was, b = 0.30, p = .004.",
                   "t(48) = 0.52 for A, whereas B was significant, p = .003",
                   "t(48) = 0.52 (adjusted p = .003)",
                   "t(48) = 0.52, which differed from the pilot, ns"):
            with self.subTest(vb=vb):
                self.assertTrangThai(vb, "KHÔNG CÓ p")

    def test_p_o_qua_xa(self):
        vb = "t(48) = 0.52 for the first comparison, whereas the second comparison was clearly significant with p = .003"
        self.assertTrangThai(vb, "KHÔNG CÓ p")


class SoP(CoSo):
    def test_lech_nhung_khong_doi_ket_luan(self):
        kq = self.assertTrangThai("t(48) = 2.31, p = .010", "LỆCH")
        self.assertAlmostEqual(kq["p_tinh"], 0.02523, places=4)

    def test_lech_nang_bai_ghi_co_y_nghia(self):
        kq = self.assertTrangThai("t(48) = 1.50, p = .03", "LỆCH NẶNG")
        self.assertIn("bài ghi có ý nghĩa", kq["ghi_chu"])
        self.assertTrangThai("t(48) = 1.50, p < .05", "LỆCH NẶNG")
        self.assertTrangThai("F(1, 48) = 2.00, p < .05", "LỆCH NẶNG")

    def test_lech_nang_bai_ghi_khong_co_y_nghia(self):
        kq = self.assertTrangThai("t(48) = 2.50, p = .20", "LỆCH NẶNG")
        self.assertIn("bài ghi không có ý nghĩa", kq["ghi_chu"])
        self.assertTrangThai("t(48) = 2.50, ns", "LỆCH NẶNG")
        self.assertTrangThai("χ²(3) = 20.00, p > .05", "LỆCH NẶNG")

    def test_p_bang_alpha_khong_suy_ra_ket_luan(self):
        self.assertTrangThai("t(48) = 1.79, p = .05", "LỆCH")

    def test_alpha_khac(self):
        self.assertTrangThai("t(48) = 2.31, p = .005", "LỆCH")                    # .025 và .005 đều < .05
        self.assertTrangThai("t(48) = 2.31, p = .005", "LỆCH NẶNG", alpha=0.01)   # .025 > .01

    def test_tinh_ca_sai_so_lam_tron_cua_thong_ke(self):
        # t = 2.1 có thể là 2.05–2.15, nên p thật nằm trong khoảng .044–.054.
        for p in (".044", ".048", ".05", ".054"):
            with self.subTest(p=p):
                self.assertTrangThai(f"t(20) = 2.1, p = {p}", "OK")
        self.assertTrangThai("t(20) = 2.1, p = .040", "LỆCH")
        self.assertTrangThai("t(20) = 2.10, p = .044", "LỆCH")        # ghi 2 chữ số thập phân thì khoảng hẹp hơn

    def test_p_lam_tron_den_hai_chu_so(self):
        self.assertTrangThai("t(48) = 2.31, p = .03", "OK")
        self.assertTrangThai("t(48) = 2.31, p = .02", "OK")       # t = 2.315 cho p = .0249, làm tròn thành .02
        self.assertTrangThai("t(48) = 2.31, p = .04", "LỆCH")
        self.assertTrangThai("t(48) = 2.01, p = .05", "OK")

    def test_p_nho_hon_nguong(self):
        self.assertTrangThai("t(120) = 3.50, p < .001", "OK")
        self.assertTrangThai("t(120) = 3.00, p < .001", "LỆCH")       # p = .003

    def test_p_bang_khong(self):
        kq = self.assertTrangThai("t(48) = 5.00, p = .000", "OK")
        self.assertIn("p < .001", kq["ghi_chu"])
        self.assertTrangThai("t(48) = 2.31, p = .000", "LỆCH")

    def test_mot_phia(self):
        vb = "t(48) = 1.80, p = .039"                                  # hai phía .078, một phía .039
        kq = self.assertTrangThai(vb, "MỘT PHÍA?")
        self.assertIn("một phía", kq["ghi_chu"])
        self.assertTrangThai(vb, "OK", mot_phia=True)
        for vb in ("A one-tailed test showed t(48) = 1.80, p = .039.", "t(48) = 1.80, p = .039 (one-sided)",
                   "Kiểm định một phía cho thấy t(48) = 1,80; p = 0,039."):
            with self.subTest(vb=vb):
                kq = self.assertTrangThai(vb, "OK")
                self.assertIn("một phía", kq["ghi_chu"])

    def test_khai_mot_phia_nhung_p_la_hai_phia(self):
        self.assertTrangThai("t(48) = 2.31, p = .025", "HAI PHÍA?", mot_phia=True)

    def test_f_va_chi_binh_phuong_khong_co_mot_phia(self):
        self.assertTrangThai("F(1, 48) = 3.24, p = .039", "LỆCH NẶNG")      # p = .078; chia đôi không áp dụng cho F
        self.assertTrangThai("F(1, 48) = 5.34, p = .025", "OK", mot_phia=True)

    def test_so_qua_lon_khong_lam_hong(self):
        self.assertTrangThai("t(48) = 2.31, p = 1e999", "KHÔNG HỢP LỆ")
        self.assertTrangThai("t(48) = 2.31, p = 1e-999", "LỆCH")
        self.assertTrangThai("t(48) = " + "9" * 400 + ", p < .001", "OK")
        self.assertTrangThai("t(" + "9" * 30 + ") = 2.00, p = .046", "OK")
        self.assertTrangThai("F(1, " + "9" * 30 + ") = 4.00, p = .046", "OK")
        self.assertTrangThai("χ²(3) = " + "9" * 400 + ", p < .001", "OK")
        self.assertTrangThai("t(48) = 2.31, p = 0." + "0" * 400 + "1", "LỆCH")

    def test_khong_hop_le(self):
        for vb in ("r(98) = 1.34, p < .001", "t(0) = 2.00, p = .05", "t(48) = 2.31, p = 1.5",
                   "F(2, 117) = -4.52, p = .013", "F(0, 117) = 4.52, p = .013", "χ²(3) = -9.21, p = .027"):
            with self.subTest(vb=vb):
                self.assertTrangThai(vb, "KHÔNG HỢP LỆ")

    def test_khong_co_p(self):
        kq = self.assertTrangThai("Kết quả: t(48) = 2.31.", "KHÔNG CÓ p")
        self.assertAlmostEqual(kq["p_tinh"], 0.02523, places=4)

    def test_vi_tri_va_thong_ke_ngat_dong(self):
        kq = self.kiem("Dòng một\nKết quả là $t(48) = 2.31$,\n$p = .025$ và\n$F(1, 48) = 5.34$, $p = .5$")
        self.assertEqual([(x["vi_tri"], x["trang_thai"]) for x in kq], [("x.tex:2", "OK"), ("x.tex:4", "LỆCH NẶNG")])
        self.assertEqual(kq[0]["thong_ke"], "t(48) = 2.31")
        self.assertEqual(kq[0]["p_ghi"], "p = .025")


class DongLenh(unittest.TestCase):
    def setUp(self):
        self._tam = tempfile.TemporaryDirectory()
        self.d = self._tam.name
        self.addCleanup(self._tam.cleanup)

    def chay(self, duong, *them, env=None):
        kq_json = os.path.join(self.d, "kq.json")
        ma, out, err = _nap.chay("kiem_thong_ke", duong, "--json", kq_json, *them, env=env)
        self.assertEqual(err, "")
        with open(kq_json, encoding="utf-8") as f:
            return ma, out, json.load(f)

    def test_ban_thao_sach(self):
        tex = _nap.ghi(self.d, "bt/main.tex", "$t(48) = 2.31$, $p = .025$\n$F(2, 117) = 4.52$, $p = .013$\n")
        ma, out, kq = self.chay(tex)
        self.assertEqual(ma, 0)
        self.assertEqual([x["trang_thai"] for x in kq["thong_ke"]], ["OK", "OK"])
        self.assertIn("| main.tex:1 | t(48) = 2.31 | p = .025 | .0252 | OK |", out)

    def test_co_lech_thi_ma_thoat_1(self):
        tex = _nap.ghi(self.d, "bt/main.tex", "$t(48) = 1.50$, $p = .03$\n")
        ma, out, kq = self.chay(tex)
        self.assertEqual(ma, 1)
        self.assertIn("LỆCH NẶNG", out)

    def test_chi_thieu_p_thi_khong_phai_loi(self):
        tex = _nap.ghi(self.d, "bt/main.tex", "$t(48) = 2.31$.\n")
        self.assertEqual(self.chay(tex)[0], 0)

    def test_di_theo_input(self):
        tex = _nap.ghi(self.d, "bt/main.tex", "\\input{sections/03-results}\n% \\input{sections/bo}\n")
        _nap.ghi(self.d, "bt/sections/03-results.tex", "Dòng 1\n$t(48) = 1.50$, $p = .03$\n")
        _nap.ghi(self.d, "bt/sections/bo.tex", "$t(48) = 9.99$, $p = .9$\n")
        ma, out, kq = self.chay(tex)
        self.assertEqual([x["vi_tri"] for x in kq["thong_ke"]], ["sections/03-results.tex:2"])

    def test_thu_muc_bo_qua_ban_vong_truoc(self):
        _nap.ghi(self.d, "bt/main.tex", "$t(48) = 2.31$, $p = .025$\n")
        _nap.ghi(self.d, "bt/vong-1/main.tex", "$t(48) = 1.50$, $p = .03$\n")
        _nap.ghi(self.d, "bt/main-diff.tex", "$t(48) = 1.50$, $p = .03$\n")
        _nap.ghi(self.d, "bt/phan-bien-2026-11-01.md", "t(48) = 1.50, p = .03\n")
        ma, out, kq = self.chay(os.path.join(self.d, "bt"))
        self.assertEqual((ma, len(kq["thong_ke"])), (0, 1))
        self.assertIn("vong-1", out)

    def test_file_markdown(self):
        md = _nap.ghi(self.d, "ket-qua.md", "Kết quả: *t*(48) = 2,31; *p* = 0,025 (50% mẫu).\n")
        ma, out, kq = self.chay(md)
        self.assertEqual((ma, [x["trang_thai"] for x in kq["thong_ke"]]), (0, ["OK"]))

    def test_khong_tim_thay_thong_ke_nao(self):
        tex = _nap.ghi(self.d, "bt/main.tex", "Chưa có số liệu.\n")
        ma, out, kq = self.chay(tex)
        self.assertEqual(ma, 0)
        self.assertIn("KHÔNG có nghĩa là số liệu đúng", out)

    def test_thu_muc_khong_co_tex(self):
        os.makedirs(os.path.join(self.d, "rong"))
        ma, out, kq = self.chay(os.path.join(self.d, "rong"))
        self.assertIn("không có file .tex", out)

    def test_tuy_chon(self):
        tex = _nap.ghi(self.d, "bt/main.tex", "$t(48) = 1.80$, $p = .039$\n$t(48) = 2.31$, $p = .005$\n")
        self.assertEqual([x["trang_thai"] for x in self.chay(tex)[2]["thong_ke"]], ["MỘT PHÍA?", "LỆCH"])
        self.assertEqual([x["trang_thai"] for x in self.chay(tex, "--mot-phia")[2]["thong_ke"]], ["OK", "LỆCH"])
        self.assertEqual([x["trang_thai"] for x in self.chay(tex, "--alpha", "0.01")[2]["thong_ke"]], ["MỘT PHÍA?", "LỆCH NẶNG"])

    def test_dau_vao_sai(self):
        for duong in (os.path.join(self.d, "khong-co.tex"), os.path.join(self.d, "khong-co")):
            ma, out, err = _nap.chay("kiem_thong_ke", duong)
            self.assertEqual(ma, 2)
            self.assertIn("khong-co", err)
        docx = _nap.ghi(self.d, "bai.docx", "PK")
        ma, out, err = _nap.chay("kiem_thong_ke", docx)
        self.assertEqual(ma, 2)
        self.assertIn(".txt", err)
        ma, out, err = _nap.chay("kiem_thong_ke", _nap.ghi(self.d, "a.tex", "x"), "--alpha", "5")
        self.assertEqual(ma, 2)

    def test_in_duoc_tieng_viet_khi_bang_ma_khong_phai_utf8(self):
        tex = _nap.ghi(self.d, "bt/main.tex", "$\\chi^2(3) = 9.21$, $p = .5$\n")
        ma, out, kq = self.chay(tex, env={"PYTHONIOENCODING": "ascii"})
        self.assertEqual(ma, 1)
        self.assertIn("LỆCH NẶNG", out)
        self.assertIn("χ", out)


if __name__ == "__main__":
    unittest.main()

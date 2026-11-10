#!/usr/bin/env python3
"""Tính lại p từ thống kê kiểm định ghi trong bản thảo và so với p đã ghi (ý tưởng của statcheck).

Chỉ dùng thư viện chuẩn của Python 3.9+.

Đọc được thống kê viết trong câu theo kiểu APA:
  t(48) = 2.31, p = .025       F(2, 117) = 4.52, p = .013       χ²(3, N = 210) = 9.21, p = .027
  r(98) = .34, p < .001        z = 2.10, p = .036
kể cả khi viết bằng LaTeX ($t(48) = 2.31$, \\textit{p} = .025, $\\chi^2(3) = 9.21$) hoặc dùng dấu phẩy thập phân
(t(48) = 2,31; p = 0,025). Không đọc được số nằm trong bảng.

Ví dụ:
  python3 kiem_thong_ke.py ban-thao/main.tex
  python3 kiem_thong_ke.py ban-thao/sections/03-results.tex --json ket-qua.json

Đường dẫn là một trong ba:
  - file .tex chính: đọc file đó và mọi file nó \\input / \\include (đệ quy);
  - thư mục: đọc mọi .tex bên trong, trừ bản lưu vòng trước (vong-*/) và file latexdiff (*-diff.tex);
  - file văn bản khác (.md, .txt): đọc đúng file đó.

Mã thoát: 0 = không có lỗi, 1 = có mục cần xem lại, 2 = lỗi đầu vào.
"""
import argparse
import html
import json
import math
import os
import re
import sys

# Trạng thái làm script thoát với mã 1.
TRANG_THAI_LOI = ("LỆCH", "LỆCH NẶNG", "MỘT PHÍA?", "HAI PHÍA?", "KHÔNG HỢP LỆ")
TEN = {"t": "t", "F": "F", "chi2": "χ²", "r": "r", "z": "z"}
CO_HAI_PHIA = ("t", "r", "z")          # F và χ² vốn chỉ có một đuôi


# ---------- phân phối xác suất (không cần scipy) ----------

NHO = 1e-300
SAI_SO = 1e-15
SO_VONG = 200000


def _lien_phan_so_beta(a, b, x):
    """Liên phân số của hàm beta không hoàn chỉnh (thuật toán Lentz cải biên)."""
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > NHO else NHO)
    h = d
    for m in range(1, SO_VONG):
        m2 = 2 * m
        for aa in (m * (b - m) * x / ((qam + m2) * (a + m2)),
                   -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))):
            d = 1.0 + aa * d
            d = 1.0 / (d if abs(d) > NHO else NHO)
            c = 1.0 + aa / c
            c = c if abs(c) > NHO else NHO
            buoc = d * c
            h *= buoc
        if abs(buoc - 1.0) < SAI_SO:
            break
    return h


def beta_chuan(a, b, x):
    """Hàm beta không hoàn chỉnh chuẩn hoá I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    truoc = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1.0) / (a + b + 2.0):
        return truoc * _lien_phan_so_beta(a, b, x) / a
    return 1.0 - truoc * _lien_phan_so_beta(b, a, 1.0 - x) / b


def gamma_tren(a, x):
    """Hàm gamma không hoàn chỉnh trên, chuẩn hoá: Q(a, x)."""
    if x <= 0.0:
        return 1.0
    truoc = math.exp(-x + a * math.log(x) - math.lgamma(a))
    if x < a + 1.0:                                # chuỗi cho P(a, x), rồi Q = 1 − P
        ap, so_hang, tong = a, 1.0 / a, 1.0 / a
        for _ in range(SO_VONG):
            ap += 1.0
            so_hang *= x / ap
            tong += so_hang
            if abs(so_hang) < abs(tong) * SAI_SO:
                break
        return min(1.0, max(0.0, 1.0 - tong * truoc))
    b = x + 1.0 - a                                # liên phân số cho Q(a, x)
    c, d = 1.0 / NHO, 1.0 / (b if abs(b) > NHO else NHO)
    h = d
    for i in range(1, SO_VONG):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        d = 1.0 / (d if abs(d) > NHO else NHO)
        c = b + an / c
        c = c if abs(c) > NHO else NHO
        buoc = d * c
        h *= buoc
        if abs(buoc - 1.0) < SAI_SO:
            break
    return min(1.0, max(0.0, truoc * h))


def p_t(t, df):
    """p hai phía của t."""
    t = abs(t)
    return 1.0 if t == 0.0 else beta_chuan(df / 2.0, 0.5, df / (df + t * t))


def p_f(f, df1, df2):
    return 1.0 if f <= 0.0 else beta_chuan(df2 / 2.0, df1 / 2.0, df2 / (df2 + df1 * f))


def p_chi2(x, df):
    return gamma_tren(df / 2.0, x / 2.0)


def p_z(z):
    """p hai phía của z."""
    return math.erfc(abs(z) / math.sqrt(2.0))


def p_r(r, df):
    """p hai phía của hệ số tương quan r với df = N − 2."""
    r = abs(r)
    return 0.0 if r >= 1.0 else p_t(r * math.sqrt(df / (1.0 - r * r)), df)


def tinh_p(loai, gt, df1, df2):
    if loai == "t":
        return p_t(gt, df1)
    if loai == "F":
        return p_f(gt, df1, df2)
    if loai == "chi2":
        return p_chi2(gt, df1)
    if loai == "r":
        return p_r(gt, df1)
    return p_z(gt)


# ---------- đọc bản thảo ----------

MAU_CHU_THICH = re.compile(r"(?<!\\)((?:\\\\)*)%.*")
MAU_INPUT = re.compile(r"\\(?:input|include|subfile)\s*\{([^{}]+)\}")
KHONG_PHAI_VAN_BAN = (".docx", ".doc", ".pdf", ".odt", ".rtf")


def bo_chu_thich(dong):
    """Bỏ chú thích LaTeX: từ dấu % trở đi, trừ khi đó là \\% (dấu phần trăm thật)."""
    return MAU_CHU_THICH.sub(r"\1", dong)


def doc_dong(duong, la_tex):
    with open(duong, encoding="utf-8-sig", errors="replace") as f:
        dong = [d.rstrip("\n") for d in f]
    return [bo_chu_thich(d) for d in dong] if la_tex else dong


def doc_ban_thao(duong_dan):
    """Đọc bản thảo. Trả về (danh sách (tên file để hiển thị, các dòng, có phải LaTeX không), cảnh báo).

    File .tex: đọc file đó rồi đi theo \\input / \\include như LaTeX (đường dẫn tính từ thư mục của file chính).
    Thư mục: đọc mọi .tex, bỏ qua vong-*/ (bản đã nộp vòng trước) và *-diff.tex (latexdiff), vì các file
    đó lặp lại bản thảo cũ. File khác: đọc đúng file đó. Ném OSError nếu không đọc được đường dẫn gốc.
    """
    canh_bao = []
    if os.path.isdir(duong_dan):
        files, bo = [], []
        for goc, thu_muc, ds in os.walk(duong_dan):
            for t in sorted(thu_muc):
                if t.startswith("vong-"):
                    bo.append(os.path.relpath(os.path.join(goc, t), duong_dan) + "/")
            thu_muc[:] = sorted(t for t in thu_muc if not t.startswith("vong-"))
            for f in sorted(ds):
                if f.endswith("-diff.tex"):
                    bo.append(os.path.relpath(os.path.join(goc, f), duong_dan))
                elif f.endswith(".tex"):
                    files.append(os.path.join(goc, f))
        if bo:
            canh_bao.append("bỏ qua bản vòng trước / latexdiff: " + ", ".join(bo))
        if not files:
            canh_bao.append("thư mục không có file .tex nào để đọc")
        return [(os.path.relpath(f, duong_dan), doc_dong(f, True), True) for f in files], canh_bao

    if duong_dan.lower().endswith(KHONG_PHAI_VAN_BAN):
        raise OSError("script chỉ đọc file văn bản (.tex, .md, .txt); với Word hoặc PDF hãy xuất ra .txt trước")
    if not duong_dan.endswith(".tex"):
        return [(os.path.basename(duong_dan), doc_dong(duong_dan, False), False)], canh_bao

    goc = os.path.dirname(duong_dan) or "."
    ket_qua, da_xem = [], set()

    def them(duong, noi_goi):
        thuc = os.path.realpath(duong)
        if thuc in da_xem:
            return
        da_xem.add(thuc)
        ten = os.path.relpath(duong, goc)
        try:
            dong = doc_dong(duong, True)
        except OSError as e:
            if noi_goi is None:
                raise
            canh_bao.append(f"không đọc được {ten} (gọi từ {noi_goi}): {e.strerror or e}; phần đó chưa được kiểm")
            return
        ket_qua.append((ten, dong, True))
        for so, d in enumerate(dong, 1):
            for m in MAU_INPUT.finditer(d):
                con = m.group(1).strip()
                thu = [con] if con.endswith(".tex") else [con + ".tex", con]
                tim = [os.path.join(g, t) for g in (goc, os.path.dirname(duong)) for t in thu]
                thay = next((p for p in tim if os.path.isfile(p)), None)
                if thay:
                    them(thay, f"{ten}:{so}")
                else:
                    canh_bao.append(f"không tìm thấy file được \\input: {con} (tại {ten}:{so}); phần đó chưa được kiểm")

    them(duong_dan, None)
    return ket_qua, canh_bao


# ---------- đưa LaTeX / Markdown về văn bản thường ----------

# Thứ tự quan trọng: lệnh có nghĩa được đổi trước, rồi mới xoá các lệnh còn lại.
THAY_LATEX = [
    (re.compile(r"\\textless(?![a-zA-Z])\s*(?:\{\})?"), "<"),
    (re.compile(r"\\textgreater(?![a-zA-Z])\s*(?:\{\})?"), ">"),
    (re.compile(r"\\(?:leqslant|leq|le)(?![a-zA-Z])"), "≤"),
    (re.compile(r"\\(?:geqslant|geq|ge)(?![a-zA-Z])"), "≥"),
    (re.compile(r"\\lt(?![a-zA-Z])"), "<"),
    (re.compile(r"\\gt(?![a-zA-Z])"), ">"),
    (re.compile(r"\\(?:up)?chi(?![a-zA-Z])"), "χ"),
    (re.compile(r"\\Delta(?![a-zA-Z])\s*"), "Δ"),
    (re.compile(r"\\times(?![a-zA-Z])"), "×"),
    (re.compile(r"\\%"), "%"),
    (re.compile(r"\\\\(?:\[[^\]]*\])?"), " "),            # xuống dòng \\ hoặc \\[2pt]
    (re.compile(r"\\[()\[\]]"), " "),                     # \( \) \[ \]
    (re.compile(r"\\[,;:!> ]|~"), " "),                   # khoảng trắng của LaTeX
    (re.compile(r"\\(?:quad|qquad|enspace|thinspace|space|nobreakspace)(?![a-zA-Z])"), " "),
    # Lệnh còn lại bị xoá hẳn, không thay bằng dấu cách: \eta^2_\text{p} phải thành ^2_p
    # để "p" còn dính với dấu "_" và không bị đọc nhầm là p-value.
    (re.compile(r"\\[a-zA-Z]+\*?"), ""),
    (re.compile(r"[{}$]"), ""),
]
THAY_CHUNG = [
    (re.compile("[\u2212\u2010\u2011]"), "-"),            # dấu trừ và gạch nối Unicode
    (re.compile("[\u2A7D\u2266]"), "≤"),
    (re.compile("[\u2A7E\u2267]"), "≥"),
    (re.compile("\u00A0|\u2009|\u202F"), " "),            # các loại dấu cách không ngắt
]
MAU_NHAN_MANH_MD = re.compile(r"(?<!\w)_([^\W_]+)_(?!\w)")   # _t_(48) của Markdown


def lam_phang(dong, la_tex):
    if not la_tex:
        dong = html.unescape(dong).replace("*", "").replace("`", "")
        dong = MAU_NHAN_MANH_MD.sub(r"\1", dong)
    for mau, thay in THAY_LATEX + THAY_CHUNG:
        dong = mau.sub(thay, dong)
    return dong


# ---------- tìm thống kê ----------

DF = r"(?:\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)"
GT = r"[-\u2013]?\s*(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d{1,3}(?:\.\d{3})+,\d+|\d+[.,]\d+|\d+|[.,]\d+)(?!\d)"
TRUOC = r"(?:(?<![\w\\^])|(?<=Δ))"                 # không nằm giữa một từ; cho phép ΔF, Δχ²
CHI = r"(?:(?:χ|(?<![\w\\])[Cc]hi|(?<![\w\\])X)\s*\^?\s*[2²](?:_[^\W_]+)?|(?<![\w\\])[Cc]hi[- ][Ss]quared?)"
MAU_THONG_KE = [
    ("t", re.compile(TRUOC + rf"t\s*\(\s*(?P<df1>{DF})\s*\)\s*=\s*(?P<gt>{GT})")),
    ("F", re.compile(TRUOC + rf"F\s*\(\s*(?P<df1>{DF})\s*[,;]\s*(?P<df2>{DF})\s*\)\s*=\s*(?P<gt>{GT})")),
    ("chi2", re.compile(CHI + rf"\s*\(\s*(?P<df1>{DF})\s*(?:[,;]\s*[Nn]\s*=\s*[\d.,\s]*\d\s*)?\)\s*=\s*(?P<gt>{GT})")),
    ("r", re.compile(TRUOC + rf"r\s*\(\s*(?P<df1>{DF})\s*\)\s*=\s*(?P<gt>{GT})")),
    ("z", re.compile(TRUOC + rf"[zZ]\s*=\s*(?P<gt>{GT})")),
]
SO_P = r"(?:\d+[.,]\d+|[.,]\d+|\d+)(?:[eE]-?\d+|\s*[×x]\s*10\s*\^?\s*-?\d+)?"
MAU_P = re.compile(
    r"(?<![\w\\^])(?:[pP](?:[- ]?values?)?|[Ss]ig\.?)\s*(?P<dau><=|>=|=<|=>|[<>=≤≥])\s*(?P<p>" + SO_P + r")(?![\d])")
MAU_NS = re.compile(r"(?<![\w.])(?:ns|n\.\s?s\.?)(?!\w)")
MAU_HET_CAU = re.compile(r"[.!?]\s+(?=(\S))|\n\s*\n")
MAU_MOT_PHIA = re.compile(r"one[- ]tailed|one[- ]sided|1[- ]tailed|một (?:phía|đuôi)", re.I)
TAM_NHIN = 100          # số ký tự sau thống kê để tìm p của nó
TAM_NS = 30
# Giữa thống kê và p của nó chỉ được có ký hiệu thống kê (95% CI […], MSE = …, d = …), không có văn xuôi.
# "F(1, 196) = 0.85, but the slope was, b = 0.30, p = .004": p này là của b, không phải của F.
MAU_TU = re.compile(r"[^\W\d_]{4,}")
TU_DUOC_PHEP = {"cohen", "cohens", "hedges", "glass", "partial", "omega", "epsilon", "cramer", "cramér",
                "tailed", "sided", "with", "value", "nghĩa", "phía", "đuôi"}


def co_van_xuoi(doan):
    """Đoạn có từ nào là văn xuôi không (từ ≥ 4 chữ cái, không phải chữ viết tắt in hoa hay tên chỉ số)?"""
    return any(not (t.isupper() or t.lower() in TU_DUOC_PHEP) for t in MAU_TU.findall(doan))


def doc_so(chuoi, phay_thap_phan):
    """'2.31' / '2,31' / '.34' / '-2.31' / '1,254.31' / '1.254,31' -> (giá trị, số chữ số thập phân)."""
    s = re.sub(r"\s+", "", chuoi).replace("\u2013", "-")
    am = s.startswith("-")
    s = s.lstrip("-")
    if re.fullmatch(r"\d{1,3}(?:,\d{3})+\.\d+", s):
        s = s.replace(",", "")                              # 1,254.31: dấu phẩy ngăn hàng nghìn
    elif re.fullmatch(r"\d{1,3}(?:\.\d{3})+,\d+", s):
        s = s.replace(".", "").replace(",", ".")            # 1.254,31: kiểu Việt
    elif re.fullmatch(r"\d{1,3},\d{3}", s):
        s = s.replace(",", "." if phay_thap_phan else "")   # 2,310: tuỳ quy ước của văn bản
    elif re.fullmatch(r"\d{1,3}(?:,\d{3})+", s):
        s = s.replace(",", "")
    else:
        s = s.replace(",", ".")                             # 2,31: dấu phẩy thập phân
    le = len(s.split(".")[1]) if "." in s else 0
    v = float(s)
    return (-v if am else v), le


def doc_bac_tu_do(chuoi):
    return float(chuoi.replace(",", ""))


def doc_p(chuoi):
    """'.025' / '0,025' / '3.2e-5' / '3.2 × 10^-5' -> (giá trị, nửa bước làm tròn)."""
    s = re.sub(r"\s+", "", chuoi).replace(",", ".")
    m = re.fullmatch(r"(\d*\.?\d+)(?:[eE]|[×x]10\^?)(-?\d+)", s)
    phan, mu = (m.group(1), int(m.group(2))) if m else (s, 0)
    le = len(phan.split(".")[1]) if "." in phan else 0
    return float(phan) * 10.0 ** mu, 0.5 * 10.0 ** (mu - le)


def dung_phay_thap_phan(van_ban):
    """Văn bản viết số thập phân bằng dấu phẩy (0,05) hay dấu chấm (0.05 / .05)?"""
    phay = len(re.findall(r"(?<![\w.,])0,\d", van_ban))
    cham = len(re.findall(r"(?<![\w.,])0?\.\d", van_ban))
    return phay > cham


def tim_thong_ke(van_ban):
    """Mọi thống kê tìm được trong văn bản đã làm phẳng, theo thứ tự xuất hiện, không chồng lên nhau."""
    tim = sorted(((m.start(), loai, m) for loai, mau in MAU_THONG_KE for m in mau.finditer(van_ban)),
                 key=lambda x: x[0])
    kq, het = [], -1
    for dau, loai, m in tim:
        if dau >= het:
            kq.append((loai, m))
            het = m.end()
    return kq


def tim_p(van_ban, tu, den):
    """p đi kèm một thống kê: tìm trong phần còn lại của câu, và chỉ nhận khi giữa hai bên không có văn xuôi.

    Trả về (dấu, giá trị, nửa bước làm tròn, chữ gốc); với "ns" là (None, None, None, "ns"); không có p thì None.
    """
    doan = van_ban[tu:den]
    for m in MAU_HET_CAU.finditer(doan):
        if m.group(1) is None or m.group(1).isupper():       # hết đoạn, hoặc hết câu (chữ sau viết hoa)
            doan = doan[:m.start()]
            break
    mp, mns = MAU_P.search(doan), MAU_NS.search(doan[:TAM_NS])
    if mns and (not mp or mns.start() < mp.start()):
        return None if co_van_xuoi(doan[:mns.start()]) else (None, None, None, "ns")
    if not mp or co_van_xuoi(doan[:mp.start()]):
        return None
    dau = {"<=": "≤", "=<": "≤", ">=": "≥", "=>": "≥"}.get(mp.group("dau"), mp.group("dau"))
    gia_tri, nua = doc_p(mp.group("p"))
    chu = " ".join(mp.group("p").split())
    return dau, gia_tri, nua, f"p {dau} {chu}"


# ---------- so p tính lại với p đã ghi ----------

def khop(dau, p_ghi, nua, p_nho, p_lon):
    """p đã ghi có thể đúng không, khi p thật nằm trong [p_nho, p_lon] (do thống kê cũng đã bị làm tròn)?"""
    du = 1e-9 * max(p_lon, 1e-300)
    if dau == "=":
        return p_ghi - nua <= p_lon + du and p_ghi + nua >= p_nho - du
    if dau == "<":
        return p_nho < p_ghi
    if dau == "≤":
        return p_nho <= p_ghi + du
    if dau == ">":
        return p_lon > p_ghi
    return p_lon >= p_ghi - du            # ≥


def co_y_nghia_theo_bai(dau, p_ghi, alpha):
    """Bài báo kết luận có ý nghĩa thống kê không? None = không suy ra được từ cách ghi."""
    if dau in ("<", "≤"):
        return True if p_ghi <= alpha else None
    if dau in (">", "≥"):
        return False if p_ghi >= alpha else None
    return None if p_ghi == alpha else p_ghi < alpha


def viet_p(p):
    if p >= 0.9995:
        return "1.000"
    return f"{p:.4f}"[1:] if p >= 0.001 else f"{p:.1e}"


def danh_gia(loai, gt, le, df1, df2, bao_cao, mot_phia=False, alpha=0.05, bai_ghi_mot_phia=False):
    """Tính lại p của một thống kê và so với p ghi trong bài.

    `bao_cao` là kết quả của tim_p (None nếu bài không ghi p). `mot_phia`: người chạy khai mọi kiểm định
    t, r, z là một phía. `bai_ghi_mot_phia`: gần thống kê này bài có viết "one-tailed" / "một phía".
    Trả về (p tính lại, trạng thái, ghi chú).
    """
    if df1 <= 0 or (df2 is not None and df2 <= 0):
        return None, "KHÔNG HỢP LỆ", "bậc tự do phải lớn hơn 0"
    if loai in ("F", "chi2") and gt < 0:
        return None, "KHÔNG HỢP LỆ", f"{TEN[loai]} không thể âm"
    if loai == "r" and abs(gt) > 1:
        return None, "KHÔNG HỢP LỆ", "r phải nằm trong [-1, 1]"

    # Thống kê trong bài đã được làm tròn: 2.31 có thể là bất kỳ giá trị nào trong [2.305, 2.315].
    nua = 0.5 * 10.0 ** (-le)
    hai = tuple(tinh_p(loai, x, df1, df2) for x in (abs(gt) + nua, abs(gt), max(abs(gt) - nua, 0.0)))
    mot = tuple(p / 2.0 for p in hai)
    co_hai_kieu = loai in CO_HAI_PHIA
    chinh, phu = (mot, hai) if (mot_phia and co_hai_kieu) else (hai, mot)
    p_tinh = chinh[1]

    if bao_cao is None:
        return p_tinh, "KHÔNG CÓ p", "bài không ghi p cho thống kê này"
    dau, p_ghi, nua_p, _ = bao_cao
    if dau is None:                                         # "ns"
        dau, p_ghi, nua_p = ">", alpha, 0.0
    if p_ghi > 1:
        return p_tinh, "KHÔNG HỢP LỆ", "p không thể lớn hơn 1"

    ghi_chu = []
    if mot_phia and co_hai_kieu:
        ghi_chu.append("tính theo kiểm định một phía")
    if dau == "=" and p_ghi == 0:
        ghi_chu.append("APA: ghi p < .001 thay cho p = .000")

    if khop(dau, p_ghi, nua_p, chinh[0], chinh[2]):
        return p_tinh, "OK", "; ".join(ghi_chu)
    if co_hai_kieu and khop(dau, p_ghi, nua_p, phu[0], phu[2]):
        if bai_ghi_mot_phia and not mot_phia:
            return phu[1], "OK", "; ".join(["khớp theo kiểm định một phía (bài có ghi một phía ở gần đó)"] + ghi_chu)
        if mot_phia:
            return p_tinh, "HAI PHÍA?", f"chỉ khớp nếu là kiểm định hai phía (p hai phía = {viet_p(phu[1])})"
        return p_tinh, "MỘT PHÍA?", (f"chỉ khớp nếu là kiểm định một phía (p một phía = {viet_p(phu[1])}); "
                                     "nếu đúng vậy, bài phải nói rõ là một phía")

    theo_bai = co_y_nghia_theo_bai(dau, p_ghi, alpha)
    theo_tinh = True if chinh[2] < alpha else (False if chinh[0] >= alpha else None)
    if theo_bai is not None and theo_tinh is not None and theo_bai != theo_tinh:
        huong = "bài ghi có ý nghĩa, tính lại thì không" if theo_bai else "bài ghi không có ý nghĩa, tính lại thì có"
        return p_tinh, "LỆCH NẶNG", "; ".join([f"đổi kết luận ở α = {alpha:g}: {huong}"] + ghi_chu)
    return p_tinh, "LỆCH", "; ".join(["p ghi trong bài không khớp p tính lại"] + ghi_chu)


def kiem_van_ban(ten, dong, la_tex, mot_phia=False, alpha=0.05):
    """Kiểm mọi thống kê trong một file. Trả về danh sách kết quả."""
    van_ban = "\n".join(lam_phang(d, la_tex) for d in dong)
    phay = dung_phay_thap_phan(van_ban)
    tim = tim_thong_ke(van_ban)
    ket_qua = []
    for i, (loai, m) in enumerate(tim):
        den = min(m.end() + TAM_NHIN, tim[i + 1][1].start() if i + 1 < len(tim) else len(van_ban))
        bao_cao = tim_p(van_ban, m.end(), den)
        gt, le = doc_so(m.group("gt"), phay)
        df1 = doc_bac_tu_do(m.group("df1")) if loai != "z" else 1.0
        df2 = doc_bac_tu_do(m.group("df2")) if loai == "F" else None
        quanh = van_ban[max(m.start() - 150, 0): den + 60]
        p_tinh, trang_thai, ghi_chu = danh_gia(loai, gt, le, df1, df2, bao_cao, mot_phia, alpha,
                                               bai_ghi_mot_phia=bool(MAU_MOT_PHIA.search(quanh)))
        ket_qua.append({
            "vi_tri": f"{ten}:{van_ban.count(chr(10), 0, m.start()) + 1}",
            "loai": loai,
            "thong_ke": re.sub(r"\s+", " ", m.group(0)).strip(),
            "p_ghi": bao_cao[3] if bao_cao else "",
            "p_tinh": p_tinh,
            "trang_thai": trang_thai,
            "ghi_chu": ghi_chu,
        })
    return ket_qua


# ---------- chương trình chính ----------

def in_utf8():
    """Windows dùng bảng mã cũ khi đầu ra bị chuyển hướng, in tiếng Việt sẽ lỗi. Ép UTF-8."""
    for luong in (sys.stdout, sys.stderr):
        if hasattr(luong, "reconfigure"):
            luong.reconfigure(encoding="utf-8", errors="replace")


def main():
    in_utf8()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("duong_dan", help="file .tex chính, thư mục chứa .tex, hoặc một file văn bản (.md, .txt)")
    p.add_argument("--mot-phia", action="store_true", help="coi mọi kiểm định t, r, z là một phía")
    p.add_argument("--alpha", type=float, default=0.05, help="mức ý nghĩa để xét lỗi nặng (mặc định 0.05)")
    p.add_argument("--json", metavar="FILE", help="ghi kết quả ra file JSON")
    a = p.parse_args()
    if not 0 < a.alpha < 1:
        p.error("--alpha phải nằm giữa 0 và 1")

    try:
        ban_thao, canh_bao = doc_ban_thao(a.duong_dan)
    except OSError as e:
        print(f"Không đọc được {a.duong_dan}: {e}", file=sys.stderr)
        sys.exit(2)

    ket_qua = []
    for ten, dong, la_tex in ban_thao:
        ket_qua += kiem_van_ban(ten, dong, la_tex, a.mot_phia, a.alpha)

    print(f"# {len(ket_qua)} thống kê tìm được trong {len(ban_thao)} file ({a.duong_dan})\n")
    for cb in canh_bao:
        print(f"- Lưu ý: {cb}")
    if not ket_qua:
        print("Không tìm thấy thống kê nào viết kiểu APA, ví dụ `t(48) = 2.31, p = .025`.")
        print("Điều này KHÔNG có nghĩa là số liệu đúng: script không đọc được số trong bảng,")
        print("cũng không đọc được thống kê viết theo kiểu khác. Những chỗ đó phải kiểm bằng tay.")
    else:
        print("| Vị trí | Thống kê | p trong bài | p tính lại | Trạng thái | Ghi chú |")
        print("|---|---|---|---|---|---|")
        for k in ket_qua:
            p_tinh = "" if k["p_tinh"] is None else viet_p(k["p_tinh"])
            print(f"| {k['vi_tri']} | {k['thong_ke']} | {k['p_ghi']} | {p_tinh} | {k['trang_thai']} | {k['ghi_chu']} |")
        dem = {}
        for k in ket_qua:
            dem[k["trang_thai"]] = dem.get(k["trang_thai"], 0) + 1
        print("\n# Tổng kết")
        for tt, n in sorted(dem.items()):
            print(f"- {tt}: {n}")
        print("\nScript chỉ đọc thống kê viết trong câu. Số trong bảng phải đối chiếu với file kết quả.")

    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"thong_ke": ket_qua, "canh_bao": canh_bao}, f, ensure_ascii=False, indent=2)

    sys.exit(1 if any(k["trang_thai"] in TRANG_THAI_LOI for k in ket_qua) else 0)


if __name__ == "__main__":
    main()

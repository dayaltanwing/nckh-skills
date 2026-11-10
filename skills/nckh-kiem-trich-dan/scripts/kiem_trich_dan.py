#!/usr/bin/env python3
"""Kiểm tra file BibTeX với Crossref và (tuỳ chọn) đối chiếu \\cite trong .tex.

Chỉ dùng thư viện chuẩn của Python 3.9+.

Ví dụ:
  python3 kiem_trich_dan.py tai-lieu.bib
  python3 kiem_trich_dan.py tai-lieu.bib --tex ban-thao/main.tex --json ket-qua.json

--tex nhận một trong hai:
  - file .tex chính: đọc file đó và mọi file nó \\input / \\include (đệ quy);
  - thư mục: đọc mọi .tex bên trong, trừ bản lưu vòng trước (vong-*/) và file latexdiff (*-diff.tex).

Mã thoát: 0 = không có lỗi, 1 = có mục cần xem lại, 2 = lỗi đầu vào.
"""
import argparse
import difflib
import html
import http.client
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

UA = "nckh-skills/1.1 (citation checker)"
CROSSREF = "https://api.crossref.org/works"

# Trạng thái làm script thoát với mã 1.
TRANG_THAI_LOI = ("KHÔNG THẤY", "LỆCH", "BỊ RÚT", "THIẾU THÔNG TIN", "LỖI MẠNG", "LỖI SCRIPT", "CHƯA KIỂM")
# Sau ngần này lỗi mạng liên tiếp thì thôi gọi Crossref: mỗi lần thử lại mất vài giây,
# một file 60 mục sẽ treo nhiều phút nếu máy không có mạng.
SO_LOI_MANG_LIEN_TIEP = 3


# ---------- đọc BibTeX (đủ dùng cho file xuất từ Zotero/doi.org) ----------

def doc_bib(van_ban):
    muc = []
    i = 0
    mau = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.S)
    while True:
        m = mau.search(van_ban, i)
        if not m:
            break
        loai, khoa = m.group(1).lower(), m.group(2)
        j, sau = m.end(), 1
        while j < len(van_ban) and sau:
            if van_ban[j] == "{":
                sau += 1
            elif van_ban[j] == "}":
                sau -= 1
            j += 1
        than = van_ban[m.end(): j - 1]
        i = j
        if loai in ("comment", "string", "preamble"):
            continue
        muc.append({"loai": loai, "khoa": khoa, **doc_truong(than)})
    return muc


def doc_truong(than):
    tr = {}
    k = 0
    pat = re.compile(r"\s*([A-Za-z_-]+)\s*=\s*", re.S)
    while k < len(than):
        m = pat.match(than, k)
        if not m:
            k += 1
            continue
        ten = m.group(1).lower()
        k = m.end()
        if k >= len(than):
            break
        c = than[k]
        if c == "{":
            sau, j = 1, k + 1
            while j < len(than) and sau:
                sau += {"{": 1, "}": -1}.get(than[j], 0)
                j += 1
            gt = than[k + 1: j - 1]
        elif c == '"':
            j = k + 1
            while j < len(than) and than[j] != '"':
                j += 1
            gt = than[k + 1: j]
            j += 1
        else:
            j = k
            while j < len(than) and than[j] not in ",\n":
                j += 1
            gt = than[k:j]
        tr[ten] = re.sub(r"\s+", " ", gt).strip()
        k = j
        while k < len(than) and than[k] in ", \n\t\r":
            k += 1
    return tr


def khoa_trung(muc):
    """Khoá xuất hiện hơn một lần trong .bib (BibTeX không phân biệt hoa thường ở khoá)."""
    dem, ten = {}, {}
    for m in muc:
        k = m["khoa"].casefold()
        dem[k] = dem.get(k, 0) + 1
        ten.setdefault(k, m["khoa"])
    return sorted(ten[k] for k, n in dem.items() if n > 1)


# ---------- chuẩn hoá chuỗi để so sánh ----------

# Chữ cái mà chuẩn hoá Unicode không tách được thành "chữ gốc + dấu".
CHU_RIENG = str.maketrans({
    "đ": "d", "Đ": "D", "ø": "o", "Ø": "O", "ł": "l", "Ł": "L", "ß": "ss", "æ": "ae", "Æ": "AE",
    "œ": "oe", "Œ": "OE", "ı": "i", "ð": "d", "Ð": "D", "þ": "th", "Þ": "Th",
})
# BibTeX đôi khi viết dấu bằng lệnh LaTeX: Nguy{\~{\^e}}n, M{\"u}ller, {\DJ}{\~{\^o}}.
LENH_RA_CHU = {
    "dj": "d", "DJ": "D", "o": "o", "O": "O", "l": "l", "L": "L", "ss": "ss", "ae": "ae", "AE": "AE",
    "oe": "oe", "OE": "OE", "aa": "a", "AA": "A", "i": "i", "j": "j", "dh": "d", "DH": "D",
    "th": "th", "TH": "Th", "ohorn": "o", "OHORN": "O", "uhorn": "u", "UHORN": "U",
}
LENH_DAT_DAU = set("cvuHkdbrth")      # \c{c} \v{s} \u{a} \d{a} \h{a}…: dấu của chữ đứng sau
KY_HIEU_DAT_DAU = set("'`^\"~=.-")    # \'e \`e \^e \"u \~n…, và \- (gạch nối tuỳ ý)


def bo_latex(s):
    """Bỏ lệnh và ngoặc LaTeX, giữ lại chữ: 'Nguy{\\~{\\^e}}n' -> 'Nguyen'."""
    def lenh(m):
        ten = m.group(1)
        if ten in LENH_RA_CHU:
            return LENH_RA_CHU[ten]
        return "" if ten in LENH_DAT_DAU else " "
    s = re.sub(r"\\([a-zA-Z]+)\s*", lenh, s or "")
    s = re.sub(r"\\([^a-zA-Z])", lambda m: "" if m.group(1) in KY_HIEU_DAT_DAU else m.group(1), s)
    return s.replace("{", "").replace("}", "")


def chuan_hoa(s):
    """Chuỗi -> danh sách từ viết thường, không dấu, không ký hiệu.

    Giữ chữ của mọi hệ chữ viết. Nếu chỉ giữ a–z thì hai tiêu đề tiếng Trung hay tiếng Nga khác hẳn nhau
    đều thành chuỗi rỗng và bị coi là giống nhau hoàn toàn.
    """
    s = unicodedata.normalize("NFKD", bo_latex(s).translate(CHU_RIENG))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[\W_]", " ", s.lower()).split()


def bo_the(s):
    """Crossref đôi khi để thẻ và ký tự HTML trong tiêu đề: <i>…</i>, &amp;."""
    return html.unescape(re.sub(r"</?[A-Za-z][A-Za-z0-9:]*(?:\s[^<>]*)?/?>", " ", s or ""))


def giong(a, b):
    return difflib.SequenceMatcher(None, " ".join(chuan_hoa(a)), " ".join(chuan_hoa(b))).ratio()


def tach_ngoai_ngoac(s, mau):
    """Tách chuỗi theo biểu thức `mau`, chỉ ở những chỗ nằm ngoài ngoặc nhọn."""
    phan, sau, dau, i = [], 0, 0, 0
    while i < len(s):
        c = s[i]
        if c == "{":
            sau += 1
        elif c == "}":
            sau = max(sau - 1, 0)
        elif sau == 0:
            m = mau.match(s, i)
            if m and m.end() > i:
                phan.append(s[dau:i])
                i = dau = m.end()
                continue
        i += 1
    phan.append(s[dau:])
    return phan


# ---------- so tiêu đề, tác giả, năm ----------

MAU_VA = re.compile(r"\s+and\s+", re.I)
MAU_PHAY = re.compile(r",")
MAU_TRANG = re.compile(r"\s+")


def tac_gia_dau(truong_author):
    return tach_ngoai_ngoac(truong_author or "", MAU_VA)[0].strip()


def ten_bib(truong_author):
    """Tác giả đầu trong .bib -> (từ của phần họ theo cách BibTeX đọc, mọi từ trong tên, tên để hiển thị)."""
    dau = tac_gia_dau(truong_author)
    if not dau or dau.lower() == "others":
        return [], [], ""
    phan = tach_ngoai_ngoac(dau, MAU_PHAY)
    if len(phan) > 1:
        ho = phan[0]                                       # "Họ, Tên"
    else:
        ho = tach_ngoai_ngoac(dau, MAU_TRANG)[-1]          # "Tên Họ"; {cả cụm trong ngoặc} là một khối
    return chuan_hoa(ho), chuan_hoa(dau), bo_latex(dau).strip()


def ten_crossref(msg):
    """Tác giả đầu trong bản ghi Crossref -> (từ của phần họ, mọi từ trong tên, tên để hiển thị)."""
    ds = [a for a in (msg.get("author") or []) if isinstance(a, dict)]
    if not ds:
        return [], [], ""
    a = next((x for x in ds if x.get("sequence") == "first"), ds[0])
    ho = a.get("family") or a.get("name") or ""
    ca = " ".join(x for x in (a.get("given"), a.get("family"), a.get("name")) if x)
    return chuan_hoa(ho), chuan_hoa(ca), ca


def khop_tac_gia(ho_bib, ca_bib, ho_cr, ca_cr):
    """Tác giả đầu của hai bên có phải một người không, xét ở mức họ.

    Tên Việt được ghi theo nhiều thứ tự (Nguyễn Văn An; An, Nguyễn Văn; Nguyen, V. A.) và mỗi tạp chí
    đăng ký với Crossref một kiểu, có tạp chí lấy tên gọi làm họ. Vì thế không so "họ với họ" mà coi là
    khớp khi phần họ của bên này nằm trong tên đầy đủ của bên kia. Thiếu dữ liệu ở một bên thì bỏ qua.
    Tên không viết bằng chữ Latin cũng bỏ qua: một bên ghi 王伟, bên kia ghi Wang Wei thì không so được.
    """
    if not ho_bib or not ho_cr:
        return True
    if not all(t.isascii() for t in ho_bib + ho_cr):
        return True
    if set(ho_cr) <= set(ca_bib) or set(ho_bib) <= set(ca_cr):
        return True
    # Hai bên viết tắt ở hai đầu khác nhau ("An, N. V." và "Nguyen, V. A."): không còn từ nào chung để so,
    # nên so chữ cái đầu của cả tên. Chỉ tin khi tên có từ ba từ trở lên, để hai người khác nhau khó trùng.
    return len(ca_bib) >= 3 and sorted(t[0] for t in ca_bib) == sorted(t[0] for t in ca_cr)


def so_tieu_de(tieu_de_bib, msg):
    """So tiêu đề trong .bib với các cách Crossref ghi tiêu đề.

    Trả về (độ giống 0–1, tiêu đề Crossref giống nhất, kiểu khớp): kiểu là "day-du", hoặc "phan-dau" khi
    tiêu đề ngắn hơn trùng trọn phần đầu của tiêu đề dài hơn (một bên thiếu phụ đề). Không có tiêu đề
    nào để so thì trả về (None, "", "").
    """
    chinh = [bo_the(t) for t in (msg.get("title") or []) if t]
    phu = [bo_the(t) for t in (msg.get("subtitle") or []) if t]
    ung_vien = chinh + [f"{c}: {p}" for c in chinh for p in phu]     # nhiều nhà xuất bản tách phụ đề riêng
    ung_vien += [bo_the(t) for t in (msg.get("original-title") or []) if t]
    if not ung_vien:
        return None, "", ""
    g, uv = max(((giong(tieu_de_bib, u), u) for u in ung_vien), key=lambda x: x[0])
    if g >= 0.80:
        return g, uv, "day-du"
    tu_bib = chuan_hoa(tieu_de_bib)
    for u in ung_vien:
        ngan, dai = sorted((tu_bib, chuan_hoa(u)), key=len)
        if len(ngan) >= 4 and dai[:len(ngan)] == ngan:      # từ 4 từ trở lên mới đủ để không trùng tình cờ
            return 1.0, u, "phan-dau"
    return g, uv, "day-du"


def nam_bib(m):
    """Năm (số nguyên) của mục BibTeX, hoặc None nếu không ghi bằng số ('n.d.', 'in press')."""
    for truong in ("year", "date"):
        t = re.search(r"(?<!\d)(1[5-9]\d\d|20\d\d)(?!\d)", m.get(truong) or "")
        if t:
            return int(t.group(1))
    return None


def nam_crossref(msg):
    for k in ("published-print", "published-online", "issued", "created"):
        dp = (msg.get(k) or {}).get("date-parts") or [[None]]
        if dp and dp[0] and dp[0][0]:
            try:
                return int(dp[0][0])
            except (TypeError, ValueError):
                continue
    return None


def bi_rut(msg):
    ghi = []
    for u in msg.get("updated-by", []) or []:
        t = (u.get("type") or "").lower()
        if t:
            ghi.append(t)
    for r in (msg.get("relation") or {}).get("is-retracted-by", []) or []:
        ghi.append("retraction")
    tieu_de = " ".join(msg.get("title") or []).lower()
    if tieu_de.startswith("retracted") or tieu_de.startswith("retraction"):
        ghi.append("retraction")
    return sorted(set(ghi))


# ---------- gọi Crossref ----------

# Lỗi do đường truyền hoặc do máy chủ, không phải do nội dung file .bib.
LOI_MANG = (OSError, http.client.HTTPException, json.JSONDecodeError)


def lay_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for lan in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code in (429, 500, 502, 503, 504) and lan < 2:
                time.sleep(2 * (lan + 1))
                continue
            raise
        except urllib.error.URLError:
            if lan < 2:
                time.sleep(2 * (lan + 1))
                continue
            raise


def kiem_muc(m):
    tieu_de = m.get("title", "")
    nam = nam_bib(m)
    nam_goc = (m.get("year") or m.get("date") or "").strip()
    doi = (m.get("doi") or "").strip()
    doi = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", doi, flags=re.I)
    kq = {"khoa": m["khoa"], "loai": m["loai"], "doi": doi, "trang_thai": "", "ghi_chu": ""}

    if doi:
        dl = lay_json(f"{CROSSREF}/{urllib.parse.quote(doi, safe='/')}")
        if dl is None:
            kq["trang_thai"] = "KHÔNG THẤY"
            kq["ghi_chu"] = "DOI không tồn tại trên Crossref (có thể do DataCite đăng ký, kiểm tra tay tại doi.org)"
            return kq
        msg = dl["message"]
        van_de, luu_y = [], []

        if tieu_de:
            g, td_cr, kieu = so_tieu_de(tieu_de, msg)
            if g is None:
                luu_y.append("Crossref không ghi tiêu đề cho DOI này nên không so được tiêu đề")
            elif g < 0.80:
                van_de.append(f"tiêu đề chỉ giống {g:.0%}; Crossref: \"{td_cr[:90]}\"")
            elif kieu == "phan-dau":
                luu_y.append(f"tiêu đề chỉ khớp phần đầu (một bên thiếu phụ đề); Crossref: \"{td_cr[:90]}\"")

        nam_cr = nam_crossref(msg)
        if nam and nam_cr and abs(nam_cr - nam) > 1:
            van_de.append(f"năm {nam} ≠ Crossref {nam_cr}")
        elif nam is None and nam_cr:
            ghi_nam = f"'{nam_goc}'" if nam_goc else "để trống"
            luu_y.append(f"năm trong .bib {ghi_nam}, Crossref ghi {nam_cr}")

        ho_bib, ca_bib, ten_b = ten_bib(m.get("author"))
        ho_cr, ca_cr, ten_c = ten_crossref(msg)
        if not khop_tac_gia(ho_bib, ca_bib, ho_cr, ca_cr):
            van_de.append(f"tác giả đầu '{ten_b}' không khớp Crossref '{ten_c}'")

        rut = bi_rut(msg)
        if any("retract" in r or "withdraw" in r for r in rut):
            kq["trang_thai"] = "BỊ RÚT"
            kq["ghi_chu"] = "; ".join(rut + van_de + luu_y)
        elif van_de:
            kq["trang_thai"] = "LỆCH"
            kq["ghi_chu"] = "; ".join(van_de + luu_y)
        elif rut:
            kq["trang_thai"] = "ĐÍNH CHÍNH"
            kq["ghi_chu"] = "; ".join(["có cập nhật: " + ", ".join(rut)] + luu_y)
        else:
            kq["trang_thai"] = "OK"
            kq["ghi_chu"] = "; ".join(luu_y)
        return kq

    if not tieu_de:
        kq["trang_thai"] = "THIẾU THÔNG TIN"
        kq["ghi_chu"] = "không có DOI lẫn tiêu đề"
        return kq
    hoi = " ".join(x for x in (bo_latex(tieu_de), bo_latex(tac_gia_dau(m.get("author"))), str(nam or "")) if x.strip())
    dl = lay_json(f"{CROSSREF}?{urllib.parse.urlencode({'query.bibliographic': hoi, 'rows': 3})}")
    tot = None
    for it in (dl or {}).get("message", {}).get("items", []):
        g, _, kieu = so_tieu_de(tieu_de, it)
        if g is not None and kieu == "day-du" and (not tot or g > tot[0]):
            tot = (g, it)
    kq["trang_thai"] = "KHÔNG DOI"
    if tot and tot[0] >= 0.90:
        kq["ghi_chu"] = f"Crossref có bản khớp {tot[0]:.0%}: DOI gợi ý {tot[1].get('DOI')}"
    else:
        kq["ghi_chu"] = "không tìm thấy trên Crossref; sách/luận văn/tài liệu tiếng Việt cần kiểm tay"
    return kq


# ---------- đọc bản thảo LaTeX ----------

MAU_CHU_THICH = re.compile(r"(?<!\\)((?:\\\\)*)%.*")
MAU_INPUT = re.compile(r"\\(?:input|include|subfile)\s*\{([^{}]+)\}")


def bo_chu_thich(dong):
    """Bỏ chú thích LaTeX: từ dấu % trở đi, trừ khi đó là \\% (dấu phần trăm thật)."""
    return MAU_CHU_THICH.sub(r"\1", dong)


def doc_dong(duong):
    with open(duong, encoding="utf-8", errors="replace") as f:
        return [bo_chu_thich(d.rstrip("\n")) for d in f]


def doc_ban_thao(duong_dan):
    """Đọc bản thảo. Trả về (danh sách (tên file để hiển thị, các dòng đã bỏ chú thích), cảnh báo).

    File: đọc file đó rồi đi theo \\input / \\include như LaTeX (đường dẫn tính từ thư mục của file chính).
    Thư mục: đọc mọi .tex, bỏ qua vong-*/ (bản đã nộp vòng trước) và *-diff.tex (latexdiff), vì các file
    đó lặp lại bản thảo cũ và sẽ làm sai kết quả. Ném OSError nếu không đọc được đường dẫn gốc.
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
        return [(os.path.relpath(f, duong_dan), doc_dong(f)) for f in files], canh_bao

    goc = os.path.dirname(duong_dan) or "."
    ket_qua, da_xem = [], set()

    def them(duong, noi_goi):
        thuc = os.path.realpath(duong)
        if thuc in da_xem:
            return
        da_xem.add(thuc)
        ten = os.path.relpath(duong, goc)
        try:
            dong = doc_dong(duong)
        except OSError as e:
            if noi_goi is None:
                raise
            canh_bao.append(f"không đọc được {ten} (gọi từ {noi_goi}): {e.strerror or e}; phần đó chưa được kiểm")
            return
        ket_qua.append((ten, dong))
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


MAU_LENH_CITE = re.compile(r"\\([a-zA-Z]*[cC]ite[a-zA-Z]*)\*?")
MAU_KHOA = re.compile(r"\s*(?:\[[^\]]*\]\s*){0,2}\{([^{}]*)\}")
MAU_KHOA_DA = re.compile(r"\s*(?:\([^()]*\)){0,2}(?:\[[^\]]*\]){0,2}\{([^{}]*)\}")   # \parencites(…)(…)[…][…]{…}
MAU_KHOA_TIEP = re.compile(r"(?:\[[^\]]*\]){0,2}\{([^{}]*)\}")
# Lệnh có chữ "cite" trong tên nhưng dùng để cấu hình hoặc định nghĩa, không trích tài liệu nào.
TIEN_TO_KHONG_TRICH = ("Declare", "AtEvery", "AtNext", "new", "renew", "provide", "set")
LENH_KHONG_TRICH = {"citestyle", "bibcite", "citereset", "mancite"}


def khoa_trong_tex(ban_thao):
    """Khoá được trích trong bản thảo -> {khoá: ["file:dòng", …]}. Khoá "*" nghĩa là \\nocite{*}."""
    khoa = {}
    for ten, dong in ban_thao:
        van_ban = "\n".join(dong)      # đọc cả file một lượt: danh sách khoá dài hay bị ngắt sang dòng sau
        for m in MAU_LENH_CITE.finditer(van_ban):
            lenh = m.group(1)
            if lenh in LENH_KHONG_TRICH or lenh.startswith(TIEN_TO_KHONG_TRICH):
                continue
            so = van_ban.count("\n", 0, m.start()) + 1
            da = lenh.lower().endswith("cites")                # \parencites{a}{b}: nhiều nhóm khoá liền nhau
            nhom = (MAU_KHOA_DA if da else MAU_KHOA).match(van_ban, m.end())
            while nhom:
                for k in nhom.group(1).split(","):
                    k = k.strip()
                    if k and "\\" not in k and "#" not in k:
                        khoa.setdefault(k, []).append(f"{ten}:{so}")
                nhom = MAU_KHOA_TIEP.match(van_ban, nhom.end()) if da else None
    return khoa


def doi_chieu(muc, khoa):
    """So khoá được trích với khoá có trong .bib -> (thiếu trong .bib, có trong .bib nhưng không được trích)."""
    co = {m["khoa"] for m in muc}
    trich = {k: v for k, v in khoa.items() if k != "*"}
    thieu = {k: v for k, v in trich.items() if k not in co}
    thua = [] if "*" in khoa else sorted(co - set(trich))
    return thieu, thua


# ---------- chương trình chính ----------

def o_bang(gia_tri):
    """Một ô của bảng Markdown: dấu | hoặc xuống dòng trong tiêu đề Crossref sẽ làm vỡ bảng."""
    return " ".join(str(gia_tri).split()).replace("|", "\\|")


def kiem_tat_ca(muc):
    """Kiểm từng mục với Crossref, in dần ra bảng. Trả về danh sách kết quả."""
    ket_qua, lien_tiep = [], 0
    print("| Khoá | Trạng thái | DOI | Ghi chú |")
    print("|---|---|---|---|")
    for i, m in enumerate(muc):
        if lien_tiep >= SO_LOI_MANG_LIEN_TIEP:
            con = muc[i:]
            ket_qua += [{"khoa": x["khoa"], "loai": x["loai"], "doi": x.get("doi", ""), "trang_thai": "CHƯA KIỂM",
                         "ghi_chu": "dừng vì lỗi mạng"} for x in con]
            print(f"\nDừng gọi Crossref sau {lien_tiep} lỗi mạng liên tiếp; {len(con)} mục CHƯA KIỂM. "
                  "Kiểm tra kết nối tới api.crossref.org rồi chạy lại.")
            break
        try:
            kq = kiem_muc(m)
            lien_tiep = 0
        except LOI_MANG as e:
            kq = {"khoa": m["khoa"], "loai": m["loai"], "doi": m.get("doi", ""), "trang_thai": "LỖI MẠNG", "ghi_chu": str(e)}
            lien_tiep += 1
        except Exception as e:  # noqa: BLE001  (một mục lạ không được làm hỏng cả lượt kiểm)
            kq = {"khoa": m["khoa"], "loai": m["loai"], "doi": m.get("doi", ""), "trang_thai": "LỖI SCRIPT",
                  "ghi_chu": f"{type(e).__name__}: {e} (lỗi của script với mục này, không phải lỗi mạng; kiểm tay mục này)"}
            lien_tiep = 0
        ket_qua.append(kq)
        print(f"| {o_bang(kq['khoa'])} | {kq['trang_thai']} | {o_bang(kq['doi'])} | {o_bang(kq['ghi_chu'])} |")
        time.sleep(0.15)
    return ket_qua


def in_utf8():
    """Windows dùng bảng mã cũ khi đầu ra bị chuyển hướng, in tiếng Việt sẽ lỗi. Ép UTF-8."""
    for luong in (sys.stdout, sys.stderr):
        if hasattr(luong, "reconfigure"):
            luong.reconfigure(encoding="utf-8", errors="replace")


def main():
    in_utf8()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("bib")
    p.add_argument("--tex", help="file .tex chính (đi theo \\input) hoặc thư mục chứa .tex, để đối chiếu \\cite")
    p.add_argument("--json", help="ghi kết quả ra file JSON")
    p.add_argument("--chi-tex", action="store_true", help="chỉ đối chiếu .tex với .bib, không gọi Crossref")
    a = p.parse_args()

    try:
        with open(a.bib, encoding="utf-8-sig", errors="replace") as f:
            muc = doc_bib(f.read())
    except OSError as e:
        print(f"Không đọc được {a.bib}: {e}", file=sys.stderr)
        sys.exit(2)
    ban_thao, canh_bao = [], []
    if a.tex:
        try:
            ban_thao, canh_bao = doc_ban_thao(a.tex)
        except OSError as e:
            print(f"Không đọc được {a.tex}: {e}", file=sys.stderr)
            sys.exit(2)

    print(f"# {len(muc)} mục trong {a.bib}\n")
    if not muc:
        print("Không tìm thấy mục BibTeX nào: file rỗng, hoặc không phải file BibTeX.\n")

    trung = khoa_trung(muc)
    if trung:
        print("## Khoá trùng trong .bib (lỗi: \\cite có thể trỏ nhầm bài)")
        for k in trung:
            print(f"- `{k}`")
        print()

    ket_qua = [] if a.chi_tex else kiem_tat_ca(muc)

    thieu, thua = {}, []
    if a.tex:
        khoa = khoa_trong_tex(ban_thao)
        thieu, thua = doi_chieu(muc, khoa)
        print(f"\n# Đối chiếu .tex: {len(ban_thao)} file, {len([k for k in khoa if k != '*'])} khoá được trích")
        for cb in canh_bao:
            print(f"- Lưu ý: {cb}")
        if "*" in khoa:
            print("- Bản thảo có \\nocite{*}: mọi mục trong .bib đều được in ra danh mục tài liệu.")
        if thieu:
            print("\n## Được \\cite nhưng KHÔNG có trong .bib (lỗi)")
            for k, vt in sorted(thieu.items()):
                print(f"- `{k}` tại {', '.join(vt[:5])}")
        if thua:
            print(f"\n## Có trong .bib nhưng không được trích ({len(thua)})")
            print(", ".join(f"`{k}`" for k in thua))

    dem = {}
    for k in ket_qua:
        dem[k["trang_thai"]] = dem.get(k["trang_thai"], 0) + 1
    print("\n# Tổng kết")
    for tt, n in sorted(dem.items()):
        print(f"- {tt}: {n}")
    if trung:
        print(f"- Khoá trùng: {len(trung)}")
    if a.tex:
        print(f"- Thiếu trong .bib: {len(thieu)}")
    chua_kiem = dem.get("LỖI MẠNG", 0) + dem.get("CHƯA KIỂM", 0)
    if chua_kiem:
        print(f"\n{chua_kiem} mục CHƯA ĐƯỢC KIỂM với Crossref vì lỗi mạng. Không coi các mục đó là đạt; chạy lại khi có mạng.")

    if a.json:
        try:
            with open(a.json, "w", encoding="utf-8") as f:
                json.dump({"muc": ket_qua, "khoa_trung": trung, "thieu_trong_bib": thieu, "khong_duoc_trich": thua,
                           "canh_bao": canh_bao}, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"Không ghi được {a.json}: {e}", file=sys.stderr)
            sys.exit(2)

    loi = sum(n for tt, n in dem.items() if tt in TRANG_THAI_LOI)
    sys.exit(1 if loi or trung or thieu else 0)


if __name__ == "__main__":
    main()

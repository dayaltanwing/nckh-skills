#!/usr/bin/env python3
"""Kiểm tra file BibTeX với Crossref và (tuỳ chọn) đối chiếu \\cite trong .tex.

Chỉ dùng thư viện chuẩn của Python 3.9+.

Ví dụ:
  python3 kiem_trich_dan.py tai-lieu.bib
  python3 kiem_trich_dan.py tai-lieu.bib --tex ban-thao/ --json ket-qua.json

Mã thoát: 0 = không có lỗi, 1 = có mục cần xem lại, 2 = lỗi đầu vào.
"""
import argparse
import difflib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

UA = "nckh-skills/1.0 (citation checker)"
CROSSREF = "https://api.crossref.org/works"


# ---------- đọc BibTeX (đủ dùng cho file xuất từ Zotero/doi.org) ----------

def doc_bib(van_ban):
    muc = []
    i = 0
    while True:
        m = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.S).search(van_ban, i)
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


# ---------- tiện ích ----------

def chuan_hoa(s):
    s = re.sub(r"\\[a-zA-Z]+\s*", " ", s or "")
    s = s.replace("{", "").replace("}", "")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("đ", "d").replace("Đ", "D")
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()


def giong(a, b):
    return difflib.SequenceMatcher(None, " ".join(chuan_hoa(a)), " ".join(chuan_hoa(b))).ratio()


def ho_dau(tac_gia_bib):
    if not tac_gia_bib:
        return ""
    dau = tac_gia_bib.split(" and ")[0].strip()
    ho = dau.split(",")[0] if "," in dau else dau.split()[-1]
    w = chuan_hoa(ho)
    return w[0] if w else ""


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


def nam_crossref(msg):
    for k in ("published-print", "published-online", "issued", "created"):
        dp = (msg.get(k) or {}).get("date-parts") or [[None]]
        if dp and dp[0] and dp[0][0]:
            return dp[0][0]
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


# ---------- kiểm tra ----------

def kiem_muc(m):
    tieu_de = m.get("title", "")
    nam = m.get("year") or (m.get("date", "")[:4])
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
        td_cr = " ".join(msg.get("title") or [])
        nam_cr = nam_crossref(msg)
        ho_cr = chuan_hoa(((msg.get("author") or [{}])[0]).get("family", ""))
        g = giong(tieu_de, td_cr)
        van_de = []
        if tieu_de and g < 0.80:
            van_de.append(f"tiêu đề chỉ giống {g:.0%}; Crossref: \"{td_cr[:90]}\"")
        if nam and nam_cr and str(nam_cr) != str(nam).strip()[:4] and abs(int(nam_cr) - int(str(nam)[:4])) > 1:
            van_de.append(f"năm {nam} ≠ Crossref {nam_cr}")
        hd = ho_dau(m.get("author"))
        if hd and ho_cr and hd != ho_cr[0]:
            van_de.append(f"tác giả đầu '{hd}' ≠ Crossref '{ho_cr[0]}'")
        rut = bi_rut(msg)
        if any("retract" in r or "withdraw" in r for r in rut):
            kq["trang_thai"] = "BỊ RÚT"
            kq["ghi_chu"] = "; ".join(rut + van_de)
        elif van_de:
            kq["trang_thai"] = "LỆCH"
            kq["ghi_chu"] = "; ".join(van_de)
        elif rut:
            kq["trang_thai"] = "ĐÍNH CHÍNH"
            kq["ghi_chu"] = "có cập nhật: " + ", ".join(rut)
        else:
            kq["trang_thai"] = "OK"
        return kq

    if not tieu_de:
        kq["trang_thai"] = "THIẾU THÔNG TIN"
        kq["ghi_chu"] = "không có DOI lẫn tiêu đề"
        return kq
    q = {"query.bibliographic": f"{tieu_de} {m.get('author', '').split(' and ')[0]} {nam}", "rows": 3}
    dl = lay_json(f"{CROSSREF}?{urllib.parse.urlencode(q)}")
    tot = None
    for it in (dl or {}).get("message", {}).get("items", []):
        g = giong(tieu_de, " ".join(it.get("title") or []))
        if not tot or g > tot[0]:
            tot = (g, it)
    if tot and tot[0] >= 0.90:
        kq["trang_thai"] = "KHÔNG DOI"
        kq["ghi_chu"] = f"Crossref có bản khớp {tot[0]:.0%}: DOI gợi ý {tot[1].get('DOI')}"
    else:
        kq["trang_thai"] = "KHÔNG DOI"
        kq["ghi_chu"] = "không tìm thấy trên Crossref; sách/luận văn/tài liệu tiếng Việt cần kiểm tay"
    return kq


def khoa_trong_tex(duong_dan):
    files = []
    goc_hien_thi = duong_dan if os.path.isdir(duong_dan) else os.path.dirname(duong_dan) or "."
    if os.path.isdir(duong_dan):
        for goc, _, ds in os.walk(duong_dan):
            files += [os.path.join(goc, f) for f in ds if f.endswith(".tex")]
    else:
        files = [duong_dan]
    khoa = {}
    pat = re.compile(r"\\[a-zA-Z]*cite[a-zA-Z]*\*?(?:\[[^\]]*\]){0,2}\{([^}]*)\}")
    for f in files:
        with open(f, encoding="utf-8", errors="replace") as fh:
            for so, dong in enumerate(fh, 1):
                if dong.lstrip().startswith("%"):
                    continue
                for m in pat.finditer(dong):
                    for k in m.group(1).split(","):
                        k = k.strip()
                        if k:
                            khoa.setdefault(k, []).append(f"{os.path.relpath(f, goc_hien_thi)}:{so}")
    return khoa


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("bib")
    p.add_argument("--tex", help="file .tex hoặc thư mục chứa .tex để đối chiếu \\cite")
    p.add_argument("--json", help="ghi kết quả ra file JSON")
    p.add_argument("--chi-tex", action="store_true", help="chỉ đối chiếu .tex với .bib, không gọi Crossref")
    a = p.parse_args()

    try:
        with open(a.bib, encoding="utf-8") as f:
            muc = doc_bib(f.read())
    except OSError as e:
        print(f"Không đọc được {a.bib}: {e}", file=sys.stderr)
        sys.exit(2)
    print(f"# {len(muc)} mục trong {a.bib}\n")

    ket_qua = []
    if not a.chi_tex:
        print("| Khoá | Trạng thái | DOI | Ghi chú |")
        print("|---|---|---|---|")
        for m in muc:
            try:
                kq = kiem_muc(m)
            except Exception as e:  # noqa: BLE001
                kq = {"khoa": m["khoa"], "doi": m.get("doi", ""), "trang_thai": "LỖI MẠNG", "ghi_chu": str(e)}
            ket_qua.append(kq)
            print(f"| {kq['khoa']} | {kq['trang_thai']} | {kq['doi']} | {kq['ghi_chu']} |")
            time.sleep(0.15)

    thieu, thua = {}, []
    if a.tex:
        cite = khoa_trong_tex(a.tex)
        co = {m["khoa"] for m in muc}
        thieu = {k: v for k, v in cite.items() if k not in co}
        thua = sorted(co - set(cite))
        print(f"\n# Đối chiếu .tex: {len(cite)} khoá được trích")
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
    if a.tex:
        print(f"- Thiếu trong .bib: {len(thieu)}")

    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"muc": ket_qua, "thieu_trong_bib": thieu, "khong_duoc_trich": thua}, f, ensure_ascii=False, indent=2)

    loi = sum(n for tt, n in dem.items() if tt in ("KHÔNG THẤY", "LỆCH", "BỊ RÚT", "THIẾU THÔNG TIN", "LỖI MẠNG"))
    sys.exit(1 if loi or thieu else 0)


if __name__ == "__main__":
    main()

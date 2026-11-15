# -*- coding: utf-8 -*-
# by @嗷呜
# 农民影视 + dmxq22 / 河豚 / 小苹果 / 懂片帝 多源合并
# 每源最多加载 20 条线路，蓝光/4K/1080 优先排序
# 修复：农民影视原有 tab 名误抓集数导致线路名错乱

import concurrent.futures
import json
import re
import sys
import time
import os
import uuid
import threading
import ssl
import gzip
import zlib
import hashlib
import hmac
import random
import base64
import html as html_lib
import urllib.parse
import urllib.request
import urllib.error
import http.cookiejar
from base64 import b64decode, b64encode
from concurrent.futures import ThreadPoolExecutor, wait

import requests
from pyquery import PyQuery as pq

try:
    from Crypto.Cipher import AES, PKCS1_v1_5
    from Crypto.PublicKey import RSA
    from Crypto.Util.Padding import pad, unpad
except Exception:
    AES = PKCS1_v1_5 = RSA = None

sys.path.append('..')
from base.spider import Spider


# ============================================================
# protobuf / AES / RSA 工具
# ============================================================

def _pb_varint(v):
    v = int(v); out = bytearray()
    while v > 0x7f:
        out.append((v & 0x7f) | 0x80); v >>= 7
    out.append(v); return bytes(out)

def _pb_int(f, v): return _pb_varint(f << 3) + _pb_varint(v)

def _pb_bytes(f, v):
    if isinstance(v, str): v = v.encode("utf-8")
    return _pb_varint((f << 3) | 2) + _pb_varint(len(v)) + v

def _pb_read_varint(d, p):
    v = 0; s = 0
    while p < len(d):
        b = d[p]; p += 1
        v |= (b & 0x7f) << s
        if not b & 0x80: return v, p
        s += 7
    raise ValueError("bad varint")

def _pb_parse(d):
    fields = {}; p = 0
    while p < len(d):
        k, p = _pb_read_varint(d, p)
        f, w = k >> 3, k & 7
        if w == 0: v, p = _pb_read_varint(d, p)
        elif w == 1: v = d[p:p+8]; p += 8
        elif w == 2:
            sz, p = _pb_read_varint(d, p); v = d[p:p+sz]; p += sz
        elif w == 5: v = d[p:p+4]; p += 4
        else: raise ValueError("bad wire")
        fields.setdefault(f, []).append(v)
    return fields

def _pb_first(fields, n, d=b""):
    v = fields.get(n); return v[0] if v else d

def _pb_text(v):
    if isinstance(v, bytes): return v.decode("utf-8", "ignore")
    return str(v or "")

def _aes_ecb_enc(t, k):
    c = AES.new(k.encode("utf-8"), AES.MODE_ECB)
    return base64.b64encode(c.encrypt(pad(t.encode("utf-8"), AES.block_size))).decode()

def _aes_cbc_hex(t, k):
    kb = k.encode("utf-8"); c = AES.new(kb, AES.MODE_CBC, iv=kb)
    return c.encrypt(pad(t.encode("utf-8"), AES.block_size)).hex()

def _rsa_enc(t, k_b64):
    key = RSA.import_key(base64.b64decode(k_b64))
    return base64.b64encode(PKCS1_v1_5.new(key).encrypt(t.encode("utf-8"))).decode()

def _rand_chars(n):
    s = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    return "".join(random.choice(s) for _ in range(max(0, n - 1))) + "="


# ============================================================
# dmxq22 源
# ============================================================

class _DmxqSource:
    HOST = "https://dmxq22.com"
    UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
    _cache = {}
    _lock = threading.Lock()

    def _ctx(self):
        c = ssl.create_default_context()
        c.check_hostname = False; c.verify_mode = ssl.CERT_NONE
        return c

    def _fetch(self, url, timeout=5):
        hdr = {"User-Agent": self.UA, "Accept-Encoding": "gzip, deflate",
               "Referer": self.HOST + "/"}
        try:
            req = urllib.request.Request(url, headers=hdr)
            r = urllib.request.urlopen(req, context=self._ctx(), timeout=timeout)
            raw = r.read()
            if raw[:2] == b"\x1f\x8b":
                raw = gzip.decompress(raw)
            return 200, r.geturl(), raw.decode("utf-8", "ignore")
        except Exception:
            return 500, url, ""

    def _parse_list(self, txt):
        out, seen = [], set()
        for full, vid in re.findall(
            r'(<a[^>]+href=[\'"][^\'"]*voddetail/(\d+)\.html[\'"][^>]*>[\s\S]*?</a>)',
            txt or "", re.I):
            if vid in seen: continue
            seen.add(vid)
            start = full[:full.find('>')+1]
            name = ""
            m = re.search(r'title=[\'"]([^\'"]+)[\'"]', start)
            if m: name = m.group(1).strip()
            if not name or name == "大米星球":
                m = re.search(r'<img[^>]+alt=[\'"]([^\'"]+)[\'"]', full, re.I)
                if m: name = m.group(1).strip()
            if not name or name == "大米星球": continue
            out.append({"vod_id": vid, "vod_name": name})
        return out

    def search(self, key):
        _, _, txt = self._fetch("%s/vodsearch/%s----------1---.html" % (
            self.HOST, urllib.parse.quote(key)))
        return self._parse_list(txt)

    def get_play_lines(self, vod_id):
        _, _, txt = self._fetch("%s/voddetail/%s.html" % (self.HOST, vod_id))
        if not txt: return [], []
        tab_names = re.findall(
            r'<div[^>]+class=[\'"][^\'"]*module-tab-item[^\'"]*[\'"][^>]*>[\s\S]*?<span>([\s\S]*?)</span>',
            txt, re.I) or re.findall(
            r'<a[^>]+data-toggle=[\'"]tab[\'"][^>]*>([\s\S]*?)</a>', txt, re.I)
        play_lists = re.findall(
            r'<div[^>]+class=[\'"][^\'"]*module-play-list[^\'"]*[\'"]>([\s\S]*?)</div>',
            txt, re.I) or re.findall(
            r'<ul[^>]+class=[\'"][^\'"]*playlist[^\'"]*[\'"]>([\s\S]*?)</ul>', txt, re.I)
        froms, urls = [], []
        for i, ph in enumerate(play_lists):
            nm = tab_names[i].strip() if i < len(tab_names) else ("线路%d" % (i+1))
            nm = re.sub(r'<[^>]+>', '', nm).strip()
            eps = re.findall(
                r'<a[^>]+href=[\'"]([^\'"]*vodplay/(\d+-\d+-\d+)\.html)[\'"][^>]*>[\s\S]*?<span>([\s\S]*?)</span>',
                ph, re.I)
            if not eps:
                eps = re.findall(
                    r'<a[^>]+href=[\'"]([^\'"]*vodplay/(\d+-\d+-\d+)\.html)[\'"][^>]*>([\s\S]*?)</a>',
                    ph, re.I)
            arr = []
            for _, eid, et in eps:
                et = re.sub(r'<[^>]+>', '', et).strip() or eid
                arr.append("%s$dmxq|%s" % (et, eid))
            if arr:
                froms.append("dmxq·" + (nm or ("线路%d" % (i+1))))
                urls.append("#".join(arr))
        return froms, urls

    def resolve(self, play_id, timeout=4):
        if play_id in self._cache: return self._cache[play_id]
        page_url = "%s/vodplay/%s.html" % (self.HOST, play_id)
        code, _, txt = self._fetch(page_url, timeout=timeout)
        if code != 200 or "<" not in txt:
            return (page_url, 1, {})
        real = ""
        m = re.search(r'var\s+player_aaaa\s*=\s*\{[\s\S]*?["\']url["\']\s*:\s*["\']([^"\']+)["\']', txt)
        if m:
            real = m.group(1).strip().replace("\\/", "/")
            e = re.search(r'["\']encrypt["\']\s*:\s*(\d+)', txt)
            if e:
                if e.group(1) == "1": real = urllib.parse.unquote(real)
                elif e.group(1) == "2":
                    try: real = base64.b64decode(real).decode("utf-8", "ignore")
                    except Exception: pass
        if real.startswith("//"): real = "https:" + real
        elif real.startswith("/"): real = self.HOST + real
        low = real.lower()
        direct = bool(real) and any(x in low for x in [".m3u8", ".mp4", ".flv"]) \
                 and "?url=" not in low and "&url=" not in low
        if direct:
            if any(d in low for d in ("rrcdnbf2.com", "ifznedy1.com", "m3u8.tv")) and real.startswith("https://"):
                real = "http://" + real[8:]
            r = (real, 0, {"User-Agent": self.UA, "Referer": self.HOST + "/"})
        else:
            r = (page_url, 1, {"User-Agent": self.UA, "Referer": self.HOST + "/"})
        with self._lock:
            self._cache[play_id] = r
            if len(self._cache) > 500:
                for k in list(self._cache.keys())[:100]: self._cache.pop(k, None)
        return r


# ============================================================
# 河豚 / 小苹果 通用 proto 源
# ============================================================

class _ProtoSource:
    COMMON_KEY = "ed5fdsgucxumegqa"

    def __init__(self, cfg):
        self.cfg = cfg
        self.host = cfg.get("host", "").rstrip("/")
        self.public_key = cfg.get("publicKey", "")
        self.data_key = cfg.get("dataKey", "")
        self.data_iv = cfg.get("dataIv", "")
        self.version = cfg.get("version", "")
        self.pkg = cfg.get("pkg", "")
        self.app_name = cfg.get("appName", "")
        self.dynamic_key = ""
        self.session = requests.Session() if requests else None
        self._init_host()

    def _init_host(self):
        h = self.host
        if h.endswith((".txt", ".json")) and self.session:
            try:
                d = self.session.get(h, timeout=8).json().get("domain", "").strip().rstrip("/")
                if d: self.host = d
            except Exception: pass
        if not self.host:
            site = self.cfg.get("site", "")
            if site and self.session:
                try:
                    d = self.session.get(site, timeout=8).json().get("domain", "").strip().rstrip("/")
                    if d: self.host = d
                except Exception: pass
        if self.host:
            try: self._load_key()
            except Exception: self.dynamic_key = ""

    def _device(self):
        uid = uuid.uuid4().hex.upper()
        vapp = self.version.replace(".", "")
        return {"country": "CN", "vName": self.version, "cpuId": "MT6893Z%2FCZA", "young": 0,
                "facturer": "Xiaomi", "pkg": self.pkg, "uuid": uid,
                "resolution": "1080x2272", "mac": "02%3A00%3A00%3A00%3A00%3A00", "abid": "397",
                "model": "M2012K11AC", "plat": "android", "udid": uid, "dpi": "440", "net": "1",
                "lang": "zh", "brand": "Xiaomi", "density": "2.75", "appName": self.app_name,
                "cpu": "arm64-v8a", "chid": "10000", "carrier": "%E8%81%94%E9%80%9A",
                "_vOsCode": 30, "vOs": "11", "v": 1, "tenantId": "",
                "vApp": vapp, "device": 0, "androidID": uid.lower()[:16]}

    def _public_headers(self, protobuf=True):
        key = self.dynamic_key or self.public_key
        dev = self._device()
        ts = int(time.time() * 1000)
        rs = _rand_chars(16)
        vapp = dev.get("vApp") or "1003"
        dev["sig"] = _rsa_enc(str(ts) + rs + vapp, key)
        dev["random_str"] = rs; dev["timestamp"] = ts
        s23 = _aes_ecb_enc(str(ts) + rs, self.data_iv)
        dev["sig2"] = s23[:8]; dev["sig3"] = s23[8:]
        params = _aes_cbc_hex(json.dumps(dev, ensure_ascii=False, separators=(",", ":")), self.COMMON_KEY)
        ct = "application/x-protobuf" if protobuf else "application/json; charset=utf-8"
        ac = "application/x-protobuf" if protobuf else "application/json"
        return {"User-Agent": "okhttp/3.12.1", "Accept": ac, "Content-Type": ct,
                "publicParams": json.dumps({"paramsData": params}, ensure_ascii=False, separators=(",", ":"))}

    def _secure_body(self, params):
        ts = int(time.time() * 1000)
        r8 = _rand_chars(8); f20 = _rand_chars(20)
        q = "&".join("%s=%s" % (k, v) for k, v in params.items() if v is not None and str(v) != "")
        enc = r8 + _aes_ecb_enc(q + str(ts), self.data_key)
        return b"".join([_pb_bytes(1, enc[:20]), _pb_bytes(2, enc[20:]),
                         _pb_bytes(3, f20), _pb_int(4, ts), _pb_bytes(5, r8)])

    def _post(self, path, body):
        if not self.session or not self.host: raise RuntimeError("host missing")
        r = self.session.post(self.host + path, data=body,
                              headers=self._public_headers(True), timeout=12)
        r.raise_for_status(); return r.content

    def _api_data(self, raw):
        return _pb_first(_pb_parse(raw), 3, b"")

    def _load_key(self):
        ts = int(time.time() * 1000); rs = _rand_chars(16)
        sign = _rsa_enc(str(ts) + rs, self.public_key)
        body = b"".join([_pb_int(1, ts), _pb_bytes(2, sign), _pb_bytes(3, _rand_chars(16)),
                         _pb_bytes(4, rs), _pb_bytes(5, _rand_chars(16))])
        f = _pb_parse(self._api_data(self._post("/api/v5/find/app/zone", body)))
        self.dynamic_key = "".join(_pb_text(_pb_first(f, n)) for n in (2, 3, 4, 5))

    def _parse_cover(self, raw):
        f = _pb_parse(raw)
        return {"path": _pb_text(_pb_first(f, 1)), "thumb": _pb_text(_pb_first(f, 2))}

    def _parse_video(self, raw):
        f = _pb_parse(raw)
        return {"title": _pb_text(_pb_first(f, 2)), "path": _pb_text(_pb_first(f, 4)),
                "source": _pb_text(_pb_first(f, 9)), "source_cn": _pb_text(_pb_first(f, 10))}

    def _parse_drama(self, raw):
        f = _pb_parse(raw)
        cover = self._parse_cover(_pb_first(f, 2, b"")) if _pb_first(f, 2, b"") else {}
        return {"vod_id": str(_pb_first(f, 3, 0)),
                "vod_name": _pb_text(_pb_first(f, 5)),
                "vod_pic": cover.get("thumb") or cover.get("path", ""),
                "vod_remarks": _pb_text(_pb_first(f, 13))}

    def search(self, key):
        raw = self._post("/api/proto/v5/drama/search",
                         self._secure_body({"searchKeys": key, "page": "1", "pagesize": "5"}))
        page = _pb_parse(self._api_data(raw))
        return [self._parse_drama(v) for v in page.get(1, [])]

    def get_play_lines(self, vod_id, prefix):
        raw = self._post("/api/proto/v5/drama/getDetail",
                         self._secure_body({"id": str(vod_id)}))
        f = _pb_parse(self._api_data(raw))
        sources = {}
        for item in f.get(29, []):
            v = self._parse_video(item)
            quality = v.get("source_cn", "") or v.get("source", "") or "未知"
            src = v.get("source", "") or ""
            line = "%s (%s)" % (quality, src) if src and quality != src else quality
            path = v["path"]
            if self._is_video(path):
                token = path
            else:
                token = base64.b64encode(json.dumps(
                    {"vodPlayFrom": src, "playUrl": path},
                    ensure_ascii=False, separators=(",", ":")).encode()).decode()
            sources.setdefault(line, []).append((v["title"] or "播放") + "$" + prefix + "|" + token)
        froms = list(sources.keys()); urls = ["#".join(v) for v in sources.values()]
        return froms, urls

    @staticmethod
    def _is_video(url):
        return bool(re.search(r"(?i)\.(?:mp4|m3u8|flv|mkv|avi|ts|mov|mpd|m4a|wmv)(?:\?.*)?$", str(url)))

    def resolve(self, token):
        if self._is_video(token):
            return (token, 0, {})
        params = json.loads(base64.b64decode(token).decode("utf-8"))
        raw = self._post("/api/proto/v5/videoUsableUrl", self._secure_body(params))
        f = _pb_parse(self._api_data(raw))
        headers = {}
        for entry in f.get(6, []):
            ef = _pb_parse(entry)
            k = _pb_text(_pb_first(ef, 1)); v = _pb_text(_pb_first(ef, 2))
            if k: headers[k] = v
        return (_pb_text(_pb_first(f, 1)), 0, headers)


# ============================================================
# 懂片帝源
# ============================================================

class _DongpianSource:
    SIGN_KEY = "8b9a908a05eac640e1ee06f52acaa741bfe4ba9e004eeffdbeb635e532e06666"
    HOST = "https://dongpian17.com"
    UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36")

    def __init__(self):
        self.session = requests.Session() if requests else None
        self._logged_in = False
        if self.session:
            requests.packages.urllib3.disable_warnings()

    def _headers(self, method, path, search):
        ts = str(int(time.time() * 1000))
        nonce = os.urandom(16).hex()
        msg = "{}\n{}{}\n{}\n{}".format(method, path, search, ts, nonce)
        sign = hmac.new(self.SIGN_KEY.encode(), msg.encode(), hashlib.sha256).hexdigest()
        return {"User-Agent": self.UA, "Accept": "application/json",
                "x-ai-movie-client-name": "movie-search-frontend",
                "x-ai-movie-client-version": "1.0.0",
                "x-ai-movie-build-version": "dongpiandi-v2026.10.04.1-episode-resume-efd9a7f2e87e-web",
                "x-ai-movie-protocol-version": "2026-07-05.library-v2.playback-v1",
                "x-ai-movie-timestamp": ts, "x-ai-movie-nonce": nonce,
                "x-ai-movie-signature": sign}

    def _get(self, path, search=""):
        try:
            r = self.session.get(self.HOST + path + search,
                                 headers=self._headers("GET", path, search),
                                 timeout=10, verify=False)
            return json.loads(r.text)
        except Exception: return {}

    def _post(self, path, search, body):
        try:
            h = self._headers("POST", path, search)
            h["Content-Type"] = "application/json"
            r = self.session.post(self.HOST + path + search, headers=h, json=body,
                                  timeout=10, verify=False)
            return json.loads(r.text)
        except Exception: return {}

    def _ensure_login(self):
        if self._logged_in: return True
        try:
            path = "/v1/users/anonymous"
            h = self._headers("POST", path, ""); h["Content-Type"] = "application/json"
            r = self.session.post(self.HOST + path, headers=h,
                                  json={"anonymous_id": "web_" + uuid.uuid4().hex},
                                  timeout=10, verify=False)
            if r.status_code in (200, 201):
                self._logged_in = True; return True
        except Exception: pass
        return False

    def _resolve_line(self, ticket, retried=False):
        d = self._post("/v1/playback/resolve-line", "?view=compact", {"ticket": ticket})
        if d.get("code") == "playback_user_session_required" and not retried:
            if self._ensure_login():
                d = self._post("/v1/playback/resolve-line", "?view=compact", {"ticket": ticket})
        return d.get("line", {}) or {}

    def search(self, key):
        q = urllib.parse.quote(key)
        data = self._get("/v1/browse/catalog", "?q=%s&page=1&limit=5" % q)
        return [{"vod_id": str(c.get("id", "")),
                 "vod_name": c.get("title", "")} for c in data.get("cards", [])]

    def get_play_lines(self, vid):
        data = self._get("/v1/catalog/" + str(vid))
        card = data.get("card", data) if isinstance(data, dict) else {}
        eps = card.get("episodes") or []
        count = card.get("episode_count") or len(eps)
        if count > len(eps):
            offset = len(eps)
            while True:
                d = self._get("/v1/catalog/%s/episodes" % vid,
                              "?limit=48&offset=%d" % offset)
                e2 = d.get("episodes", []) or []
                if not e2: break
                eps.extend(e2)
                pi = d.get("episode_pagination", {}) or {}
                if not pi.get("has_more"): break
                offset += len(e2)

        tokens = []
        for ep in eps:
            title = ep.get("title") or ep.get("display_name") or "第%s集" % ep.get("number", "")
            tk = ep.get("token", "")
            if tk: tokens.append((title, tk))
        if not tokens: return [], []

        rdata = self._get("/v1/playback/resolve/" + tokens[0][1], "?view=compact")
        lines = rdata.get("line_options", []) or []
        lines = [ln for ln in lines if self._is_official(ln)]
        lines.sort(key=lambda ln: 0 if "4K" in (ln.get("label") or "").upper() else 1)
        if not lines:
            froms = ["dpd·默认"]
            urls = ["#".join("%s$dpd|%s@@" % (t, tk) for t, tk in tokens)]
            return froms, urls

        froms, urls = [], []
        used = {}
        for ln in lines:
            lid = ln.get("id", "")
            if not lid: continue
            label = ln.get("label") or "线路"
            label = self._short(label)
            if label in used:
                used[label] += 1; label = "%s%d" % (label, used[label])
            else: used[label] = 1
            froms.append("dpd·" + label)
            urls.append("#".join("%s$dpd|%s@@%s" % (t, tk, lid) for t, tk in tokens))
        return froms, urls

    def _short(self, label):
        if "官方" in label:
            base = label.split("·")[0].strip()
            for seg in reversed(base.split("-")):
                if "官方" in seg:
                    n = seg.strip()
                    if "4K" in base.upper() and not n.upper().startswith("4K"): n = "4K" + n
                    return n
        return label

    def _is_official(self, ln):
        label = ln.get("label") or ""
        prov = (ln.get("provider_id") or "").lower()
        if "官方" in label: return True
        if prov.startswith("official") or prov.startswith("bytevod"): return True
        return False

    def resolve(self, payload):
        line_id = ""
        if "@@" in payload:
            token, line_id = payload.split("@@", 1)
        else:
            token = payload
        data = self._get("/v1/playback/resolve/" + token, "?view=compact")
        lines = data.get("line_options", []) or []
        official = [ln for ln in lines if self._is_official(ln)]
        fallback = official + [ln for ln in lines if ln not in official]

        target = None
        if line_id:
            for ln in lines:
                if ln.get("id") == line_id: target = ln; break

        def _extract(ln):
            if ln.get("url_kind") == "m3u8" and not ln.get("resolve_required") and ln.get("url"):
                return ln["url"]
            tk = (ln.get("url") or "").replace("resolve://", "")
            if tk:
                line = self._resolve_line(tk)
                return line.get("url", "") or ""
            return ""

        if target is not None:
            u = _extract(target)
            if u: return (u, 0, {"User-Agent": self.UA})
        cands = [ln for ln in fallback if ln.get("selected")] or fallback
        for ln in cands:
            u = _extract(ln)
            if u: return (u, 0, {"User-Agent": self.UA})
        return ("", 1, {"User-Agent": self.UA})


# ============================================================
# 主类：农民影视 + 多源合并
# ============================================================

class Spider(Spider):

    # ==== 每源最多追加多少条线路 ====
    MAX_LINES_PER_SOURCE = 20
    # 多源并行总超时（秒）
    EXTRA_TOTAL_TIMEOUT = 10
    # 每个源最多尝试几个匹配的 vid
    MAX_MATCH_PER_SOURCE = 3

    def init(self, extend=""):
        self.host = "https://vip.wwgz.cn:5200"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'Referer': self.host + '/',
            'Accept': 'text/html'
        }
        self.cateConfig = {
            "12": [{"key": "cateId", "name": "类型", "value": [{"n": "国产剧", "v": "12"}]}],
            "4": [{"key": "cateId", "name": "类型", "value": [{"n": "动漫", "v": "4"}]}],
            "1": [{"key": "cateId", "name": "类型", "value": [{"n": "电影", "v": "1"}]}],
            "2": [{"key": "cateId", "name": "类型", "value": [{"n": "电视剧", "v": "2"}]}],
            "3": [{"key": "cateId", "name": "类型", "value": [{"n": "综艺", "v": "3"}]}],
            "26": [{"key": "cateId", "name": "类型", "value": [{"n": "短剧", "v": "26"}]}]
        }
        self.filterConfig = {}

        # ===== 多源延迟初始化 =====
        self._multi_lock = threading.Lock()
        self._multi_ready = False
        self._dmxq = None
        self._hetun = None
        self._xpg = None
        self._dpd = None
        self._play_cache = {}
        self._play_cache_lock = threading.Lock()

    def _ensure_multi_sources(self):
        """首次进入详情时初始化重源，避免阻塞首页"""
        if getattr(self, "_multi_ready", False):
            return
        with self._multi_lock:
            if getattr(self, "_multi_ready", False):
                return
            try:
                self._dmxq = _DmxqSource()
            except Exception:
                self._dmxq = None
            try:
                self._dpd = _DongpianSource()
            except Exception:
                self._dpd = None
            if requests is not None and AES is not None:
                try:
                    self._hetun = _ProtoSource({
                        "appName": "河豚",
                        "publicKey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCr8SzZhjYy+rsya1K09t8d2K50pWFoBkgUqMpKOiW+3IEVKd4eTdvg9RSOjQ82kypL6R9BnsmrS1V8s4PVDwjQbUtYhTPPC9Hz16qY7rpD6m0d2vr09/UpWQ5uOy9PR0QTrsioveZ+DIe9jc3C+zBCu/kZSY/R8stwJoiitki3gwIDAQAB",
                        "dataKey": "V04XQZNYRWN6T0JODZFIAG5CTZB3PT0=",
                        "dataIv": "OC1A06E197EF10CF3F6058CA7A803B5E",
                        "pkg": "com.djlxxl.xcydzkj",
                        "host": "https://az1-1456692500.cos.ap-guangzhou.myqcloud.com/az1.txt",
                        "version": "7.0.0.2"
                    })
                except Exception:
                    self._hetun = None
                try:
                    self._xpg = _ProtoSource({
                        "appName": "小苹果",
                        "publicKey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCduNEnfxGaLuQRk5ABzXHhPV43zi00sCHjLo8BYc+Wi6xXm2b4v0i28Sq4WlNCKhseft9fz8kO/qLr6/022o1RcuOU7e4GFL3U9WnNODwRBYSYWd+K8nqpI/tAUDmZEBGRWqjrc7x6aMl3A+xpnWkLbPCLsuhbuuUE3tv09oeOpwIDAQAB",
                        "dataKey": "S0VNDTJHOFHHCNMRAW5IV2TOS2PBPQ==",
                        "dataIv": "OC1A06E197EF10CF3F6058CA7A803B5E",
                        "pkg": "com.juechufsh.android.xpg1",
                        "site": "https://xpgandroid03-1372779881.cos.ap-beijing.myqcloud.com/app_xpg_android.txt",
                        "version": "1.0.0.3"
                    })
                except Exception:
                    self._xpg = None
            else:
                self._hetun = None
                self._xpg = None
            self._multi_ready = True

    def getName(self):
        return "农民影视"

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass

    # ==================== 首页 / 分类 ====================

    def homeContent(self, filter):
        result = {}
        classes = [
            {'type_name': '国产剧', 'type_id': '12'},
            {'type_name': '动漫', 'type_id': '4'},
            {'type_name': '电影', 'type_id': '1'},
            {'type_name': '电视剧', 'type_id': '2'},
            {'type_name': '综艺', 'type_id': '3'},
            {'type_name': '短剧', 'type_id': '26'}
        ]
        try:
            data = self.fetch(self.host, headers=self.headers).text
            doc = pq(data)
            videos = []
            seen_ids = set()
            for item in doc('.globalPicList li:has(img)').items():
                vod_id = self.host + item('a').attr('href')
                if vod_id not in seen_ids:
                    seen_ids.add(vod_id)
                    pic_url = item('img').attr('data-echo') or item('img').attr('data-src') or item('img').attr('src')
                    if pic_url and 'pic.lzzypic.com' in pic_url:
                        pic_url = pic_url.replace('https://pic.lzzypic.com', 'https://img.lzzyimg.com')
                    videos.append({
                        'vod_id': vod_id,
                        'vod_name': item('.sTit').text(),
                        'vod_pic': pic_url,
                        'vod_remarks': item('.sBottom').text()
                    })
            result['class'] = classes
            result['filters'] = self.cateConfig
            result['list'] = videos
        except Exception as e:
            print(f"首页数据获取失败: {str(e)}")
            result['class'] = classes
            result['filters'] = self.cateConfig
            result['list'] = []
        return result

    def homeVideoContent(self):
        pass

    def categoryContent(self, tid, pg, filter, extend):
        result = {}
        try:
            if tid == "4-dm":
                url = "https://www.wwgz.cn/vod-list-id-4-pg-{}-order--by-hits-class-0-year-0-letter--area-大陆-lang-.html".format(pg)
            else:
                cateId = tid
                url = f"{self.host}/vod-list-id-{cateId}-pg-{pg}.html"

            data = self.fetch(url, headers=self.headers).text
            doc = pq(data)

            videos = []
            for item in doc('.globalPicList li').items():
                pic_url = item('img').attr('data-echo') or item('img').attr('data-src') or item('img').attr('src')
                if pic_url and 'pic.lzzypic.com' in pic_url:
                    pic_url = pic_url.replace('https://pic.lzzypic.com', 'https://img.lzzyimg.com')
                videos.append({
                    'vod_id': self.host + item('a').attr('href'),
                    'vod_name': item('.sTit').text(),
                    'vod_pic': pic_url,
                    'vod_remarks': item('.sBottom').text()
                })

            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        except Exception as e:
            print(f"分类数据获取失败: {str(e)}")
            result['list'] = []
            result['page'] = pg
            result['pagecount'] = 1
            result['limit'] = 90
            result['total'] = 0
        return result

    # ==================== 线路画质权重 ====================

    @staticmethod
    def _line_weight(name):
        n = (name or "").lower()
        if "蓝光" in name or "bluray" in n or "blu-ray" in n:
            return 100
        if "4k" in n or "2160" in n or "uhd" in n:
            return 95
        if "1080" in n or "fhd" in n or "fullhd" in n or "full hd" in n:
            return 90
        if "720" in n or " hd" in n:
            return 80
        if "高清" in n:
            return 75
        if "标清" in n or " sd" in n:
            return 40
        return 50

    # ==================== 详情 ====================

    def detailContent(self, ids):
        result = {}
        try:
            url = ids[0]
            data = self.fetch(url, headers=self.headers).text
            doc = pq(data)

            play_from = []
            play_url = []

            # 修复：只取 tab 头（第一个 ul 的直接子 li），避免误抓 .numList 里的集数
            tab_ul = doc('#leftTabBox ul').eq(0)
            for tab in tab_ul.children('li').items():
                play_from.append(tab.text().strip())

            # 每个 .numList 对应一条线路
            play_lists = []
            for num_list in doc('#leftTabBox .numList').items():
                episodes = []
                for ep in list(num_list('li').items())[::-1]:
                    episodes.append(f"{ep('a').text()}${self.host}{ep('a').attr('href')}")
                play_lists.append('#'.join(episodes))
            play_url = play_lists

            # 对齐长度（防止 zip 截断错位）
            n = min(len(play_from), len(play_url))
            play_from = play_from[:n] if n > 0 else []
            play_url = play_url[:n] if n > 0 else []

            vod_name = doc('h1 a').text()

            vod = {
                'vod_id': url,
                'vod_name': vod_name,
                'vod_year': doc('span:contains("年代：")').text().replace('年代：', ''),
                'vod_area': '',
                'vod_actor': doc('.sDes:contains("主演:")').text().replace('主演:', ''),
                'vod_director': '',
                'vod_content': doc('.detail-con p').text().replace('简介:', ''),
                'vod_play_from': '$$$'.join(play_from),
                'vod_play_url': '$$$'.join(play_url)
            }

            # 追加多源线路 + 排序
            title = (vod_name or '').strip()
            if title:
                extra_froms, extra_urls = self._append_extra_sources(title)
                if extra_froms:
                    play_from.extend(extra_froms)
                    play_url.extend(extra_urls)
                    n = min(len(play_from), len(play_url))
                    play_from = play_from[:n]
                    play_url = play_url[:n]
                    if play_from:
                        pairs = list(zip(play_from, play_url))
                        pairs.sort(key=lambda p: -self._line_weight(p[0]))
                        play_from = [p[0] for p in pairs]
                        play_url = [p[1] for p in pairs]
                    vod['vod_play_from'] = '$$$'.join(play_from)
                    vod['vod_play_url'] = '$$$'.join(play_url)

            result['list'] = [vod]
        except Exception as e:
            print(f"详情数据获取失败: {str(e)}")
            result['list'] = []
        return result

    # ==================== 多源调度 ====================

    def _match_vod(self, title, results):
        t = (title or "").strip()
        if not t:
            return results or []
        exact = [r for r in results if (r.get("vod_name") or "").strip() == t]
        contain = [r for r in results
                   if t in (r.get("vod_name") or "")
                   or (r.get("vod_name") or "") in t]
        return exact or contain or (results or [])

    @staticmethod
    def _safe_call(fn, *args):
        try:
            return fn(*args)
        except Exception:
            return [], []

    def _append_extra_sources(self, title):
        """4 源并行，每源最多 20 条线路"""
        if not title:
            return [], []
        self._ensure_multi_sources()

        tasks = [
            ("dmxq",  self._extra_dmxq),
            ("hetun", lambda t: self._extra_src(self._hetun, t, "hetun")),
            ("xpg",   lambda t: self._extra_src(self._xpg,   t, "xpg")),
            ("dpd",   self._extra_dpd),
        ]
        results = {}
        pool = ThreadPoolExecutor(max_workers=len(tasks))
        futs = {}
        try:
            for tag, fn in tasks:
                futs[pool.submit(self._safe_call, fn, title)] = tag
            done, not_done = wait(list(futs.keys()), timeout=self.EXTRA_TOTAL_TIMEOUT)
            for f in done:
                try:
                    results[futs[f]] = f.result()
                except Exception:
                    results[futs[f]] = ([], [])
            for f in not_done:
                results[futs[f]] = ([], [])
        finally:
            try:
                pool.shutdown(wait=False, cancel_futures=True)
            except TypeError:
                pool.shutdown(wait=False)

        froms, urls = [], []
        for tag, _ in tasks:
            fs, us = results.get(tag, ([], []))
            froms.extend(fs)
            urls.extend(us)
        return froms, urls

    def _extra_src(self, src, title, prefix):
        if not src:
            return [], []
        try:
            res = src.search(title)
        except Exception:
            return [], []
        pool = self._match_vod(title, res)[:self.MAX_MATCH_PER_SOURCE]
        all_f, all_u = [], []
        for r in pool:
            try:
                fs, us = src.get_play_lines(r["vod_id"], prefix)
            except Exception:
                fs, us = [], []
            for f, u in zip(fs, us):
                if len(all_f) >= self.MAX_LINES_PER_SOURCE:
                    break
                all_f.append(f)
                all_u.append(u)
            if len(all_f) >= self.MAX_LINES_PER_SOURCE:
                break
        return all_f, all_u

    def _extra_dmxq(self, title):
        if not self._dmxq:
            return [], []
        try:
            res = self._dmxq.search(title)
        except Exception:
            return [], []
        pool = self._match_vod(title, res)[:self.MAX_MATCH_PER_SOURCE]
        all_f, all_u = [], []
        for r in pool:
            try:
                fs, us = self._dmxq.get_play_lines(r["vod_id"])
            except Exception:
                fs, us = [], []
            for f, u in zip(fs, us):
                if len(all_f) >= self.MAX_LINES_PER_SOURCE:
                    break
                all_f.append(f)
                all_u.append(u)
            if len(all_f) >= self.MAX_LINES_PER_SOURCE:
                break
        return all_f, all_u

    def _extra_dpd(self, title):
        if not self._dpd:
            return [], []
        try:
            res = self._dpd.search(title)
        except Exception:
            return [], []
        pool = self._match_vod(title, res)[:self.MAX_MATCH_PER_SOURCE]
        all_f, all_u = [], []
        for r in pool:
            try:
                fs, us = self._dpd.get_play_lines(r["vod_id"])
            except Exception:
                fs, us = [], []
            for f, u in zip(fs, us):
                if len(all_f) >= self.MAX_LINES_PER_SOURCE:
                    break
                all_f.append(f)
                all_u.append(u)
            if len(all_f) >= self.MAX_LINES_PER_SOURCE:
                break
        return all_f, all_u

    # ==================== 搜索 ====================

    def searchContent(self, key, quick, pg="1"):
        result = {}
        try:
            url = f"{self.host}/index.php?m=vod-search"
            data = {'wd': key}
            headers = {
                'User-Agent': self.headers['User-Agent'],
                'Referer': self.host + '/'
            }
            html = self.post(url, data=data, headers=headers).text
            doc = pq(html)

            videos = []
            for item in doc('#data_list li').items():
                pic_url = item('.lazyload').attr('data-src')
                if pic_url and 'pic.lzzypic.com' in pic_url:
                    pic_url = pic_url.replace('https://pic.lzzypic.com', 'https://img.lzzyimg.com')
                videos.append({
                    'vod_id': self.host + item('a').attr('href'),
                    'vod_name': item('.sTit').text(),
                    'vod_pic': pic_url,
                    'vod_remarks': item('.sDes').eq(-1).text()
                })

            result['list'] = videos
            result['page'] = pg
        except Exception as e:
            print(f"搜索数据获取失败: {str(e)}")
            result['list'] = []
            result['page'] = pg
        return result

    # ==================== 播放分流 ====================

    def playerContent(self, flag, id, vipFlags):
        result = {}
        raw = str(id).strip()

        # 播放缓存
        now = time.time()
        with self._play_cache_lock:
            c = self._play_cache.get(raw)
            if c and now - c[0] < 300:
                return c[1]

        try:
            # 多源前缀分流
            hit = self._dispatch_multi(raw)
            if hit is not None:
                with self._play_cache_lock:
                    self._play_cache[raw] = (now, hit)
                return hit

            # 农民影视原有逻辑
            if '@' in id:
                ids = id.split('@')
                if not ids[0]:
                    raise Exception('未找到播放地址')

                js_url = f"{self.host}/player/{ids[0]}.js"
                js_data = self.fetch(js_url, headers=self.headers).text
                jxurl = re.search(r'http.*?url=', js_data).group()

                data = self.fetch(f"{jxurl}{ids[1]}", headers=self.headers).text
                matches = re.findall(r'http.*?url=', data)

                if matches:
                    url = []
                    for i, x in enumerate(matches):
                        js = {'jx': x, 'id': ids[1]}
                        purl = f"{self.getProxyUrl()}&wdict={self.e64(json.dumps(js))}"
                        url.extend([f'线路{i + 1}', purl])
                else:
                    url = re.search(r"url='(.*?)'", data).group(1)

                if not url:
                    raise Exception('未找到播放地址')

                p = 0
            else:
                p, url = 1, id

            result['parse'] = p
            result['url'] = url
            result['header'] = self.headers
        except Exception as e:
            print(f"播放数据获取失败: {str(e)}")
            result['parse'] = 1
            result['url'] = id
            result['header'] = self.headers

        with self._play_cache_lock:
            if len(self._play_cache) > 300:
                for k in [k for k, v in self._play_cache.items() if now - v[0] >= 300]:
                    self._play_cache.pop(k, None)
            self._play_cache[raw] = (now, result)
        return result

    def _dispatch_multi(self, raw):
        """按前缀分流到多源；未命中返回 None"""
        self._ensure_multi_sources()

        if raw.startswith("dmxq|") and self._dmxq:
            pid = raw[len("dmxq|"):]
            try:
                url, pf, hd = self._dmxq.resolve(pid)
            except Exception:
                url, pf, hd = pid, 1, {}
            return {"parse": pf, "playUrl": "", "url": url, "header": hd or {}}

        if raw.startswith("hetun|") and self._hetun:
            token = raw[len("hetun|"):]
            try:
                url, pf, hd = self._hetun.resolve(token)
            except Exception:
                url, pf, hd = token, 1, {}
            return {"parse": pf, "playUrl": "", "url": url, "header": hd or {}}

        if raw.startswith("xpg|") and self._xpg:
            token = raw[len("xpg|"):]
            try:
                url, pf, hd = self._xpg.resolve(token)
            except Exception:
                url, pf, hd = token, 1, {}
            return {"parse": pf, "playUrl": "", "url": url, "header": hd or {}}

        if raw.startswith("dpd|") and self._dpd:
            payload = raw[len("dpd|"):]
            try:
                url, pf, hd = self._dpd.resolve(payload)
            except Exception:
                url, pf, hd = payload, 1, {}
            return {"parse": pf, "playUrl": "", "url": url, "header": hd or {}}

        return None

    # ==================== 代理 / 杂项 ====================

    def localProxy(self, param):
        try:
            wdict = json.loads(self.d64(param['wdict']))
            url = f"{wdict['jx']}{wdict['id']}"
            data = self.fetch(url, headers=self.headers).text
            doc = pq(data)
            html = doc('script').eq(-1).text()
            url = re.search(r'src="(.*?)"', html).group(1)
            return [302, 'text/html', None, {'Location': url}]
        except Exception as e:
            print(f"代理处理失败: {str(e)}")
            return [500, 'text/plain', str(e).encode('utf-8')]

    def liveContent(self, url):
        pass

    def e64(self, text):
        try:
            text_bytes = text.encode('utf-8')
            encoded_bytes = b64encode(text_bytes)
            return encoded_bytes.decode('utf-8')
        except Exception as e:
            print(f"Base64编码错误: {str(e)}")
            return ""

    def d64(self, encoded_text):
        try:
            encoded_bytes = encoded_text.encode('utf-8')
            decoded_bytes = b64decode(encoded_bytes)
            return decoded_bytes.decode('utf-8')
        except Exception as e:
            print(f"Base64解码错误: {str(e)}")
            return ""
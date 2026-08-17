# -*- coding: utf-8 -*-
"""Pure Python a_bogus generator.

This is a direct SM3 + RC4 + custom-base64 implementation, adapted from the
public DouyinLiveRecorder/F2-style a_bogus algorithm. It does not read mapping
tables and does not invoke Node.js.
"""
import math
import time
from urllib.parse import urlsplit


S3_TABLE = "ckdp1h4ZKsUB80/Mfvw36XIgR25+WQAlEi7NLboqYTOPuzmFjJnryx9HVGDaStCe"
S4_TABLE = "Dkdpgh2ZmsQB80/MfvV36XI1R45-WUAlEixNLwoqYTOPuzKFjJnry79HbGcaStCe"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)
DEFAULT_WINDOW_ENV = "1920|1080|1920|1040|0|30|0|0|1872|92|1920|1040|1857|92|1|24|Win32"


def _rc4_encrypt(plaintext, key):
    state = list(range(256))
    j = 0
    key_bytes = [ord(c) for c in key]
    for i in range(256):
        j = (j + state[i] + key_bytes[i % len(key_bytes)]) & 255
        state[i], state[j] = state[j], state[i]

    i = j = 0
    out = []
    for char in plaintext:
        i = (i + 1) & 255
        j = (j + state[i]) & 255
        state[i], state[j] = state[j], state[i]
        out.append(chr(state[(state[i] + state[j]) & 255] ^ ord(char)))
    return "".join(out)


def _left_rotate(value, bits):
    bits %= 32
    return ((value << bits) | (value >> (32 - bits))) & 0xFFFFFFFF


def _tj(index):
    return 0x79CC4519 if index < 16 else 0x7A879D8A


def _ff(index, x, y, z):
    return (x ^ y ^ z) & 0xFFFFFFFF if index < 16 else ((x & y) | (x & z) | (y & z)) & 0xFFFFFFFF


def _gg(index, x, y, z):
    return (x ^ y ^ z) & 0xFFFFFFFF if index < 16 else ((x & y) | (~x & z)) & 0xFFFFFFFF


class _SM3:
    def __init__(self):
        self.reset()

    def reset(self):
        self.reg = [
            0x7380166F,
            0x4914B2B9,
            0x172442D7,
            0xDA8A0600,
            0xA96F30BC,
            0x163138AA,
            0xE38DEE4D,
            0xB0FB0E4E,
        ]
        self.chunk = []
        self.size = 0

    def write(self, data):
        data = list(data.encode("utf-8")) if isinstance(data, str) else list(data)
        self.size += len(data)
        fill = 64 - len(self.chunk)
        if len(data) < fill:
            self.chunk.extend(data)
            return

        self.chunk.extend(data[:fill])
        while len(self.chunk) >= 64:
            self._compress(self.chunk)
            self.chunk = data[fill : fill + 64] if fill < len(data) else []
            fill += 64

    def sum(self, data=None):
        if data is not None:
            self.reset()
            self.write(data)

        bit_length = self.size * 8
        self.chunk.append(0x80)
        while len(self.chunk) % 64 != 56:
            self.chunk.append(0)
        for shift in range(56, -1, -8):
            self.chunk.append((bit_length >> shift) & 255)

        for offset in range(0, len(self.chunk), 64):
            self._compress(self.chunk[offset : offset + 64])

        digest = []
        for value in self.reg:
            digest.extend([(value >> 24) & 255, (value >> 16) & 255, (value >> 8) & 255, value & 255])
        self.reset()
        return digest

    def _compress(self, data):
        w = [0] * 132
        for i in range(16):
            w[i] = (data[4 * i] << 24) | (data[4 * i + 1] << 16) | (data[4 * i + 2] << 8) | data[4 * i + 3]
        for i in range(16, 68):
            value = w[i - 16] ^ w[i - 9] ^ _left_rotate(w[i - 3], 15)
            value ^= _left_rotate(value, 15) ^ _left_rotate(value, 23)
            w[i] = (value ^ _left_rotate(w[i - 13], 7) ^ w[i - 6]) & 0xFFFFFFFF
        for i in range(64):
            w[i + 68] = (w[i] ^ w[i + 4]) & 0xFFFFFFFF

        a, b, c, d, e, f, g, h = self.reg
        for i in range(64):
            ss1 = _left_rotate((_left_rotate(a, 12) + e + _left_rotate(_tj(i), i)) & 0xFFFFFFFF, 7)
            ss2 = ss1 ^ _left_rotate(a, 12)
            tt1 = (_ff(i, a, b, c) + d + ss2 + w[i + 68]) & 0xFFFFFFFF
            tt2 = (_gg(i, e, f, g) + h + ss1 + w[i]) & 0xFFFFFFFF
            d, c, b, a = c, _left_rotate(b, 9), a, tt1
            h, g, f = g, _left_rotate(f, 19), e
            e = (tt2 ^ _left_rotate(tt2, 9) ^ _left_rotate(tt2, 17)) & 0xFFFFFFFF

        for i, value in enumerate([a, b, c, d, e, f, g, h]):
            self.reg[i] ^= value


def _custom_base64(data, table):
    result = []
    for block in range(int(math.ceil(len(data) / 3))):
        offset = block * 3
        value = (
            (ord(data[offset]) if offset < len(data) else 0) << 16
            | (ord(data[offset + 1]) if offset + 1 < len(data) else 0) << 8
            | (ord(data[offset + 2]) if offset + 2 < len(data) else 0)
        )
        result.extend(
            [
                table[(value & 0xFC0000) >> 18],
                table[(value & 0x03F000) >> 12],
                table[(value & 0x000FC0) >> 6],
                table[value & 0x00003F],
            ]
        )
    return "".join(result)


def _random_prefix():
    values = [(0.123456789, [3, 45]), (0.987654321, [1, 0]), (0.555555555, [1, 5])]
    out = []
    for value, option in values:
        number = int(value * 10000)
        b1, b2 = number & 255, (number >> 8) & 255
        out.extend(
            [
                (b1 & 170) | (option[0] & 85),
                (b1 & 85) | (option[0] & 170),
                (b2 & 170) | (option[1] & 85),
                (b2 & 85) | (option[1] & 170),
            ]
        )
    return "".join(chr(byte) for byte in out)


def _bytes4(number):
    return [(number >> 24) & 255, (number >> 16) & 255, (number >> 8) & 255, number & 255]


def _rc4_body(query, user_agent, timestamp, window_env=DEFAULT_WINDOW_ENV):
    sm3 = _SM3()
    start_time = int(timestamp if timestamp is not None else time.time() * 1000)
    end_time = start_time + 100
    url_hash = sm3.sum(sm3.sum(query + "cus"))
    cus_hash = sm3.sum(sm3.sum("cus"))
    ua_hash = sm3.sum(_custom_base64(_rc4_encrypt(user_agent, "\x00\x01\x0e"), S3_TABLE))

    start = _bytes4(start_time)
    end = _bytes4(end_time)
    arg0, arg1, arg2 = _bytes4(0), _bytes4(1), _bytes4(14)
    page_id = _bytes4(110624)
    aid = 6383
    env = [ord(char) for char in window_env]

    b = {
        18: 44,
        20: start[0],
        21: start[1],
        22: start[2],
        23: start[3],
        24: int(start_time / 256 / 256 / 256 / 256) & 255,
        25: int(start_time / 256 / 256 / 256 / 256 / 256) & 255,
        26: arg0[0],
        27: arg0[1],
        28: arg0[2],
        29: arg0[3],
        30: 0,
        31: 1,
        32: arg1[0],
        33: arg1[1],
        34: arg2[0],
        35: arg2[1],
        36: arg2[2],
        37: arg2[3],
        38: url_hash[21],
        39: url_hash[22],
        40: cus_hash[21],
        41: cus_hash[22],
        42: ua_hash[23],
        43: ua_hash[24],
        44: end[0],
        45: end[1],
        46: end[2],
        47: end[3],
        48: 3,
        49: int(end_time / 256 / 256 / 256 / 256) & 255,
        50: int(end_time / 256 / 256 / 256 / 256 / 256) & 255,
        52: page_id[0],
        53: page_id[1],
        54: page_id[2],
        55: page_id[3],
        57: aid & 255,
        58: (aid >> 8) & 255,
        59: (aid >> 16) & 255,
        60: (aid >> 24) & 255,
        65: len(env) & 255,
        66: (len(env) >> 8) & 255,
        70: 0,
        71: 0,
    }
    b[72] = 0
    for key in [18, 20, 26, 30, 38, 40, 42, 21, 27, 31, 35, 39, 41, 43, 22, 28, 32, 36,
                23, 29, 33, 37, 44, 45, 46, 47, 48, 49, 50, 24, 25, 52, 53, 54, 55,
                57, 58, 59, 60, 65, 66, 70, 71]:
        b[72] ^= b[key]

    order = [18, 20, 52, 26, 30, 34, 58, 38, 40, 53, 42, 21, 27, 54, 55, 31, 35, 57,
             39, 41, 43, 22, 28, 32, 60, 36, 23, 29, 33, 37, 44, 45, 59, 46, 47, 48,
             49, 50, 24, 25, 65, 66, 70, 71]
    body = [b[key] for key in order] + env + [b[72]]
    return _rc4_encrypt("".join(chr(byte) for byte in body), "y")


def _query_from_url(url):
    parsed = urlsplit(url)
    return parsed.query or url


def generate_abogus(url, timestamp=None, user_agent=DEFAULT_USER_AGENT):
    """Generate a_bogus without Node.js, browsers, or prebuilt mapping tables."""
    user_agent = user_agent or DEFAULT_USER_AGENT
    query = _query_from_url(url)
    return _custom_base64(_random_prefix() + _rc4_body(query, user_agent, timestamp), S4_TABLE) + "="

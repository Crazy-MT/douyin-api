import 'dart:math';

class ABogusSigner {
  static const _s3Table =
      'ckdp1h4ZKsUB80/Mfvw36XIgR25+WQAlEi7NLboqYTOPuzmFjJnryx9HVGDaStCe';
  static const _s4Table =
      'Dkdpgh2ZmsQB80/MfvV36XI1R45-WUAlEixNLwoqYTOPuzKFjJnry79HbGcaStCe';
  static const _windowEnv =
      '1920|1080|1920|1040|0|30|0|0|1872|92|1920|1040|1857|92|1|24|Win32';

  String generate({
    required String query,
    required String userAgent,
    int? timestamp,
  }) {
    final ts = timestamp ?? DateTime.now().millisecondsSinceEpoch;
    final payload = '${_randomPrefix()}${_rc4Body(query, userAgent, ts)}';
    return '${_customBase64(payload, _s4Table)}=';
  }

  String _rc4Body(String query, String userAgent, int timestamp) {
    final sm3 = _SM3();
    final endTime = timestamp + 100;
    final urlHash = sm3.sum(sm3.sumString('${query}cus'));
    final cusHash = sm3.sum(sm3.sumString('cus'));
    final uaHash =
        sm3.sumString(_customBase64(_rc4(userAgent, '\x00\x01\x0e'), _s3Table));

    final start = _bytes4(timestamp);
    final end = _bytes4(endTime);
    final arg0 = _bytes4(0);
    final arg1 = _bytes4(1);
    final arg2 = _bytes4(14);
    final pageId = _bytes4(110624);
    const aid = 6383;
    final env = _windowEnv.codeUnits;

    final b = <int, int>{
      18: 44,
      20: start[0],
      21: start[1],
      22: start[2],
      23: start[3],
      24: (timestamp ~/ 0x100000000) & 255,
      25: (timestamp ~/ 0x10000000000) & 255,
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
      38: urlHash[21],
      39: urlHash[22],
      40: cusHash[21],
      41: cusHash[22],
      42: uaHash[23],
      43: uaHash[24],
      44: end[0],
      45: end[1],
      46: end[2],
      47: end[3],
      48: 3,
      49: (endTime ~/ 0x100000000) & 255,
      50: (endTime ~/ 0x10000000000) & 255,
      52: pageId[0],
      53: pageId[1],
      54: pageId[2],
      55: pageId[3],
      57: aid & 255,
      58: (aid >> 8) & 255,
      59: (aid >> 16) & 255,
      60: (aid >> 24) & 255,
      65: env.length & 255,
      66: (env.length >> 8) & 255,
      70: 0,
      71: 0,
    };
    b[72] = 0;
    for (final key in [
      18,
      20,
      26,
      30,
      38,
      40,
      42,
      21,
      27,
      31,
      35,
      39,
      41,
      43,
      22,
      28,
      32,
      36,
      23,
      29,
      33,
      37,
      44,
      45,
      46,
      47,
      48,
      49,
      50,
      24,
      25,
      52,
      53,
      54,
      55,
      57,
      58,
      59,
      60,
      65,
      66,
      70,
      71,
    ]) {
      b[72] = b[72]! ^ b[key]!;
    }

    final body = <int>[
      for (final key in [
        18,
        20,
        52,
        26,
        30,
        34,
        58,
        38,
        40,
        53,
        42,
        21,
        27,
        54,
        55,
        31,
        35,
        57,
        39,
        41,
        43,
        22,
        28,
        32,
        60,
        36,
        23,
        29,
        33,
        37,
        44,
        45,
        59,
        46,
        47,
        48,
        49,
        50,
        24,
        25,
        65,
        66,
        70,
        71,
      ])
        b[key]!,
      ...env,
      b[72]!,
    ];
    return _rc4(String.fromCharCodes(body), 'y');
  }

  String _rc4(String plaintext, String key) {
    final state = List<int>.generate(256, (i) => i);
    final keyUnits = key.codeUnits;
    var j = 0;
    for (var i = 0; i < 256; i++) {
      j = (j + state[i] + keyUnits[i % keyUnits.length]) & 255;
      final tmp = state[i];
      state[i] = state[j];
      state[j] = tmp;
    }

    var i = 0;
    j = 0;
    final output = <int>[];
    for (final unit in plaintext.codeUnits) {
      i = (i + 1) & 255;
      j = (j + state[i]) & 255;
      final tmp = state[i];
      state[i] = state[j];
      state[j] = tmp;
      output.add(state[(state[i] + state[j]) & 255] ^ unit);
    }
    return String.fromCharCodes(output);
  }

  String _customBase64(String data, String table) {
    final result = StringBuffer();
    for (var block = 0; block < (data.length / 3).ceil(); block++) {
      final offset = block * 3;
      final value = ((offset < data.length ? data.codeUnitAt(offset) : 0) <<
              16) |
          ((offset + 1 < data.length ? data.codeUnitAt(offset + 1) : 0) << 8) |
          (offset + 2 < data.length ? data.codeUnitAt(offset + 2) : 0);
      result
        ..write(table[(value & 0xFC0000) >> 18])
        ..write(table[(value & 0x03F000) >> 12])
        ..write(table[(value & 0x000FC0) >> 6])
        ..write(table[value & 0x00003F]);
    }
    return result.toString();
  }

  String _randomPrefix() {
    final output = <int>[];
    for (final item in [
      (0.123456789, [3, 45]),
      (0.987654321, [1, 0]),
      (0.555555555, [1, 5]),
    ]) {
      final number = (item.$1 * 10000).toInt();
      final byte1 = number & 255;
      final byte2 = (number >> 8) & 255;
      output
        ..add((byte1 & 170) | (item.$2[0] & 85))
        ..add((byte1 & 85) | (item.$2[0] & 170))
        ..add((byte2 & 170) | (item.$2[1] & 85))
        ..add((byte2 & 85) | (item.$2[1] & 170));
    }
    return String.fromCharCodes(output);
  }

  List<int> _bytes4(int number) => [
        (number >> 24) & 255,
        (number >> 16) & 255,
        (number >> 8) & 255,
        number & 255,
      ];
}

class _SM3 {
  _SM3() {
    reset();
  }

  late List<int> _reg;
  List<int> _chunk = [];
  var _size = 0;

  void reset() {
    _reg = [
      0x7380166F,
      0x4914B2B9,
      0x172442D7,
      0xDA8A0600,
      0xA96F30BC,
      0x163138AA,
      0xE38DEE4D,
      0xB0FB0E4E,
    ];
    _chunk = [];
    _size = 0;
  }

  List<int> sumString(String data) => sum(data.codeUnits);

  List<int> sum(List<int> data) {
    reset();
    _write(data);
    final bitLength = _size * 8;
    _chunk.add(0x80);
    while (_chunk.length % 64 != 56) {
      _chunk.add(0);
    }
    for (var shift = 56; shift >= 0; shift -= 8) {
      _chunk.add((bitLength >> shift) & 255);
    }
    for (var offset = 0; offset < _chunk.length; offset += 64) {
      _compress(_chunk.sublist(offset, offset + 64));
    }
    final digest = <int>[];
    for (final value in _reg) {
      digest
        ..add((value >> 24) & 255)
        ..add((value >> 16) & 255)
        ..add((value >> 8) & 255)
        ..add(value & 255);
    }
    reset();
    return digest;
  }

  void _write(List<int> data) {
    _size += data.length;
    var fill = 64 - _chunk.length;
    if (data.length < fill) {
      _chunk.addAll(data);
      return;
    }

    _chunk.addAll(data.take(fill));
    while (_chunk.length >= 64) {
      _compress(_chunk);
      _chunk = fill < data.length
          ? data.sublist(fill, min(fill + 64, data.length))
          : [];
      fill += 64;
    }
  }

  void _compress(List<int> data) {
    final w = List<int>.filled(132, 0);
    for (var i = 0; i < 16; i++) {
      w[i] = ((data[4 * i] << 24) |
              (data[4 * i + 1] << 16) |
              (data[4 * i + 2] << 8) |
              data[4 * i + 3]) &
          0xFFFFFFFF;
    }
    for (var i = 16; i < 68; i++) {
      var value = w[i - 16] ^ w[i - 9] ^ _leftRotate(w[i - 3], 15);
      value ^= _leftRotate(value, 15) ^ _leftRotate(value, 23);
      w[i] = (value ^ _leftRotate(w[i - 13], 7) ^ w[i - 6]) & 0xFFFFFFFF;
    }
    for (var i = 0; i < 64; i++) {
      w[i + 68] = (w[i] ^ w[i + 4]) & 0xFFFFFFFF;
    }

    var a = _reg[0];
    var b = _reg[1];
    var c = _reg[2];
    var d = _reg[3];
    var e = _reg[4];
    var f = _reg[5];
    var g = _reg[6];
    var h = _reg[7];
    for (var i = 0; i < 64; i++) {
      final ss1 = _leftRotate(
          (_leftRotate(a, 12) + e + _leftRotate(_tj(i), i)) & 0xFFFFFFFF, 7);
      final ss2 = ss1 ^ _leftRotate(a, 12);
      final tt1 = (_ff(i, a, b, c) + d + ss2 + w[i + 68]) & 0xFFFFFFFF;
      final tt2 = (_gg(i, e, f, g) + h + ss1 + w[i]) & 0xFFFFFFFF;
      d = c;
      c = _leftRotate(b, 9);
      b = a;
      a = tt1;
      h = g;
      g = _leftRotate(f, 19);
      f = e;
      e = (tt2 ^ _leftRotate(tt2, 9) ^ _leftRotate(tt2, 17)) & 0xFFFFFFFF;
    }

    final values = [a, b, c, d, e, f, g, h];
    for (var i = 0; i < values.length; i++) {
      _reg[i] = (_reg[i] ^ values[i]) & 0xFFFFFFFF;
    }
  }

  int _leftRotate(int value, int bits) {
    bits %= 32;
    return ((value << bits) | (value >> (32 - bits))) & 0xFFFFFFFF;
  }

  int _tj(int index) => index < 16 ? 0x79CC4519 : 0x7A879D8A;

  int _ff(int index, int x, int y, int z) => index < 16
      ? (x ^ y ^ z) & 0xFFFFFFFF
      : ((x & y) | (x & z) | (y & z)) & 0xFFFFFFFF;

  int _gg(int index, int x, int y, int z) =>
      index < 16 ? (x ^ y ^ z) & 0xFFFFFFFF : ((x & y) | (~x & z)) & 0xFFFFFFFF;
}

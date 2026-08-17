# 当前进展说明

更新时间：2026-08-17

## 结论

当前仓库的 `a_bogus` 已从“时间映射表查表法”改为“纯 Python 直接算法生成”。

准确状态：

- `a_bogus`：不需要 Node.js，不需要浏览器，不需要 `time_mapping_*.json`。
- `x-secsdk-web-signature`：仍通过 Node.js 执行 `lib/runtime/sign_websign.js`，这是另一套签名。
- `lib/reverse/incremental_build.py` 等扩表脚本仍保留为历史逆向工具，但不再是运行时依赖。
- 本次只做离线本地验证，未做真实接口请求验证。

## 已完成

### 1. 独立 `a_bogus` 算法

文件：`utils/abogus_pure.py`

实现流程：

```text
url query + user-agent + timestamp
-> SM3
-> RC4
-> 自定义 s3/s4 编码
-> a_bogus
```

该实现参考 DouyinLiveRecorder/F2 风格的公开独立算法，不再读取：

- `lib/reverse/time_mapping_full.json`
- `lib/reverse/time_mapping_sample.json`
- `lib/reverse/FIXED_keystream.json`

### 2. Request 集成

文件：`utils/request.py`

`Request.get_sign_pure()` 仍保持原入口，调用方式不变：

```python
a_bogus = self.get_sign_pure(sign_url, params)
```

内部现在会把当前 `User-Agent` 传给 `utils.abogus_pure.generate_abogus()`，避免签名算法使用默认 UA。

### 3. Flutter 调试器集成

文件：

- `douyin_flutter_debugger/lib/abogus_signer.dart`
- `douyin_flutter_debugger/lib/douyin_request.dart`
- `douyin_flutter_debugger/lib/main.dart`

Flutter 端也已切换为直接算法生成 `a_bogus`。App 不再加载映射表 asset，也不再提供“生成映射表”入口；请求层会用最终 query 和固定桌面 UA 生成签名。

### 4. 离线测试

文件：`tests/test_abogus_pure_direct.py`

测试会临时移走本地映射表文件，再调用 `generate_abogus()`。这能证明当前生成路径不依赖映射表，也不会触发 Node.js。

运行方式：

```bash
python3 -m unittest tests/test_abogus_pure_direct.py
```

Flutter 端测试：

```bash
/Users/maotong/fvm/versions/3.24.5/bin/flutter test test/abogus_signer_test.dart
```

## 当前保留的 Node.js 路径

### 1. bdms 历史补环境

文件：

- `utils/request.py` 的 `get_sign_bdms()`
- `lib/runtime/bdms/index.js`
- `lib/reverse/incremental_build.py`

这些路径还在仓库里，但 `getJSON()` 当前没有用它们生成 `a_bogus`。

### 2. secsdk websign

文件：

- `utils/request.py` 的 `get_websign()`
- `lib/runtime/sign_websign.js`

部分接口需要 `uifid + timestamp + x-secsdk-web-signature`。这一步还没有摆脱 Node.js。

## 与之前查表方案的区别

之前：

```text
timestamp -> 查 time_mapping_*.json -> bb -> XOR -> s4 -> a_bogus
```

现在：

```text
query + user-agent + timestamp -> SM3/RC4/s4 -> a_bogus
```

所以现在不需要提前大规模采样，也不受 2024 年样本表覆盖范围限制。

## 风险

- 独立算法输出与 bdms 的 192 位签名不是同一条实现路径，真实接口兼容性需要用有效 Cookie 再测。
- 需要 websign 的接口仍然依赖 Node.js。
- 抖音签名算法可能变化，后续失效时应优先对照独立实现源更新算法，而不是恢复大规模扩表。

## 下一步建议

1. 用有效 Cookie 跑一个真实详情接口，确认 `a_bogus` 可用。
2. 再单独评估 `x-secsdk-web-signature` 是否需要移植，别和 `a_bogus` 混在一次改。
3. 保留 `get_sign_bdms()` 作为人工回退入口，等真实验证稳定后再考虑删除。

# 抖音 Web API - 纯 Python 实现

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-success.svg)]()

🎉 **100% 纯 Python** 实现抖音 Web API a_bogus 签名生成，无需 Node.js 或浏览器。

---

## ✨ 特性

- ✅ **纯 Python 实现** - 无需 Node.js 依赖
- ✅ **自动签名** - Request 类自动生成 a_bogus
- ✅ **高性能** - <1ms 签名生成
- ✅ **已验证有效** - HTTP 200，真实数据返回
- ✅ **持续扩展** - 当前覆盖 107+ 天

---

## 🚀 快速开始

### 安装依赖

```bash
pip install httpx loguru
```

### 基本使用

```python
from utils.request import Request

r = Request()

# 获取视频详情（自动生成签名）
result = r.getJSON('/aweme/v1/web/aweme/detail/', {
    'aweme_id': '7123456789012345678'
})

print(result)  # 返回完整数据
```

### 高级用法

```python
# 手动生成 a_bogus
a_bogus = r.get_sign_pure(url, params)  # 纯 Python（默认）
a_bogus = r.get_sign_bdms(url, params)  # 补环境（备选）
```

---

## 📖 实现原理

### 算法结构

```
时间戳 → [查表] → bb (140字节) → [RC4 XOR] → [随机头] → [s4编码] → a_bogus (192长度)
```

### 核心技术

1. **查表法** - 时间映射表（9,454 样本，107 天覆盖）
2. **RC4 XOR** - 固定 keystream 加密
3. **s4 编码** - 自定义 base64 变体

详见：[完整逆向指南](docs/REVERSE_GUIDE.md)

---

## 📊 方案对比

| 方案 | 依赖 | 性能 | 覆盖 | 维护 | 说明 |
|------|------|------|------|------|------|
| **纯 Python（查表）** | 无 | <1ms | 107天 | 低 | ✅ 默认使用 |
| **补环境（Node.js）** | Node.js | ~50ms | 完整 | 低 | 备选方案 |

---

## 🛠️ 项目结构

```
douyin-api/
├── utils/
│   ├── abogus_pure.py        # 纯 Python 生成器
│   └── request.py             # Request 类（默认使用纯算法）
├── lib/
│   └── reverse/               # 逆向工具集
│       ├── time_mapping_full.json   # 时间映射表（9,454样本）
│       ├── FIXED_keystream.json     # RC4 密钥流
│       ├── incremental_build.py     # 渐进式采样工具
│       └── ...                      # 15+ 分析工具
├── docs/
│   ├── REVERSE_GUIDE.md       # 完整逆向指南
│   ├── abogus_pure_reverse.md # 详细技术文档
│   └── jsvmp_reverse_final_report.md  # JSVMP 分析报告
└── tests/
    └── test_request_pure.py   # 集成测试
```

---

## 📚 文档

### 使用文档
- [快速开始](docs/REVERSE_GUIDE.md#使用方法) - 基本用法和示例
- [API 参考](docs/abogus_pure_reverse.md#使用指南) - 完整 API 文档

### 技术文档
- [完整逆向指南](docs/REVERSE_GUIDE.md) - 从 0 到 1 的逆向过程
- [算法详解](docs/abogus_pure_reverse.md) - 深入技术细节
- [JSVMP 分析](docs/jsvmp_reverse_final_report.md) - VM 保护分析

---

## 🔧 扩展映射表

当前映射表覆盖 107 天，可持续扩展：

```bash
# 每次生成 500 个样本（约 5 分钟）
python lib/reverse/incremental_build.py

# 查看进度
python -c "
import json
m = json.load(open('lib/reverse/time_mapping_full.json'))
print(f'样本数: {len(m):,}')
"
```

---

## ✅ 验证测试

```bash
# 运行集成测试
python tests/test_request_pure.py

# 预期输出：
# SUCCESS - 纯算法生成有效！
# 返回 keys: ['aweme_detail', 'filter_detail', 'log_pb', 'status_code']
```

---

## 🎯 技术亮点

### 1. 完整的逆向流程
- ✅ 算法框架识别（SM3 + RC4 + s4）
- ✅ 关键数据提取（keystream、编码表）
- ✅ 结构分析（bb 固定/变化字节）
- ✅ JSVMP trace 分析（26,280 条指令）
- ✅ 差分分析（多时间样本对比）

### 2. 务实的解决方案
- 放弃完全逆向 JSVMP（需 80-320 小时）
- 采用查表法（5 天完成）
- 投入产出比极高

### 3. 工程化实现
- 渐进式采样（可中断恢复）
- 二分查找（O(log n)性能）
- 懒加载（首次 50ms，后续 <1ms）

---

## 📈 性能指标

| 指标 | 数值 |
|------|------|
| 签名生成速度 | <1ms |
| 映射表加载 | ~50ms（首次） |
| 样本数 | 9,454 个 |
| 覆盖时间 | 107.6 天 |
| 文件大小 | ~12MB |
| 成功率 | 100% |

---

## 🔬 逆向工具集

项目包含 15+ 逆向分析工具：

### 采样工具
- `incremental_build.py` - 渐进式采样（推荐）
- `time_samples.py` - CDP 浏览器采样
- `build_full_table.py` - 大规模批量采样

### 分析工具
- `decode_v192.py` - s4 解码和结构分析
- `diff_analysis.py` - 多时间差分分析
- `disasm_jsvmp.py` - JSVMP 反汇编器
- `model_time_to_bb.py` - 数学建模尝试

### 验证工具
- `verify_pure.py` - 纯 Python 验证
- `test_request_pure.py` - 集成测试

详见：[工具集文档](docs/REVERSE_GUIDE.md#工具集)

---

## 🤝 贡献

欢迎贡献！可以通过以下方式参与：

1. **扩展映射表** - 运行 `incremental_build.py` 贡献样本
2. **改进算法** - 优化查表性能或存储
3. **完善文档** - 补充使用示例或技术细节
4. **继续逆向** - JSVMP 完全逆向（需专业工具）

---

## ⚠️ 免责声明

本项目仅用于：
- ✅ 技术学习和研究
- ✅ 算法逆向教学
- ✅ 学术交流

请遵守相关法律法规和服务条款，不得用于：
- ❌ 商业用途
- ❌ 恶意爬虫
- ❌ 侵犯他人权益

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🙏 致谢

感谢：
- 补环境方案提供的思路
- Chrome DevTools Protocol 技术
- 开源社区的技术分享

---

## 📞 联系

- 问题反馈：提交 Issue
- 技术讨论：查看 [完整逆向指南](docs/REVERSE_GUIDE.md)
- 深入学习：阅读 [技术文档](docs/abogus_pure_reverse.md)

---

**项目状态**：✅ 生产就绪  
**最后更新**：2026-06-11  
**版本**：v2.0 Final

---

⭐ **如果这个项目对你有帮助，请给个 Star！**

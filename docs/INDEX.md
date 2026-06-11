# 文档索引

## 📚 完整文档列表

### 使用文档

| 文档 | 说明 | 适合人群 |
|------|------|----------|
| [README.md](../README.md) | 项目主页 | 所有用户 |
| [README_PURE.md](../README_PURE.md) | 纯 Python 实现详解 | 开发者 |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | 快速参考（5 步逆向） | 快速上手 |

### 技术文档

| 文档 | 说明 | 适合人群 |
|------|------|----------|
| [REVERSE_GUIDE.md](REVERSE_GUIDE.md) | 完整逆向指南（从 0 到 1） | 逆向学习者 |
| [abogus_pure_reverse.md](abogus_pure_reverse.md) | 详细技术文档 | 深度研究者 |
| [jsvmp_reverse_final_report.md](jsvmp_reverse_final_report.md) | JSVMP 分析报告 | 逆向工程师 |
| [sign_reverse_findings.md](sign_reverse_findings.md) | 早期发现记录 | 历史参考 |

### 工具文档

| 文档 | 说明 |
|------|------|
| [lib/reverse/README.md](../lib/reverse/README.md) | 逆向工具集使用说明 |
| [lib/reverse/PROJECT_STATUS.md](../lib/reverse/PROJECT_STATUS.md) | 项目完成清单 |

---

## 🎯 根据你的需求选择

### 我想快速使用
→ [README.md](../README.md) - 项目主页，快速开始

### 我想了解如何逆向
→ [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 5 步逆向总结  
→ [REVERSE_GUIDE.md](REVERSE_GUIDE.md) - 完整逆向指南

### 我想深入研究算法
→ [abogus_pure_reverse.md](abogus_pure_reverse.md) - 详细技术文档  
→ [jsvmp_reverse_final_report.md](jsvmp_reverse_final_report.md) - JSVMP 分析

### 我想扩展映射表
→ [lib/reverse/README.md](../lib/reverse/README.md) - 工具使用说明

### 我想继续完全逆向 JSVMP
→ [jsvmp_reverse_final_report.md](jsvmp_reverse_final_report.md#未来工作) - 下一步计划  
→ [REVERSE_GUIDE.md](REVERSE_GUIDE.md#未来工作) - 需要的工具和技能

---

## 📖 推荐阅读顺序

### 入门路径
1. [README.md](../README.md) - 项目概览
2. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 5 步逆向
3. 开始使用！

### 学习路径
1. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 快速了解
2. [REVERSE_GUIDE.md](REVERSE_GUIDE.md) - 完整流程
3. [abogus_pure_reverse.md](abogus_pure_reverse.md) - 深入细节
4. [jsvmp_reverse_final_report.md](jsvmp_reverse_final_report.md) - 高级分析

### 研究路径
1. [REVERSE_GUIDE.md](REVERSE_GUIDE.md) - 了解背景
2. [jsvmp_reverse_final_report.md](jsvmp_reverse_final_report.md) - JSVMP 分析
3. 查看工具源码：`lib/reverse/*.py`
4. 分析数据文件：`lib/reverse/*.json`

---

## 🔗 快速链接

### 核心文件
- [纯 Python 实现](../utils/abogus_pure.py) - 生产代码
- [Request 类](../utils/request.py) - 集成使用
- [时间映射表](../lib/reverse/time_mapping_full.json) - 9,454 样本
- [RC4 密钥流](../lib/reverse/FIXED_keystream.json) - 关键数据

### 工具脚本
- [渐进式采样](../lib/reverse/incremental_build.py) - 扩展映射表
- [差分分析](../lib/reverse/diff_analysis.py) - 多时间对比
- [JSVMP 反汇编](../lib/reverse/disasm_jsvmp.py) - VM 分析

### 测试验证
- [集成测试](../tests/test_request_pure.py) - 验证有效性
- [纯算法验证](../lib/reverse/verify_pure.py) - 单独测试

---

## 💡 常见问题

### Q: 纯 Python 方案覆盖范围有限怎么办？
A: 运行 `python lib/reverse/incremental_build.py` 扩展映射表。

### Q: 如何继续完全逆向 JSVMP？
A: 查看 [jsvmp_reverse_final_report.md](jsvmp_reverse_final_report.md#未来工作)，需要 IDA Pro 等专业工具。

### Q: 查表法性能如何？
A: 首次 ~50ms（加载映射表），后续 <1ms。

### Q: 算法升级怎么办？
A: 查表法：重新采样；补环境：自动跟随。

---

**最后更新**：2026-06-11  
**文档版本**：v2.0 Final

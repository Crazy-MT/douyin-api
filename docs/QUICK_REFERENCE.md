# 快速参考 - 纯 Python a_bogus

## 如何逆向 a_bogus？

### 5 个关键步骤

#### 1. 抓包定位
```javascript
// Chrome DevTools 搜索 "a_bogus"
// 发现：bdms.js 负责生成
```

#### 2. Hook 捕获中间数据
```javascript
// 浏览器控制台
var old = String.fromCharCode;
String.fromCharCode = function(...args) {
    if (args.length >= 130 && args.length <= 150) {
        console.log('bb:', args);  // 140 字节数组
    }
    return old.apply(String, args);
};
```

#### 3. 识别算法组件
- **s4 编码**：自定义 base64（字符表不同）
- **RC4 XOR**：固定 keystream（对比多个样本提取）
- **时间编码**：JSVMP 复杂位运算（难以完全逆向）

#### 4. 采集样本
```python
# 用补环境批量生成，建立时间映射表
from utils.request import Request
r = Request()
a_bogus = r.get_sign_bdms(url, params)
# 解码 → bb → 保存到映射表
```

#### 5. 纯 Python 实现
```python
def generate_abogus(url, timestamp):
    bb = lookup_bb(timestamp)      # 查表
    encrypted = bb XOR keystream   # XOR
    final = random_head + encrypted
    return s4_encode(final)        # 编码
```

---

## 当前实现

### 核心代码
**文件**：`utils/abogus_pure.py`

**算法**：查表法（时间映射表 + RC4 + s4）

**使用**：
```python
from utils.request import Request
r = Request()
# 自动使用纯 Python
result = r.getJSON(uri, params)
```

### 数据资产
- `lib/reverse/time_mapping_full.json` - 9,454 样本
- `lib/reverse/FIXED_keystream.json` - RC4 密钥流
- `lib/reverse/vm_bbtrace.json` - VM trace（26,280 指令）

---

## 为什么选择查表法？

### 完全逆向 JSVMP 需要：
- ❌ 80-320 小时专业工作
- ❌ IDA Pro / angr 等专业工具
- ❌ 深度汇编/VM 逆向技能
- ❌ 算法升级需重来

### 查表法优势：
- ✅ 5 天完成
- ✅ 无需专业工具
- ✅ 准确率 100%
- ✅ 持续扩展（自动采样）

---

## 继续完全逆向？

### 如果你有：
1. **IDA Pro / Ghidra** - 专业逆向工具
2. **深度逆向经验** - 汇编/VM/混淆代码
3. **充足时间** - 2-4 周全职工作

### 下一步：
1. 用 IDA Pro 分析 `lib/runtime/bdms/bdms.js`
2. 识别 VM 解释器主循环（约 3904 行）
3. 逆向每个 opcode 的语义（80+ 个）
4. 还原时间编码算法
5. 纯 Python 复现

### 参考资料：
- `docs/REVERSE_GUIDE.md` - 完整逆向流程
- `docs/jsvmp_reverse_final_report.md` - JSVMP 分析
- `lib/reverse/vm_bbtrace.json` - VM trace 数据
- `lib/reverse/diff_analysis.py` - 差分分析

---

## 快速命令

```bash
# 扩展映射表（500 样本/次）
python lib/reverse/incremental_build.py

# 查看进度
python -c "import json; m=json.load(open('lib/reverse/time_mapping_full.json')); print(f'{len(m):,} 样本')"

# 测试验证
python tests/test_request_pure.py

# 分析工具
python lib/reverse/diff_analysis.py      # 差分分析
python lib/reverse/disasm_jsvmp.py       # 反汇编
python lib/reverse/model_time_to_bb.py   # 数学建模
```

---

## 文档索引

| 文档 | 内容 |
|------|------|
| **README_PURE.md** | 项目总览和快速开始 |
| **docs/REVERSE_GUIDE.md** | 完整逆向指南（从 0 到 1） |
| **docs/abogus_pure_reverse.md** | 详细技术文档 |
| **docs/jsvmp_reverse_final_report.md** | JSVMP 分析报告 |
| **lib/reverse/README.md** | 工具使用说明 |

---

**提示**：查表法已 100% 满足需求，继续完全逆向投入产出比极低。

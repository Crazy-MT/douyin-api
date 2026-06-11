# JSVMP 完全逆向 - 实施路线图

## 当前状态

### 已完成（30%）
- ✅ 算法框架识别（SM3 + RC4 + s4）
- ✅ RC4 keystream 提取（132 字节）
- ✅ bb 结构分析（24 固定 + 113 变化字节）
- ✅ VM trace 采集（26,280 条指令）
- ✅ 差分分析（5 个不同时间样本）
- ✅ 模式识别（发现循环结构）
- ✅ 动态插桩尝试（bdms.js 混淆太强）

### 未完成（70%）
- ❌ VM 指令语义（80+ opcodes）
- ❌ 时间编码算法（115 字节生成规则）
- ❌ 变长结构序列化器
- ❌ 纯 Python 完整实现

---

## 🎯 完全逆向实施步骤

### 阶段 1：工具准备（1-2 天）

#### 必需工具
1. **IDA Pro 或 Ghidra**
   - 用途：反汇编 JavaScript VM
   - 许可证：IDA Pro ~$1,000+
   - 替代：Ghidra（免费，学习曲线陡）

2. **Node.js Debugger**
   - Chrome DevTools Protocol
   - 动态断点追踪

3. **Python 符号执行工具**
   - angr 或 Z3
   - 用于约束求解

#### 安装
```bash
# IDA Pro（需购买）
# 或 Ghidra
brew install ghidra  # Mac
# 或下载 https://ghidra-sre.org/

# Python 工具
pip install angr z3-solver
```

### 阶段 2：VM 解释器定位（2-3 天）

#### 步骤
1. **定位 VM 主循环**
   ```bash
   # 在 IDA/Ghidra 中打开 lib/runtime/bdms/bdms.js
   # 搜索关键字：switch, case, opcode
   ```

2. **识别指令分发表**
   - 位置：约 3904 行
   - 结构：`switch (opcode) { case 0: ... }`

3. **提取 opcode 列表**
   ```python
   # 从 bdms.js 提取所有 case 分支
   opcodes = [0, 2, 3, 5, 6, 7, ...]  # 80+ 个
   ```

### 阶段 3：逐个 opcode 逆向（2-4 周）

#### 每个 opcode 的逆向流程

**示例：opcode 74**

1. **定位代码**
   ```javascript
   case 74:
       // IDA 中查看这段代码的反汇编
   ```

2. **动态调试**
   ```bash
   node --inspect-brk lib/runtime/bdms/index.js
   # Chrome DevTools → 设置断点在 case 74
   # 观察寄存器/栈变化
   ```

3. **推断语义**
   ```python
   # 根据观察推断操作
   # opcode 74: PUSH value
   # opcode 38: ADD
   # opcode 12: STORE array[index]
   ```

4. **验证**
   ```python
   # 用 Python 模拟这个 opcode
   def op_74(stack, args):
       stack.append(args[1])
   
   # 对比 VM trace 验证
   ```

#### 预计工作量
- 简单 opcode（PUSH/POP）：30 分钟
- 中等 opcode（运算）：1-2 小时
- 复杂 opcode（分支/循环）：2-4 小时
- **总计：80 opcodes × 2 小时 = 160 小时（4 周）**

### 阶段 4：还原算法（1-2 周）

#### 步骤

1. **重建 VM 解释器**
   ```python
   class JSVMP:
       def __init__(self, bytecode):
           self.bytecode = bytecode
           self.stack = []
           self.memory = {}
       
       def execute(self):
           for ins in self.bytecode:
               opcode = ins[0]
               if opcode == 74:
                   self.op_push(ins[1])
               elif opcode == 38:
                   self.op_add()
               # ... 80+ opcodes
   ```

2. **追踪时间戳流**
   ```python
   # 从 VM trace 找出时间戳的传播
   timestamp = 1700000000000
   # → VM 中间变量 X
   # → 位运算 Y
   # → 写入 bb[20]
   ```

3. **提取算法**
   ```python
   def generate_bb(timestamp):
       # 根据 VM 执行还原的算法
       bb = bytearray(140)
       
       # 时间字节（从 VM trace 还原）
       t_high = timestamp >> 32
       t_mid = (timestamp >> 16) & 0xFFFF
       t_low = timestamp & 0xFFFF
       
       # 复杂的位运算...
       bb[20] = (t_low ^ 0xAA) & 0xFF
       bb[21] = ...
       
       return bb
   ```

4. **验证**
   ```python
   # 对比真实 bb
   generated = generate_bb(1700000000000)
   real = [171, 85, 42, ...]
   
   assert generated == real
   ```

### 阶段 5：纯 Python 实现（3-5 天）

```python
# utils/abogus_jsvmp.py
def generate_abogus_jsvmp(url, timestamp):
    """完全逆向版本（无需映射表）"""
    # 1. 时间编码（从 VM 还原）
    bb = encode_time(timestamp)
    
    # 2. query 处理（SM3）
    query_hash = sm3(url_query)
    bb[38:70] = query_hash
    
    # 3. XOR 校验
    bb[72] = xor_checksum(bb)
    
    # 4. RC4 XOR
    encrypted = rc4_xor(bb, FIXED_KEYSTREAM)
    
    # 5. s4 编码
    return s4_encode(random_head(4) + encrypted)
```

---

## 📊 工作量总结

| 阶段 | 工作量 | 技能要求 |
|------|--------|----------|
| 工具准备 | 1-2 天 | 中级 |
| VM 定位 | 2-3 天 | 高级 |
| opcode 逆向 | 2-4 周 | 专家级 |
| 算法还原 | 1-2 周 | 专家级 |
| Python 实现 | 3-5 天 | 高级 |
| **总计** | **6-8 周** | **逆向工程专家** |

---

## 💰 成本估算

### 时间成本
- 全职工作：6-8 周
- 业余时间：3-6 个月

### 工具成本
- IDA Pro：$1,000+
- 或 Ghidra：免费（学习成本高）

### 风险成本
- 算法升级：前功尽弃
- 概率：50%（半年内）

### 机会成本
- 查表法已满足需求
- 投入产出比：**极低**

---

## 🤔 是否值得继续？

### 查表法方案
| 维度 | 评分 |
|------|------|
| 完成度 | 100% ✅ |
| 可用性 | 100% ✅ |
| 性能 | 优秀 ✅ |
| 维护成本 | 低 ✅ |
| 投入时间 | 5 天 ✅ |

### 完全逆向方案
| 维度 | 评分 |
|------|------|
| 完成度 | 30% ⚠️ |
| 可用性 | 0% ❌ |
| 性能 | 极优 ⚠️ |
| 维护成本 | 极高 ❌ |
| 投入时间 | 6-8 周 ❌ |
| 风险 | 极高 ❌ |

---

## 🎯 建议

### 如果你有：
- ✅ IDA Pro 许可证
- ✅ 6-8 周空闲时间
- ✅ 深度逆向工程经验
- ✅ 强烈的学习动机

→ **可以尝试完全逆向**（作为技术挑战）

### 如果你需要：
- ✅ 快速可用的方案
- ✅ 生产环境部署
- ✅ 低维护成本

→ **保持查表法方案**（已 100% 满足需求）

---

## 📚 参考资料

### 学习资源
- [IDA Pro Book](https://nostarch.com/idapro2) - IDA Pro 权威指南
- [Practical Malware Analysis](https://nostarch.com/malware) - 逆向工程基础
- [angr Documentation](https://docs.angr.io/) - 符号执行

### 类似案例
- [V8 JavaScript 引擎逆向](https://doar-e.github.io/blog/2019/01/28/introduction-to-spidermonkey-exploitation/)
- [Ollvm 混淆还原](https://github.com/obfuscator-llvm/obfuscator)

---

**最终建议：接受查表法，结束 JSVMP 逆向。**

投入产出比极低，且算法随时可能升级。

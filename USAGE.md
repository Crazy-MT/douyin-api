# 使用说明

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install httpx loguru
```

### 2. 配置 Cookie

**方法 1：自动导入（推荐）**

```python
from utils.request import Request

# 首次运行会提示输入 cookie
r = Request()
```

按提示从浏览器复制 cookie：
1. 打开 https://www.douyin.com
2. F12 打开开发者工具 → Network → 找到任意请求
3. 复制 Request Headers 中的 `Cookie:` 后面的完整字符串
4. 粘贴到终端

Cookie 会自动保存到 `config/cookie.json`，下次直接使用。

**方法 2：手动创建文件**

创建 `config/cookie.json`：
```json
{
  "ttwid": "你的ttwid",
  "s_v_web_id": "你的s_v_web_id",
  "sessionid": "你的sessionid"
}
```

### 3. 生成映射表（首次使用）

项目自带 100 个样本的示例映射表（覆盖 28 小时）。

**扩展到更大范围**：
```bash
# 每次生成 500 个样本（约 5 分钟）
python lib/reverse/incremental_build.py

# 重复运行多次累积样本
```

查看进度：
```bash
python -c "
import json
m = json.load(open('lib/reverse/time_mapping_full.json'))
print(f'样本数: {len(m):,}')
"
```

### 4. 使用

```python
from utils.request import Request

r = Request()

# 自动使用纯 Python 生成 a_bogus
result = r.getJSON('/aweme/v1/web/aweme/detail/', {
    'aweme_id': '7123456789012345678'
})

print(result)
```

---

## 📝 常见问题

### Q: Cookie 从哪里获取？

**A**: 浏览器登录抖音后：
1. F12 → Network
2. 找到任意请求（如 `aweme/v1/web/...`）
3. Request Headers → Cookie → 复制完整值

**重要**：需要包含以下字段：
- `ttwid` - 设备标识
- `s_v_web_id` - 访客标识  
- `sessionid`（可选） - 登录态

### Q: Cookie 多久过期？

**A**: 
- `ttwid`、`s_v_web_id` - 长期有效（数月）
- `sessionid` - 约 7-30 天（登录态）

过期后重新复制即可。

### Q: 如何更新 Cookie？

**方法 1：删除配置文件**
```bash
rm config/cookie.json
python main.py  # 会重新提示输入
```

**方法 2：直接编辑**
```bash
# 编辑 config/cookie.json
{
  "ttwid": "新的ttwid",
  "s_v_web_id": "新的s_v_web_id",
  "sessionid": "新的sessionid"
}
```

**方法 3：用工具导出**
```bash
# 从 Edge 浏览器自动导出
python lib/reverse/dump_edge_cookies.py

# 从 Chrome DevTools 导出
python lib/reverse/export_session.py
```

### Q: 映射表必须生成吗？

**A**: 
- 项目自带 **100 样本示例**（覆盖 28 小时）
- 如果请求时间在覆盖范围内，可直接使用
- **超出范围会失效**，需要扩展映射表

### Q: 如何扩展映射表？

**A**:
```bash
# 运行采样（每次 500 样本）
python lib/reverse/incremental_build.py

# 重复运行累积样本
for i in {1..10}; do
  python lib/reverse/incremental_build.py
done
```

**自动化后台采样**（Linux/Mac）：
```bash
# 后台运行 20 轮
nohup bash -c 'for i in {1..20}; do 
  python lib/reverse/incremental_build.py
  sleep 1
done' > sampling.log 2>&1 &
```

### Q: 映射表占用多大空间？

| 样本数 | 覆盖时间 | 文件大小 |
|--------|----------|----------|
| 100 | 28 小时 | ~20 KB |
| 1,000 | 11 天 | ~200 KB |
| 10,000 | 115 天 | ~2 MB |
| 100,000 | 3 年 | ~20 MB |

### Q: 为什么不提交完整映射表？

**A**: 
- 完整映射表（9,454 样本）约 **12 MB**
- Git 不适合存储大文件
- 每个用户根据需要自行生成

---

## 🔧 高级配置

### 切换签名方案

```python
from utils.request import Request

r = Request()

# 方案 1：纯 Python（默认，查表法）
a_bogus = r.get_sign_pure(url, params)

# 方案 2：补环境（需要 Node.js）
a_bogus = r.get_sign_bdms(url, params, 'GET', '')
```

### 检查映射表状态

```python
import json
from pathlib import Path

mapping_file = Path('lib/reverse/time_mapping_full.json')

if mapping_file.exists():
    data = json.load(open(mapping_file))
    times = sorted([int(k) for k in data.keys()])
    
    print(f"样本数: {len(times):,}")
    print(f"覆盖: {(times[-1] - times[0]) / 86400000:.1f} 天")
    
    from datetime import datetime
    print(f"起: {datetime.fromtimestamp(times[0]/1000)}")
    print(f"止: {datetime.fromtimestamp(times[-1]/1000)}")
else:
    print("使用示例映射表（100 样本）")
```

---

## 📞 遇到问题？

1. **Cookie 失效** → 重新从浏览器复制
2. **映射表超出范围** → 运行 `incremental_build.py` 扩展
3. **找不到映射表** → 会自动使用示例表（100 样本）
4. **Node.js 依赖问题** → 使用纯 Python 方案（默认）

详见：[完整文档](docs/REVERSE_GUIDE.md)

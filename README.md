
# Douyin API

🎉 **最新更新**：已实现 100% 纯 Python a_bogus 签名生成！无需 Node.js 或浏览器。

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Pure Python](https://img.shields.io/badge/a__bogus-Pure%20Python-success.svg)](docs/REVERSE_GUIDE.md)

---

## 🚀 纯 Python 签名实现

本项目已完成 a_bogus 签名的**纯 Python 逆向实现**：

- ✅ **100% 纯 Python** - 无需 Node.js 依赖
- ✅ **自动签名** - Request 类默认使用纯算法
- ✅ **无映射表** - 直接算法生成，不需要预采样
- ✅ **本地可测** - 离线测试覆盖无映射表生成

**快速开始**：
```python
from utils.request import Request

r = Request()
result = r.getJSON('/aweme/v1/web/aweme/detail/', {'aweme_id': '123'})
# 自动使用纯 Python 生成 a_bogus
```

**使用说明**：
- 📖 [完整使用指南](USAGE.md) - Cookie 配置
- 📖 [完整逆向指南](docs/REVERSE_GUIDE.md) - 从 0 到 1 的逆向过程
- 📖 [快速参考](docs/QUICK_REFERENCE.md) - 5 步逆向总结

**重要提示**：
- 首次使用需配置 Cookie（自动提示输入）
- `a_bogus` 生成不需要 Node.js；部分接口的 `x-secsdk-web-signature` 仍走 Node.js 补环境

详细文档：
- 📖 [完整逆向指南](docs/REVERSE_GUIDE.md) - 从 0 到 1 的逆向过程
- 📖 [快速参考](docs/QUICK_REFERENCE.md) - 5 步逆向总结
- 📖 [技术文档](docs/abogus_pure_reverse.md) - 深入技术细节

---

## 简介
本项目提供了用于获取抖音平台用户及视频信息的API接口，方便开发者获取用户作品、收藏、喜欢、观看历史等数据。

## 安装依赖
请先确保你的环境已经安装了 `pip`，然后运行以下命令安装本项目所需的所有依赖项：

```shell
pip install -r requirements.txt
```

## 导出依赖
如果你需要将本项目的依赖导出到 `requirements.txt`，可以使用以下命令：

```shell
pip freeze > requirements.txt
```

## 接口文档
详细的接口文档已在 `docs` 文件夹中提供。你可以通过以下链接查看：

- [用户信息接口文档](./docs/user-api.md)
- [视频接口文档](./docs/video-api.md)

## 使用方法
请参照对应的接口文档，按照说明进行API调用。
使用前，会弹出输入cookie，请从douyin的网页的接口复制cookie后输入，会自动生成config文件夹。

## 文件结构
```text
├── README.md         # 项目简介及使用说明
├── requirements.txt  # 项目依赖文件
├── docs              # 文档目录
│   ├── user-api.md   # 用户信息相关接口文档
│   └── video-api.md  # 视频相关接口文档
├── api               # 接口文件目录
│   └── ...           # 接口相关代码文件
├── utils             # 工具类目录
│   └── ...           # 工具类函数代码
├── tests             # 测试目录
│   └── ...           # 测试代码
├── config            # 配置文件目录
│   └── cookie.json   # 存储cookie的配置文件
├── app.py            # 启动文件

```

## 贡献
欢迎提交问题或贡献代码。

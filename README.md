# AI 提示词工具箱

> 命令行版 AI 提示词管理工具，让 AI 输出更精准

## 功能特性

- 📦 **50+ 预设提示词** - 写作、编程、翻译、运营全覆盖
- ⚡ **一键调用** - 支持 Claude / ChatGPT / 本地模型
- 🔄 **持续更新** - 社区贡献 + 定期更新
- 🆓 **免费开源** - 欢迎 Star ⭐

## 安装

```bash
git clone https://github.com/matafyan/ai-prompt-toolbox.git
cd ai-prompt-toolbox
pip install -r requirements.txt
```

## 使用方法

```bash
# 查看所有分类
python promptool.py list

# 查看某分类下的提示词
python promptool.py list writing

# 复制提示词到剪贴板
python promptool.py copy writing blog-intro

# 直接打印提示词
python promptool.py get writing blog-intro
```

## 提示词分类

| 分类 | 数量 | 场景 |
|------|------|------|
| writing | 12 | 写作辅助 |
| coding | 10 | 编程开发 |
| translate | 8 | 翻译 |
| operation | 10 | 运营营销 |
| life | 10 | 生活实用 |

## 支持作者

如果这个工具对你有帮助，欢迎打赏 ☕

[**PayPal 打赏**](https://www.paypal.me/matafeiyan)

---

## 许可证

MIT License - 欢迎 Fork 和贡献

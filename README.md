# My OCR - Mistral AI OCR 工具

基于 Mistral AI 的 PDF 文档光学字符识别（OCR）工具，能够将 PDF 文档转换为 Markdown 格式，并提取其中的图片。

## 🚀 功能特性

- **PDF 文档 OCR 处理**：使用 Mistral AI 的最新 OCR 模型进行文档识别
- **智能文本提取**：将 PDF 内容转换为结构化的 Markdown 格式
- **图片提取保存**：自动提取并保存文档中的图片文件
- **批量处理支持**：shell 脚本自动查找并处理当前目录的 PDF 文件
- **完整输出管理**：生成 Markdown 文件、JSON 响应文件和提取的图片
- **环境变量管理**：支持 `.env` 文件配置 API 密钥

## 📋 系统要求

- Python 3.9+
- uv 包管理工具
- 有效的 Mistral AI API 密钥
- macOS、Linux 或 Windows 系统

## 🛠️ 安装配置

### 1. 安装 uv 工具

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**或者使用 pip 安装:**
```bash
pip install uv
```

### 2. 克隆或下载项目

```bash
# 进入项目目录
cd my_ocr
```

### 3. 创建项目依赖文件

创建 `pyproject.toml` 文件（如果不存在）：

```toml
[project]
name = "my-ocr"
version = "0.1.0"
description = "Mistral AI OCR工具"
requires-python = ">=3.9"
dependencies = [
    "mistralai>=1.7.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

> **注意**：只需要声明 `mistralai` 一个依赖，其他必需的包（如 `httpx`、`pydantic` 等）会作为传递依赖自动安装。

### 4. 使用 uv 安装依赖

```bash
# 创建虚拟环境并安装依赖（一步完成）
uv sync
```

或者分步执行：

```bash
# 创建虚拟环境
uv venv

# 安装依赖（只需安装mistralai，其他依赖会自动安装）
uv pip install mistralai
```

### 5. 配置 API 密钥

创建 `.env` 文件并添加您的 Mistral AI API 密钥：

```bash
# .env
MISTRAL_API_KEY=your_mistral_api_key_here
```

> **注意**：请确保您已经在 [Mistral AI 平台](https://console.mistral.ai/) 上注册并获取了有效的 API 密钥。

## 📖 使用方法

### 方法一：使用 Shell 脚本（推荐）

1. 将需要处理的 PDF 文件放置在任意目录中
2. 在该目录下运行脚本：

```bash
# 使脚本可执行
chmod +x /path/to/my_ocr/my_ocr.sh

# 运行脚本（会自动处理当前目录的第一个PDF文件）
/path/to/my_ocr/my_ocr.sh
```

### 方法二：直接使用 Python 脚本

```bash
# 使用 uv 运行脚本
uv run python my_ocr.py /path/to/your/document.pdf
```

或者激活虚拟环境后运行：

```bash
# 激活虚拟环境
source .venv/bin/activate

# 运行 OCR 处理
python my_ocr.py /path/to/your/document.pdf
```

## 📁 输出结果

处理完成后，会在 PDF 文件所在目录生成一个输出文件夹：

```
原PDF文件目录/
├── document.pdf                          # 原始PDF文件
└── document_ocr_output/                  # OCR输出目录
    ├── document_ocr.md                   # Markdown格式的文本内容
    ├── document_ocr_response.json        # 完整的API响应数据
    ├── img-0-0                          # 提取的图片文件
    ├── img-0-1                          # 提取的图片文件
    └── ...                              # 其他提取的图片
```

## 🔧 项目结构

```
my_ocr/
├── .venv/                    # Python虚拟环境
├── .env                      # 环境变量配置文件
├── .gitignore               # Git忽略文件配置
├── pyproject.toml           # 项目配置和依赖管理
├── my_ocr.py                # 主要的OCR处理脚本
├── my_ocr.sh                # Shell执行脚本
└── README.md                # 项目说明文档
```

## ⚙️ 主要依赖

- **mistralai**: Mistral AI 官方 Python SDK，提供 OCR 和聊天功能

### 传递依赖（自动安装）
以下依赖会在安装 `mistralai` 时自动安装，无需手动指定：

- **httpx**: 现代化的 HTTP 客户端
  - 用于与 Mistral AI API 服务器通信
  - 支持异步请求和 HTTP/2 协议
- **pydantic**: 数据验证和序列化库
  - 用于验证 API 请求参数和响应数据
  - 提供类型安全和数据序列化功能
- **python-dateutil**: 日期时间处理
- **typing-inspection**: 运行时类型检查

> **说明**：您只需要在 `pyproject.toml` 中声明 `mistralai` 依赖，其他包会作为传递依赖自动安装。

## 📝 使用示例

### 处理单个PDF文件
```bash
# 使用 uv 运行
uv run python my_ocr.py /Users/username/Documents/report.pdf

# 或者激活环境后运行
source .venv/bin/activate
python my_ocr.py /Users/username/Documents/report.pdf
```

### 批量处理当前目录PDF文件
```bash
# 在包含PDF文件的目录中运行
./my_ocr.sh
```

### 添加新依赖
```bash
# 使用 uv 添加新的依赖包
uv add package_name

# 移除依赖包
uv remove package_name
```

## ❗ 注意事项

1. **API 密钥安全**：请勿将 `.env` 文件提交到版本控制系统
2. **文件大小限制**：请注意 Mistral AI 对上传文件大小的限制
3. **网络连接**：需要稳定的网络连接来访问 Mistral AI 服务
4. **输出目录**：如果输出目录已存在，新文件会覆盖同名文件
5. **uv 工具**：确保已正确安装 uv 工具，它比传统的 pip 更快更可靠

## 🐛 故障排除

### 常见问题

**1. API 密钥错误**
```
错误：MISTRAL_API_KEY 环境变量未设置
```
解决方案：检查 `.env` 文件是否正确配置了 API 密钥

**2. PDF 文件未找到**
```
错误：文件 xxx.pdf 未找到
```
解决方案：确认文件路径正确，且文件确实存在

**3. uv 工具问题**
```
错误：uv: command not found
```
解决方案：重新安装 uv 工具或检查 PATH 环境变量

**4. 虚拟环境问题**
```
错误：无法激活虚拟环境
```
解决方案：使用 `uv venv` 重新创建虚拟环境

**5. Python 版本问题**
```
错误：mistralai>=1.7.0 需要 Python>=3.9
```
解决方案：升级到 Python 3.9 或更高版本

## 📜 许可证

本项目仅供学习和个人使用。使用 Mistral AI 服务需要遵循其服务条款。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

---

**作者**：由 AI 助手生成  
**更新时间**：2025年5月
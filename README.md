# My OCR - Mistral AI OCR 工具

基于 Mistral AI 的 PDF 文档光学字符识别（OCR）工具，能够将 PDF 文档转换为 Markdown 格式，并提取其中的图片。

## 🚀 功能特性

- **PDF 文档 OCR 处理**：使用 Mistral AI 的最新 OCR 模型进行文档识别
- **智能文本提取**：将 PDF 内容转换为结构化的 Markdown 格式
- **图片提取保存**：自动提取并保存文档中的图片文件
- **批量处理支持**：shell 脚本自动查找并处理当前目录的 PDF 文件

## 📋 系统要求

- Python 3.9+
- uv 包管理工具
- 有效的 Mistral AI API 密钥

## 🛠️ 安装配置

### 1. 安装 uv 工具

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 安装依赖

```bash
# 创建虚拟环境并安装依赖
uv sync
```

### 3. 配置 API 密钥

创建 `.env` 文件并添加您的 Mistral AI API 密钥：

```bash
# .env
MISTRAL_API_KEY=your_mistral_api_key_here
```

## 📖 使用方法

### 方法一：使用 Shell 脚本（推荐）

```bash
# 使脚本可执行
chmod +x /path/to/my_ocr/my_ocr.sh

# 运行脚本（会自动处理当前目录的第一个PDF文件）
/path/to/my_ocr/my_ocr.sh
```

### 方法二：直接使用 Python 脚本

```bash
# 使用 uv 运行脚本
uv run python main.py /path/to/your/document.pdf
```

## 📁 输出结果

处理完成后，会在 PDF 文件所在目录生成一个输出文件夹：

```
原PDF文件目录/
├── document.pdf                          # 原始PDF文件
└── document_ocr_output/                  # OCR输出目录
    ├── document_ocr.md                   # Markdown格式的文本内容
    ├── document_ocr_response.json        # 完整的API响应数据
    └── img-0-0, img-0-1, ...            # 提取的图片文件
```

## 🔧 项目结构

```
my_ocr/
├── .venv/                    # Python虚拟环境
├── .env                      # 环境变量配置文件
├── pyproject.toml           # 项目配置和依赖管理
├── main.py                  # 主要的OCR处理脚本
├── my_ocr.sh                # Shell执行脚本
└── README.md                # 项目说明文档
```

## 📝 使用示例

```bash
# 处理单个PDF文件
uv run python main.py /Users/username/Documents/report.pdf

# 批量处理当前目录PDF文件
./my_ocr.sh
```

## ❗ 注意事项

1. **API 密钥安全**：请勿将 `.env` 文件提交到版本控制系统
2. **文件大小限制**：请注意 Mistral AI 对上传文件大小的限制
3. **网络连接**：需要稳定的网络连接来访问 Mistral AI 服务

## 🐛 故障排除

**API 密钥错误**
```
错误：MISTRAL_API_KEY 环境变量未设置
```
解决方案：检查 `.env` 文件是否正确配置了 API 密钥

**PDF 文件未找到**
```
错误：文件 xxx.pdf 未找到
```
解决方案：确认文件路径正确，且文件确实存在

---

**更新时间**：2025年5月
# PDF OCR - Mistral AI OCR Tool

A PDF Optical Character Recognition (OCR) tool powered by Mistral AI, capable of converting PDF documents to Markdown format and extracting embedded images.

**🌏 Language**: [中文文档 / Chinese Documentation](./README_CN.md)

## 🚀 Features

- **PDF Document OCR Processing**: Utilizes Mistral AI's latest OCR models for document recognition
- **Intelligent Text Extraction**: Converts PDF content to structured Markdown format
- **Image Extraction & Saving**: Automatically extracts and saves images from documents
- **Command Line Interface**: Modern CLI tool with multiple usage options
- **Automatic File Discovery**: Smart detection and processing of PDF files in directories

## 📋 Requirements

- Python 3.9+
- uv package manager
- Valid Mistral AI API key

## 🛠️ Installation & Setup

### 1. Install uv Tool

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install as System Tool (Recommended)

```bash
# Install pdf-ocr tool globally
uv tool install .
```

### 3. Or Install Dependencies for Development

```bash
# Create virtual environment and install dependencies
uv sync
```

### 4. Configure API Key

Create a `.env` file and add your Mistral AI API key:

```bash
# .env
MISTRAL_API_KEY=your_mistral_api_key_here
```

## 📖 Usage

### Method 1: Using Installed CLI Tool (Recommended)

```bash
# Process a specific PDF file
pdf-ocr /path/to/your/document.pdf

# Auto-find and process PDF files in current directory
pdf-ocr --auto-find

# Search for PDF files in a specific directory
pdf-ocr --directory /path/to/pdf/folder

# View help information
pdf-ocr --help
```

### Method 2: Direct Script Execution

```bash
# Run with uv
uv run python cli.py ocr /path/to/your/document.pdf

# Auto-find PDF files in current directory
uv run python cli.py ocr --auto-find

# View version information
uv run python cli.py version
```

### Method 3: Using Original Python Script

```bash
# Run with uv
uv run python main.py /path/to/your/document.pdf
```

## 📁 Output Structure

After processing, an output folder will be generated in the PDF file's directory:

```
PDF_Directory/
├── document.pdf                          # Original PDF file
└── document_ocr_output/                  # OCR output directory
    ├── document_ocr.md                   # Markdown formatted text content
    ├── document_ocr_response.json        # Complete API response data
    └── img-0-0, img-0-1, ...            # Extracted image files
```

## 🔧 Project Structure

```
pdf_ocr/
├── .venv/                    # Python virtual environment
├── .env                      # Environment variables configuration
├── pyproject.toml           # Project configuration and dependency management
├── main.py                  # Main OCR processing script
├── cli.py                   # Command line interface script
├── README.md                # Project documentation (English)
└── README_CN.md             # Project documentation (Chinese)
```

## 📝 Usage Examples

```bash
# Using system installed tool
pdf-ocr ~/Documents/report.pdf
pdf-ocr --auto-find

# Using development environment
uv run python cli.py ocr ~/Documents/report.pdf
uv run python cli.py ocr --auto-find

# Traditional approach
uv run python main.py ~/Documents/report.pdf
```

## ❗ Important Notes

1. **API Key Security**: Do not commit the `.env` file to version control systems
2. **File Size Limitations**: Be aware of Mistral AI's file size upload limits
3. **Network Connection**: Requires stable network connection to access Mistral AI services

## 🐛 Troubleshooting

**API Key Error**
```
Error: MISTRAL_API_KEY environment variable not set
```
Solution: Check if the API key is correctly configured in the `.env` file

**PDF File Not Found**
```
Error: File xxx.pdf not found
```
Solution: Verify the file path is correct and the file exists

---

**Last Updated**: May 2025
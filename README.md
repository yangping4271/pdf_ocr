# PDF OCR - Mistral AI OCR Tool

A PDF Optical Character Recognition (OCR) tool powered by Mistral AI, capable of converting PDF documents to Markdown format and extracting embedded images.

**🌏 Language**: [中文文档 / Chinese Documentation](./README_CN.md)

## 🚀 Features

- **PDF Document OCR Processing**: Utilizes Mistral AI's latest OCR models for document recognition
- **Intelligent Text Extraction**: Converts PDF content to structured Markdown format
- **Image Extraction & Saving**: Automatically extracts and saves images from documents
- **Batch Processing Support**: Shell script automatically finds and processes PDF files in current directory

## 📋 Requirements

- Python 3.9+
- uv package manager
- Valid Mistral AI API key

## 🛠️ Installation & Setup

### 1. Install uv Tool

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Dependencies

```bash
# Create virtual environment and install dependencies
uv sync
```

### 3. Configure API Key

Create a `.env` file and add your Mistral AI API key:

```bash
# .env
MISTRAL_API_KEY=your_mistral_api_key_here
```

## 📖 Usage

### Method 1: Using Shell Script (Recommended)

```bash
# Make script executable
chmod +x /path/to/my_ocr/pdf_ocr.sh

# Run script (automatically processes the first PDF file in current directory)
/path/to/my_ocr/pdf_ocr.sh
```

### Method 2: Direct Python Script Usage

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
my_ocr/
├── .venv/                    # Python virtual environment
├── .env                      # Environment variables configuration
├── pyproject.toml           # Project configuration and dependency management
├── main.py                  # Main OCR processing script
├── pdf_ocr.sh               # Shell execution script
├── README.md                # Project documentation (English)
└── README_CN.md             # Project documentation (Chinese)
```

## 📝 Usage Examples

```bash
# Process a single PDF file
uv run python main.py /Users/username/Documents/report.pdf

# Batch process PDF files in current directory
./pdf_ocr.sh
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
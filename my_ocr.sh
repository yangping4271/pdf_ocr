#!/bin/bash

# 获取脚本所在目录（用于找到虚拟环境和my_ocr.py）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 获取当前工作目录（执行脚本的路径）
CURRENT_DIR="$(pwd)"

# 加载.env文件（如果存在）
ENV_FILE="$SCRIPT_DIR/.env"
if [ -f "$ENV_FILE" ]; then
    echo "从 $ENV_FILE 加载环境变量..."
    # 使用set -a来自动导出变量，然后source .env文件
    set -a
    source "$ENV_FILE"
    set +a
    echo "环境变量加载完成"
else
    echo "未找到.env文件: $ENV_FILE"
fi

# 检查是否安装了uv工具
if command -v uv &> /dev/null; then
    echo "检测到 uv 工具，使用 uv 运行脚本..."
    USE_UV=true
else
    echo "未检测到 uv 工具，使用传统虚拟环境..."
    USE_UV=false
fi

# 虚拟环境路径
VENV_PATH="$SCRIPT_DIR/.venv"

# 如果不使用uv，检查虚拟环境是否存在
if [ "$USE_UV" = false ]; then
    if [ ! -d "$VENV_PATH" ]; then
        echo "错误：虚拟环境 $VENV_PATH 不存在"
        echo "请先运行以下命令创建虚拟环境："
        echo "  cd $SCRIPT_DIR"
        echo "  python3 -m venv .venv"
        echo "  source .venv/bin/activate"
        echo "  pip install mistralai httpx pydantic"
        exit 1
    fi

    # 激活虚拟环境
    echo "激活虚拟环境..."
    source "$VENV_PATH/bin/activate"

    # 检查是否成功激活
    if [ -z "$VIRTUAL_ENV" ]; then
        echo "错误：无法激活虚拟环境"
        exit 1
    fi

    echo "虚拟环境已激活: $VIRTUAL_ENV"
fi

# 查找当前工作目录下的PDF文件
echo "在当前目录查找PDF文件: $CURRENT_DIR"
PDF_FILES=($(find "$CURRENT_DIR" -maxdepth 1 -name "*.pdf" -type f))

if [ ${#PDF_FILES[@]} -eq 0 ]; then
    echo "错误：在当前目录 $CURRENT_DIR 中未找到PDF文件"
    if [ "$USE_UV" = false ]; then
        deactivate
    fi
    exit 1
fi

# 如果有多个PDF文件，选择第一个
PDF_PATH="${PDF_FILES[0]}"
echo "找到PDF文件: $PDF_PATH"

# 检查my_ocr.py是否存在
MY_OCR_SCRIPT="$SCRIPT_DIR/my_ocr.py"
if [ ! -f "$MY_OCR_SCRIPT" ]; then
    echo "错误：OCR处理脚本 $MY_OCR_SCRIPT 不存在"
    if [ "$USE_UV" = false ]; then
        deactivate
    fi
    exit 1
fi

# 运行OCR处理
echo "开始运行OCR处理..."
if [ "$USE_UV" = true ]; then
    # 使用uv运行脚本
    cd "$SCRIPT_DIR"
    uv run python "$MY_OCR_SCRIPT" "$PDF_PATH"
    OCR_EXIT_CODE=$?
else
    # 使用传统方式运行脚本
    python "$MY_OCR_SCRIPT" "$PDF_PATH"
    OCR_EXIT_CODE=$?
    # 停用虚拟环境
    deactivate
fi

if [ $OCR_EXIT_CODE -eq 0 ]; then
    echo "OCR处理成功完成！"
else
    echo "OCR处理失败，退出码: $OCR_EXIT_CODE"
fi

exit $OCR_EXIT_CODE 
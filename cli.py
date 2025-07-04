#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from typing import Optional, List

import typer
from typing_extensions import Annotated

from main import process_pdf_ocr, load_env_file

app = typer.Typer(
    name="pdf-ocr",
    help="PDF OCR - 基于 Mistral AI 的 PDF 文档光学字符识别工具",
    add_completion=False,
)


def find_pdf_files(directory: Path) -> List[Path]:
    """在指定目录中查找PDF文件"""
    pdf_files = list(directory.glob("*.pdf"))
    return pdf_files


def load_environment():
    """加载环境变量"""
    script_dir = Path(__file__).parent.absolute()
    env_file = script_dir / '.env'
    
    if env_file.exists():
        typer.echo(f"从 {env_file} 加载环境变量...")
        if load_env_file(env_file):
            typer.echo("环境变量加载完成")
        else:
            typer.echo("环境变量加载失败")
    else:
        typer.echo(f"未找到.env文件: {env_file}")


@app.command()
def ocr(
    pdf_path: Annotated[
        Optional[str], 
        typer.Argument(help="PDF文件路径。如果未指定，将在当前目录查找PDF文件")
    ] = None,
    auto_find: Annotated[
        bool, 
        typer.Option("--auto-find", "-a", help="自动在当前目录查找PDF文件")
    ] = False,
    directory: Annotated[
        Optional[str], 
        typer.Option("--directory", "-d", help="指定搜索PDF文件的目录")
    ] = None,
):
    """
    对PDF文件进行OCR处理
    
    如果未指定PDF文件路径，将自动在当前目录（或指定目录）查找PDF文件。
    如果找到多个PDF文件，将使用第一个文件。
    """
    # 加载环境变量
    load_environment()
    
    # 确定要处理的PDF文件
    target_pdf = None
    
    if pdf_path:
        # 直接指定了PDF文件路径
        target_pdf = Path(pdf_path)
        if not target_pdf.exists():
            typer.echo(f"错误：文件 {pdf_path} 不存在", err=True)
            raise typer.Exit(1)
        if not target_pdf.suffix.lower() == '.pdf':
            typer.echo(f"错误：文件 {pdf_path} 不是PDF文件", err=True)
            raise typer.Exit(1)
    else:
        # 自动查找PDF文件
        search_dir = Path(directory) if directory else Path.cwd()
        
        if not search_dir.exists():
            typer.echo(f"错误：目录 {search_dir} 不存在", err=True)
            raise typer.Exit(1)
        
        typer.echo(f"在目录查找PDF文件: {search_dir}")
        pdf_files = find_pdf_files(search_dir)
        
        if not pdf_files:
            typer.echo(f"错误：在目录 {search_dir} 中未找到PDF文件", err=True)
            raise typer.Exit(1)
        
        # 使用第一个找到的PDF文件
        target_pdf = pdf_files[0]
        typer.echo(f"找到PDF文件: {target_pdf}")
        
        if len(pdf_files) > 1:
            typer.echo(f"注意：找到 {len(pdf_files)} 个PDF文件，使用第一个: {target_pdf.name}")
    
    # 处理PDF文件
    typer.echo("开始运行OCR处理...")
    success = process_pdf_ocr(str(target_pdf))
    
    if success:
        typer.echo("OCR处理成功完成！")
    else:
        typer.echo("OCR处理失败", err=True)
        raise typer.Exit(1)


@app.command()
def version():
    """显示版本信息"""
    typer.echo("pdf-ocr v0.1.0")
    typer.echo("基于 Mistral AI 的 PDF 文档光学字符识别工具")


def main():
    """CLI入口点"""
    app()


if __name__ == "__main__":
    main()
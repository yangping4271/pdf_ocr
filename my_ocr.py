import os
import base64
import json
import re
import sys
from pathlib import Path
from mistralai import Mistral

def load_env_file(env_path):
    """从.env文件加载环境变量"""
    if not os.path.exists(env_path):
        return False
    
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释行
                if not line or line.startswith('#'):
                    continue
                
                # 解析 KEY=VALUE 格式
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # 移除引号（如果有的话）
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    # 设置环境变量
                    os.environ[key] = value
        return True
    except Exception as e:
        print(f"读取.env文件时出错: {e}")
        return False

def process_pdf_ocr(pdf_path):
    """处理PDF的OCR功能"""
    # 尝试从脚本所在目录的.env文件加载环境变量
    script_dir = Path(__file__).parent.absolute()
    env_file = script_dir / '.env'
    
    if env_file.exists():
        print(f"从 {env_file} 加载环境变量...")
        if load_env_file(env_file):
            print("环境变量加载成功")
        else:
            print("环境变量加载失败")
    else:
        print(f"未找到.env文件: {env_file}")
    
    # 从环境变量中获取API密钥
    api_key = os.environ.get("MISTRAL_API_KEY")

    if not api_key:
        print("错误：MISTRAL_API_KEY 环境变量未设置。")
        print("请确保在.env文件中设置了 MISTRAL_API_KEY=your_api_key")
        return False
    
    client = Mistral(api_key=api_key)
    if not os.path.exists(pdf_path):
        print(f"错误：文件 {pdf_path} 未找到。")
        return False
    
    try:
        print(f"正在上传文件: {pdf_path}...")
        # 上传本地PDF文件
        with open(pdf_path, "rb") as f:
            uploaded_pdf = client.files.upload(
                file={
                    "file_name": os.path.basename(pdf_path),
                    "content": f,
                },
                purpose="ocr"
            )
        print(f"文件上传成功。文件ID: {uploaded_pdf.id}")

        # 获取签名URL
        print("正在获取签名URL...")
        signed_url_response = client.files.get_signed_url(file_id=uploaded_pdf.id)
        document_signed_url = signed_url_response.url
        print(f"获取签名URL成功: {document_signed_url}")

        # 使用签名URL进行OCR处理
        print("正在进行OCR处理...")
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": document_signed_url
            },
            include_image_base64=True  # 设置为True以获取图片base64数据
        )
        print("\nOCR处理完成。")
        
        # 构造输出目录名和文件名 - 保存到PDF文件所在目录
        base_filename = os.path.splitext(os.path.basename(pdf_path))[0]
        pdf_dir = Path(pdf_path).parent
        output_dir = pdf_dir / f"{base_filename}_ocr_output"
        output_dir.mkdir(parents=True, exist_ok=True) # 创建输出目录
        output_md_path = output_dir / f"{base_filename}_ocr.md"
        
        # 保存完整的OCR响应到JSON文件，方便查看
        response_dict = ocr_response.model_dump() if hasattr(ocr_response, 'model_dump') else vars(ocr_response)
        json_path = output_dir / f"{base_filename}_ocr_response.json"
        try:
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(response_dict, json_file, indent=2, default=str)
            print(f"已保存完整OCR响应到: {json_path}")
        except Exception as je:
            print(f"保存JSON响应时出错: {je}")
        
        # 创建一个图片映射，关联图片ID与实际保存的文件名
        image_map = {}
        
        # 先处理和保存所有图片
        if hasattr(ocr_response, 'pages') and ocr_response.pages:
            for page_idx, page in enumerate(ocr_response.pages):
                print(f"提取页面 {page_idx} 的图片:")
                
                # 处理图片（从images属性中提取图片）
                if hasattr(page, 'images') and page.images:
                    print(f"页面 {page_idx} 包含 {len(page.images)} 个图片")
                    
                    for img_idx, img_obj in enumerate(page.images):
                        # 获取图片ID
                        img_id = getattr(img_obj, 'id', f"img-{page_idx}-{img_idx}")
                        
                        # 检查image_base64属性
                        if hasattr(img_obj, 'image_base64'):
                            base64_data = img_obj.image_base64
                            
                            # 检查base64数据是否包含前缀
                            if base64_data and isinstance(base64_data, str):
                                # 如果包含 "data:" 前缀，去除它
                                if base64_data.startswith('data:'):
                                    # 格式应该类似: data:image/jpeg;base64,/9j/4AAQ...
                                    base64_data = base64_data.split(',', 1)[1]
                                
                                try:
                                    # 使用图片ID作为文件名，保持图片引用一致性
                                    image_filename = f"{img_id}"
                                    image_path = output_dir / image_filename
                                    
                                    # 保存图片
                                    with open(image_path, "wb") as img_file:
                                        img_file.write(base64.b64decode(base64_data))
                                    
                                    print(f"  图片已保存到: {image_path}")
                                    
                                    # 将图片ID映射到实际的文件名 - 在这里保持文件名与图片ID一致
                                    image_map[img_id] = image_filename
                                except Exception as e:
                                    print(f"  保存图片时出错: {e}")
                        else:
                            print(f"  图片 {img_idx} 没有image_base64属性")
                else:
                    print(f"页面 {page_idx} 没有图片")
        
        # 然后将结果写入Markdown文件
        print(f"正在将结果保存到目录: {output_dir}...")
        with open(output_md_path, "w", encoding="utf-8") as md_file:
            if hasattr(ocr_response, 'pages') and ocr_response.pages:
                for page_idx, page in enumerate(ocr_response.pages):
                    print(f"\n处理页面 {page_idx} 的文本:")
                    
                    # 直接写入页面文本内容，图片引用已经在文本中，无需额外添加
                    if hasattr(page, 'markdown'):
                        markdown_content = page.markdown
                        # 保持Markdown文本中的图片引用不变，因为我们已经使用相同的文件名保存了图片
                        md_file.write(markdown_content)
                    else:
                        print(f"警告: 页面 {page_idx} 没有markdown属性")
                        # 尝试其他可能的文本内容属性
                        if hasattr(page, 'text'):
                            md_file.write(page.text)
                        elif hasattr(page, 'content'):
                            md_file.write(page.content)
                        else:
                            md_file.write(f"[无法提取页面 {page_idx} 的文本内容]")
                    
                    md_file.write("\n")
            else:
                md_file.write(str(ocr_response))
                
        print(f"结果已成功保存到 {output_md_path}")
        return True

    except FileNotFoundError:
        print(f"错误：文件 {pdf_path} 未找到。")
        return False
    except Exception as e:
        print(f"处理过程中发生错误: {e}")
        return False

if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("用法: python my_ocr.py <pdf_file_path>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    success = process_pdf_ocr(pdf_path)
    sys.exit(0 if success else 1) 
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Jemdoc Chinese Support Wrapper
这个脚本用于正确处理中文编码的jemdoc转换
"""

import sys
import os
import subprocess
import shutil

def convert_jemdoc_with_encoding(jemdoc_path, conf_file, input_file):
    """
    使用jemdoc转换文件，并确保输出文件使用UTF-8编码
    
    Args:
        jemdoc_path: jemdoc脚本的路径
        conf_file: 配置文件路径
        input_file: 输入的jemdoc文件路径
    """
    # 获取输出文件名
    if input_file.endswith('.jemdoc'):
        output_file = input_file.replace('.jemdoc', '.html')
    else:
        output_file = input_file + '.html'
    
    # 构建jemdoc命令
    command = [
        sys.executable,
        jemdoc_path,
        '-c', conf_file,
        input_file
    ]
    
    print(f"正在转换: {input_file} -> {output_file}")
    
    # 执行jemdoc命令
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    
    if result.returncode != 0:
        print(f"错误: jemdoc转换失败")
        print(f"错误输出: {result.stderr}")
        return False
    
    # 读取生成的HTML文件（使用二进制模式）
    try:
        with open(output_file, 'rb') as f:
            content = f.read()
        
        # 尝试解码为UTF-8
        try:
            decoded_content = content.decode('utf-8')
            print(f"✓ 文件已经是UTF-8编码")
        except UnicodeDecodeError:
            # 如果不是UTF-8，尝试使用系统默认编码解码，然后重新编码为UTF-8
            print(f"⚠ 文件不是UTF-8编码，正在转换...")
            try:
                decoded_content = content.decode('gbk')  # Windows系统常用编码
            except UnicodeDecodeError:
                try:
                    decoded_content = content.decode('gb2312')
                except UnicodeDecodeError:
                    try:
                        decoded_content = content.decode('latin1')
                    except UnicodeDecodeError:
                        print(f"✗ 无法解码文件内容")
                        return False
            
            # 重新写入UTF-8编码
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(decoded_content)
            print(f"✓ 已转换为UTF-8编码")
        
        print(f"✓ 转换成功: {output_file}")
        return True
        
    except Exception as e:
        print(f"✗ 处理文件时出错: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("使用方法: python jemdoc_chinese_wrapper.py <input_file.jemdoc>")
        print("示例: python jemdoc_chinese_wrapper.py chinese.jemdoc")
        return
    
    # jemdoc脚本路径
    jemdoc_path = os.path.join(os.path.dirname(__file__), '..', 'jemdoc')
    
    # 配置文件路径
    conf_file = 'mysite.conf'
    
    # 输入文件
    input_file = sys.argv[1]
    
    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"✗ 文件不存在: {input_file}")
        return
    
    # 检查配置文件是否存在
    if not os.path.exists(conf_file):
        print(f"✗ 配置文件不存在: {conf_file}")
        return
    
    # 执行转换
    success = convert_jemdoc_with_encoding(jemdoc_path, conf_file, input_file)
    
    if success:
        print(f"\n✓ 中文网页生成完成！")
        print(f"您现在可以在浏览器中打开 {input_file.replace('.jemdoc', '.html')} 查看结果。")
    else:
        print(f"\n✗ 生成失败，请检查错误信息。")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
简单的音频文件转文字工具
支持 MP4, WAV, MP3 等常见音频格式
"""

import sys
import os
from pathlib import Path
from faster_whisper import WhisperModel
from pydub import AudioSegment
import numpy as np
import time

def convert_audio_to_text(audio_file_path, model_size="tiny", language="zh"):
    """
    将音频文件转换为文字

    Args:
        audio_file_path: 音频文件路径
        model_size: Whisper模型大小 ("tiny", "base", "small", "medium", "large-v3")
        language: 语言代码 ("zh"=中文, "en"=英文, None=自动检测)
    """

    # 检查文件是否存在
    if not os.path.exists(audio_file_path):
        print(f"❌ 错误: 文件 '{audio_file_path}' 不存在")
        return

    print(f"🎵 正在处理音频文件: {audio_file_path}")
    print(f"🤖 使用模型: {model_size}")
    print(f"🌍 语言设置: {language if language else '自动检测'}")
    print("-" * 50)

    try:
        # 加载Whisper模型
        print("⏳ 正在加载Whisper模型...")
        model = WhisperModel(model_size, device="cpu")
        print("✅ 模型加载完成")

        # 读取并处理音频文件
        print("⏳ 正在读取音频文件...")
        audio = AudioSegment.from_file(audio_file_path)

        # 转换为Whisper需要的格式
        audio = audio.set_frame_rate(16000).set_channels(1)

        # 转换为numpy数组
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
        if audio.sample_width == 2:  # 16-bit
            samples = samples / 32768.0
        elif audio.sample_width == 4:  # 32-bit
            samples = samples / 2147483648.0

        print(f"📊 音频信息: 时长 {len(audio)/1000:.1f}秒, 采样点 {len(samples)}")
        print("✅ 音频处理完成")

        # 开始转录
        print("⏳ 正在进行语音转文字...")
        start_time = time.time()

        segments, info = model.transcribe(
            samples,
            language=language,
            beam_size=5,
            best_of=5,
            temperature=0.0
        )

        # 输出结果
        print("🎯 转录结果:")
        print("=" * 50)

        full_text = ""
        for segment in segments:
            timestamp = f"[{segment.start:.1f}s - {segment.end:.1f}s]"
            text = segment.text.strip()
            print(f"{timestamp} {text}")
            full_text += text + " "

        print("=" * 50)
        print(f"📝 完整文字: {full_text.strip()}")

        end_time = time.time()
        print(f"⏱️  处理时间: {end_time - start_time:.1f}秒")
        print(f"🎛️  检测语言: {info.language}")
        print(f"📊 语言概率: {info.language_probability:.2%}")

        # 保存到文件
        output_file = Path(audio_file_path).stem + "_transcript.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"音频文件: {audio_file_path}\n")
            f.write(f"处理时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"检测语言: {info.language} ({info.language_probability:.2%})\n")
            f.write(f"模型: {model_size}\n")
            f.write("-" * 50 + "\n\n")

            for segment in segments:
                timestamp = f"[{segment.start:.1f}s - {segment.end:.1f}s]"
                f.write(f"{timestamp} {segment.text.strip()}\n")

            f.write("\n" + "=" * 50 + "\n")
            f.write(f"完整文字:\n{full_text.strip()}")

        print(f"💾 转录结果已保存到: {output_file}")

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    print("🎤 音频转文字工具")
    print("支持格式: MP4, MP3, WAV, M4A 等")
    print()

    if len(sys.argv) < 2:
        print("用法:")
        print("  python audio_to_text.py <音频文件路径> [模型大小] [语言]")
        print()
        print("示例:")
        print("  python audio_to_text.py audio.mp4")
        print("  python audio_to_text.py audio.mp4 small")
        print("  python audio_to_text.py audio.mp4 base en")
        print()
        print("模型大小: tiny(最快) < base < small < medium < large-v3(最准确)")
        print("语言代码: zh(中文), en(英文), 留空自动检测")
        return

    audio_file = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "tiny"
    language = sys.argv[3] if len(sys.argv) > 3 else "zh"

    # 如果语言参数是"auto"，则设为None让模型自动检测
    if language.lower() in ["auto", "none", "detect"]:
        language = None

    convert_audio_to_text(audio_file, model_size, language)

if __name__ == "__main__":
    main()
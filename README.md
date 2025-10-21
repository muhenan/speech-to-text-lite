# 音频转文字工具 (Speech-to-Text Lite)

一个简单易用的音频转文字工具，基于 OpenAI 的 Whisper 模型，支持多种音频格式。

## 功能特点

- 支持多种音频格式：MP4, MP3, WAV, M4A 等
- 基于 faster-whisper 实现，速度快
- 支持多种模型大小选择（从快速到高精度）
- 支持中文、英文及多语言自动检测
- 输出带时间戳的转录结果
- 自动保存转录文本到文件

## 环境要求

- Python 3.8+
- 推荐使用 uv 进行依赖管理

## 安装

本项目使用 `uv` 作为包管理工具。如果你还没有安装 `uv`，请先安装：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

然后安装项目依赖：

```bash
uv sync
```

## 快速录音

如果你需要录制音频，可以使用以下方法：

### 使用终端命令（ffmpeg）

```bash
# 安装 ffmpeg（如果还没有安装）
brew install ffmpeg

# 录制 MP3 音频
ffmpeg -f avfoundation -i ":0" -acodec libmp3lame output.mp3
```

按 `Ctrl + C` 停止录制。

## 使用方法

### 基本用法

```bash
python audio_to_text.py <音频文件路径>
```

### 指定模型大小

```bash
python audio_to_text.py <音频文件路径> <模型大小>
```

### 指定语言

```bash
python audio_to_text.py <音频文件路径> <模型大小> <语言代码>
```

## 使用示例

```bash
# 使用默认模型 (tiny) 和中文语言
python audio_to_text.py audio.mp4

# 使用 small 模型
python audio_to_text.py audio.mp4 small

# 使用 base 模型，英文语言
python audio_to_text.py audio.mp4 base en

# 自动检测语言
python audio_to_text.py audio.mp4 base auto
```

## 模型大小说明

模型按速度和准确度排序：

| 模型 | 速度 | 准确度 | 适用场景 |
|------|------|--------|----------|
| `tiny` | 最快 | 较低 | 快速预览、测试 |
| `base` | 快 | 中等 | 日常使用 |
| `small` | 中等 | 较高 | 平衡速度和准确度 |
| `medium` | 较慢 | 高 | 要求较高准确度 |
| `large-v3` | 最慢 | 最高 | 专业转录需求 |

## 语言代码

- `zh` - 中文
- `en` - 英文
- `auto` / `none` / `detect` - 自动检测语言

支持更多语言代码，详见 [Whisper 语言支持列表](https://github.com/openai/whisper#available-models-and-languages)。

## 输出说明

程序会在控制台输出转录过程和结果，并自动保存转录文本到文件：

- 输出文件名：`<原音频文件名>_transcript.txt`
- 包含内容：
  - 音频文件信息
  - 处理时间和检测语言
  - 带时间戳的分段文本
  - 完整转录文本

## 依赖项

主要依赖：

- `faster-whisper` - Whisper 模型的优化实现
- `pydub` - 音频文件处理
- `numpy` - 数值计算

## 常见问题

### 1. 首次运行时下载模型

首次使用某个模型大小时，会自动下载对应的模型文件，请确保网络连接正常。

### 2. 音频格式不支持

如果遇到音频格式问题，请确保已安装 ffmpeg：

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# 请从 https://ffmpeg.org/download.html 下载并安装
```

### 3. 内存不足

如果处理大文件或使用大模型时遇到内存问题，可以：
- 使用更小的模型（如 tiny 或 base）
- 分段处理长音频文件

## 开发

### 项目结构

```
speech-to-text-lite/
├── audio_to_text.py      # 主程序
├── pyproject.toml        # 项目配置
├── uv.lock              # 依赖锁定文件
└── README.md            # 项目说明
```

### 代码说明

主要函数：

- `convert_audio_to_text()` - 核心转换函数 (audio_to_text.py:15)
  - 加载 Whisper 模型
  - 处理音频文件
  - 执行转录
  - 保存结果

- `main()` - 命令行入口 (audio_to_text.py:112)
  - 解析命令行参数
  - 调用转换函数

## License

MIT

## 贡献

欢迎提交 Issue 和 Pull Request！

## 致谢

本项目基于以下开源项目：

- [OpenAI Whisper](https://github.com/openai/whisper)
- [faster-whisper](https://github.com/guillaumekln/faster-whisper)
- [pydub](https://github.com/jiaaro/pydub)

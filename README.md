<h2 align="center">Nikki Auto Player</h2>

# Overview 🌟
This is a program that automatically plays custom music scores using instruments in the game [Infinity Nikki](). It supports creating original scores or importing existing ones.
# Features ✨
- ⌨️ 自定义按键映射

- 🔄 支持长按/短按演奏

- 🎸 支持多种乐器演奏

- 📝 灵活的乐谱格式

# Usage 🚀

**Dev**
确保你的操作系统含有[Python 3.10+](https://www.python.org/downloads/) 环境
1. Clone the repository
```bash
git clone https://github.com/teriyakisushi/nikki-auto-player.git
```
1. Install the required packages
```bash
pip install -r requirements.txt
```
1. Run and test the program
```bash
python main.py
```

**User**
1. 从 [Releases]() 处下载最新的版本
2. 双击 `NikkiAutoPlayer.exe` 运行该程序（或者在终端中运行以下命令）
```bash
./NikkiAutoPlayer.exe
```

## 编辑配置文件

打开并修改`config.json`文件，编辑`user_config`字段的内容

- `score_dir`: 乐谱文件夹路径, 默认为目录下的`scores`
- `global_bpm`: 全局BPM, 默认为`120`
- `beat`: 乐谱的拍子数, 默认为`4`，即4/4拍
- `hold_threshold`: 长按阈值, 默认为 0.05s
- `enable_key`：启动演奏按键（当前版本无效）
- `exit_key`：退出演奏按键（当前版本无效）
- `play_interput`：演奏中断按键（当前版本无效）
- `debug`: true/false, 调试模式(输出日志)
- `key_bind`: 按键映射表


# Custom your score 🎵

详细请看 [CUSTOM.md](CUSTOM.md)

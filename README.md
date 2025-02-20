<h2 align="center">Nikki Auto Player</h2>

## Overview 🌟
本项目是为[无限暖暖](https://infinitynikki.nuanpaper.com/home)游戏开发的自动演奏工具，可通过程序自动演奏自定义乐谱。支持原创乐谱创作和现有乐谱导入功能。
## Features ✨
- ⌨️ 自定义按键映射

- 🔄 支持长按/短按演奏

- 🎸 支持多种乐器演奏

- 📝 灵活的乐谱格式

## 使用指南 🚀

**Dev**
确保你的操作系统含有 [Python 3.10+](https://www.python.org/downloads/) 环境，可选`pyinstaller`和`upx`
1. 克隆本仓库
```bash
git clone https://github.com/teriyakisushi/nikki-auto-player.git
```
2. 安装依赖包
```bash
pip install -r requirements.txt
```
3. 运行&测试程序
```bash
python main.py
```

**转译为windows可执行文件(*.exe)**
```bash
pyinstaller build.spec --clean
```
如需添加新模块，可运行`gen_spec.py`生成新的spec配置文件


**User**
1. 从 [Releases](https://github.com/teriyakisushi/nikki-auto-player/releases) 处下载最新的版本
2. 双击 `NikkiAutoPlayer.exe` 运行该程序（或者在终端中运行）
```bash
./NikkiAutoPlayer.exe
```

首次运行时建议选择并试听Demo乐谱《千本樱》进行功能验证

### 编辑配置文件

打开并修改`config.yaml`文件，编辑`user_config`字段的内容

- `score_dir`: 乐谱文件夹路径 (默认:同级目录下的`scores`)
- `global_bpm`: 全局BPM, (默认:120)
- `beat`: 乐谱的拍子数  (默认:4，即4/4拍)
- `hold_threshold`: 长按阈值 *(默认:0.05s)*
- `enable_key`：启动演奏按键
- `exit_key`：退出演奏按键
- `play_interput`：是否允许中断演奏（当前版本按退出键中断）
- `debug`: true/false, 调试日志输出
- `key_bind`: 自定义按键映射表


## Custom your score 🎵

详细请看 [CUSTOM.md](CUSTOM.md)

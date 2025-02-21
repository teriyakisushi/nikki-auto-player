<div align="center">
<p align="right">
<a href="README_EN.md">English</a> | <a href="README.md">中文</a>
</p>
  <img src="./asset/violin.ico" width="80" />
  <h1>Nikki Auto Player</h1>
  <p>为《无限暖暖》打造的自动演奏工具</p>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/github/license/teriyakisushi/nikki-auto-player" alt="License">
    <img src="https://img.shields.io/github/stars/teriyakisushi/nikki-auto-player" alt="Stars">
  </p>
</div>

## ✨ 功能特色

- 🎵 自定义乐谱导入
- ⌨️ 自定义按键映射
- 🎸 支持多种乐器演奏模式
- 🔄 支持长按/短按演奏
- 📝 简洁灵活的乐谱格式

## 🚀 快速开始

### User

1. 从 [Releases](https://github.com/teriyakisushi/nikki-auto-player/releases) 下载最新版本
2. 运行程序:
   ```bash
   双击 NikkiAutoPlayer.exe
   # 或通过命令行运行
   ./NikkiAutoPlayer.exe
   ```
3. 首次运行推荐选择Demo乐谱《千本樱》进行功能体验

### Dev

```bash
# 克隆仓库
git clone https://github.com/teriyakisushi/nikki-auto-player.git

# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py
```

### 构建 windows 可执行文件(Optional)
```bash
pyinstaller build.spec --clean
```
> 如需添加新模块，请先运行 `gen_spec.py` 生成新的spec配置文件，该脚本会自动分析所需依赖

## ⚙️ 配置说明

编辑 `config.yaml` 文件中的 `user_config` 部分：

| 配置项         | 说明           | 默认值           |
| -------------- | -------------- | ---------------- |
| score_dir      | 乐谱文件夹路径 | ./scores         |
| global_bpm     | 全局演奏速度   | 120              |
| beat           | 乐谱拍子数     | 4 (4/4拍)        |
| hold_threshold | 长按判定阈值   | 0.05s            |
| enable_key     | 启动演奏热键   | C                |
| exit_key       | 退出演奏热键   | ESC              |
| play_interput  | 允许中断演奏   | 与`exit_key`一致 |
| debug          | 调试日志开关   | false            |
| key_bind       | 按键映射表     | -                |

## 📝 自定义乐谱

请参考 [CUSTOM.md](CUSTOM.md) 了解更多

## 📄 LICENSE

This program is released under the [MIT License]().
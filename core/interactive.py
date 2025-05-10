import sys
import time
import msvcrt
from pathlib import Path
from core import config, score, Melody, play, press_key as pk
from utils import tools
from utils.logs import log
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import rich.box as box

console = Console()
enable = tools.get_vk_code(config.enable_key)
exit_code = tools.get_vk_code(config.exit_key)


def is_config_not_exists() -> bool:
    return config.is_config_not_exist


def show_welcome():
    score_num = len(score.score_files)
    title = Text("Nikki Auto Player", style="bold magenta")
    content = Text.assemble(
        ("Version: ", "dark_orange"),
        (f"{config.version}\n", "bright_yellow"),
        ("已加载乐谱: ", "dark_orange"),
        (f"{score_num}\n", "bright_yellow"),
        ("1. 开始演奏\n", "bright_white"),
        ("2. 检查乐谱\n", "bright_white"),
        ("3. 导入乐谱\n", "bright_white"),
        ("4. 退出", "bright_white"),

    )

    welcome_panel = Panel(
        content,
        title=title,
        title_align="center",
        border_style="bright_blue",
        padding=(0, 1),
        box=box.ROUNDED,
        width=50,
    )
    console.print(welcome_panel)


def _choose_option() -> int:
    show_welcome()
    op = input("Choose an option: ")
    if op == "1":
        return 1
    elif op == "2":
        return 2
    elif op == "3":
        return 3
    elif op == "4":
        log("See you 😊!", style="bright_yellow", level="INFO")
        sys.exit(0)
    else:
        log("Invalid option", style="bright_red", level="ERROR")


def _wait_for_action() -> int:
    """
    Returns:
        int: 0 - Menu
             1 - Choose another melody
             2 - Replay
    """
    log(f"\n按下启动键 {config.enable_key} 重新演奏，或输入选项:", style="cyan", level="INFO")
    print("0. 返回主菜单")
    print("1. 选择其他乐谱")
    op = ""

    while True:
        if pk.is_key_pressed(enable):
            return 2

        if msvcrt.kbhit():
            char = msvcrt.getch().decode('utf-8')

            if char == '\r':
                if op == "0":
                    return 0
                elif op == "1":
                    return 1
                else:
                    log("ERROR: Invalid op!", style="bright_red", level="ERROR")
                op = ""
            elif char == '\b':
                op = op[:-1]
                print('\r' + ' ' * 20 + '\r' + op, end='', flush=True)
            elif char.isdigit():
                op += char
                print(char, end='', flush=True)

        time.sleep(0.05)


def _start_():
    while True:
        score_list = score.get_score_list()
        log("选择需要演奏的乐曲 (输入0返回)", style="yellow", level="INFO")
        for i, s in enumerate(score_list):
            print(f"{i + 1}. {s}")
            logger.info(f"{i + 1}. {s}")

        try:
            score_num = int(input("Play: "))
            logger.info(f"已选择: {score_num}")
            if score_num == 0:
                return

            if 1 <= score_num <= len(score_list):
                melody = Melody(score.score_files[score_num - 1])
                log(f"已加载乐曲: {melody.music_name}, 按下{config.enable_key}键开启演奏", style="bright_green", level="INFO")

                while True:
                    # wait for start
                    if not _wait_for_key():
                        log("Action: 取消演奏", level="INFO")
                        break

                    try:
                        play.melody_play(melody)
                    except Exception as e:
                        log(f"ERROR: 演奏出错: {str(e)}", style="bright_red", level="ERROR")

                    action = _wait_for_action()
                    if action == 2:
                        continue
                    elif action == 1:
                        break
                    else:
                        return

            else:
                log("ERROR: 无效的乐谱编号!", style="bright_red", level="ERROR")
        except ValueError:
            log("ERROR: 请输入有效的数字!", style="bright_red", level="ERROR")


def _wait_for_key() -> bool:

    while True:
        if pk.is_key_pressed(enable):
            log(f"{config.enable_key} Pressed, Starting", style="bright_green", level="SUCCESS")
            return True
        if pk.is_key_pressed(exit_code):
            return False


def _import_():
    trans_dir = Path("trans")

    if not trans_dir.exists():
        log("ERROR: Trans dir not exists! check your file!", style="bright_red", level="ERROR")
        return

    files_process = [
        f for f in trans_dir.glob("*.*")
        if f.suffix.lower() in [".txt", ".melody"]
    ]

    if not files_process:
        log("WARNING: 没有找到可转换的文件", style="bright_yellow", level="WARNING")
        return

    file_cnt = 0

    for file in files_process:
        try:
            if tools.melody_to_json(str(file)):
                file_cnt += 1

        except Exception as e:
            log(f"ERROR: 处理 {file.name} 时出错: {str(e)}", style="bright_red", level="ERROR")
            continue

    if file_cnt:
        log(f"SUCCESS: 成功转换 {file_cnt} 个文件", style="bright_green", level="SUCCESS")
    else:
        log("WARNING: 没有找到可转换的文件", style="bright_yellow", level="WARNING")


def init():
    if is_config_not_exists():
        sys.exit(0)

    # trans dir
    trans_dir = Path("trans")
    try:
        trans_dir.mkdir(exist_ok=True)

    except Exception as e:
        print(e)
        sys.exit(1)


def main():
    init()
    while True:
        if i := _choose_option():
            if i == 1:
                _start_()
            elif i == 2:
                break
            elif i == 3:
                _import_()
            else:
                break

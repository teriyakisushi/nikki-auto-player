import sys
from pathlib import Path
from core import config, score, Melody, play
from utils import tools
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import rich.box as box
from rich import print as rprint

console = Console()


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
        rprint("[bright_yellow]See you 😊! [/bright_yellow]")
        logger.info("Closing...")
        sys.exit(0)
    else:
        rprint("[red]Invalid option[/red]")
        logger.error("Invalid option")


def _ask_if_continue() -> int:
    print("\n1. Replay")
    print("2. 选择其他乐谱")
    print("0. 返回主菜单")
    answer = input("Choose an option: ")

    if answer == "1":
        return 1
    elif answer == "2":
        return 2
    elif answer == "0":
        return 0
    else:
        rprint("[red]Invalid option, returning to main menu...[/red]")
        logger.error("Invalid option, returning to main menu...")
        return 0


def _start_():
    while True:
        score_list = score.get_score_list()
        rprint("[yellow] 选择需要演奏的乐曲 (输入0返回)[/yellow]")
        logger.info("选择需要演奏的乐曲 (输入0返回)")
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
                rprint(f"[green]Loaded {melody.music_name}[/green]")

                while True:
                    play.melody_play(melody)
                    choice = _ask_if_continue()

                    if choice == 0:
                        return
                    elif choice == 2:
                        break

            else:
                rprint("[red]Invalid score number![/red]")
                logger.error("Invalid score number!")
        except ValueError:
            rprint("[red]Please enter a valid number![/red]")
            logger.error("Please enter a valid number!")


def _check_():
    pass


def _import_():
    rprint("[cyan]请将旋律文件放入目录下的 trans 文件夹中[/cyan]")
    trans_dir = Path("trans")

    if not trans_dir.exists():
        rprint("[red]Trans dir not exists! check your file![/red]")
        logger.error("Trans dir not exists! check your file!")
        return

    files_process = [
        f for f in trans_dir.glob("*.*")
        if f.suffix.lower() in [".txt", ".melody"]
    ]

    if not files_process:
        rprint("[yellow]没有找到可转换的文件[/yellow]")
        logger.warning("没有找到可转换的文件")
        return

    file_cnt = 0

    for file in files_process:
        try:
            if tools.melody_to_json(str(file)):
                file_cnt += 1

        except Exception as e:
            rprint(f"[red]处理 {file.name} 时出错: {str(e)}[/red]")
            logger.error(f"处理 {file.name} 时出错: {str(e)}")
            continue

    if file_cnt:
        rprint(f"[green]成功转换 {file_cnt} 个文件[/green]")
        logger.success(f"成功转换 {file_cnt} 个文件")
    else:
        rprint("[yellow]没有找到可转换的文件[/yellow]")
        logger.warning("没有找到可转换的文件")


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

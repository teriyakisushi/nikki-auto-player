import sys
from config import tconfig
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import rich.box as box
# from rich import print as rprint

console = Console()


# def init():
#     console.clear()
#     title = Text("Nikki Auto Player", style="bold magenta")
#     content = Text.assemble(
#         (t("version"), "dark_orange"),
#         (f"{config.version}\n", "bright_yellow"),
#     )

def is_config_not_exists() -> bool:
    return tconfig.is_config_not_exist


def show_welcome():
    title = Text("Nikki Auto Player", style="bold magenta")
    content = Text.assemble(
        ("Version: ", "dark_orange"),
        (f"{tconfig.version}\n", "bright_yellow"),
        ("Loaded Score file: ", "dark_orange"),
        (f"{tconfig.load_score}\n", "bright_yellow"),
        ("1. Start Auto Player\n", "bright_white"),
        ("2. Check Score\n", "bright_white"),
        ("3. Exit", "bright_white"),

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
    option = input("Choose an option: ")
    if option == "1":
        return 1
    elif option == "2":
        return 2
    elif option == "3":
        sys.exit(0)
    else:
        print("Invalid option")


def _test_interface(score: list):
    print(f"Playing {score['score_name']}...")


def _start_interface():
    print("Choose a score to play, 0 to go back")
    for i, v in enumerate(tconfig._get_scores()):
        print(f"{i + 1}. {v['score_name']}")

    score = int(input("Choose a score: "))
    if score:
        _test_interface(tconfig._get_scores()[int(score) - 1])
    if score == 0:
        return


def _check_interface():
    print("Choose a score to check, 0 to go back")
    for i, v in enumerate(tconfig._get_scores()):
        print(f"{i + 1}. {v['score_name']}")

    score = int(input("Choose a score: "))
    if score:
        print(f"Checking {tconfig._get_scores()[int(score) - 1]['score_name']}...")
    if score == 0:
        return


def init():
    if is_config_not_exists():
        sys.exit(0)


if __name__ == '__main__':
    init()
    while True:
        if i := _choose_option():
            if i == 1:
                _start_interface()
            elif i == 2:
                _check_interface()

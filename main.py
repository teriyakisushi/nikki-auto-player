from core.interactive import main
from rich import print as rprint


def handle_exit():
    print("\n")
    rprint("[yellow]请问你要？[/yellow]")
    print("1. 退出程序")
    print("2. 返回主菜单")

    try:
        choice = input("选择 (1/2): ").strip()
        if choice == "1":
            rprint("[bright_yellow]See you 😊! [/bright_yellow]")
            return True
        elif choice == "2":
            rprint("[green]Restart Menu[/green]")
            return False
        else:
            rprint("[yellow]invalid op, program closing[/yellow]")
            return True
    except KeyboardInterrupt:
        print("\n")
        rprint("[bright_yellow]See you 😊! [/bright_yellow]")
        return True


def run():
    while True:
        try:
            main()
        except KeyboardInterrupt:
            if handle_exit():
                break


if __name__ == "__main__":
    run()

def convert_melody_text(file_path: str) -> list:
    """
    将文本格式的旋律转换为tuple列表

    Args:
        file_path (str)
    Returns:
        list: (note, duration) tuple list
    """
    melody_list = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # filter empty lines and comments
            lines = [line.strip() for line in f.readlines()
                     if line.strip() and not line.strip().startswith('//')]

            for line in lines:
                # separate note and duration
                parts = line.split()
                if len(parts) == 2:
                    # if duration is provided
                    note, duration = parts
                    melody_list.append((note, duration))
                elif len(parts) == 1:
                    # if no duration, set default duration to 0
                    note = parts[0]
                    melody_list.append((note, 0))

        return melody_list

    except FileNotFoundError:
        raise FileNotFoundError(f"Cannot found: {file_path}")
    except Exception as e:
        raise Exception(f"Something wrong: {str(e)}")


if __name__ == "__main__":
    try:
        # transform melody text to tuple list
        melody = convert_melody_text("melody_demo.txt")

        print("res:")
        print("melody = [")
        for note, duration in melody:
            print(f"    ('{note}', '{duration}'),")
        print("]")

        with open("melody_output.py", "w", encoding='utf-8') as f:
            f.write("melody = [\n")
            for note, duration in melody:
                f.write(f"    ('{note}', '{duration}'),\n")
            f.write("]\n")

    except Exception as e:
        print(f"err: {str(e)}")

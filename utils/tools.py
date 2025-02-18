import win32con
import json
from pathlib import Path
from core import config, score
from loguru import logger
from typing import List, Dict, Union

GLOBAL_BPM = config.get('user_config', {}).get('bpm', 120)


# get vk code
def get_vk_code(key_name: str) -> int:
    """
    string -> win32con.VK_*

    Args:
        key_name (str)
    Returns:
        int
    """
    key_mapping = {
        'F1': win32con.VK_F1,
        'F2': win32con.VK_F2,
        'F3': win32con.VK_F3,
        'F4': win32con.VK_F4,
        'F5': win32con.VK_F5,
        'F6': win32con.VK_F6,
        'F7': win32con.VK_F7,
        'F8': win32con.VK_F8,
        'F9': win32con.VK_F9,
        'F10': win32con.VK_F10,
        'F11': win32con.VK_F11,
        'F12': win32con.VK_F12,
        'ESC': win32con.VK_ESCAPE,
        'ESCAPE': win32con.VK_ESCAPE,
        'TAB': win32con.VK_TAB,
        'SPACE': win32con.VK_SPACE,
        'RETURN': win32con.VK_RETURN,
        'ENTER': win32con.VK_RETURN,
        'BACKSPACE': win32con.VK_BACK,
        'DELETE': win32con.VK_DELETE,
        'DEL': win32con.VK_DELETE,
        'CTRL': win32con.VK_CONTROL,
        'CONTROL': win32con.VK_CONTROL,
        'ALT': win32con.VK_MENU,
        'SHIFT': win32con.VK_SHIFT,
        'UP': win32con.VK_UP,
        'DOWN': win32con.VK_DOWN,
        'LEFT': win32con.VK_LEFT,
        'RIGHT': win32con.VK_RIGHT,
        'CAPSLOCK': win32con.VK_CAPITAL,
        'NUMLOCK': win32con.VK_NUMLOCK,
        'SCROLLLOCK': win32con.VK_SCROLL,
    }

    # Letter keys
    for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        key_mapping[c] = ord(c)

    # Nums keys
    for n in '0123456789':
        key_mapping[n] = ord(n)

    # case-insensitive
    key_upper = key_name.upper()
    if key_upper in key_mapping:
        return key_mapping[key_upper]
    else:
        raise ValueError(f"这个按键不支持喵: {key_name}，请自行添加")


# calculate duration
def calculate_duration(beat_value=None, bpm=None):
    """
    计算音符持续时间

    Args:
        beat_value: 时值标记
        bpm: 当前速度，None则使用全局速度

    Returns:
        float: 持续时间(秒)
    """
    # 使用当前部分的 BPM 或 谱子全局 BPM
    cur_beat = 60 / (bpm if bpm else GLOBAL_BPM)

    if beat_value is None or beat_value == 'b':
        return cur_beat

    if isinstance(beat_value, (int, float)):
        return float(beat_value)

    if beat_value.startswith('b*'):  # 乘数
        try:
            muNum = float(beat_value[2:])
            return cur_beat * muNum
        except ValueError:
            logger.error(f"Invalid format: {beat_value}")
            return cur_beat

    if beat_value == 'b2':  # 延长一拍
        return cur_beat * 2

    if beat_value == 'b.':  # 附点音符
        return cur_beat * 1.5

    if beat_value == 'b._':  # 附点音符2
        return cur_beat * 0.75

    if beat_value == 'b_':  # 半拍
        return cur_beat * 0.5

    if beat_value == 'b__':  # 四分之一拍
        return cur_beat * 0.25

    if beat_value.startswith('b/'):
        d = int(beat_value[2:])
        if not d:
            raise ValueError("Invalid format!")
        return cur_beat / d

    return cur_beat


# read melody
def read_melody(melody: list = None) -> List[Dict[str, Union[str, int, list]]]:
    """
    从全局score实例中读取并解析所有乐谱文件

    Args:
        melody (list, optional): 默认值设为None，用于向后兼容

    Returns:
        List[Dict]: 包含所有乐谱数据的列表，每个字典包含完整的乐谱信息
    """
    if melody is not None:
        return melody

    all_melodies = []

    for file_path in score.score_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # check required args
            required_fields = ['nikki_player_version', 'instrument', 'music_name', 'bpm', 'melody']
            if not all(field in data for field in required_fields):
                logger.warning(f"{file_path} probably doesn't match the melody file format\n该文件可能非本项目支持的乐谱文件格式")
                continue

            # check version
            if not is_support_version(data['nikki_player_version']):
                pass

            # logger.success(f"{file_path} Loaded")
            # logger.info(f"Version: {data['nikki_player_version']}")
            # logger.info(f"Instructment: {data['instrument']}")
            # logger.info(f"Music Name: {data['music_name']}")
            # logger.info(f"BPM: {data['bpm']}")

            all_melodies.append(data)

        except json.JSONDecodeError:
            logger.error(f"JSON Decode Error: {file_path}")
            continue
        except FileNotFoundError:
            logger.error(f"Could not Found: {file_path}")
            continue
        except Exception as e:
            logger.error(f"{file_path}: {str(e)}")
            continue

    return all_melodies


# process melody note
def process_melody_note(note_tuple):
    """
    预处理

    Args:
        note_tuple (tuple)

    Returns:
        tuple
    """
    note, duration = note_tuple

    # perhaps it's a special note (I mean, extra note)
    if duration == 0 or duration == '0':
        note_str = str(note)
        if note_str.endswith('__'):
            # e.g. 1#__ -> ('1#', 'b__')
            base_note = note_str[:-2]
            return (base_note, 'b__')
        elif note_str.endswith('_'):
            # e.g. 3_ -> ('3', 'b_')
            base_note = note_str[:-1]
            return (base_note, 'b_')

    return note_tuple


# check version
def is_support_version(cur_version: str) -> bool:
    """
    Args:
        cur_version (str)

    Returns:
        bool
    """
    if cur_version != '1.0':
        logger.warning(f"Current version probably doesn't match the melody file: {cur_version}")
        return False
    return True


def melody_to_json(file_path: str) -> bool:
    try:
        json_data = {
            "nikki_player_version": "1.0",
            "instrument": "violin",
            "music_name": "untitled",
            "bpm": 120,
            "melody": []
        }

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('//')]

        # 解析头部信息
        current_line = 0
        header_fields = {"version": "nikki_player_version", "instrument": "instrument", "music_name": "music_name", "bpm": "bpm"}

        for i, line in enumerate(lines):
            parts = line.split(maxsplit=1)
            if len(parts) == 2 and parts[0].lower() in header_fields:
                field = header_fields[parts[0].lower()]
                value = parts[1].strip()

                if field == "bpm":
                    try:
                        value = int(value)
                    except ValueError:
                        logger.warning(f"Invalid BPM value: {value}, using default")
                        continue
                json_data[field] = value
                current_line = i + 1
            else:
                break

        # melody
        melody_list = []
        for line in lines[current_line:]:
            if not line.strip() or line.startswith('//'):
                continue

            parts = line.split()
            if len(parts) == 2:
                note, duration = parts
                melody_list.append([note, duration])
            elif len(parts) == 1:
                # set default duration to 0
                melody_list.append([parts[0], "0"])

        json_data["melody"] = melody_list

        score_dir = Path("score")
        score_dir.mkdir(exist_ok=True)

        file_name = Path(file_path).name
        transed_file = score_dir / f"{Path(file_name).stem}.json"

        with open(transed_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)

        logger.success(f"Successfully converted {file_path} to {transed_file}")
        return True

    except FileNotFoundError:
        logger.error(f"err: {file_path}")
    except Exception as e:
        logger.error(f"err: {str(e)}")

    return False


'''
if __name__ == "__main__":
    try:
        melody_data = read_melody(file_path='miku.json', is_file=True)
        print(melody_data[-4:-5])
    except Exception as e:
        raise e
'''

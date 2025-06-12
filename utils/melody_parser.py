import json
import re
from pathlib import Path
from loguru import logger


def melody_parser(version: int = 1, file_path: str = ''):
    """
    Parse a melody file and convert it to JSON format.
    Args:
        version (int): Version of the parser to use. Default is 1.
        file_path (str): Path to the melody file.
    Returns:
        bool: True if conversion is successful, False otherwise.
    """
    if version == 1:
        return melody_to_json(file_path)
    elif version == 2:
        return melody_to_json_v2(file_path)
    else:
        raise ValueError(f"Unsupported version: {version}. Supported versions are 1 and 2.")


# v1 parser
def melody_to_json(file_path: str = '') -> bool:
    '''
    Convert a melody file to JSON format by using v1 parser
    Args:
        file_path (str): Path to the melody file.
    Returns:
        bool: True if conversion is successful, False otherwise.
    '''
    try:
        json_data = {
            "nikki_player_version": "1.0",
            "instrument": "violin",
            "music_name": "untitled",
            "bpm": 120,
            "timeSig": "4/4",
            "melody": []
        }

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('//')]

        # head fields
        current_line = 0
        header_fields = {"version": "nikki_player_version", "instrument": "instrument", "music_name": "music_name", "bpm": "bpm", "timeSig": "timeSig"}

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


# v2 Parser
def _parse_header_v2(header_text: str) -> dict:
    """解析v2格式的头部信息"""
    header = {
        'music_name': 'Untitled',
        'nkver': '2.0',
        'instrument': 'violin',
        'bpm': 120,
        'timeSig': '4/4'
    }

    for line in header_text.split('\n'):
        line = line.strip()
        if not line or ':' not in line:
            continue

        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()

        if key == 'bpm':
            try:
                value = int(value)
            except ValueError:
                logger.warning(f"Invalid BPM value: {value}, using default 120")
                value = 120

        header[key] = value

    return header


def _expand_grouped_notes(line: str) -> str:
    """展开分组的音符表示法"""
    pattern = r'\(\s*([\d#\s]+)\s*\)(_+)'

    while re.search(pattern, line):
        match = re.search(pattern, line)
        if not match:
            break

        group = match.group(0)
        notes_text = match.group(1)
        rhythm = match.group(2)

        # 提取音符
        notes = re.findall(r'[0-7][#]?', notes_text)
        replacement = ' '.join([f"{n}{rhythm}" for n in notes])
        line = line.replace(group, ' ' + replacement + ' ')

    return line


def _parse_melody_v2(melody_text: str) -> list:
    """解析v2格式的乐谱内容"""
    melody = []
    lines = melody_text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # barline
        if line.startswith('@@'):
            parts = line.split('@@', 1)[1].strip()
            melody.append(["@@", parts])
            continue

        # bpm and timeSig changes
        if line.startswith('bpm'):
            parts = line.split('bpm', 1)[1].strip()
            melody.append(["bpm", parts])
            continue
        elif line.startswith('timeSig'):
            parts = line.split('timeSig', 1)[1].strip()
            melody.append(["timeSig", parts])
            continue

        # remove comments
        line = line.replace('|', ' ')

        # grouped notes
        line = _expand_grouped_notes(line)

        tokens = line.split()
        i = 0

        while i < len(tokens):
            token = tokens[i].strip()

            # basic note matching
            note_match = re.match(r'^([0-7][#]?)(.*)$', token)
            if note_match:
                note, modifiers = note_match.groups()

                # duration defaults
                if modifiers:
                    duration = modifiers
                else:
                    duration = "b"

                melody.append([note, duration])
                i += 1

                # extend duration with following dashes
                while i < len(tokens) and tokens[i] == '-':
                    if melody[-1][1] == 'b':
                        melody[-1][1] = '-'
                    else:
                        melody[-1][1] += '-'
                    i += 1

                continue

            # 单独的延音符
            if token == '-':
                if melody and not melody[-1][0].startswith('@@'):
                    if melody[-1][1] == 'b':
                        melody[-1][1] = '-'
                    else:
                        melody[-1][1] += '-'
                i += 1
                continue

            # skip unknown tokens
            i += 1

    return melody


def melody_to_json_v2(file_path: str = '') -> bool:
    """
    Convert a melody file to JSON format by using v2 parser

    Args:
        file_path (str): Path to the melody file.

    Returns:
        bool: True if conversion is successful, False otherwise.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # check for the presence of '---' to separate header and melody
        if '---' in content:
            parts = content.split('---', 2)
            if len(parts) < 3:
                logger.error("Missing proper separator '---'")
                return False

            header_text = parts[1].strip()
            melody_text = parts[2].strip()
            header = _parse_header_v2(header_text)
        else:
            # use default header if no separator found
            # melody_text = content
            # header = {
            #     'music_name': 'Untitled',
            #     'nkver': '2.0',
            #     'instrument': 'violin',
            #     'bpm': 120,
            #     'timeSig': '4/4'
            # }
            logger.info(f"skipping {file_path}, No v2 melody")
            return False

        melody = _parse_melody_v2(melody_text)

        json_data = header.copy()
        json_data['melody'] = melody

        score_dir = Path("score")
        score_dir.mkdir(exist_ok=True)

        file_name = Path(file_path).name
        transed_file = score_dir / f"{Path(file_name).stem}.json"

        with open(transed_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)

        logger.success(f"Successfully converted {file_path} to {transed_file}")
        return True

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")

    return False

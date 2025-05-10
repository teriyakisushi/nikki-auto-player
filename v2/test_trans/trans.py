import json
import re
import os
import sys


def parse_melody_file(file_path: str) -> dict:
    """解析简谱文件为JSON格式"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if '---' in content:
        parts = content.split('---', 2)
        if len(parts) < 3:
            raise ValueError("缺少适当的分隔符 '---'")

        header_text = parts[1].strip()
        melody_text = parts[2].strip()
        header = parse_header(header_text)
    else:
        # use default
        melody_text = content
        header = {
            'music_name': 'Untitled',
            'nkver': '1.0',
            'instrument': 'violin',
            'bpm': 120,
            'timeSig': '4/4'
        }

    melody = parse_melody(melody_text)

    result = header.copy()
    result['melody'] = melody

    return result


def parse_header(header_text: str) -> dict:
    """解析头部信息为字典"""
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
                print(f"警告: bpm值 '{value}' 不是有效的整数，使用默认值120")
                value = 120

        header[key] = value

    return header


def expand_grouped_notes(line: str) -> str:
    pattern = r'\(\s*([\d#\s]+)\s*\)(_+)'

    while re.search(pattern, line):
        match = re.search(pattern, line)
        if not match:
            break

        group = match.group(0)
        notes_text = match.group(1)
        rhythm = match.group(2)

        # Notes
        notes = re.findall(r'[0-7][#]?', notes_text)
        replacement = ' '.join([f"{n}{rhythm}" for n in notes])
        line = line.replace(group, ' ' + replacement + ' ')

    return line


def parse_melody(melody_text: str) -> list:
    """解析乐谱内容为列表"""
    melody = []
    lines = melody_text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Bar Line
        if line.startswith('@@'):
            parts = line.split('@@', 1)[1].strip()
            melody.append(["@@", parts])
            continue

        # Change bpm or timeSig
        if line.startswith('bpm'):
            parts = line.split('bpm', 1)[1].strip()
            melody.append(["bpm", parts])
            continue
        elif line.startswith('timeSig'):
            parts = line.split('timeSig', 1)[1].strip()
            melody.append(["timeSig", parts])
            continue

        # remove separators
        line = line.replace('|', ' ')

        # grouped notes
        line = expand_grouped_notes(line)

        tokens = line.split()
        i = 0

        while i < len(tokens):
            token = tokens[i].strip()

            note_match = re.match(r'^([0-7][#]?)(.*)$', token)
            if note_match:
                note, modifiers = note_match.groups()

                # notes持续时间
                if modifiers:
                    duration = modifiers
                else:
                    duration = "b"

                melody.append([note, duration])
                i += 1

                # Add additional modifiers
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

            # Skip unknown tokens
            i += 1

    return melody


def bmelody_to_json(txt_file_path: str, json_file_path: str = None) -> str:
    """转换为JSON文件"""
    try:
        result = parse_melody_file(txt_file_path)

        if json_file_path is None:
            # 默认输出与输入同名但扩展名为.json的文件
            base_name = os.path.splitext(txt_file_path)[0]
            json_file_path = f"{base_name}.json"

        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"转换成功! JSON文件已保存到: {json_file_path}")
        return json_file_path

    except Exception as e:
        print(f"转换过程中出错: {str(e)}")
        return None


def main():

    txt_file = sys.argv[1]

    if len(sys.argv) > 2:
        json_file = sys.argv[2]
    else:
        json_file = None

    bmelody_to_json(txt_file, json_file)


if __name__ == "__main__":
    main()

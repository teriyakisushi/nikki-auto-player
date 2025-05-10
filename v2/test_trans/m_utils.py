import re


def parse_header(self, header_text: str) -> dict:
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

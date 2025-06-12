import time
import random
import pyautogui
from utils import tools
from utils.vkcode import get_vk_code
from loguru import logger
from utils.logs import log
from . import press_key_hum as pk
from core import config, Melody

GLOBAL_BPM = config.global_bpm


def add_humanization(duration: float, note_velocity: float = 1.0, is_critical: bool = False) -> tuple[float, float]:
    """
    添加人性化处理

    Args:
        duration: 原始时长
        note_velocity: 音符力度 (0.5-1.5)
        is_critical: 是否为关键音符（长音符、重要节拍点等），关键音符的时间偏移更小

    Returns:
        (微调后的时长, 按键力度系数)
    """
    # 关键音符的时间偏移更小，保持节奏稳定
    if is_critical:
        timing_variance = random.uniform(-0.005, 0.005)  # ±0.5%
    else:
        timing_variance = random.uniform(-0.015, 0.015)  # ±1.5%

    humanized_duration = duration * (1 + timing_variance)

    # 力度随机化 - 保持在合理范围内
    velocity_variance = random.uniform(0.85, 1.15) * note_velocity

    return humanized_duration, velocity_variance


def calculate_phrase_context(pmelody, current_index, window_size=5):
    """
    分析当前音符在乐句中的上下文

    Returns:
        dict: 包含乐句位置、音符密度等信息
    """
    start_idx = max(0, current_index - window_size)
    end_idx = min(len(pmelody), current_index + window_size + 1)
    window = pmelody[start_idx:end_idx]

    # 计算音符密度（非休止符的比例）
    actual_notes = [n for n, _ in window if n not in [0, '0', '@@', 'bpm', 'timeSig']]
    density = len(actual_notes) / len(window) if window else 0

    # 判断是否在乐句开头/结尾
    is_phrase_start = current_index == 0 or pmelody[current_index-1][0] in ['@@', 0, '0']
    is_phrase_end = (current_index == len(pmelody)-1 or
                     (current_index+1 < len(pmelody) and pmelody[current_index+1][0] in ['@@', 0, '0']))

    return {
        'density': density,
        'is_phrase_start': is_phrase_start,
        'is_phrase_end': is_phrase_end,
        'position_in_phrase': (current_index - start_idx) / max(1, len(window)-1)
    }


def melody_play(melody: Melody) -> None:
    '''
    播放旋律数据
    '''
    pyautogui.FAILSAFE = True
    log("Action: Playing melody...", level="INFO")

    # 严格的时间控制
    start_time = time.time()
    accumulated_time = 0.0

    cur_notes = []
    current_bpm = melody.bpm
    current_timeSignature = "4/4"

    # 音乐表现相关变量
    consecutive_notes = 0
    # last_was_rest = False
    phrase_breath_count = 0  # 乐句间的呼吸计数

    # 预处理旋律数据
    pmelody = [tools.process_melody_note(note_tuple) for note_tuple in melody.melody]

    for i, (note, beat_value) in enumerate(pmelody):
        # 检查退出
        if pk.is_key_pressed(get_vk_code(config.exit_key)):
            log("演奏已中断", style="bright_yellow", level="INFO")
            return

        # 分析当前音符的上下文
        context = calculate_phrase_context(pmelody, i)

        # 预测下一个音符
        next_note = None
        if i + 1 < len(pmelody):
            next_note = pmelody[i + 1][0]

        # 严格按照累积时间等待
        target_time = start_time + accumulated_time
        current_time = time.time()
        if current_time < target_time:
            time.sleep(target_time - current_time)

        # BPM变化处理
        if note == 'bpm':
            try:
                current_bpm = float(beat_value)
                log(f"BPM changed to: {current_bpm}", style="cyan", level="INFO")
                continue
            except (ValueError, TypeError):
                log(f"Invalid BPM value: {beat_value}", style="red", level="ERROR")
                continue

        # 拍号变化处理
        if note == "timeSig":
            try:
                current_timeSignature = beat_value
                log(f"Time signature changed to: {current_timeSignature}", style="cyan", level="INFO")
                continue
            except Exception:
                log(f"Invalid time signature value: {beat_value}", style="red", level="ERROR")
                continue

        # Section处理
        if note == '@@':
            if cur_notes:
                log(f"Notes: {' '.join(cur_notes)}", style="yellow", level="DEBUG")
                cur_notes = []

            log(f"cur section {beat_value} (BPM: {current_bpm})", style="bright_blue", level="INFO")

            # Section间的音乐性停顿
            phrase_breath_count += 1
            if phrase_breath_count % 4 == 0:  # 每4个section来一次更长的停顿
                breath_time = random.uniform(0.08, 0.2)
            else:
                breath_time = random.uniform(0.03, 0.08)

            time.sleep(breath_time)
            accumulated_time += breath_time
            consecutive_notes = 0
            continue

        try:
            # 计算基础时长
            base_duration = tools.calculate_duration(beat_value, current_bpm, current_timeSignature)

            # 判断是否为关键音符（长音符或重要节拍位置）
            is_critical_note = (base_duration >= config.hold_threshold or context['is_phrase_start'] or context['is_phrase_end'])

            # 音乐表现力计算
            note_velocity = 1.0

            # 乐句开头稍强
            if context['is_phrase_start']:
                note_velocity = min(1.2, note_velocity + 0.15)

            # 乐句结尾渐弱
            if context['is_phrase_end']:
                note_velocity = max(0.8, note_velocity - 0.1)

            # 高密度段落稍弱，营造层次感
            if context['density'] > 0.8:
                note_velocity = max(0.7, note_velocity - 0.2)

            # 连续音符的微妙变化
            if consecutive_notes > 0:
                cycle_position = consecutive_notes % 4
                if cycle_position == 0:  # 每4个音符的第一个稍强
                    note_velocity = min(1.1, note_velocity + 0.05)
                elif cycle_position == 3:  # 第4个稍弱
                    note_velocity = max(0.9, note_velocity - 0.05)

            # 人性化处理（但保持时间准确性）
            duration, velocity_factor = add_humanization(base_duration, note_velocity, is_critical_note)

            # 休止符处理
            if note == 0 or note == '0':
                cur_notes.append('0')
                # last_was_rest = True
                consecutive_notes = 0
                # 休止符严格按照原时长，不添加随机性
                accumulated_time += base_duration
            else:
                try:
                    key = config.key_mapping[str(note)].lower()
                    cur_notes.append(str(note))
                    consecutive_notes += 1
                    # last_was_rest = False
                except KeyError:
                    log(f"Unknown note: {note}, skipped.", style="yellow", level="WARNING")
                    accumulated_time += base_duration
                    continue

                # 连奏检测
                is_legato = (next_note and next_note not in [0, '0', '@@', 'bpm', 'timeSig'])

                # 按键处理
                if base_duration >= config.hold_threshold:
                    # 长音符：严格控制持续时间，只在力度上添加表现力
                    actual_hold_time = base_duration * 0.95  # 稍微缩短避免重叠
                    if is_legato:
                        actual_hold_time *= 0.98
                    pk.hold_key(key, actual_hold_time, velocity_factor)
                else:
                    # 短音符：只调整力度，不改变时长
                    pk.press_key(key, velocity_factor)

                # 时间累积严格按照原始节拍
                accumulated_time += base_duration

                # 只在非关键位置添加微小的人性化延迟
                if not is_critical_note and random.random() < 0.3:
                    micro_delay = random.uniform(0.001, 0.003)
                    time.sleep(micro_delay)
                    accumulated_time += micro_delay

        except ValueError:
            log(f"Invalid value: {beat_value}, Skipped", style="red", level="ERROR")
            continue
        except Exception as e:
            log(f"Fault: {note} {beat_value}, Skipped", style="red", level="ERROR")
            logger.error(f"err: {str(e)}")
            continue

    # 最后的音符
    if cur_notes:
        log(f"Notes: {' '.join(cur_notes)}", style="cyan", level="DEBUG")

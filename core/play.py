import time
import pyautogui
from utils import tools
from loguru import logger
from utils.logs import log
from . import press_key as pk
from core import config, Melody
# from rich import print as rprint

GLOBAL_BPM = config.global_bpm


def melody_play(melody: Melody):
    '''
    Returns:
        bool: True - done
              False - interrupt or exit
    '''
    pyautogui.FAILSAFE = True
    log("Action: Playing melody...", level="INFO")
    next_note_time = time.time()
    cur_notes = []  # this section's notes
    current_bpm = melody.bpm

    # logger.info(f"Cur: {melody.melody}")

    # 预处理旋律数据
    pmelody = [tools.process_melody_note(note_tuple) for note_tuple in melody.melody]

    # logger.info(pmelody)

    for i, (note, beat_value) in enumerate(pmelody):
        # check if exit
        if pk.is_key_pressed(tools.get_vk_code(config.exit_key)):
            log("演奏已中断", style="bright_yellow", level="INFO")
            return

        cur_time = time.time()
        if cur_time < next_note_time:
            time.sleep(next_note_time - cur_time)

        if note == 'bpm':
            try:
                current_bpm = float(beat_value)
                log(f"BPM changed to: {current_bpm}", style="cyan", level="INFO")
                continue
            except (ValueError, TypeError):
                log(f"Invalid BPM value: {beat_value}", style="red", level="ERROR")
                continue

        # 遇到新的Section时，先输出之前收集的音符
        if note == '@@':
            if cur_notes:
                log(f"Notes: {' '.join(cur_notes)}", style="yellow", level="DEBUG")
                cur_notes = []

            log(f"cur section {beat_value} (BPM: {current_bpm})", style="bright_blue", level="INFO")
            continue

        try:
            # 使用当前BPM计算时值
            duration = tools.calculate_duration(beat_value, current_bpm)

            # 休止符
            if note == 0 or note == '0':
                cur_notes.append('0')
                time.sleep(duration * 0.96)
            else:
                try:
                    key = config.key_mapping[str(note)].lower()
                    cur_notes.append(str(note))
                except KeyError:
                    log(f"Unknown note: {note}, skipped.", style="yellow", level="WARNING")
                    continue

                # 长按/短按
                if duration >= config.hold_threshold:
                    pk.hold_key(key, duration)
                else:
                    pk.press_key(key)
                    time.sleep(duration * 0.92)

            next_note_time = cur_time + duration
            time.sleep(min(0.01, duration * 0.05))

        except ValueError:
            log(f"Invalid value: {beat_value}, Skipped", style="red", level="ERROR")
            continue
        except Exception as e:
            log(f"Fault: {note} {beat_value}, Skipped", style="red", level="ERROR")
            logger.error(f"err: {str(e)}")
            continue

    # last notes
    if cur_notes:
        log(f"Notes: {' '.join(cur_notes)}", style="cyan", level="DEBUG")

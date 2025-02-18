import time
from . import press_key as pk
import pyautogui
from loguru import logger
from rich import print as rprint
from core import config, Melody
from utils import tools

GLOBAL_BPM = config.global_bpm


# def init(melody: Melody):
#     melody = Melody(melody)
#     return melody


def melody_play(melody: Melody):
    pyautogui.FAILSAFE = True
    rprint("[bright]Playing melody...[/bright]")
    logger.info("Playing melody...")
    # melody = init(melody)
    next_note_time = time.time()
    cur_notes = []  # this section's notes
    current_bpm = melody.bpm

    # logger.info(f"Cur: {melody.melody}")

    # 预处理旋律数据
    pmelody = [tools.process_melody_note(note_tuple) for note_tuple in melody.melody]

    # logger.info(pmelody)

    for i, (note, beat_value) in enumerate(pmelody):
        cur_time = time.time()
        if cur_time < next_note_time:
            time.sleep(next_note_time - cur_time)

        if note == 'bpm':
            try:
                current_bpm = float(beat_value)
                rprint(f"[cyan]BPM changed to: {current_bpm}[/cyan]")
                logger.info(f"BPM changed to: {current_bpm}")
                continue
            except (ValueError, TypeError):
                rprint("[red]Invalid BPM value![/red]")
                logger.error(f"Invalid BPM value: {beat_value}")
                continue

        # 遇到新的Section时，先输出之前收集的音符
        if note == '@@':
            if cur_notes:
                rprint(f"[bright_yellow]Notes: {' '.join(cur_notes)}[/bright_yellow]")
                logger.debug(f"Notes: {' '.join(cur_notes)}")
                cur_notes = []

            rprint(f"[bright_blue]Section: {beat_value}[/bright_blue]")
            logger.info(f"cur section {beat_value} (BPM: {current_bpm})")
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
                    rprint(f"[bright_yellow]Unknown note: {note}, skipped.[/bright_yellow]")
                    logger.warning(f"Unknown note: {note}, skipped.")
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
            rprint(f"[red]Invalid value: {beat_value}, Skipped[/red]")
            logger.error(f"invalid value: {beat_value}，Skipped")
            continue
        except Exception as e:
            rprint(f"[red]Fault: {note} {beat_value}, Skipped[/red]")
            logger.error(f"Fault: {note} {beat_value}，Skipped")
            logger.error(f"err: {str(e)}")
            continue

    # last notes
    if cur_notes:
        rprint(f"[cyan]Notes: {' '.join(cur_notes)}[/cyan]")
        logger.debug(f"Notes: {' '.join(cur_notes)}")

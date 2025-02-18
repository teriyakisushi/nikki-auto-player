import time
import tools
from loguru import logger
from map import notes_mapping
from melody_deal import hold_key, press_key, is_key_pressed


hold_threshold = 0.05


def play_melody():
    logger.info("Playing melody...")
    next_note_time = time.time()
    cur_notes = []  # this section's notes
    current_bpm = CURRENT_BPM

    # 预处理旋律数据
    pmelody = [tools.process_melody_note(note_tuple) for note_tuple in melody]

    for i, (note, beat_value) in enumerate(pmelody):
        cur_time = time.time()
        if cur_time < next_note_time:
            time.sleep(next_note_time - cur_time)

        if note == 'bpm':
            try:
                current_bpm = float(beat_value)
                logger.info(f"BPM changed to: {current_bpm}")
                continue
            except (ValueError, TypeError):
                logger.error(f"Invalid BPM value: {beat_value}")
                continue

        # 遇到新的Section时，先输出之前收集的音符
        if note == '@@':
            if cur_notes:
                logger.debug(f"Notes: {' '.join(cur_notes)}")
                cur_notes = []
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
                    key = notes_mapping[str(note)].lower()
                    cur_notes.append(str(note))
                except KeyError:
                    logger.warning(f"Unknown note: {note}, skipped.")
                    continue

                # 长按/短按
                if duration >= hold_threshold:
                    hold_key(key, duration)
                else:
                    press_key(key)
                    time.sleep(duration * 0.92)

            next_note_time = cur_time + duration
            time.sleep(min(0.01, duration * 0.05))

        except ValueError:
            logger.error(f"invalid value: {beat_value}，Skipped")
            continue
        except Exception as e:
            logger.error(f"Fault: {note} {beat_value}，Skipped")
            logger.error(f"err: {str(e)}")
            continue

    # last notes
    if cur_notes:
        logger.debug(f"Notes: {' '.join(cur_notes)}")


if __name__ == '__main__':
    from ref import Melody
    object = 'miku.json'
    r_melody = Melody(object)
    melody = r_melody.melody
    CURRENT_BPM = r_melody.bpm
    # print(f"Current BPM: {CURRENT_BPM}\nMelody: {melody}")
    print("Press C to start playing")
    while True:
        if is_key_pressed('C'):
            play_melody()
            break
        time.sleep(0.1)

from core import config
from loguru import logger

GLOBAL_BPM = config.get('user_config', {}).get('bpm', 120)


# calculate duration
def calculate_duration(beat_value=None, bpm=None, time_signature=None) -> float:

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

    # Time Signature, default is 4/4
    if time_signature is None:
        time_signature = '4/4'

    # Analyze time signature
    try:
        numerator, denominator = map(int, time_signature.split('/'))
    except (ValueError, AttributeError):
        logger.warning(f"Invalid time signature: {time_signature}, using 4/4")
        numerator, denominator = 4, 4

    if denominator:
        # for ignore ide warning
        ...

    # 在不同拍号下，一拍的时值保持不变，但每小节的总拍数会变化
    # 例如，3/4拍的小节有3拍，而4/4拍的小节有4拍

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

    if beat_value == 'b__':  # 四分之一拍(十六分音符)
        return cur_beat * 0.25

    if beat_value == 'b___':  # 八分之一拍(三十二分音符)
        return cur_beat * 0.125

    # 根据-的数量返回cur_beat的时长
    # (notes, -) 即 (notes, beat*2)
    if beat_value.startswith('-'):
        try:
            dash_cnt = len(beat_value)
            return cur_beat * (dash_cnt + 1)
        except ValueError:
            logger.error(f"Invalid format: {beat_value}")
            return cur_beat

    # 根据 _ 的数量返回cur_beat的时长
    # 和上述的 b_, b__ ... 类似
    # 一个 _ 表示半拍，按照 b_ 的规则处理
    if beat_value.startswith('_'):
        try:
            und_cnt = len(beat_value)
            return cur_beat / (und_cnt * 2)
        except ValueError:
            logger.error(f"Invalid format: {beat_value}")
            return cur_beat

    if beat_value.startswith('b/'):
        d = int(beat_value[2:])
        if not d:
            raise ValueError("Invalid format!")
        return cur_beat / d

    if beat_value == 'bar':  # 一小节
        return cur_beat * numerator

    if beat_value.startswith('bar*'):  # 小节乘数
        try:
            bar_count = float(beat_value[4:])
            return (cur_beat * numerator) * bar_count
        except ValueError:
            logger.error(f"Invalid bar format: {beat_value}")
            return cur_beat * numerator

    return cur_beat


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

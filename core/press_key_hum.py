import time
import random
import win32api
import win32con


def is_key_pressed(key_code: int) -> bool:
    """
    检测按键是否被按下

    Args:
        key_code (int): 虚拟键码
    """
    return win32api.GetAsyncKeyState(key_code) & 0x8000 != 0


def hold_key(key: str, duration: float, velocity: float = 1.0) -> None:
    """
    长按 - 严格控制时长，只在按压力度上体现人性化

    Args:
        key (str): note
        duration (float): 精确持续时间
        velocity (float): 力度系数
    """
    vk_code = ord(key.upper())
    scan_code = win32api.MapVirtualKey(vk_code, 0)

    # 按下 - 根据力度调整按压时间
    press_strength = random.uniform(0.001, 0.003) * velocity
    win32api.keybd_event(vk_code, scan_code, 0, 0)
    time.sleep(press_strength)  # 模拟按压深度的差异

    # 精确持续时间，不添加随机性
    hold_time = max(duration - press_strength, 0.01)
    time.sleep(hold_time)

    # 释放
    win32api.keybd_event(vk_code, scan_code, win32con.KEYEVENTF_KEYUP, 0)


def press_key(key: str, velocity: float = 1.0) -> None:
    """
    短按 - 只在按压特性上体现人性化，不影响整体时序

    Args:
        key (str): note
        velocity (float): 力度系数
    """
    vk_code = ord(key.upper())
    scan_code = win32api.MapVirtualKey(vk_code, 0)

    # 按下
    win32api.keybd_event(vk_code, scan_code, 0, 0)

    # 根据力度调整按键持续时间，但保持在很小的范围内
    press_duration = random.uniform(0.001, 0.004) * velocity
    time.sleep(press_duration)

    # 释放
    win32api.keybd_event(vk_code, scan_code, win32con.KEYEVENTF_KEYUP, 0)

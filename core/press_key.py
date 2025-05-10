import time
import win32api
import win32con


def is_key_pressed(key_code: int) -> bool:
    """
    检测按键是否被按下

    Args:
        key_code (int): 虚拟键码
    """

    return win32api.GetAsyncKeyState(key_code) & 0x8000 != 0


def hold_key(key: str, duration: float) -> None:
    """
    长按

    Args:
        key (str): note
        duration (float): 持续时间
    """
    vk_code = ord(key.upper())
    scan_code = win32api.MapVirtualKey(vk_code, 0)
    win32api.keybd_event(vk_code, scan_code, 0, 0)
    time.sleep(max(duration * 0.98, 0.05))  # 保证演奏的连贯性
    # 释放按键
    win32api.keybd_event(vk_code, scan_code, win32con.KEYEVENTF_KEYUP, 0)


def press_key(key: str) -> None:
    """
    短按

    Args:
        key (str): note
    """
    vk_code = ord(key.upper())
    scan_code = win32api.MapVirtualKey(vk_code, 0)
    win32api.keybd_event(vk_code, scan_code, 0, 0)
    time.sleep(0.003)  # 短暂延迟
    win32api.keybd_event(vk_code, scan_code, win32con.KEYEVENTF_KEYUP, 0)

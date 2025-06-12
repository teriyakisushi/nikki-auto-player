import win32con


def get_vk_code(key_name: str) -> int:
    """
    string -> win32con.VK_*

    Args:
        key_name (str)
    Returns:
        int
    """
    key_mapping = {
        'F1': win32con.VK_F1,
        'F2': win32con.VK_F2,
        'F3': win32con.VK_F3,
        'F4': win32con.VK_F4,
        'F5': win32con.VK_F5,
        'F6': win32con.VK_F6,
        'F7': win32con.VK_F7,
        'F8': win32con.VK_F8,
        'F9': win32con.VK_F9,
        'F10': win32con.VK_F10,
        'F11': win32con.VK_F11,
        'F12': win32con.VK_F12,
        'ESC': win32con.VK_ESCAPE,
        'ESCAPE': win32con.VK_ESCAPE,
        'TAB': win32con.VK_TAB,
        'SPACE': win32con.VK_SPACE,
        'RETURN': win32con.VK_RETURN,
        'ENTER': win32con.VK_RETURN,
        'BACKSPACE': win32con.VK_BACK,
        'DELETE': win32con.VK_DELETE,
        'DEL': win32con.VK_DELETE,
        'CTRL': win32con.VK_CONTROL,
        'CONTROL': win32con.VK_CONTROL,
        'ALT': win32con.VK_MENU,
        'SHIFT': win32con.VK_SHIFT,
        'UP': win32con.VK_UP,
        'DOWN': win32con.VK_DOWN,
        'LEFT': win32con.VK_LEFT,
        'RIGHT': win32con.VK_RIGHT,
        'CAPSLOCK': win32con.VK_CAPITAL,
        'NUMLOCK': win32con.VK_NUMLOCK,
        'SCROLLLOCK': win32con.VK_SCROLL,
    }

    # Letter keys
    for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        key_mapping[c] = ord(c)

    # Nums keys
    for n in '0123456789':
        key_mapping[n] = ord(n)

    # case-insensitive
    key_upper = key_name.upper()
    if key_upper in key_mapping:
        return key_mapping[key_upper]
    else:
        raise ValueError(f"这个按键不支持呢: {key_name}，请自行添加")

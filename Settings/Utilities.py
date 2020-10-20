import win32api
import win32gui


_is_window_fullscreen = False  


def screen_size():
    return (win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))


def window_position():
    return win32gui.GetWindowRect(None)[:2]


def window_size():
    return win32gui.GetWindowRect(None)[3:]


def screen_width():
    return screen_size()[0]


def screen_height():
    return screen_size()[1]


def window_width():
    return window_size()[0]


def window_height():
    return window_size()[1]


def set_window_fullscreen(flag):
    global _is_window_fullscreen
    _is_window_fullscreen = flag


def is_window_fullscreen():
    return _is_window_fullscreen


def init_config():
    pass
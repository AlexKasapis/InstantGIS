import win32api
import win32gui
import math
from PyQt5 import QtCore


window_starting_width = 840
window_starting_height = 600

window_min_width = 600
window_min_height = 400

def screen_size():
    return (win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))

def screen_width():
    return screen_size()[0]

def screen_height():
    return screen_size()[1]

def window_position():
    return win32gui.GetWindowRect(None)[:2]

def window_size():
    return win32gui.GetWindowRect(None)[3:]

def window_width():
    return window_size()[0]

def window_height():
    return window_size()[1]

# Keep a number within a certain range.
def clamp(n, nmin, nmax):
    return min(nmax, max(n, nmin))

# Returns the euclidean distance between two points.
def get_euclidean_distance(p1, p2):
    if len(p1) is not len(p2):
        return
    sum = 0
    for i in range(len(p1)):
        sum += (p1[i] - p2[i]) ** 2
    return math.sqrt(sum)

def get_mouse_position():
    _, _, (x,y) = win32gui.GetCursorInfo()
    return QtCore.QPoint(x, y)

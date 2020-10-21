import enum
from Components.BorderFrame import BorderOrientation


# Denoting the resize anchor orientation.
class ResizeOrientation(enum.Enum):
    Left = 1
    TopLeft = 2
    Top = 3
    TopRight = 4
    Right = 5
    BottomRight = 6
    Bottom = 7
    BottomLeft = 8

def get_resize_transformations(window, resize_orientation, distance):
        
        if resize_orientation == ResizeOrientation.Left:
            resize_vector = (-distance[0], 0)
            move_vector = (distance[0], 0)
        elif resize_orientation == ResizeOrientation.TopLeft:
            resize_vector = (-distance[0], -distance[1])
            move_vector = (distance[0], distance[1])
        elif resize_orientation == ResizeOrientation.Top:
            resize_vector = (0, -distance[1])
            move_vector = (0, distance[1])
        elif resize_orientation == ResizeOrientation.TopRight:
            resize_vector = (distance[0], -distance[1])
            move_vector = (0, distance[1])
        elif resize_orientation == ResizeOrientation.Right:
            resize_vector = (distance[0], 0)
            move_vector = (0, 0)
        elif resize_orientation == ResizeOrientation.BottomRight:
            resize_vector = (distance[0], distance[1])
            move_vector = (0, 0)
        elif resize_orientation == ResizeOrientation.Bottom:
            resize_vector = (0, distance[1])
            move_vector = (0, 0)
        else:
            resize_vector = (-distance[0], distance[1])
            move_vector = (distance[0], 0)

        geometry = window.geometry()
        new_size = (max(geometry.width() + resize_vector[0], 400), max(geometry.height() + resize_vector[1], 400))
        if is_resizing_from_left(resize_orientation) and geometry.width() == new_size[0] == 400:
            move_vector = (0, move_vector[1])
        if is_resizing_from_top(resize_orientation) and geometry.height() == new_size[1] == 400:
            move_vector = (move_vector[0], 0)
        new_pos = (geometry.x() + move_vector[0], geometry.y() + move_vector[1])
        return new_size, new_pos

def is_resizing_from_left(resize_orientation):
    if resize_orientation == ResizeOrientation.Left \
        or resize_orientation == ResizeOrientation.TopLeft \
        or resize_orientation == ResizeOrientation.BottomLeft:
            return True

def is_resizing_from_top(resize_orientation):
    if resize_orientation == ResizeOrientation.Top \
        or resize_orientation == ResizeOrientation.TopLeft \
        or resize_orientation == ResizeOrientation.TopRight:
            return True

def get_resize_mode(border_orientation, width, height, diagonal_resize_threshold, x, y):
    if border_orientation == BorderOrientation.Left:
        if y <= diagonal_resize_threshold:
            return ResizeOrientation.TopLeft
        elif y >= height - diagonal_resize_threshold:
            return ResizeOrientation.BottomLeft
        else:
            return ResizeOrientation.Left
    elif border_orientation == BorderOrientation.Top:
        if x <= diagonal_resize_threshold:
            return ResizeOrientation.TopLeft
        elif x >= width - diagonal_resize_threshold:
            return ResizeOrientation.TopRight
        else:
            return ResizeOrientation.Top
    elif border_orientation == BorderOrientation.Right:
        if y <= diagonal_resize_threshold:
            return ResizeOrientation.TopRight
        elif y >= height - diagonal_resize_threshold:
            return ResizeOrientation.BottomRight
        else:
            return ResizeOrientation.Right
    else:
        if x <= diagonal_resize_threshold:
            return ResizeOrientation.BottomLeft
        elif x >= width - diagonal_resize_threshold:
            return ResizeOrientation.BottomRight
        else:
            return ResizeOrientation.Bottom

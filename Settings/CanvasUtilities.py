import Settings.Utilities


# Return the window position (x/y) in respect to where the world coordinates (lon/lat)
# is in combination to the plot limits.
def convert_world_to_window(figure_canvas, longitude, latitude):
    xlim = figure_canvas.axes.get_xlim()
    ylim = figure_canvas.axes.get_ylim()
    plot_width = figure_canvas.width()
    plot_height = figure_canvas.height()

    x = (longitude - xlim[0]) * plot_width / (xlim[1] - xlim[0])
    y = plot_height - (latitude - ylim[0]) * plot_height / (ylim[1] - ylim[0])

    return (int(x), int(y))

# Return the world coordinates (lon/lat) in respect to where the window position (x/y)
# is in combination to the plot limits.
def convert_window_to_world(figure_canvas, x, y):
    xlim = figure_canvas.axes.get_xlim()
    ylim = figure_canvas.axes.get_ylim()
    plot_width = figure_canvas.width()
    plot_height = figure_canvas.height()

    dist_lon = x * (xlim[1] - xlim[0]) / plot_width
    dist_lat = y * (ylim[1] - ylim[0]) / plot_height

    return (int(xlim[0] + dist_lon), int(ylim[1] - dist_lat))

# Update the plot limits depending on the position of the anchors.
def update_plot_limits(figure_canvas, anchors):
    if abs(anchors[0].x - anchors[1].x) < 1 or abs(anchors[0].y - anchors[1].y) < 1:
            return

    anchor_x_left = get_achor_x_left(anchors)
    anchor_x_right = get_achor_x_right(anchors)
    anchor_y_top = get_achor_y_top(anchors)
    anchor_y_bottom = get_achor_y_bottom(anchors)

    # Calculate the x limits.
    x_dist1 = anchor_x_left.x * (anchor_x_right.lon - anchor_x_left.lon) / (anchor_x_right.x - anchor_x_left.x)
    x_lim1 = int(anchor_x_left.lon - x_dist1)
    x_dist2 = (figure_canvas.width() - anchor_x_right.x) * (anchor_x_right.lon - anchor_x_left.lon) / (anchor_x_right.x - anchor_x_left.x)
    x_lim2 = int(anchor_x_right.lon + x_dist2)

    # Calculate the y limits.
    y_dist1 = anchor_y_top.y * (anchor_y_bottom.lat - anchor_y_top.lat) / (anchor_y_bottom.y - anchor_y_top.y)
    y_lim1 = int(anchor_y_top.lat - y_dist1)
    y_dist2 = (figure_canvas.height() - anchor_y_bottom.y) * (anchor_y_bottom.lat - anchor_y_top.lat) / (anchor_y_bottom.y - anchor_y_top.y)
    y_lim2 = int(anchor_y_bottom.lat + y_dist2)  
    
    # Apply the limits
    figure_canvas.axes.set_xlim([x_lim1, x_lim2])
    figure_canvas.axes.set_ylim([y_lim2, y_lim1])

    redraw_plot(figure_canvas)    

def redraw_plot(figure_canvas):
    figure_canvas.figure.canvas.draw()
    figure_canvas.figure.canvas.flush_events()

def get_achor_x_left(anchors):
    return anchors[0] if anchors[0].x < anchors[1].x else anchors[1]

def get_achor_x_right(anchors):
    return anchors[1] if anchors[1].x > anchors[0].x else anchors[0]

def get_achor_y_top(anchors):
    return anchors[0] if anchors[0].y < anchors[1].y else anchors[1]

def get_achor_y_bottom(anchors):
    return anchors[1] if anchors[1].y > anchors[0].y else anchors[0]

def get_achor_x_left_index(anchors):
    return 0 if anchors[0].x < anchors[1].x else 1

def get_achor_x_right_index(anchors):
    return 1 if anchors[1].x > anchors[0].x else 0

def get_achor_y_top_index(anchors):
    return 0 if anchors[0].y < anchors[1].y else 1

def get_achor_y_bottom_index(anchors):
    return 1 if anchors[1].y > anchors[0].y else 0

# Zoom a limit set (x or y axis) given a zoom value.
# Positive values zoom in, negative values zoom out.
def zoom_limits(x_lim, y_lim, x_zoom, y_zoom, zoom_modifier):
    new_xlim0 = x_lim[0] - x_zoom * zoom_modifier
    new_xlim1 = x_lim[1] + x_zoom * zoom_modifier

    if x_zoom == y_zoom:
        xlim_perc = (new_xlim1 - new_xlim0) / (x_lim[1] - x_lim[0])
        new_ylim0 = y_lim[0] - ((y_lim[1] - y_lim[0]) * xlim_perc - (y_lim[1] - y_lim[0])) / 2
        new_ylim1 = y_lim[1] + ((y_lim[1] - y_lim[0]) * xlim_perc - (y_lim[1] - y_lim[0])) / 2
        if 10 <= new_xlim1 - new_xlim0 <= 360 and 5 <= new_ylim1 - new_ylim0 <= 180:
            return [new_xlim0, new_xlim1], [new_ylim0, new_ylim1]
        else:
            return x_lim, y_lim
    else:
        new_ylim0 = y_lim[0] - y_zoom * zoom_modifier
        new_ylim1 = y_lim[1] + y_zoom * zoom_modifier
        return [new_xlim0, new_xlim1] if 10 <= new_xlim1 - new_xlim0 <= 360 else x_lim, \
                [new_ylim0, new_ylim1] if 5 <= new_ylim1 - new_ylim0 <= 180 else y_lim

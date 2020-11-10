from matplotlib import lines
from PyQt5.QtWidgets import QDesktopWidget, QFileDialog
from Settings import Utilities
from Settings import ResizeUtilities
from Settings import CanvasUtilities
from Components.PathPoint import PathPoint
from Components.ExportMenu import ExportMenu
from Components.MessageDialog import MessageDialog


class MainController():

    def __init__(self, *args, **kwargs):
        
        # UI References
        self.main_window = None
        self.anchors = []
        self.map_canvas = None
        self.current_path = []
        self.free_map_mode = True
        self.footer = None

    def get_window_min_width(self):
        return Utilities.window_min_width

    def get_window_min_height(self):
        return Utilities.window_min_height

    def get_window_starting_width(self):
        return Utilities.window_starting_width

    def get_window_starting_height(self):
        return Utilities.window_starting_height

    def fix_anchor_world_coordinates(self):
        x_l = CanvasUtilities.get_achor_x_left_index(self.anchors)
        x_r = CanvasUtilities.get_achor_x_right_index(self.anchors)
        y_t = CanvasUtilities.get_achor_y_top_index(self.anchors)
        y_b = CanvasUtilities.get_achor_y_bottom_index(self.anchors)

        if (self.anchors[x_l].lon > self.anchors[x_r].lon):
            temp = self.anchors[x_r].lon
            self.anchors[x_r].lon = self.anchors[x_l].lon
            self.anchors[x_l].lon = temp

        if (self.anchors[y_t].lat < self.anchors[y_b].lat):
            temp = self.anchors[y_b].lat
            self.anchors[y_b].lat = self.anchors[y_t].lat
            self.anchors[y_t].lat = temp
            
    def fix_path_world_coordinates(self):
        for i in range(len(self.current_path)):
            (lon, lat) = CanvasUtilities.convert_window_to_world(self.map_canvas, self.current_path[i].x, self.current_path[i].y)
            self.current_path[i].lon = lon
            self.current_path[i].lat = lat

    # Returns the other anchor between the two anchors.
    def get_other_anchor(self, anchor):
        return self.anchors[0] if anchor is not self.anchors[0] else self.anchors[1]

    # Event handling panning the plot. Panning slides the plot limits linearly.
    # Panning also changes the anchors' lon/lat values, because they remain in the same x/y window positions.
    def plot_pan(self, dist):
        # Calculate the move distance for X and Y separately, depending on their zoom level.
        x_lim = self.map_canvas.axes.get_xlim()
        y_lim = self.map_canvas.axes.get_ylim()
        x_modifier = 0.015 + ((x_lim[1] - x_lim[0]) - 10) / 800
        y_modifier = 0.015 + ((y_lim[1] - y_lim[0]) - 5) / 600
        move_dist = [dist.x() * x_modifier, dist.y() * y_modifier]

        # Move the plot limits.
        self.map_canvas.axes.set_xlim(x_lim[0] - move_dist[0], x_lim[1] - move_dist[0])
        self.map_canvas.axes.set_ylim(y_lim[0] + move_dist[1], y_lim[1] + move_dist[1])

        # Update anchor coordinates.
        self.anchors_snap_to_window()

        if len(self.current_path) > 0:
            self.fix_path_world_coordinates()
        CanvasUtilities.redraw_plot(self.map_canvas, self)

    # Event handline zooming the plot. Zooming changes the anchors' lon/lat values, because they remain in the same x/y window positions.
    def plot_zoom(self, dist):
        # Move the plot limits.
        x_lim = self.map_canvas.axes.get_xlim()
        y_lim = self.map_canvas.axes.get_ylim()
        x_modifier = 0.015 + ((x_lim[1] - x_lim[0]) - 10) / 300
        y_modifier = 0.015 + ((y_lim[1] - y_lim[0]) - 5) / 200
        
        new_xlim, new_ylim = CanvasUtilities.zoom_limits(
            x_lim, y_lim,
            -dist[0] * x_modifier, -dist[1] * (x_modifier if dist[0] == dist[1] else y_modifier), 
            0.5)
        self.map_canvas.axes.set_xlim(new_xlim[0], new_xlim[1])
        self.map_canvas.axes.set_ylim(new_ylim[0], new_ylim[1])

        # Update anchor coordinates.
        self.anchors_snap_to_window()

        # Redraw the plot.
        if len(self.current_path) > 0:
            self.fix_path_world_coordinates()
        CanvasUtilities.redraw_plot(self.map_canvas, self)

    # Change the anchors' world coordinates depending on where they are positioned in the window.
    def anchors_snap_to_window(self):
        for i in range(len(self.anchors)):
            (lon, lat) = CanvasUtilities.convert_window_to_world(self.map_canvas, self.anchors[i].x, self.anchors[i].y)
            self.anchors[i].lon = lon
            self.anchors[i].lat = lat

    # Change the anchors' window coordinates depending on where they are positioned in the world.
    def anchors_snap_to_world(self):
        for i in range(len(self.anchors)):
            (x, y) = CanvasUtilities.convert_world_to_window(self.map_canvas, self.anchors[i].lon, self.anchors[i].lat)
            self.anchors[i].x = x
            self.anchors[i].y = y

    def resize_window(self, border, distance):
        # Depending on different resize modes, sometimes the window must be moved along with being resized
        # in order to produce the expected resizing functionality. Calculate the resize and move vectors.
        new_size, new_pos = ResizeUtilities.get_resize_transformations(self.main_window, border.resize_orientation, distance)

        # Apply the transformations.
        self.main_window.setGeometry(new_pos[0], new_pos[1], new_size[0], new_size[1])

        # Set the anchors' new window positions (x,y). Resizing moves the anchors' window positions, not the world positions.
        x_r_idx = CanvasUtilities.get_achor_x_right_index(self.anchors)
        y_b_idx = CanvasUtilities.get_achor_y_bottom_index(self.anchors)
        (x, _) = CanvasUtilities.convert_world_to_window(self.map_canvas, self.anchors[x_r_idx].lon, self.anchors[x_r_idx].lat)
        self.anchors[x_r_idx].x = x
        (_, y) = CanvasUtilities.convert_world_to_window(self.map_canvas, self.anchors[y_b_idx].lon, self.anchors[y_b_idx].lat)
        self.anchors[y_b_idx].y = y

        self.anchors[x_r_idx].setGeometry(self.anchors[x_r_idx].x, self.anchors[x_r_idx].y, self.anchors[x_r_idx].width(), self.anchors[x_r_idx].height())
        self.anchors[y_b_idx].setGeometry(self.anchors[y_b_idx].x, self.anchors[y_b_idx].y, self.anchors[y_b_idx].width(), self.anchors[y_b_idx].height())
        
        CanvasUtilities.update_plot_limits(self.map_canvas, self.anchors)
        CanvasUtilities.redraw_plot(self.map_canvas, self)

    def update_limits(self):
        CanvasUtilities.update_plot_limits(self.map_canvas, self.anchors)
        CanvasUtilities.redraw_plot(self.map_canvas, self)

    def reset_plot(self):
        self.map_canvas.axes.set_xlim(-180, 180)
        self.map_canvas.axes.set_ylim(-90, 90)

        (x, y) = CanvasUtilities.convert_world_to_window(self.map_canvas, -160, 80)
        self.anchors[0].setGeometry(x, y, self.anchors[0].width(), self.anchors[0].height())
        self.anchors[0].x = x
        self.anchors[0].y = y
        self.anchors[0].lon = -160
        self.anchors[0].lat = 80
        
        (x, y) = CanvasUtilities.convert_world_to_window(self.map_canvas, 160, -80)
        self.anchors[1].setGeometry(x, y, self.anchors[1].width(), self.anchors[1].height())
        self.anchors[1].x = x
        self.anchors[1].y = y
        self.anchors[1].lon = 160
        self.anchors[1].lat = -80

        CanvasUtilities.redraw_plot(self.map_canvas, self)

    def show_help_window(self):
        print('Beep boop... showing help...')

    def show_about_us_window(self):
        print('Beep boop... it\'s us..!')

    def show_export_menu(self, x, y):
        if len(self.current_path) > 0:
            export_menu = ExportMenu(x, y)
            export_menu.accepted.connect(self.export)
            export_menu.exec_()
        else:
            message_dialog = MessageDialog('There is no path to export.')
            message_dialog.setParent(self.main_window)
            w = self.main_window.width()
            h = self.main_window.height()
            message_dialog.setGeometry(w / 2 - 250 / 2, h / 2 - 90 / 2, 250, 90)
            message_dialog.exec_()

    def toggle_plot_mode(self):
        self.free_map_mode = not self.free_map_mode
        self.footer.update_mode_label()
        self.set_footer_description('Change to {} mode'.format('path creation' if self.free_map_mode else 'free map'))

    def set_footer_description(self, string):
        self.footer.description_label.setText(string)

    def add_path_point(self, x, y):
        self.current_path.append(PathPoint((x, y), CanvasUtilities.convert_window_to_world(self.map_canvas, x, y), self, parent=self.map_canvas))
        self.current_path[-1].show()
        self.redraw_path()

    def remove_path_point(self, path_point):
        self.current_path.remove(path_point)
        path_point.deleteLater()
        path_point = None
        self.redraw_path()

    def redraw_path(self):
        lines_list = []
        for i in range(len(self.current_path) - 1):
            p1 = self.current_path[i]
            p2 = self.current_path[i + 1]
            lines_list.append(lines.Line2D([p1.x, p2.x], [self.map_canvas.height() - p1.y, self.map_canvas.height() - p2.y], color='#D66355'))
        self.map_canvas.figure.lines = lines_list
        CanvasUtilities.redraw_plot(self.map_canvas, self)

    def reset_path(self):
        for i in range(len(self.current_path)):
            self.current_path[i].deleteLater()
            self.current_path[i] = None
        self.current_path = []
        self.redraw_path()

    def export(self, export_info):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)

        if file_dialog.exec_():
            file_path = str(file_dialog.selectedFiles()[0])

            if export_info['export_type'] == 'new_csv':
                output = '0#' + '#'.join(['{}~{}'.format(point.lon, point.lat) for point in self.current_path]) + '\n'
                f = open(file_path, "w")
                f.write(output)
                f.close()
            elif export_info['export_type'] == 'append_csv':
                output = '0#' + '#'.join(['{}~{}'.format(point.lon, point.lat) for point in self.current_path]) + '\n'
                f = open(file_path, "a")
                f.write(output)
                f.close()
            elif export_info['export_type'] == 'new_excel':
                pass
            elif export_info['export_type'] == 'append_excel':
                pass

            if export_info['reset_path']:
                self.reset_path()

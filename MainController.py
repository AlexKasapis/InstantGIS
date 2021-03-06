import os
import geopandas
import shapefile
from matplotlib import lines
from PyQt5.QtWidgets import QDesktopWidget, QFileDialog
from Settings import Utilities
from Settings import ResizeUtilities
from Settings import CanvasUtilities
from Components.PathPoint import PathPoint
from Components.ExportMenu import ExportMenu
from Components.MessageDialog import MessageDialog
from Components.OptionsMenu import OptionsMenu
from Components.MapCanvas import MapCanvas
from Components.AboutUsWindow import AboutUsWindow
from Components.HelpWindow import HelpWindow


class MainController():

    def __init__(self, *args, **kwargs):

        # Application version
        self.version = '0.4.0'
        
        # UI References
        self.main_window = None
        self.anchors = []
        self.gis_frame = None
        self.map_canvas = None
        self.current_path = []
        self.free_map_mode = True
        self.footer = None

        self.map_file_index = 1  # Default -- Medium resolution
        self.path_color_index = 0  # Default -- Red/Blue
        self.point_size_index = 1  # Default -- Medium

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
        xlim = self.map_canvas.axes.get_xlim()
        ylim = self.map_canvas.axes.get_ylim()

        # Translate the mouse move distance to world coordinate sizes.
        x_move_world = dist.x() * (xlim[1] - xlim[0]) / self.map_canvas.width()
        y_move_world = dist.y() * (ylim[1] - ylim[0]) / self.map_canvas.height()

        # Move the plot limits.
        self.map_canvas.axes.set_xlim(xlim[0] - x_move_world, xlim[1] - x_move_world)
        self.map_canvas.axes.set_ylim(ylim[0] + y_move_world, ylim[1] + y_move_world)

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
        x_modifier = max(0.02, ((x_lim[1] - x_lim[0]) - 10) / 300)
        y_modifier = max(0.02, ((y_lim[1] - y_lim[0]) - 5) / 200)
        
        new_xlim, new_ylim = CanvasUtilities.zoom_limits(
            x_lim, y_lim,
            -dist[0] * x_modifier, -dist[1] * (x_modifier if dist[0] == dist[1] else y_modifier), 
            0.5)

        # Zoom limit
        if new_xlim[1] - new_xlim[0] <= 1 or new_ylim[1] - new_ylim[0] <= 1:
            return

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
        help_window = HelpWindow(self)
        help_window.setParent(self.main_window)
        w = self.main_window.width()
        h = self.main_window.height()
        help_window.setGeometry(w / 2 - 600 / 2, h / 2 - 400 / 2, 600, 400)
        help_window.exec_()

    def show_about_us_window(self):
        about_us_window = AboutUsWindow(self)
        about_us_window.setParent(self.main_window)
        w = self.main_window.width()
        h = self.main_window.height()
        about_us_window.setGeometry(w / 2 - 400 / 2, h / 2 - 350 / 2, 400, 350)
        about_us_window.exec_()

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

    def show_options_window(self, x, y):
        options_menu = OptionsMenu(x, y, self)
        options_menu.exec_()

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
        colors = ['#2143E0', '#F51BEB']
        lines_list = []
        for i in range(len(self.current_path) - 1):
            p1 = self.current_path[i]
            p2 = self.current_path[i + 1]
            lines_list.append(lines.Line2D([p1.x, p2.x], [self.map_canvas.height() - p1.y, self.map_canvas.height() - p2.y], color=colors[self.path_color_index]))
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

            if export_info['export_type'] == 'csv':
                output = '{}#'.format(export_info['path_id']) + '#'.join(['{}~{}'.format(point.lon, point.lat) for point in self.current_path]) + '\n'
                f = open(file_path, "a")
                f.write(output)
                f.close()
            elif export_info['export_type'] == 'shapefile':
                # Insert previous data.
                lines = []
                records = []
                if os.path.exists(file_path):
                    with shapefile.Reader(file_path) as existing_data:
                        for i in range(len(existing_data.shapes())):
                            lines.append(existing_data.shape(i))
                            records.append(existing_data.record(i))

                with shapefile.Writer(file_path, shapeType=shapefile.POLYLINE) as w:
                    w.field('name', 'C')

                    for i in range(len(lines)):
                        line = lines[i]
                        record = records[i]
                        w.line([[[point[0], point[1]] for point in line.points]])  
                        w.record(record[0])
                    
                    # Insert new path
                    w.line([[[point.lon, point.lat] for point in self.current_path]])
                    w.record(export_info['path_id'])

            if export_info['reset_path']:
                self.reset_path()

    def reset_map(self, map_detail, keep_coordinates=False):
        map_files = [
            'ne_110m_coastline.geojson',
            'ne_50m_coastline.geojson',
            'ne_10m_coastline.geojson'
        ]

        self.map_file_index = map_detail

        if keep_coordinates:
            xlim = self.map_canvas.axes.get_xlim()
            ylim = self.map_canvas.axes.get_ylim()
        
        self.gis_frame.layout().removeWidget(self.gis_frame.map_canvas)
        self.gis_frame.map_canvas.deleteLater()
        self.gis_frame.map_canvas = None
        self.gis_frame.map_canvas = MapCanvas(controller=self, map_file=map_files[self.map_file_index], parent=self.gis_frame, dpi=self.gis_frame.dpi)
        self.gis_frame.layout().addWidget(self.gis_frame.map_canvas)

        for point in self.current_path:
            # Get the required info
            x = point.x
            y = point.y
            index = self.current_path.index(point)

            # Remove the old point
            self.gis_frame.layout().removeWidget(point)
            point.deleteLater()
            point = None

            # Inser the new point
            self.current_path[index] = PathPoint((x, y), CanvasUtilities.convert_window_to_world(self.map_canvas, x, y), self, parent=self.map_canvas)

        if keep_coordinates:
            self.map_canvas.axes.set_xlim(xlim[0], xlim[1])
            self.map_canvas.axes.set_ylim(ylim[0], ylim[1])
            CanvasUtilities.redraw_plot(self.map_canvas, self)
            self.redraw_path()

    def change_path_color(self, color_index):
        self.path_color_index = color_index
        for path_point in self.current_path:
            path_point.reset_visuals()
        self.redraw_path()

    def change_point_size(self, size_index):
        self.point_size_index = size_index
        for path_point in self.current_path:
            path_point.reset_visuals()

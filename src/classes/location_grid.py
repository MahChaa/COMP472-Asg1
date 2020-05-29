import shapefile as shp
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from matplotlib import colors


class LocationGrid:
    __axis_font_size: str
    __x_axis_angle: int
    __alignment: str
    __block_graph_intervals: list
    __block_graph_data: list
    __block_graph_data_formatted: list
    __grid_size: float
    __threshold: float
    __x_axis_ticks: np.ndarray
    __y_axis_ticks: np.ndarray
    __block_df: pd.DataFrame
    __crime_count: int
    __crime_mean: float
    __crime_standard_deviation: float

    def __init__(self, shapefile: str, grid_size: float = 0.002, threshold: float = 0.5):
        with shp.Reader(shapefile, "r", encoding="ANSI") as sf:
            self.__points_x = [point.points[0][0] for point in sf.shapes()]
            self.__points_y = [point.points[0][1] for point in sf.shapes()]
            self.__area_coordinates = sf.bbox

            fields = [x[0] for x in sf.fields][1:]
            records = [y[:] for y in sf.records()]
            points = [s.points[0] for s in sf.shapes()]
            self.__crime_df = pd.DataFrame(columns=fields, data=records)
            self.__crime_df = self.__crime_df.assign(Coordinates=points)

        self.windowed_graph(True)

        self.threshold = threshold
        self.grid_size = grid_size

    def show_block(self) -> None:
        self.__format_axis()

        fig, block_plot = plt.subplots()

        if plt.get_backend() == "TkAgg":
            fig.suptitle("Block Graph: " + str(self.__grid_size) + " grid size; " + str(self.__threshold) +
                         " threshold")

        color_map = colors.ListedColormap(['blue', 'red'])
        bounds = [0, float(self.__block_df.quantile(self.__threshold, axis=1)),
                  int(self.__block_df.max(axis=1))]
        norm = colors.BoundaryNorm(bounds, color_map.N)

        block_plot.imshow(np.array(self.__block_graph_data_formatted), cmap=color_map, norm=norm, aspect="auto",
                          extent=[self.__area_coordinates[0], self.__area_coordinates[2],
                                  self.__area_coordinates[1], self.__area_coordinates[3]])

        self.__set_axis_ticks()

        plt.show(block=False)

    def show_scatter(self) -> None:
        self.__format_axis()

        fig, scatter_plot = plt.subplots()

        if plt.get_backend() == "TkAgg":
            fig.suptitle("Scatter Graph: " + str(self.__grid_size) + " grid size")

        plt.axis([self.__area_coordinates[0], self.__area_coordinates[2], self.__area_coordinates[1],
                  self.__area_coordinates[3]])

        self.__set_axis_ticks()

        plt.grid(True)

        scatter_plot.scatter(self.__points_x, self.__points_y)

        plt.show(block=False)

    def __format_axis(self) -> None:
        if self.__grid_size >= 0.0015:
            self.__axis_font_size = "large"
            self.__x_axis_angle = 45
            self.__alignment = "right"
        elif self.__grid_size >= 0.001:
            self.__axis_font_size = "small"
            self.__x_axis_angle = 50
            self.__alignment = "right"
        else:
            self.__axis_font_size = "xx-small"
            self.__x_axis_angle = 90
            self.__alignment = "center"

    def __set_axis_ticks(self) -> None:
        plt.xticks(self.__x_axis_ticks, rotation=self.__x_axis_angle, horizontalalignment=self.__alignment,
                   size=self.__axis_font_size)
        plt.yticks(self.__y_axis_ticks, size=self.__axis_font_size)

    def windowed_graph(self, val: bool) -> None:
        matplotlib.use("TkAgg" if val else "module://backend_interagg")

    @property
    def grid_size(self) -> float:
        return self.__grid_size

    @grid_size.setter
    def grid_size(self, grid_size: float) -> None:
        if hasattr(self, "grid_size") and self.__grid_size == grid_size:
            return

        self.__grid_size = grid_size

        self.__x_axis_ticks = np.arange(self.__area_coordinates[0], self.__area_coordinates[2], self.__grid_size)
        self.__y_axis_ticks = np.arange(self.__area_coordinates[1], self.__area_coordinates[3], self.__grid_size)

        self.__block_graph_intervals = []
        self.__block_graph_data = []
        self.__block_graph_data_formatted = []

        for j in range(0, len(self.__x_axis_ticks)):
            bottom_boundary = self.__y_axis_ticks[-j - 1]
            top_boundary = self.__y_axis_ticks[-j] if j != 0 else bottom_boundary + self.__grid_size

            for i, x_coord in enumerate(self.__x_axis_ticks):
                left_boundary = x_coord
                right_boundary = self.__x_axis_ticks[i + 1] if i != len(self.__x_axis_ticks) - 1 \
                    else x_coord + self.__grid_size

                self.__block_graph_intervals.append([left_boundary, bottom_boundary, right_boundary, top_boundary])

        for i, block in enumerate(self.__block_graph_intervals):
            self.__block_graph_data.append(0)

            for point in self.__crime_df["Coordinates"]:
                if (block[0] <= point[0] < block[2]) and (block[1] <= point[1] < block[3]):
                    self.__block_graph_data[i] += 1

        for i, block in enumerate(self.__block_graph_intervals):
            if i % len(self.__x_axis_ticks) == 0:
                self.__block_graph_data_formatted.append([])
            self.__block_graph_data_formatted[math.floor(i / len(self.__x_axis_ticks))].append(0)

            for point in self.__crime_df["Coordinates"]:
                if (block[0] <= point[0] < block[2]) and (block[1] <= point[1] < block[3]):
                    self.__block_graph_data_formatted[math.floor(i / len(self.__x_axis_ticks))][
                        i % len(self.__x_axis_ticks)] += 1

        self.__block_df = pd.DataFrame(columns=[str(x)[1:-2] for x in self.__block_graph_intervals],
                                       data=np.array([self.__block_graph_data]))

        self.__crime_count = int(self.__block_df.sum(axis=1))
        self.__crime_mean = float(self.__block_df.mean(axis=1))
        self.__crime_standard_deviation = float(self.__block_df.std(axis=1))

    @property
    def threshold(self) -> float:
        return self.__threshold

    @threshold.setter
    def threshold(self, threshold: float) -> None:
        self.__threshold = threshold if 0 <= threshold <= 1 else 0.5

    @property
    def crime_count(self) -> int:
        return self.__crime_count

    @property
    def crime_mean(self) -> float:
        return self.__crime_mean

    @property
    def crime_standard_deviation(self) -> float:
        return self.__crime_standard_deviation

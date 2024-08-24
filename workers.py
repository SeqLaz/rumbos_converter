import csv
import math
import folium
from folium import plugins
import pandas as pd
from pyproj import Transformer
from num2words import num2words
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


class Rumboscreator:
    def __init__(self, input_file_path, output_file_path):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path

    def generate_rumbos(self):
        with open(self.input_file_path, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            data = [row for row in reader]

        with open(self.output_file_path, "w", newline="") as csv_output_file:
            fieldnames = [
                "punto",
                "x",
                "y",
                "X1*Y1",
                "Y1*X1",
                "AX",
                "AY",
                "Distancia_Tramo",
                "RDEG",
                "DirNS",
                "DirEO",
                "Grados",
                "Minutos",
                "Segundos",
            ]
            writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames)
            writer.writeheader()

            for i in range(len(data)):
                # Adding X1*Y1
                x1, y1 = float(data[i]["x"]), float(data[0]["y"])
                if i == len(data) - 1:
                    x2, y2 = float(data[0]["x"]), float(data[0]["y"])
                else:
                    x2, y2 = float(data[i + 1]["x"]), float(data[i + 1]["y"])
                result_x1y1 = x1 * y2

                x1, y1 = float(data[0]["x"]), float(data[i]["y"])
                if i == len(data) - 1:
                    x2, y2 = float(data[0]["x"]), float(data[0]["y"])
                else:
                    x2, y2 = float(data[i + 1]["x"]), float(data[i + 1]["y"])
                result_y1x1 = y1 * x2

                # Adding the AX
                x0 = float(data[i]["x"])  # Get x-coordinate from current Point
                y0 = float(data[i]["y"])
                if i == len(data) - 1:
                    x1 = float(
                        data[0]["x"]
                    )  # Get x-coordinate from Point 0 for the last point
                    y1 = float(data[0]["y"])
                else:
                    x1 = float(data[i + 1]["x"])  # Get x-coordinate from next Point
                    y1 = float(data[i + 1]["y"])
                result_ax = x1 - x0
                result_ay = y1 - y0
                distance = round(math.sqrt((result_ax**2) + (result_ay**2)), 2)
                changed_ay = result_ay if (result_ay != 0) else (result_ay + 0.001)
                division_ax_ay = result_ax / changed_ay
                rdeg = abs(math.atan(division_ax_ay) * 180 / math.pi)
                dir_ns = "Norte" if (result_ay > 0) else "Sur"
                dir_ew = "Este" if (result_ax > 0) else "Oeste"
                degrees = math.trunc(rdeg)
                minutes = math.trunc((rdeg - degrees) * 60)
                seconds = math.trunc(
                    round(((((rdeg - degrees) * 60) - minutes) * 60), 0)
                )
                writer.writerow(
                    {
                        "punto": data[i]["punto"],
                        "x": data[i]["x"],
                        "y": data[i]["y"],
                        "X1*Y1": result_x1y1,
                        "Y1*X1": result_y1x1,
                        "AX": result_ax,
                        "AY": result_ay,
                        "Distancia_Tramo": distance,
                        "RDEG": rdeg,
                        "DirNS": dir_ns,
                        "DirEO": dir_ew,
                        "Grados": degrees,
                        "Minutos": minutes,
                        "Segundos": seconds,
                    }
                )
        return self.output_file_path


class MapGenerator:
    def __init__(self, csv_file, coordinate_system_origin, output_file_path):
        self.output_file_path = output_file_path
        self.data = pd.read_csv(csv_file)
        self.in_proj = f"{coordinate_system_origin}"  # UTM Zone 16N projection
        self.out_proj = "epsg:4326"  # WGS84 coordinate system

    def utm_to_latlon(self, x, y):
        transformer_obj = Transformer.from_crs(
            self.in_proj, self.out_proj, always_xy=True
        )
        lon, lat = transformer_obj.transform(x, y)
        return lat, lon

    def calculate_centroid(self):
        centroid_x = self.data["x"].mean()
        centroid_y = self.data["y"].mean()
        return centroid_x, centroid_y

    def generate_map(self):
        # Create map centered on the first point
        centroid_lat, centroid_lon = self.utm_to_latlon(*self.calculate_centroid())
        first_point = self.data.iloc[0]
        center_lat, center_lon = self.utm_to_latlon(first_point["x"], first_point["y"])
        m = folium.Map(
            location=[centroid_lat, centroid_lon],
            zoom_start=17,
            zoom_control=False,
            attribution_control=False,
        )

        # Add points with circles and labels
        for _, row in self.data.iterrows():
            lat, lon = self.utm_to_latlon(row["x"], row["y"])
            label = f"Punto {row['punto']}"  # Label using the Punto field
            folium.CircleMarker(
                location=[lat, lon],
                radius=7,
                fill=True,
                fill_color="white",
                color="black",
                popup=label,
                tooltip=label,
            ).add_to(m)

        # Add polygon
        points = [
            (self.utm_to_latlon(row["x"], row["y"])) for _, row in self.data.iterrows()
        ]
        folium.Polygon(
            locations=points, color="black", fill=True, fill_opacity=0.3
        ).add_to(m)
        minimap = plugins.MiniMap(zoom_level_fixed=7, width=350, height=350)
        m.add_child(minimap)
        m.save(self.output_file_path)


class DataProcessor:
    def __init__(self, csv_file, output_file_path):
        self.csv_file = csv_file
        self.data = pd.DataFrame()
        self.area = None
        self.paragraph = ""
        self.output_file_path = output_file_path
        print(self.csv_file)

    def read_csv(self):
        self.data = pd.read_csv(self.csv_file)

    def calculate_area(self):
        x1_y1_sum = self.data["X1*Y1"].astype(float).sum()
        y1_x1_sum = self.data["Y1*X1"].astype(float).sum()
        self.area = abs((x1_y1_sum - y1_x1_sum) / 2)

    def format_dms(self, degrees, minutes, seconds):
        degrees_str = num2words(degrees, lang="es").lower()
        minutes_str = num2words(minutes, lang="es").lower()
        seconds_str = num2words(seconds, lang="es").lower()
        return f"{degrees_str} grados, {minutes_str} minutos, {seconds_str} segundos ({degrees}° {minutes}' {seconds}'')"

    def format_direction(self, dir_ns, dir_eo):
        ns_str = "Nor" if dir_ns == "Norte" else "Sur"
        eo_str = "este" if dir_eo == "Este" else "oeste"
        return f"{ns_str.lower()}{eo_str.lower()}"

    def format_distance(self, distance):
        return f"{num2words(round(distance,2), lang='es').lower()} metros ({distance:.2f} m)"

    def generate_paragraph(self):
        first_row = self.data.iloc[0]
        self.paragraph = f"Inicia con el punto {num2words(first_row['punto'], lang='es').lower()} con Coordenada X {first_row['x']} y Coordenada Y {first_row['y']}, con rumbo {self.format_direction(first_row['DirNS'], first_row['DirEO'])}, a {self.format_dms(first_row['Grados'], first_row['Minutos'], first_row['Segundos'])} con distancia de {self.format_distance(first_row['Distancia_Tramo'])}, seguido del punto "

        for i in range(1, len(self.data)):
            row = self.data.iloc[i]
            punto = num2words(row["punto"], lang="es").lower()
            rumbo = self.format_direction(row["DirNS"], row["DirEO"])
            rumbo_grados = self.format_dms(
                row["Grados"], row["Minutos"], row["Segundos"]
            )
            distancia = self.format_distance(row["Distancia_Tramo"])

            self.paragraph += f"{punto} con Coordenada X {row['x']} y Coordenada Y {row['y']}, con rumbo {rumbo.lower()}, a {rumbo_grados} con distancia de {distancia}, "
            self.paragraph += "seguido del punto " if i < len(self.data) - 1 else ""

    def save_to_file(self):
        with open(self.output_file_path, "w") as file:
            file.write(f"El área en metros cuadrados: {self.area} m² - \n")
            file.write(f"El área en Hetáreas: {round((self.area/10000),2)} Ha - \n")
            file.write(
                f"El área Manzanas: {round(((self.area/10000)*1.418415),2)} Mz - \n"
            )
            file.write("Descripción de rumbos: \n")
            file.write(self.paragraph)

    def process_data(self):
        self.read_csv()
        self.calculate_area()
        self.generate_paragraph()


class GenerateGraph:
    def __init__(self, csv_file, output_file_path):
        self.df = pd.read_csv(csv_file)
        self.df.loc[-1] = ["", self.df["x"][0], self.df["y"][0]]
        self.output_file_path = output_file_path

    def generate(self):
        plt.plot(
            self.df["x"],
            self.df["y"],
            marker="o",
            color="#000000ff",
        )
        plt.grid()

        for i, (x, y, label) in enumerate(
            zip(self.df["x"], self.df["y"], self.df["punto"])
        ):
            plt.annotate(
                label,
                (x, y),
                textcoords="offset points",
                xytext=(0, 10),  # Offset for the label (x, y) coordinates
                ha="center",
            )

        ax = plt.gca()
        ax.xaxis.set_major_formatter(ticker.ScalarFormatter(False))
        ax.yaxis.set_major_formatter(ticker.ScalarFormatter(False))
        ax.get_yaxis().get_major_formatter().set_scientific(False)

        plt.savefig(f"{self.output_file_path}", format="png")
        plt.close()

    def reset(self):
        self.df = None
        self.output_file_path = None


if __name__ == "__main__":
    csv_file = "test_coordinate.csv"
    graph = GenerateGraph(csv_file, "graph.png")
    graph.generate()

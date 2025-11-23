from .tuples import Color


class Canvas:
    def __init__(self, width: int, height: int, color=Color(0, 0, 0)) -> None:
        self.width = width
        self.height = height
        self.maximum_color_value = 255
        self.pixels = [color for i in range(width * height)]

    def pixel_at(self, column, row) -> Color:
        return self.pixels[row * self.width + column]

    def write_pixel(self, column, row, color):
        self.pixels[row * self.width + column] = color

    def scale(self, pixel_value):
        scale_value = round(pixel_value * self.maximum_color_value)
        if scale_value > self.maximum_color_value:
            return self.maximum_color_value
        if scale_value < 0:
            return 0
        return scale_value

    def convert_to_ppm(self) -> str:
        ppm = f"P3\n{self.width} {self.height}\n{self.maximum_color_value}"

        for row in range(self.height):
            ppm += "\n"

            for column in range(self.width):
                pixel = self.pixel_at(column, row)
                ppm = (
                    ppm
                    + f"{self.scale(pixel.red)} {self.scale(pixel.green)} {self.scale(pixel.blue)} "
                )
        ppm += "\n"

        # ppm_with_linebreaks = ""
        # for line in ppm.splitlines():
        #     if len(line) > 70:
        #         splitted = line.split()

        #         index = 0
        #         while index < len(splitted):
        #             current_line = ""
        #             while len(current_line) <= 70 and index < len(splitted):
        #                 current_line += splitted[index]
        #                 index += 1
        #             ppm_with_linebreaks = current_line + "\n"
        #         #ppm_with_linebreaks  += str('\n'.join(line[i:i+70] for i in range(0,len(line), 70)))
        #     else:
        #         ppm_with_linebreaks += line
        #         ppm_with_linebreaks += "\n"
        return ppm

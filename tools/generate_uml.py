from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "uml" / "car-builder.png"

WIDTH = 2400
HEIGHT = 1600
BACKGROUND = "white"
LINE = "#2E3440"
HEADER = "#DCE6F1"
ABSTRACT_HEADER = "#E7E6E6"
BODY = "#FAFAFA"

FONT_PATH = "/usr/share/fonts/liberation/LiberationSans-Regular.ttf"
BOLD_FONT_PATH = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"
ITALIC_FONT_PATH = "/usr/share/fonts/liberation/LiberationSans-Italic.ttf"

title_font = ImageFont.truetype(BOLD_FONT_PATH, 54)
name_font = ImageFont.truetype(BOLD_FONT_PATH, 31)
stereotype_font = ImageFont.truetype(ITALIC_FONT_PATH, 24)
member_font = ImageFont.truetype(FONT_PATH, 24)
label_font = ImageFont.truetype(FONT_PATH, 22)

image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
draw = ImageDraw.Draw(image)


def centered_text(box, text, font, fill=LINE, y_offset=0):
    left, top, right, bottom = box
    text_box = draw.textbbox((0, 0), text, font=font)
    text_width = text_box[2] - text_box[0]
    x = left + (right - left - text_width) / 2
    y = top + y_offset
    draw.text((x, y), text, font=font, fill=fill)


def uml_box(x, y, w, title, members, stereotype=None, header_fill=HEADER):
    title_height = 86 if stereotype is None else 118
    line_height = 34
    body_height = 28 + line_height * len(members)
    h = title_height + body_height
    draw.rectangle((x, y, x + w, y + h), fill=BODY, outline=LINE, width=4)
    draw.rectangle((x, y, x + w, y + title_height), fill=header_fill, outline=LINE, width=4)

    if stereotype:
        centered_text((x, y, x + w, y + title_height), stereotype, stereotype_font, y_offset=13)
        centered_text((x, y, x + w, y + title_height), title, name_font, y_offset=54)
    else:
        centered_text((x, y, x + w, y + title_height), title, name_font, y_offset=25)

    text_y = y + title_height + 14
    for member in members:
        draw.text((x + 18, text_y), member, font=member_font, fill=LINE)
        text_y += line_height
    return (x, y, x + w, y + h)


def dashed_line(points, fill=LINE, width=4, dash=16, gap=12):
    for start, end in zip(points, points[1:]):
        x1, y1 = start
        x2, y2 = end
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if length == 0:
            continue
        dx = (x2 - x1) / length
        dy = (y2 - y1) / length
        position = 0
        while position < length:
            segment_end = min(position + dash, length)
            draw.line(
                (x1 + dx * position, y1 + dy * position,
                 x1 + dx * segment_end, y1 + dy * segment_end),
                fill=fill,
                width=width,
            )
            position += dash + gap


def triangle_arrow(tip, direction="up", size=24, fill="white"):
    x, y = tip
    if direction == "up":
        points = [(x, y), (x - size, y + size * 1.5), (x + size, y + size * 1.5)]
    elif direction == "right":
        points = [(x, y), (x - size * 1.5, y - size), (x - size * 1.5, y + size)]
    else:
        points = [(x, y), (x + size * 1.5, y - size), (x + size * 1.5, y + size)]
    draw.polygon(points, fill=fill, outline=LINE)
    draw.line(points + [points[0]], fill=LINE, width=4)


def open_arrow(tip, direction="right", size=20):
    x, y = tip
    if direction == "right":
        draw.line((x, y, x - size, y - size), fill=LINE, width=4)
        draw.line((x, y, x - size, y + size), fill=LINE, width=4)
    elif direction == "left":
        draw.line((x, y, x + size, y - size), fill=LINE, width=4)
        draw.line((x, y, x + size, y + size), fill=LINE, width=4)


draw.text((70, 30), "Car Builder Pattern UML Class Diagram", font=title_font, fill=LINE)

builder = uml_box(
    870, 115, 720, "CarBuilder",
    [
        "+ reset(): CarBuilder",
        "+ setModel(String): CarBuilder",
        "+ setEngine(Engine): CarBuilder",
        "+ setSeats(int): CarBuilder",
        "+ setTransmission(Transmission): CarBuilder",
        "+ setColor(String): CarBuilder",
        "+ addFeature(String): CarBuilder",
        "+ build(): Car",
    ],
    stereotype="<<interface>>",
)

abstract_builder = uml_box(
    870, 640, 720, "AbstractCarBuilder",
    [
        "# construction state",
        "+ fluent setter implementations",
        "+ build(): Car",
        "- validateCommonState(): void",
        "# validateSpecificState(): void",
    ],
    stereotype="<<abstract>>",
    header_fill=ABSTRACT_HEADER,
)

passenger = uml_box(
    470, 1165, 600, "PassengerCarBuilder",
    ["# validateSpecificState(): void", "  requires 4 to 7 seats"],
)

sports = uml_box(
    1320, 1165, 600, "SportsCarBuilder",
    ["# validateSpecificState(): void", "  requires <= 2 seats and >= 300 hp"],
)

car = uml_box(
    1740, 520, 600, "Car",
    [
        "- model: String",
        "- type: CarType",
        "- engine: Engine",
        "- seats: int",
        "- transmission: Transmission",
        "- color: String",
        "- features: List<String>",
    ],
)

director = uml_box(
    70, 175, 650, "CarDirector",
    [
        "+ constructFamilyCar(CarBuilder): Car",
        "+ constructSportsCar(CarBuilder): Car",
    ],
)

client = uml_box(
    70, 705, 500, "Main",
    ["+ main(String[]): void"],
)

# Realization and inheritance relationships.
draw.line((1230, abstract_builder[1], 1230, builder[3]), fill=LINE, width=4)
triangle_arrow((1230, builder[3]), direction="up")

draw.line((passenger[2], 1260, 1160, 1260, 1160, abstract_builder[3]), fill=LINE, width=4)
draw.line((sports[0], 1260, 1230, 1260, 1230, abstract_builder[3]), fill=LINE, width=4)
triangle_arrow((1160, abstract_builder[3]), direction="up")
triangle_arrow((1230, abstract_builder[3]), direction="up")

# Dependencies.
dashed_line([(director[2], 300), (790, 300), (790, 260), (builder[0], 260)])
open_arrow((builder[0], 260), direction="right")
draw.text((735, 215), "directs", font=label_font, fill=LINE)

dashed_line([(client[2], 770), (700, 770), (700, 420), (builder[0], 420)])
open_arrow((builder[0], 420), direction="right")
draw.text((620, 730), "uses", font=label_font, fill=LINE)

dashed_line([(abstract_builder[2], 830), (1665, 830), (1665, 710), (car[0], 710)])
open_arrow((car[0], 710), direction="right")
draw.text((1600, 785), "builds", font=label_font, fill=LINE)

dashed_line([(client[2], 840), (620, 840), (620, 370), (director[0], 370)])
open_arrow((director[0], 370), direction="left")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
image.save(OUTPUT, quality=95)
print(OUTPUT)

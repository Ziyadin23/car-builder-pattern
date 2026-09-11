from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "report" / "Builder_Pattern_Car_Report.docx"
UML_IMAGE = ROOT / "docs" / "uml" / "car-builder.png"
GITHUB_URL = "https://github.com/Ziyadin23/car-builder-pattern"

BLACK = "000000"
DARK_BLUE = "1F4E78"
PALE_BLUE = "EAF2F8"
LIGHT_GRAY = "D9D9D9"


def set_run_font(run, name, size=None, bold=None, italic=None, color=BLACK):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    run.font.color.rgb = RGBColor.from_string(color)


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shading = tc_pr.find(qn("w:shd"))
    if shading is None:
        shading = OxmlElement("w:shd")
        tc_pr.append(shading)
    shading.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=120, start=130, bottom=120, end=130):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_table_borders(table, color=LIGHT_GRAY, size="8"):
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.find(qn("w:tblBorders"))
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = f"w:{edge}"
        element = borders.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), color)


def repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    table_header = OxmlElement("w:tblHeader")
    table_header.set(qn("w:val"), "true")
    tr_pr.append(table_header)


def style_table(table, widths=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table)
    repeat_table_header(table.rows[0])

    for row_index, row in enumerate(table.rows):
        for column_index, cell in enumerate(row.cells):
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_margins(cell)
            if widths:
                cell.width = widths[column_index]
            if row_index == 0:
                set_cell_shading(cell, DARK_BLUE)
            elif row_index % 2 == 0:
                set_cell_shading(cell, PALE_BLUE)

            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_after = Pt(0)
                paragraph.paragraph_format.line_spacing = 1.05
                for run in paragraph.runs:
                    set_run_font(
                        run,
                        "Arial",
                        9.5,
                        bold=(row_index == 0),
                        color="FFFFFF" if row_index == 0 else BLACK,
                    )


def add_table(doc, headers, rows, widths):
    table = doc.add_table(rows=1, cols=len(headers))
    for index, header in enumerate(headers):
        table.rows[0].cells[index].text = header
    for values in rows:
        cells = table.add_row().cells
        for index, value in enumerate(values):
            cells[index].text = value
    style_table(table, widths)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return table


def add_code(doc, code):
    paragraph = doc.add_paragraph()
    paragraph.style = doc.styles["Normal"]
    paragraph.paragraph_format.left_indent = Inches(0.3)
    paragraph.paragraph_format.right_indent = Inches(0.15)
    paragraph.paragraph_format.space_before = Pt(3)
    paragraph.paragraph_format.space_after = Pt(7)
    paragraph.paragraph_format.line_spacing = 1.0
    paragraph.paragraph_format.keep_together = True
    run = paragraph.add_run(code)
    set_run_font(run, "Liberation Mono", 8.8)
    return paragraph


def add_bullet(doc, text):
    paragraph = doc.add_paragraph(style="List Bullet")
    paragraph.add_run(text)
    return paragraph


def keep_heading_with_next(paragraph):
    paragraph.paragraph_format.keep_with_next = True


doc = Document()
section = doc.sections[0]
section.page_width = Inches(8.5)
section.page_height = Inches(11)
section.top_margin = Inches(0.75)
section.bottom_margin = Inches(0.7)
section.left_margin = Inches(0.78)
section.right_margin = Inches(0.78)

styles = doc.styles
normal = styles["Normal"]
normal.font.name = "Arial"
normal._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
normal.font.size = Pt(11)
normal.font.color.rgb = RGBColor(0, 0, 0)
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.line_spacing = 1.08

title_style = styles["Title"]
title_style.font.name = "Arial"
title_style._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
title_style._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
title_style.font.size = Pt(25)
title_style.font.bold = True
title_style.font.color.rgb = RGBColor(0, 0, 0)
title_ppr = title_style._element.get_or_add_pPr()
title_border = title_ppr.find(qn("w:pBdr"))
if title_border is not None:
    title_ppr.remove(title_border)

for style_name, size in (("Heading 1", 16), ("Heading 2", 13), ("Heading 3", 11.5)):
    style = styles[style_name]
    style.font.name = "Arial"
    style._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    style._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = RGBColor(0, 0, 0)
    style.paragraph_format.space_before = Pt(12 if style_name == "Heading 1" else 9)
    style.paragraph_format.space_after = Pt(5)
    style.paragraph_format.keep_with_next = True

# Cover page
for _ in range(3):
    doc.add_paragraph()

title = doc.add_paragraph(style="Title")
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.add_run("Builder Pattern Implementation for a Car")

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
subtitle.paragraph_format.space_before = Pt(8)
subtitle.paragraph_format.space_after = Pt(30)
run = subtitle.add_run("Assignment 1 Report")
set_run_font(run, "Arial", 16, bold=True)

metadata = [
    ("Course", "ShP-2216 Software Design Patterns"),
    ("Institution", "Astana IT University School of Computer Engineering"),
    ("Student", "[Enter your full name]"),
    ("Group", "[Enter your group]"),
    ("Language", "Java 17"),
    ("Repository", GITHUB_URL),
    ("Submission date", "[Confirm the date in Moodle]"),
]
for label, value in metadata:
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_after = Pt(7)
    label_run = paragraph.add_run(label + "  ")
    set_run_font(label_run, "Arial", 11, bold=True)
    value_run = paragraph.add_run(value)
    set_run_font(value_run, "Arial", 11)

summary = doc.add_paragraph()
summary.alignment = WD_ALIGN_PARAGRAPH.CENTER
summary.paragraph_format.left_indent = Inches(0.7)
summary.paragraph_format.right_indent = Inches(0.7)
summary.paragraph_format.space_before = Pt(28)
summary.add_run(
    "This report explains a complete Builder pattern implementation that creates "
    "passenger and sports cars through the same fluent construction interface."
)

doc.add_page_break()

# 1 Introduction
doc.add_heading("1 Introduction", level=1)
doc.add_paragraph(
    "I chose Car as the product because a car contains required and optional parts that are easier "
    "to understand when configured step by step. The model, engine, seats, transmission, color, "
    "and optional features form one finished object, but different use cases require different "
    "combinations. A single constructor containing every value would be long, difficult to read, "
    "and unable to express the rules of passenger and sports cars clearly."
)
doc.add_paragraph(
    "The implementation uses CarBuilder as the construction interface, AbstractCarBuilder for "
    "shared behavior, PassengerCarBuilder and SportsCarBuilder as the two concrete builders, "
    "CarDirector for reusable recipes, and Main as the client. Calling build() validates the "
    "configuration and returns an immutable Car. The project compiles on JDK 17 without external "
    "libraries and includes seven executable tests."
)

doc.add_heading("2 Builder Pattern Structure", level=1)
doc.add_paragraph(
    "Builder is a creational design pattern. It separates the process of constructing an object "
    "from the finished object itself. The same sequence of named steps can produce different "
    "representations while the client avoids a large constructor and does not manage validation "
    "details directly."
)

add_table(
    doc,
    ["Pattern role", "Implementation", "Responsibility"],
    [
        ("Product", "Car", "Stores the finished immutable configuration."),
        ("Builder", "CarBuilder", "Declares every fluent construction step and build()."),
        ("Shared implementation", "AbstractCarBuilder", "Stores state and centralizes common setters and validation."),
        ("Concrete Builder", "PassengerCarBuilder", "Produces cars intended for normal passenger use."),
        ("Concrete Builder", "SportsCarBuilder", "Produces high-performance cars with stricter rules."),
        ("Director", "CarDirector", "Runs reusable family-car and sports-car build sequences."),
        ("Client", "Main", "Selects builders, requests products, and prints the results."),
    ],
    [Inches(1.28), Inches(1.55), Inches(4.0)],
)

doc.add_heading("Construction Flow", level=2)
for text in (
    "The client selects a concrete builder.",
    "The client or Director calls named configuration methods in the required sequence.",
    "Each method stores one value and returns the builder, which enables method chaining.",
    "build() checks common rules and rules specific to the selected representation.",
    "The builder creates an immutable Car and resets its temporary state for safe reuse.",
):
    add_bullet(doc, text)

doc.add_page_break()

# 3 UML
doc.add_heading("3 UML Class Diagram", level=1)
doc.add_paragraph(
    "The diagram shows realization and inheritance with solid triangular arrows. Dashed arrows "
    "show dependencies: the Director works through CarBuilder, Main uses the Director and builders, "
    "and AbstractCarBuilder creates the Car product."
)
picture_paragraph = doc.add_paragraph()
picture_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
picture_paragraph.paragraph_format.space_before = Pt(8)
picture_paragraph.paragraph_format.space_after = Pt(4)
picture_paragraph.add_run().add_picture(str(UML_IMAGE), width=Inches(6.75))
caption = doc.add_paragraph()
caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
caption.paragraph_format.space_after = Pt(10)
caption_run = caption.add_run("Figure 1  UML class diagram of the Car Builder implementation")
set_run_font(caption_run, "Arial", 9.5, italic=True)

doc.add_heading("Two Product Representations", level=2)
add_table(
    doc,
    ["Characteristic", "Passenger car", "Sports car"],
    [
        ("Concrete builder", "PassengerCarBuilder", "SportsCarBuilder"),
        ("Type", "PASSENGER", "SPORTS"),
        ("Seat rule", "Four to seven seats", "At most two seats"),
        ("Power rule", "Any positive horsepower", "At least 300 horsepower"),
        ("Transmission rule", "Any supported transmission", "Manual or dual clutch"),
        ("Director example", "AITU Family One", "AITU Velocity"),
    ],
    [Inches(1.65), Inches(2.55), Inches(2.55)],
)

doc.add_heading("Fluent Construction Example", level=2)
doc.add_paragraph(
    "The following client code builds a custom electric passenger car without using the Director. "
    "The method names expose the intent of each value, and the final build() call marks the point "
    "where validation and object creation occur."
)
add_code(
    doc,
    "Car customPassengerCar = new PassengerCarBuilder()\n"
    "        .setModel(\"AITU Eco Custom\")\n"
    "        .setEngine(new Engine(\"Electric Drive\", 220, FuelType.ELECTRIC))\n"
    "        .setSeats(5)\n"
    "        .setTransmission(Transmission.AUTOMATIC)\n"
    "        .setColor(\"Pearl White\")\n"
    "        .addFeature(\"Fast charging\")\n"
    "        .addFeature(\"Heated seats\")\n"
    "        .build();",
)

# 4 Clean Code
doc.add_heading("4 Clean Code Principles", level=1)
doc.add_paragraph(
    "The implementation applies the following seven Clean Code principles. Each subsection uses "
    "an excerpt from the submitted source code and explains the specific improvement it provides."
)

doc.add_heading("4 1 Meaningful Names", level=2)
doc.add_paragraph(
    "Names state the purpose of each object and operation. constructFamilyCar communicates a "
    "complete reusable recipe, while familyCar and sportsCar identify the resulting values. A name "
    "such as create() or object1 would hide this intent."
)
add_code(
    doc,
    "Car familyCar = director.constructFamilyCar(new PassengerCarBuilder());\n"
    "Car sportsCar = director.constructSportsCar(new SportsCarBuilder());",
)

doc.add_heading("4 2 Small Focused Classes and Methods", level=2)
doc.add_paragraph(
    "Each concrete builder contains only the rules unique to its representation. The passenger "
    "builder does not print output, construct predefined recipes, or validate sports cars. This "
    "keeps the class focused on one reason to change."
)
add_code(
    doc,
    "@Override\n"
    "protected void validateSpecificState() {\n"
    "    if (seats < MINIMUM_PASSENGER_SEATS || seats > MAXIMUM_PASSENGER_SEATS) {\n"
    "        throw new IllegalStateException(\n"
    "                \"Passenger car seat count must be between \"\n"
    "                        + MINIMUM_PASSENGER_SEATS + \" and \"\n"
    "                        + MAXIMUM_PASSENGER_SEATS\n"
    "        );\n"
    "    }\n"
    "}",
)

doc.add_heading("4 3 No Duplicated Construction Logic", level=2)
doc.add_paragraph(
    "AbstractCarBuilder implements the fluent setters and the common build sequence once. Both "
    "concrete builders inherit this behavior and supply only validateSpecificState(). Without the "
    "abstract class, the same fields, setters, reset code, and common validation would appear in "
    "both concrete builders."
)
add_code(
    doc,
    "@Override\n"
    "public final CarBuilder setSeats(int seats) {\n"
    "    this.seats = seats;\n"
    "    return this;\n"
    "}\n\n"
    "protected abstract void validateSpecificState();",
)

doc.add_heading("4 4 Validated Construction", level=2)
doc.add_paragraph(
    "build() refuses to create an incomplete or invalid product. The exception tells the client "
    "which required value is missing. Common validation runs before representation-specific rules, "
    "so every returned Car satisfies both levels of constraints."
)
add_code(
    doc,
    "if (engine == null) {\n"
    "    throw new IllegalStateException(\n"
    "            \"Car engine must be provided before build()\");\n"
    "}\n"
    "if (transmission == null) {\n"
    "    throw new IllegalStateException(\n"
    "            \"Car transmission must be provided before build()\");\n"
    "}",
)

doc.add_heading("4 5 No Magic Numbers", level=2)
doc.add_paragraph(
    "Named constants explain why numeric limits exist. The comparison reads as a business rule, "
    "and a future change to the minimum power requirement has one clear location."
)
add_code(
    doc,
    "private static final int MAXIMUM_SPORTS_SEATS = 2;\n"
    "private static final int MINIMUM_SPORTS_HORSEPOWER = 300;\n\n"
    "if (engine.horsepower() < MINIMUM_SPORTS_HORSEPOWER) {\n"
    "    throw new IllegalStateException(\n"
    "            \"Sports car engine must produce at least \"\n"
    "                    + MINIMUM_SPORTS_HORSEPOWER + \" hp\"\n"
    "    );\n"
    "}",
)

doc.add_heading("4 6 Immutable Finished Product", level=2)
doc.add_paragraph(
    "Car fields are final and the constructor copies the feature collection. Client code cannot "
    "change the completed product by retaining or modifying the builder's original list. This "
    "separates mutable construction state from the stable result."
)
add_code(
    doc,
    "private final Engine engine;\n"
    "private final List<String> features;\n\n"
    "this.engine = Objects.requireNonNull(engine);\n"
    "this.features = List.copyOf(features);",
)

doc.add_heading("4 7 Minimal Purposeful Comments", level=2)
doc.add_paragraph(
    "Comments describe design intent that is not fully visible from the syntax. The class comment "
    "explains why the abstract builder exists, while readable method names and small methods avoid "
    "line-by-line comments that would repeat the code."
)
add_code(
    doc,
    "/**\n"
    " * Holds construction state and shared build logic so concrete builders do not\n"
    " * duplicate fluent setters or common validation.\n"
    " */\n"
    "public abstract class AbstractCarBuilder implements CarBuilder {",
)

# 5 Verification
doc.add_heading("5 Demonstration and Verification", level=1)
doc.add_paragraph(
    "The Main client demonstrates three paths: a family car constructed by the Director, a sports "
    "car constructed by the Director, and a custom electric car constructed directly through the "
    "fluent API. The helper scripts use javac with the Java 17 release target, so no external Java "
    "dependency is required."
)
add_code(doc, "./scripts/run.sh\n./scripts/test.sh")

add_table(
    doc,
    ["Test", "Purpose"],
    [
        ("Director builds a passenger car", "Confirms passenger type, seats, and transmission."),
        ("Director builds a sports car", "Confirms sports type and the power rule."),
        ("Product feature list is immutable", "Confirms the finished product cannot be modified."),
        ("Missing required state is rejected", "Confirms incomplete products are blocked."),
        ("Invalid passenger seats are rejected", "Confirms passenger-specific validation."),
        ("Underpowered sports car is rejected", "Confirms sports-specific validation."),
        ("Builder resets after build", "Confirms temporary state does not leak into the next car."),
    ],
    [Inches(2.75), Inches(4.0)],
)
doc.add_paragraph(
    "All seven tests pass on OpenJDK 17. The successful demonstration prints the complete state of "
    "each car, making the two representations and their features visible during the defense."
)

# Conclusion and repository
doc.add_heading("6 Conclusion", level=1)
doc.add_paragraph(
    "While implementing this project, I found that Builder made complex construction easier to "
    "read because every argument gained a descriptive method name. Moving common behavior into "
    "AbstractCarBuilder also prevented duplicated setters and common checks. The concrete builders "
    "gave each representation a clear place for its own rules, and CarDirector made standard "
    "configurations repeatable."
)
doc.add_paragraph(
    "The main disadvantage was the additional structure. A small Car class became an interface, "
    "an abstract builder, two concrete builders, and a Director. The builder lifecycle also required "
    "a deliberate reset after a successful build so old values would not leak into the next product. "
    "Another limitation is that the Director accepts the CarBuilder interface, so a client must pair "
    "the family recipe with PassengerCarBuilder and the sports recipe with SportsCarBuilder. The "
    "validation catches a wrong pairing, but stronger type separation could prevent it earlier at "
    "the cost of a less uniform Director API."
)
doc.add_paragraph(
    "For this product, the benefits justify the extra classes because Car has multiple required "
    "parts, optional features, reusable configurations, and representation-specific constraints. "
    "For an object with only two or three simple values, a normal constructor would probably be "
    "clearer."
)

doc.add_heading("7 GitHub Repository", level=1)
doc.add_paragraph(
    "The complete compiling source code, README instructions, UML source, test runner, report, and "
    "incremental commit history are available at:"
)
repo_paragraph = doc.add_paragraph()
repo_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
repo_paragraph.paragraph_format.space_before = Pt(6)
repo_paragraph.paragraph_format.space_after = Pt(12)
repo_run = repo_paragraph.add_run(GITHUB_URL)
set_run_font(repo_run, "Arial", 11, bold=True)

doc.add_heading("References", level=1)
add_bullet(doc, "Freeman, E., and Robson, E. Head First Design Patterns. Builder pattern chapter.")
add_bullet(doc, "Martin, R. C. Clean Code A Handbook of Agile Software Craftsmanship. Prentice Hall, 2008.")
add_bullet(doc, "Refactoring.Guru. Builder Design Pattern. https://refactoring.guru/design-patterns/builder")

# Prevent headings from being stranded at page bottoms.
for paragraph in doc.paragraphs:
    if paragraph.style.name.startswith("Heading"):
        keep_heading_with_next(paragraph)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUTPUT)
print(OUTPUT)

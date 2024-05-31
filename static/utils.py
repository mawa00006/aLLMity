import codecs
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pylatex import Document, Section
import markdown2
from html2text import HTML2Text


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")


def get_data(patient_id, letter_type, read_breaks=False):

    arztbriefe = ""
    pflegedokumentation = ""

    arztbriefe = read_arztbrief(patient_id, read_breaks)

    if letter_type == "pflege":
        pflegedokumentation += read_pflegedokumentation(patient_id, read_breaks)
        #print("pflege:", pflegedokumentation)

    return arztbriefe, pflegedokumentation


def read_document2(filepath):
    with codecs.open(filepath, "r", encoding="utf-8") as file:
        data = file.read().replace("\n", "")

    return data


def read_document(filepath):
    with codecs.open(filepath, "r", encoding="utf-8") as file:

        data = ""
        for line in file:
            line = line.replace("\n", "").replace("\r", "")
            data += line

    return data


def read_arztbrief(patient_id, read_breaks=False):
    path = f"data/{patient_id}_arzt.txt"

    if read_breaks:
        arztbriefe = read_document2(path)
    else:
        arztbriefe = read_document(path)
    return arztbriefe


def read_pflegedokumentation(patient_id, read_breaks=False):
    path = f"data/{patient_id}_pflege.txt"
    if read_breaks:
        pflegedokumentation = read_document2(path)
    else:
        pflegedokumentation = read_document(path)
    return pflegedokumentation


def write_arztbrief(arzttexte, pflegetexte):
    persona = "Du bist ein Stationsarzt in einem Krankenhaus. Du sitzt in deinem Büro am Computer "
    task = (
        "und du schreibst einen fachlichen Arztbrief auschließlich aus den folgenden Daten. Konzentriere dich dabei"
        " auschließlich auf relevante ereignisse: "
    )
    context = " Arzttexte: " + arzttexte + " Pflegetexte: " + pflegetexte

    format = "Format: gebe nicht diese zeichen aus: \n* , \n"

    prompt = persona + task + context + format

    # LLM befragen
    response = model.generate_content(prompt)

    arztbrief = str(response._result.candidates[0].content.parts[0].text)
    print(arztbrief)

    return arztbrief


# Function to wrap text
def wrap_text(text, width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= width:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def render_latex(arztbrief):
    geometry_options = {"tmargin": "4cm", "lmargin": "3cm", "rmargin": "3cm"}
    doc = Document(geometry_options=geometry_options)

    with doc.create(Section("Arztbrief")):
        doc.append(arztbrief)

    doc.generate_pdf("full", clean_tex=False)


def markdown_to_latex(markdown_string):
    # Convert Markdown to HTML
    html_string = markdown2.markdown(markdown_string)

    # Initialize HTML2Text
    h = HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.body_width = 0  # To avoid text wrapping

    # Convert HTML to LaTeX
    latex_string = h.handle(html_string)

    return latex_string

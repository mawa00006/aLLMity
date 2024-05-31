import codecs
import os
import google.generativeai as genai
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_data(patient_id, letter_type):

    arztbriefe = ""
    pflegedokumentation = ""

    arztbriefe = read_arztbrief(patient_id)

    if letter_type == 1:
        pflegedokumentation += read_pflegedokumentation(patient_id)

    return arztbriefe, pflegedokumentation


def read_document2(filepath):
    with open(filepath, 'r') as file:
        data = file.read().replace('\n', '')

    return data

def read_document(filepath):
    with codecs.open(filepath, 'r', encoding='utf-8') as file:

        data = ""
        for line in file:
            line = line.replace('\n', '').replace('\r', '')
            data += line

    return data

def read_arztbrief(patient_id):
    path = f"data/{patient_id}_arzt.txt"
    arztbriefe = read_document(path)
    return arztbriefe

def read_pflegedokumentation(patient_id):
    path = f"data/{patient_id}_pflege.txt"
    pflegedokumentation = read_document(path)
    return pflegedokumentation

def write_arztbrief(arzttexte, pflegetexte):
    persona = "Du bist ein Stationsarzt in einem Krankenhaus. Du sitzt in deinem Büro am Computer "
    task = ("und du schreibst einen fachlichen Arztbrief auschließlich aus den folgenden Daten. Konzentriere dich dabei"
            " auschließlich auf relevante ereignisse: ")
    context = " Arzttexte: " + arzttexte + " Pflegetexte: " + pflegetexte

    format = "Format: gebe nicht diese zewichen aus: \n* , \n"

    prompt = persona + task + context + format

    # LLM befragen
    response = model.generate_content(prompt)
    print(response)

    arztbrief = str(response._result.candidates[0].content.parts[0]).replace('\n', '')


    return arztbrief

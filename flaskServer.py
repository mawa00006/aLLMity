from flask import Flask, render_template, redirect, url_for, request
import random
import json
import csv

from static.utils import *

# Create a Flask web application instance
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True


# Define the root route, which redirects to the 'base' route
@app.route('/')
def index():
    return redirect(url_for('base'))


# Define the 'base' route, which renders the 'base.html' template
@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/getData', methods=['GET'])
def return_data():
    patient_id = request.args.get('patient_id')
    letter_type = request.args.get('type')

    print(letter_type)
    print(patient_id)

    arztbriefe, pflegedokumentation = get_data(patient_id, letter_type)

    if letter_type=="pflege":
        return "Ärztliche Dokumentation:\n\n"+arztbriefe+"\n\n\nPflegerische Dokumentation:\n\n"+pflegedokumentation
    elif letter_type=="arzt":
        return "Ärztliche Dokumentation:\n\n"+arztbriefe
    else:
        return "invalid type"

@app.route('/generate_letter', methods=['GET'])
def generate_letter():
    patient_id = request.args.get('patient_id')
    letter_type = request.args.get('type')

    print(letter_type)
    print(patient_id)

    arztbriefe, pflegedokumentation = get_data(patient_id, letter_type)

    letter = write_arztbrief(arztbriefe, pflegedokumentation)

    # Logic to generate the doctor's letter based on patient_id and letter_type
    letter_content = letter

    return letter_content

if __name__ == '__main__':
    app.run(debug=True, port=5000)
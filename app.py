import os

import pandas as pd
from dotenv import load_dotenv
from flask import Flask, render_template, request

from report_generator import generate_report

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))


@app.route('/', methods=['GET', 'POST'])
def index():
    report = None
    error = None
    if request.method == 'POST':
        if 'file' not in request.files:
            error = 'No file part'
            return render_template('index.html', error=error)
        file = request.files['file']
        if file.filename == '':
            error = 'No selected file'
            return render_template('index.html', error=error)

        if file and file.filename.lower().endswith('.csv'):
            try:
                df = pd.read_csv(file)
            except Exception as e:
                error = f'Could not read the CSV file: {e}'
                return render_template('index.html', error=error)

            groq_api_key = os.getenv('GROQ_API_KEY')
            if not groq_api_key:
                error = 'GROQ_API_KEY is not set. Copy .env.example to .env and add your key.'
                return render_template('index.html', error=error)

            try:
                report = generate_report(df, groq_api_key)
            except Exception as e:
                error = str(e)
        else:
            error = 'File must be a CSV'

    return render_template('index.html', report=report, error=error)


if __name__ == '__main__':
    app.run(debug=True)

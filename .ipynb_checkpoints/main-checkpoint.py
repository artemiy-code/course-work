from flask import Flask, render_template, request
import os
from pyresparser import ResumeParser
app = Flask(__name__)

# Функция для извлечения ключевых атрибутов из резюме
def extract_resume_info(resume_path):
    # Извлечение текста из файла резюме (поддерживаются форматы .docx, .pdf, .txt)
    # Извлечение данных из резюме с использованием ResumeParser
    data = ResumeParser(resume_path).get_extracted_data()
    return data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        resume_file = request.files['resume']
        if resume_file.filename == '':
            return render_template('index.html', message='No file selected')

        if resume_file:
            # Создаем директорию 'temp', если она не существует
            if not os.path.exists('temp'):
                os.makedirs('temp')
            # Сохраняем файл во временную директорию
            resume_path = os.path.join('temp', resume_file.filename)
            resume_file.save(resume_path)
            resume_info = extract_resume_info(resume_path)
            return render_template('result.html', resume_info=resume_info)

if __name__ == '__main__':
    app.run(debug=True)

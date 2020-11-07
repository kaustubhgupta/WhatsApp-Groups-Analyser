from flask import current_app as app
from flask import render_template, request, redirect    
from WhatsApp.functions import ExtractDataFrame, GenerateStats
import os

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(os.path.join('uploads/' + uploaded_file.filename))

    return redirect(f'/process/{uploaded_file.filename}')

@app.route('/process/<file_name>')
def processing_phase(file_name):
    chats = ExtractDataFrame(os.path.join('uploads/' + file_name))
    chats.process()
    df = chats.dataframe()
    os.remove(os.path.join('uploads/' + file_name))
    stats = GenerateStats()
    ratio = stats.mediaRatio(df) 
    total = stats.totalEmojis(df) 
    unique = stats.uniqueEmojis(df) 

    return render_template('analysis.html', total=total, ratio=ratio, unique=unique)
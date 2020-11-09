from flask import current_app as app
from flask import render_template, request, redirect, abort, Markup
from WhatsApp.functions import ExtractDataFrame, GenerateStats
from app.graphs import *
import os


@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404


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
    if file_name=='':
        abort(404)
    try:
        chats = ExtractDataFrame(os.path.join('uploads/' + file_name))
        chats.process()
        df = chats.dataframe()
        os.remove(os.path.join('uploads/' + file_name))
        stats = GenerateStats()
        media_ratio = stats.mediaRatio(df) 
        total_emojis = stats.totalEmojis(df) 
        unique_emojis = stats.uniqueEmojis(df) 
        frequent_emojis = stats.frequentEmojis(df)
        active_members = stats.activeMembers(df)
        lazy_members = stats.lazyMembers(df)
        result_dates = stats.activityOverDates(df)
        datesActivityGraph = activityDate_Graph(result_dates)
        result_time = stats.activityOverTime(df)
        timeActivityGraph = activityTime_Graph(result_time)
        

    except:
        abort(404)
    morn_night = stats.nightOwls_earlyBirds(df)
    morning = morn_night['morning']
    night = morn_night['night']

    return render_template('analysis.html', total_emojis=total_emojis, 
                            media_ratio=media_ratio, unique_emojis=unique_emojis,
                            frequent_emojis=frequent_emojis.to_html(classes='frequent_emojis'),
                            active_members=active_members.to_html(classes='active_members'),
                            lazy_members=lazy_members.to_html(classes='lazy_members'),
                            bar_plot1=datesActivityGraph, bar_plot2=timeActivityGraph,
                            morning = morning.to_html(classes='morning'), 
                            night=night.to_html(classes='night'),)
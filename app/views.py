from flask import current_app as app
from flask import render_template, request, redirect, abort
from WhatsApp.functions import ExtractDataFrame, GenerateStats
from app.graphs import *
import os


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(os.path.join('uploads/' + uploaded_file.filename))

    return redirect(f'/process/{uploaded_file.filename}')


@app.route('/process/<file_name>')
def processing_phase(file_name):
    if file_name == '':
        abort(404)
    try:
        chats = ExtractDataFrame(os.path.join('uploads/' + file_name))
        chats.process()
        df = chats.dataframe()  # The Final Processed DataFrame

        os.remove(os.path.join('uploads/' + file_name))
        stats = GenerateStats()

        media_ratio = round(stats.mediaRatio(df), 2)  # Media Ratio

        total_emojis = stats.totalEmojis(df)  # Total Emojis

        unique_emojis = stats.uniqueEmojis(df)  # Total Unique Emojis

        frequent_emojis = stats.frequentEmojis(df)
        emoji_donut = Emojis_donut(
            frequent_emojis, 'Emoji Distribution')  # Emojis Donut Plot

        active_members = stats.activeMembers(df)
        activeMemberPlot = membersBarPlot(
            active_members, 'Active Members of The Group')  # Active Members Bar Chart

        lazy_members = stats.lazyMembers(df)
        lazyMemberPlot = membersBarPlot(
            lazy_members, 'Lazy Members of The Group')  # Lazy Members Bar Chart

        result_dates = stats.activityOverDates(df)
        datesActivityGraph = activityDate_Graph(
            result_dates)  # Overall Dates Activity Line Plot

        result_time = stats.activityOverTime(df)
        timeActivityGraph = activityTime_Graph(
            result_time)  # Overall Day Activity Line Plot

        morn_night = stats.nightOwls_earlyBirds(df)
        morning = morn_night['morning']
        morning_plot = night_morningPlot(
            morning, 'Early Birds (6 am to 9 am)')  # Morning Authors Pie Chart
        night = morn_night['night']
        night_plot = night_morningPlot(
            night, 'Night Owls (11 pm to 3 am)')  # Night Authors Pie Chart

        con_less = stats.emojiCon_Emojiless(df)
        emoji_con = con_less['Emoji_con']
        emojiAdictsPlot = emojiAdicts_LessPlot(
            emoji_con, 'Emoji Addicts')  # Emoji Addict Bar Chart

        holidays = stats.holidays_dict
        returned = stats.holidaysDataFrame(df)
        holiday_authors = {}
        holiday_freq_emojis = {}
        j = 1
        for i in holidays.values():
            if not returned[i].empty:
                holiday_authors['eventGraphAuthor'+str(j)] = membersBarPlot(
                    stats.activeMembers(returned[i]), i)  # Holidays Author Bar Plot
                holiday_freq_emojis['eventGraphEmoji'+str(j)] = Emojis_donut(
                    stats.frequentEmojis(returned[i]), i)  # Holidays Emojis Donut Plot
                j += 1

    except:
        abort(404)

    return render_template('analysis.html', total_emojis=total_emojis, total=df.shape[0],
                           media_ratio=media_ratio, unique_emojis=unique_emojis,
                           activeMemberPlot=activeMemberPlot, lazyMemberPlot=lazyMemberPlot,
                           bar_plot_dates=datesActivityGraph, bar_plot_time=timeActivityGraph,
                           morning_plot=morning_plot, night_plot=night_plot,
                           emojiAdictsPlot=emojiAdictsPlot, holiday_authors=holiday_authors,
                           holiday_freq_emojis=holiday_freq_emojis, emoji_donut=emoji_donut
                           )

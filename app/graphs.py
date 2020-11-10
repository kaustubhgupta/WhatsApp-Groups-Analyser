import plotly
import plotly.graph_objs as go
import plotly.express as px
import json


def activityDate_Graph(df):
    fig_batch = {
                    'data': [
                        go.Scatter(
                            x=df.index,
                            y=df['Number of Messages'].values,
                            # text=y,
                            # textposition='auto',
                            mode='lines+markers'
                        )],

                    'layout': go.Layout(
                        xaxis={'title': 'Dates'},
                        yaxis={'title': 'Number of Messages'},
                        hovermode='closest',
                        title='Activity Over Whole Timeline'
                    )}
    graphJSON = json.dumps(fig_batch, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def activityTime_Graph(df):
    y = df['Number of Messages'].values
    fig_batch = {
                    'data': [
                        go.Scatter(
                            x=df.index,
                            y=df['Number of Messages'].values,
                            # text=y,
                            # textposition='auto',
                            mode='lines+markers',
                        )],

                    'layout': go.Layout(
                        xaxis={'title': 'Time'},
                        yaxis={'title': 'Number of Messages'},
                        hovermode='closest',
                        title='Activity Over Whole Day'
                    )}
    graphJSON = json.dumps(fig_batch, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def frequentEmojis_donut(df):
    labels = df.Emoji.values
    values = df.Count.values
    fig = go.Figure(data=[
                    go.Pie(labels=labels, values=values, hole=.5, textinfo='label+percent',
                             insidetextorientation='radial')
                    ])

    fig.update_layout(
                        annotations=[dict(text='Emoji Distribution', x=0.5, y=0.5, font_size=13, showarrow=False),
                                     ])

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def membersBarPlot(df, title):
    fig = px.bar(df, x=df.index, y=df['Message Count'].values, 
                labels={'y':'Number of Messages'}, text=df['Message Count'].values, title=title,
             )
    fig.update_layout(xaxis_tickangle=-45)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
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
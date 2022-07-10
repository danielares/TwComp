import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo

def create_html_chart(df):
    df.reset_index(inplace=True)
    df.rename(columns = {'index':'words', 0:'importance'}, inplace = True)
    fig = go.Figure(
        px.bar(df, x='words', y='importance', height=500, width=1000, template='plotly_dark', color="words")
    )
    
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    
    config={'responsive': True}
    chart_html = pyo.plot(fig, config=config, output_type='div')
    
    return chart_html
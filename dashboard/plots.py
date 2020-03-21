
import plotly.express as px

def dummy_function(data):
    import pdb
    pdb.set_trace()
    fig = px.scatter(x=range(10), y=range(10))
    return fig.to_html(full_html=False, include_plotlyjs=True)#, include_mathjax=True)
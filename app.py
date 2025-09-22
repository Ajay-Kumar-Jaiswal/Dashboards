import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv("netflix_titles.csv")
df.dropna(subset=['type','release_year','rating','country','duration'], inplace=True)

titles=len(df)
movies=len(df[df['type']=='Movie'])
shows=len(df[df['type']=='TV Show'])
countries=df['country'].nunique()

app=Dash(__name__)
server = app.server 
app.title="Netflix Dashborad"

app.layout=html.Div(style={'font-family': 'sans-serif','display':'flex'},children=[
    html.Div(style={'flex':'0 0 250px', 'min-width':'200px', 'max-width':'300px', 'overflowY':'auto', 'backgroundColor':'#111','color':'white','height':'100vh','padding':'20px'},children=[
        html.H4("Netflix",style={'color':'red'}),
        html.Label('Select Type'),
        dcc.Dropdown(
            id="type_filter",
            options=[{'label':t,'value':t} for t in df['type'].unique()]+[{'label':'All','value':'All'}],
            value='All',
            clearable=False,
            style={'margin-bottom':'20px','color':'black'}
        ),
        html.Label('Select Country'),
        dcc.Dropdown(
            id="county_type",
            options=[{'label': c, 'value': c} for c in df['country'].value_counts().head(10).index] + [{'label': 'All', 'value': 'All'}],
            value='All',
            clearable=False,
            style={'margin-bottom':'20px','color':'black'}
        ),
        html.Label('Range Slider'),
        dcc.RangeSlider(
            id='year_slider',
            min=int(df['release_year'].min()),
            max=int(df['release_year'].max()),
            value=(int(df['release_year'].min()),int(df['release_year'].max())),
            marks={year:str(year) for year in range(int(df['release_year'].min()),int(df['release_year'].max())+1,15)},
            tooltip={'placement':'bottom','always_visible':True}
        ),
    ]),
    html.Div(style={'backgroundColor':'#000','color':'black','flex':1},children=[
        html.H1("Netflix Data Analysis Dashboard",style={'color':'#1DB954','textAlign':'center'}),
        html.Div(style={'display':'flex','flex-wrap':'wrap','justify-content':'space-around'},children=[

            html.Div(style={'backgroundColor':'#111','width':'22%','border-radius':'10px','color':'white','textAlign':'center','padding':'20px','margin':'3px'},children=[
                html.H3('Title'),
                html.H2(titles),
            ]),
            html.Div(style={'backgroundColor':'#111','width':'22%','border-radius':'10px','color':'white','textAlign':'center','padding':'10px','margin':'3px'},children=[
                html.H3('Total Movies'),
                html.H2(movies),
            ]),
            html.Div(style={'backgroundColor':'#111','width':'22%','border-radius':'10px','color':'white','textAlign':'center','padding':'10px','margin':'3px'},children=[
                html.H3('Total Shows'),
                html.H2(shows),
            ]),
            html.Div(style={'backgroundColor':'#111','width':'22%','border-radius':'10px','color':'white','textAlign':'center','padding':'10px','margin':'3px'},children=[
                html.H3('Countries'),
                html.H2(countries),
            ]),
        ]),
        dcc.Tabs([
            dcc.Tab(label='Type & Rating',children=[
                html.Div([
                    dcc.Graph(id='filter_chart',style={'flex':1}),
                    dcc.Graph(id='rating_chart',style={'flex':1}),
                ],style={'display':'flex','flex-wrap':'wrap','justify-content':'space-around'}),
            ]),
            dcc.Tab(label='Movie Duration',children=[
                dcc.Graph(id='duration_chart')
            ]),
            dcc.Tab(label='Release & Country',children=[
                html.Div([
                    dcc.Graph(id='release_chart',style={'flex':1}),
                    dcc.Graph(id='country_chart',style={'flex':1}),
                ],style={'display':'flex','flex-wrap':'wrap','justify-content':'space-around'}),
            ]),
            dcc.Tab(label='Yearly Comparison',children=[
                dcc.Graph(id='yearly_chart')
            ]),
        ]),
    ]),
])

@app.callback(
    Output('filter_chart','figure'),
    Output('rating_chart','figure'),
    Output('duration_chart','figure'),
    Output('release_chart','figure'),
    Output('country_chart','figure'),
    Output('yearly_chart','figure'),
    Input('type_filter','value'),
    Input('county_type','value'),
    Input('year_slider','value'),
)

def update_chart(selected_type,selected_country,year_range):
    filtered=df.copy()
    if selected_type!='All':
        filtered=filtered[filtered['type']==selected_type]
    if selected_country!='All':
        filtered=filtered[filtered['country']==selected_country]
    filtered=filtered[(filtered['release_year']>=year_range[0]) & (filtered['release_year']<=year_range[1])]



    type_count=filtered['type'].value_counts()
    fig_type=px.bar(x=type_count.index,y=type_count.values,color=type_count.index,title="Comparison between Movies and TV Shows",labels={"x":"Type of Contents","y":"Number of Titles"})
    fig_type.update_layout(template="plotly_dark")

    rating_count=filtered['rating'].value_counts()
    rig_type=px.pie(names=rating_count.index,values=rating_count.values,title="Percentage of Content Ratings")
    rig_type.update_layout(template="plotly_dark")

    release_count=filtered['release_year'].value_counts()
    reg_type=px.line(x=release_count.index,y=release_count.values,title="Release Year vs Number of Shows",labels={'x':'Release Year','y':'Number of Shows'})
    reg_type.update_layout(template="plotly_dark")

    duration_count=filtered[filtered['type']=='Movie'].copy()
    duration_count['duration_int']=duration_count['duration'].str.replace(' min','').astype(int)
    dur_type=px.histogram(duration_count,x='duration_int',title="Distribution of Movie Duration",labels={'Count':'No. of Movies','duration_int':'Duration'})
    dur_type.update_traces(marker_line_color="black", marker_line_width=1)
    dur_type.update_layout(template="plotly_dark")

    country_count=filtered['country'].value_counts().head(10)
    count_type=px.bar(x=country_count.values,y=country_count.index,orientation='h',title="Top 10 Countries by Number of Shows",labels={'x':'Number of Shows','y':'Country'})
    count_type.update_layout(template="plotly_dark")

    content_by_year=filtered.groupby(['release_year','type']).size().unstack().fillna(0)
    filt_type=go.Figure()
    if 'Movie' in content_by_year.columns:
        filt_type.add_trace(go.Scatter(x=content_by_year.index,y=content_by_year['Movie'],mode='lines+markers',name='Movies'))
    if 'TV Show' in content_by_year.columns:
        filt_type.add_trace(go.Scatter(x=content_by_year.index,y=content_by_year['TV Show'],mode='lines+markers',name='TV Show'))
    filt_type.update_layout(title="Movies vs TV Shows Released per Year",template="plotly_dark",xaxis_title='Year',yaxis_title='Number of Shows')

    return fig_type,rig_type,dur_type,reg_type,count_type,filt_type
if __name__=="__main__":
    app.run(debug=True)


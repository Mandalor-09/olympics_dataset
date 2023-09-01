import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import helper
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

dataset1 = pd.read_csv('athlete_events.csv')
dataset2 = pd.read_csv('noc_regions.csv')

dataset = helper.preprocess(dataset1,dataset2)

st.sidebar.title('Olympic Analysis')
sidebar_data = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Countrywise Analysis','Athlete Wise Analysis')
)

if sidebar_data =='Medal Tally':
    medal_tally_data = helper.medal_tallys(dataset)
    countrylist,yearlist=helper.country_and_year(dataset)
    country = st.sidebar.selectbox('Select Country',countrylist)
    year = st.sidebar.selectbox('Select Year',yearlist)

    if country == 'Overall' and year == 'Overall':
        st.title('Olympic Countrywise Performannce')
        data = medal_tally_data
        st.table(data)
    if country != 'Overall' and year == 'Overall':
        st.title(f'Overall Olympic Data for Country: {country}')
        data = helper.country_data(country,dataset)
        st.table(data)
    if country == 'Overall' and year != 'Overall':
        st.title(f'Olympic Data for Year: {year}')
        data = helper.year_data(year,dataset)
        st.table(data)
    if country !='Overall' and year != 'Overall':
        st.title(f'Olympic Data for {country} in {year}')
        data = helper.both_present(country,year,dataset)
        st.table(data)

if sidebar_data == 'Overall Analysis':
    st.title('Overall Analysis')
    olympic_detail = helper.olympic_details(dataset)
    col1 ,col2,col3 =st.columns(3)
    with col1:
        st.header('Edition')
        st.title(olympic_detail['edition'])
    with col2:
        st.header('Hosts')
        st.title(olympic_detail['cities'])
    with col3:
        st.header('Events')
        st.title(olympic_detail['events'])
    col1 ,col2,col3 =st.columns(3)
    with col1:
        st.header('Sports')
        st.title(olympic_detail['sports'])
    with col3:
        st.header('Athletes')
        st.title(olympic_detail['athletes'])
    with col2:
        st.header('Nation')
        st.title(olympic_detail['nation'])

    line_plot_data = dataset.drop_duplicates(subset=['Year','region']).groupby('Year').count().reset_index().rename(columns={'region':'nation'})
    st.title('Participating nation Over the Years')
    fig = px.line(line_plot_data, x="Year", y="nation")
    fig.update_layout(yaxis_title="Number of Countries")
    fig.update_layout(xaxis_title="Years")
    st.plotly_chart(fig)
    
    line_plot_data=dataset.drop_duplicates(subset=['Year','Event']).groupby('Year').count()['Event'].reset_index().rename(columns={'event':'Event'})
    st.title('Events Over the Year')
    fig = px.line(line_plot_data, x="Year", y="Event")
    fig.update_layout(yaxis_title="Number of Events")
    fig.update_layout(xaxis_title="Years")
    st.plotly_chart(fig)

    line_plot_data=dataset.drop_duplicates(subset=['Year','Name']).groupby('Year').count()['Name'].reset_index().rename(columns={'Name':'Total Athlets'})
    st.title('Total Athlets in Olympics Over the years')
    fig = px.line(line_plot_data, x="Year", y="Total Athlets")
    fig.update_layout(yaxis_title="Number of Athlets")
    fig.update_layout(xaxis_title="Years")
    st.plotly_chart(fig)

    '''
    st.title('Popular Sports')
    heat_map_data = dataset.drop_duplicates(subset=['Sport', 'Year', 'Event']).pivot_table(index='Sport', columns='Year', aggfunc='count', fill_value=0).drop(columns=[1], errors='ignore')
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(heat_map_data, annot=True, fmt='g', cmap='YlOrBr', linewidths=0.5, ax=ax)
    st.pyplot(fig)
    '''

    st.title('Filter By Sport')
    sportlist = helper.sport_list(dataset)
    sport = st.selectbox('Select Sport', sportlist)
    data = helper.sport_bestmen(sport, dataset)
    if sport != 'Overall':
        a = data[data['Sport'] == sport].sort_values('Total', ascending=False).iloc[0:50].reset_index()
        st.table(a)
    else:
        st.table(data.iloc[0:50])




if sidebar_data == 'Countrywise Analysis':
    st.title('Country Analysis')
    sportlist = np.sort(dataset['region'].unique().tolist()).tolist()  # Or Use helper.country_and_year
    selected_country = st.selectbox('Select Sport', sportlist)
    st.header('Country Selected:', selected_country)

    st.title('Olympic Medal Over the Years')
    data = helper.country_analysis(selected_country, dataset)
    fig = px.line(data, x="Year", y=["Total", "Gold", "Silver", "Bronze"])
    st.plotly_chart(fig)

    st.title('Countries Best Performing Sports')
    data2 = helper.country_best_performing_sport(selected_country, dataset)
    fig2 = px.bar(data2, x="Event", y=["Total", "Gold", "Silver", "Bronze"])
    st.plotly_chart(fig2)

    st.title('Popular Sports')
    heat_map_data = helper.overall_game_performance(selected_country, dataset)
    fig = px.imshow(heat_map_data, labels=dict(x="Year", y="Event"), x=heat_map_data.columns, y=heat_map_data.index)
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig)

    st.title('Top Performin Athlits in the Country')
    data = dataset[dataset['region']==selected_country].groupby('Name').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index().iloc[0:25]
    data['Total']=data['Gold']+data['Silver']+data['Bronze']
    data = data.merge(dataset ,on='Name').drop_duplicates('Name')[['Name','Sport','Event','Gold_x','Silver_x','Bronze_x','Total']].rename(columns={'Gold_x':'Gold','Silver_x':'Silver','Bronze_x':'Bronze'}).reset_index().drop(columns=['index'])
    st.table(data)

if sidebar_data == 'Athlete Wise Analysis':
    st.title('Athlete Wise Analysis')
    data = dataset.drop_duplicates(subset=['Name', 'region'])
    x1 = data.dropna(subset=['Age'], axis=0)
    x2 = x1[x1['Medal'] == 'Gold']
    x3 = x1[x1['Medal'] == 'Silver']
    x4 = x1[x1['Medal'] == 'Bronze']

    fig = go.Figure()

    # Add a histogram trace for the age distribution of all athletes
    fig.add_trace(go.Histogram(x=x1['Age'], name='All Athletes', histnorm='probability density'))

    # Add a histogram trace for the age distribution of gold medalists
    fig.add_trace(go.Histogram(x=x2['Age'], name='Gold Medalists', histnorm='probability density'))

    # Add a histogram trace for the age distribution of silver medalists
    fig.add_trace(go.Histogram(x=x3['Age'], name='Silver Medalists', histnorm='probability density'))

    # Add a histogram trace for the age distribution of bronze medalists
    fig.add_trace(go.Histogram(x=x4['Age'], name='Bronze Medalists', histnorm='probability density'))

    fig.update_layout(barmode='overlay', title='Athlete Age Distribution by Medal Category')
    fig.update_traces(opacity=0.75)
    st.plotly_chart(fig)

    st.title('Weight/Height plot')
        
    data = dataset.drop_duplicates(subset=['Name', 'region'])
    data['Medal'].fillna('No Medal', inplace=True)

    sportlist = sorted(dataset['Sport'].unique().tolist())
    sportlist.insert(0, 'Overall')

    selected_sport = st.selectbox('Select Sport', sportlist)
    if selected_sport == 'Overall':
        data = data
    else:
        data = data[data['Sport'] == selected_sport]
        
    fig = px.scatter(data, x="Weight", y="Height", color="Medal",symbol="Sex" )
    st.plotly_chart(fig)

    st.title('Participation')
    fig = px.line(dataset.groupby(['Year', 'Sex']).size().reset_index(name='Count'), x='Year', y='Count', color='Sex')
    st.plotly_chart(fig)
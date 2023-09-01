from re import A
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns


def preprocess(dataset1,dataset2):
    dataset1 = dataset1[dataset1['Season']=='Summer']
    dataset = dataset1.merge(dataset2,on='NOC',how = 'left')
    dataset.drop_duplicates(inplace=True)
    data = pd.get_dummies(dataset['Medal'])
    dataset = pd.concat([dataset,data],axis=1) 
    return dataset

def medal_tallys(dataset):
    medal_tally = dataset.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

def country_and_year(dataset):
    countrylist = np.unique(dataset['region'].dropna().values).tolist()
    countrylist.sort()
    countrylist.insert(0,'Overall')

    yearlist = dataset['Year'].unique().tolist()
    yearlist.sort()
    yearlist.insert(0,'Overall')
    return countrylist,yearlist

def country_data(country,dataset):
    new = dataset.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    new = new[new['region']== country].sort_values('Year')
    new = new.groupby('Year').sum()[['Gold','Silver','Bronze']]
    new['Total'] = new['Gold']+new['Silver']+new['Bronze']
    return new

def year_data(year, dataset):
    new2 = dataset.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    new2 =new2[new2['Year']==year]
    new2 = new2.groupby('region')
    new2 = new2.sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False)
    new2['Total'] = new2['Gold'] + new2['Silver'] + new2['Bronze']
    return new2

def both_present(country, year, dataset):
    new3 = dataset.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])   
    new3 = new3[(new3['region'] == country) & (new3['Year'] == int(year))]
    new3 = new3.sort_values('Gold',ascending =False)[['Gold','Silver','Bronze']]
    new3['Total'] = new3['Gold'] + new3['Silver'] + new3['Bronze']
    return new3.sum()

def olympic_details(dataset):
    edition = len(dataset['Year'].unique().tolist())
    cities = len(dataset['City'].unique().tolist())
    sports = len(dataset['Sport'].unique().tolist())
    events = len(dataset['Event'].unique().tolist())
    athletes = len(dataset['Name'].unique().tolist())
    nation = len(dataset['region'].unique().tolist())

    return {'edition':edition,'cities':cities,'sports':sports,'events':events,'athletes':athletes,'nation':nation}


def sport_list(dataset):
    sportlist = np.unique(dataset['Sport'].dropna().values).tolist()
    sportlist.sort()
    sportlist.insert(0,'Overall')
    return sportlist

def sport_bestmen(sport,dataset):
    a = dataset.groupby('Name').sum()[['Gold','Silver','Bronze']]
    a['Total']=a['Gold']+a['Silver']+a['Bronze']
    a = a.sort_values('Total',ascending=False).iloc[:,3].reset_index()
    b = a.merge(dataset[['Name', 'region', 'City','Sport']], on='Name', how='left')

    b=b.drop_duplicates('Name')
    return b
    
def country_analysis(selected_country, dataset):
    dataset = dataset.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    data = dataset[dataset['region'] == selected_country].groupby('Year')[['Year', 'Gold', 'Silver', 'Bronze']].sum()
    data['Total'] = data['Gold'] + data['Silver'] + data['Bronze']
    data = data.drop(columns=['Year']).reset_index()
    return data

def country_best_performing_sport(selected_country,dataset):
    data = dataset[dataset['region']==selected_country]
    data = data.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal']).groupby('Event').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index().iloc[0:11]
    data['Total']=data['Gold']+data['Silver']+data['Bronze']
    return data

def overall_game_performance(selected_country,dataset):
  data = dataset[dataset['region']==selected_country]
  data = data.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
  data['Total']=data['Gold']+data['Silver']+data['Bronze']
  data = data.sort_values('Total',ascending=False)
  data = data.pivot_table(index='Event', columns='Year', aggfunc='count', fill_value=0)
  return data.reset_index()
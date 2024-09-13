import numpy as np 
import prepocessor
import pandas as pd

ab = prepocessor.preprocess()

def medal_tally(df):

    df = df.drop_duplicates(subset=['Team','NOC',"Games",'Year','City','Sport',"Event",'Medal'])

    medal_tally = df.groupby('region')[['Gold','Silver','Bronze']].sum().sort_values('Gold',ascending=False).reset_index()

    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def fetch_medal_tally(year,country):
 
    medal_df = ab.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def data_over_year(df,col):
    x = df.drop_duplicates(subset=['Year',col])['Year'].value_counts().reset_index().sort_values('Year').rename(columns={'count':col})
    return x

def sports_event_heatmap(df):
    a = df.drop_duplicates(subset=['Year','Sport','Event'])
    aa = pd.pivot_table(a,index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int')
    return aa

def most_sucessful_player(df,pm):
  t_df = df.dropna(subset=['Medal'])

  if pm == 'Overall':

    x = t_df['Name'].value_counts().reset_index().merge(t_df,left_on='Name',right_on = 'Name',how='left').drop_duplicates(subset=['Name']).head(15)[['Name','count','Sport','region']].rename(columns={'count':'Medals'})
    return x
  else:
    a = t_df[t_df['Sport']==pm]
    x = a['Name'].value_counts().reset_index().merge(t_df,left_on='Name',right_on = 'Name',how='left').drop_duplicates(subset=['Name']).head(15)[['Name','count','Sport','region']].rename(columns={'count':'Medals'})
    
    return x

def country_wise_medal(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team','NOC',"Games",'Year','City','Sport',"Event",'Medal'])
    new_df = temp_df[temp_df['region']==country]
    final_df = new_df.groupby('Year')['Medal'].count().reset_index()
    return final_df

def country_sport_medal_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team','NOC',"Games",'Year','City','Sport',"Event",'Medal'])
    new_df = temp_df[temp_df['region']==country]
    table = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype('int')
    return table


def country_top_athlete(df,pm):
  t_df = df.dropna(subset=['Medal'])


  a = t_df[t_df['region']==pm]
  x = a['Name'].value_counts().reset_index().merge(t_df,left_on='Name',right_on = 'Name',how='left').drop_duplicates(subset=['Name']).head(10)[['Name','count','Sport']].rename(columns={'count':'Medals'})
    
  return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final

print(country_wise_medal(ab,'USA'))


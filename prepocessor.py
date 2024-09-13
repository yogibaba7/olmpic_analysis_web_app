import pandas as pd

athlete = pd.read_csv('athlete_events.csv')
print(athlete.head())
region = pd.read_csv('noc_regions.csv')
print(region.head())

def preprocess():
    global athlete,region

    # selecting summer season
    df = athlete[athlete['Season']=='Summer']

    # merge with reason df
    df = df.merge(region,on='NOC',how="left")

    df = pd.concat([df,pd.get_dummies(df['Medal'],dtype='int')],axis=1)

    # drop duplicates
    df = df.drop_duplicates()
    
    return df

print(preprocess())


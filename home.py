import streamlit as st 
import pandas as pd 
import prepocessor,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff 

df = prepocessor.preprocess()
st.sidebar.header('Olmpic Analysis')
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
menu = st.sidebar.radio('select an option',['medal tally','overall analysis','country-wise analysis','athelete-wise analysis'])



if menu =='medal tally':
    st.sidebar.header('Medal Tally')
    years,country = helper.country_year_list(df)
    
    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select country',country)
    medal_tally = helper.fetch_medal_tally(selected_year,selected_country)

    if selected_year=='Overall' and selected_country == 'Overall':
        st.title('Overall Medal Tally')

    

    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Overall Olmpic Performance')
    
    if selected_year != 'Overall' and selected_country != 'overall':
        st.title(selected_country + " Performance In " + str(selected_year) + ' Olmpic')
    st.table(medal_tally)


if menu == 'overall analysis':
    editions = df['Year'].nunique()-1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    st.title('Top Statics')

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Athletes')
        st.title(athletes)
    with col3:
        st.header('Nations')
        st.title(nations)

    x = helper.data_over_year(df,'region')
    fig = px.line(x, x="Year", y='region')
    st.title('Participating Nations Over The Year')
    st.plotly_chart(fig)

    xx = helper.data_over_year(df,'Event')
    fig = px.line(xx, x="Year", y='Event')
    st.title('Events Over The Year')
    st.plotly_chart(fig)

    xxx = helper.data_over_year(df,'Name')
    fig = px.line(xxx, x="Year", y='Name')
    st.title('Athletes Over The Year')
    st.plotly_chart(fig)


    st.title("No. of Events over time(Every Sport)")
    xxxx = helper.sports_event_heatmap(df)
    fig,ax= plt.subplots(figsize=(20,20))
    ax = sns.heatmap(xxxx,annot=True)
    st.pyplot(fig)

    st.title('Most Sucessful Player')
    x= df['Sport'].unique().tolist()
    x.sort()
    x.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport',x)
    x = helper.most_sucessful_player(df,selected_sport)
    st.table(x)


if menu=='country-wise analysis':
    st.title('Country Wise Analysis')

    a = df['region'].dropna().unique().tolist()
    a.sort()

    selected_country = st.sidebar.selectbox('Select a Country',a)


    f_df = helper.country_wise_medal(df,selected_country)
    fig = px.line(f_df, x="Year", y="Medal")
    st.title(selected_country + 'Medal Tally Over The Years')
    st.plotly_chart(fig)



    st.title(selected_country + ' excels in the following sports')

    h_df = helper.country_sport_medal_heatmap(df,selected_country)
    fig,ax= plt.subplots(figsize=(20,20))
    ax = sns.heatmap(h_df,annot=True)
    st.pyplot(fig)


    st.title('Top 10 athletes of ' + selected_country)
    f_df = helper.country_top_athlete(df,selected_country)
    st.table(f_df)
print(df)


if menu == 'athelete-wise analysis':

    x = df.drop_duplicates(subset=['Name','region'])
    x1 = x['Age'].dropna()
    x2 = x[x['Medal']=='Gold']['Age'].dropna()
    x3 = x[x['Medal']=='Silver']['Age'].dropna()
    x4 = x[x['Medal']=='Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medallist','Silver Medallist','Bronze Medallist'],show_hist=False,show_rug=False)
    st.title('Distribution Of Age')
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)


    xx = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = x[x['Sport'] == sport]
        xx.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(xx, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x = temp_df['Weight'],y = temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],size=60)
    st.pyplot(fig)


    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
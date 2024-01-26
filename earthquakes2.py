import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px

# st.subheader('Earthquake interactive map by A.F.')
txt1 = 'Earthquake Interactive Map: A.Falkovskiy Jan 24 2024'
st.subheader(txt1)
col1, col2, col3, col4 = st.columns(4)




df = pd.read_csv("./data/database2.csv")

with col1:
      # Year slider
    year = st.slider("Select year", min_value=1965, max_value=2016, value=1970,  step=1)
    # st.text("year = " + str(year))
with col2:    
    yr = st.slider("Select year range", min_value=0, max_value=5, value=1,  step=1)
    # st.text("year range = " + str(yr))
with col3:    
    minMag = st.slider("Select minimum magnitude", min_value=5.5, max_value=10., value=6.,  step=0.5)
    # st.text("min magnitude = " + str(minMag))
with col4: shaw_all = st.checkbox('Shaw all earthquakes')

if shaw_all:
     txt1 = 'Earthquakes from 1965-2016'
     min_yr = 1965
     max_yr = 2016

else:     
    if yr>0:
        min_yr = max(year - yr, 1965)
        max_yr = min(year + yr, 2016)
        txt1 = 'Earthquakes from ' + str(min_yr) + " - " + str(max_yr)
    else:
            txt1 = 'Earthquakes ' + str(year)
st.header(txt1)



df['lat'] = df['Latitude']
df['lon'] = df['Longitude']
df['yr'] = df['Date']
df['yr'] = df['yr'].apply(lambda x: x.split('/')[-1])
df["yr"] = pd.to_numeric(df["yr"])
df['mg'] = df['Magnitude']
# df['mg'] = df['mg'].apply(lambda x: 2**x)
df['mg'] = df['mg'].apply(lambda x: 10.*(x-5.5))

# st.header('Data Header')
    

# df_flt = df.loc[df['yr'] == year]
df_flt = df.loc[(df['yr'] >= min_yr) & (df['yr'] <= max_yr) & (df['Magnitude'] > minMag)]

df2 = df_flt[['lat','lon','Magnitude','mg']]



colorArr=np.empty(len(df2.index))
for el in colorArr:
     el='red'
fig = px.scatter_mapbox(df2, lat="lat", lon="lon", title='Eathquakes', size='mg',
                        hover_data=['lat','lon','Magnitude'], color_discrete_sequence=[" #915C83"],
                        # hover_data=['lat','lon','Magnitude'], color_discrete_sequence=["darkred"],
                        # hover_data=['lat','lon','Magnitude'], color_discrete_sequence=["darkviolet"],
                        center=dict(lon=-8.674051848928324, lat=39.63074957184749), size_max=15, zoom=0.)

fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)

# st.map(df2)

st.subheader('Data Header')
st.write(df_flt.head())
# st.write(df2.head())
url1 = "https://www.rmseismic.com/lasviewer.html"
st.write("More geophysical web apps: [link](%s)" % url1)

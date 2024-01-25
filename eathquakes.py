import streamlit as st
import pandas as pd
import numpy as np

st.subheader('Earthquake interactive map by A.F.')
col1, col2, col3 = st.columns(3)






df = pd.read_csv("./data/database2.csv")

with col1:
      # Year slider
    year = st.slider("Select year", min_value=1965, max_value=2016, value=1970,  step=1)
    st.text("year = " + str(year))
with col2:    
    yr = st.slider("Select year range", min_value=0, max_value=5, value=1,  step=1)
    st.text("year range = " + str(yr))

with col3:    
    minMag = st.slider("Select minimum magnitude", min_value=0., max_value=10., value=1.,  step=0.5)
    st.text("min magnitude = " + str(minMag))

if yr>0:
    txt1 = 'Earthquakes from ' + str(year - yr) + " - " + str(year + yr)
else:
        txt1 = 'Earthquakes ' + str(year)
st.header(txt1)



df['lat'] = df['Latitude']
df['lon'] = df['Longitude']
df['yr'] = df['Date']
df['yr'] = df['yr'].apply(lambda x: x.split('/')[-1])
df["yr"] = pd.to_numeric(df["yr"])
df['mg'] = df['Magnitude']
df['mg'] = df['mg'].apply(lambda x: 5**x)

# st.header('Data Header')

df_flt = df.loc[df['yr'] == year]
df_flt = df.loc[(df['yr'] >= year - yr) & (df['yr'] <= year + yr) & (df['Magnitude'] > minMag)]

df2 = df_flt[['lat','lon','mg']]


import plotly.express as px



# Updated for Numpy 1.7.0:(Hat-tip to @Rolf Bartstra.)

colorArr=np.empty(len(df2.index))
for el in colorArr:
     el='red'
fig = px.scatter_mapbox(df2, lat="lat", lon="lon", title='Eathquakes', size='mg',
                        center=dict(lon=-8.674051848928324, lat=39.63074957184749), size_max=20, zoom=1)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)

# st.map(df2)

st.subheader('Data Header')
st.write(df_flt.head())
# st.write(df2.head())
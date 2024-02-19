import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px

# st.subheader('Earthquake interactive map by A.F.')
txt1 = 'Earthquake Interactive Map: A.Falkovskiy Feb 18 2024'
st.subheader(txt1)
col1, col2, col3, col4 = st.columns(4)




# df = pd.read_csv("./data/database2.csv")
df = pd.read_csv("./data/Significant_Earthquakes_new1.csv")
# df = pd.read_csv("./data/a1.csv")

with col1:
      # Year slider
    year = st.slider("Select year", min_value=1900, max_value=2024, value=1970,  step=1)
    # st.text("year = " + str(year))
with col2:    
    # yr = st.slider("Select year range", min_value=0, max_value=5, value=1,  step=1)
    yrRange = st.slider("Select year range", min_value=year, max_value=2024, value=(year,year),  step=1)
    min_yr = yrRange[0]
    max_yr = yrRange[1]
    yr=min_yr
    # st.text("year range = " + str(yr))
with col3:    
    # minMag = st.slider("Select minimum magnitude", min_value=5.5, max_value=10., value=6.,  step=0.25)
    # st.text("min magnitude = " + str(minMag))

    minMaxM = st.slider('Select magnitude range', 5.5, 10.0, (6.0, 10.0), step=0.25)
    minMag = minMaxM[0]
    maxMag = minMaxM[1]
    # st.write('Values:', minMag, maxMag)

with col4: shaw_all = st.checkbox('All earthquakes')

if shaw_all:
     txt1 = 'Earthquakes from 1900-2024'
     min_yr = 1900
     max_yr = 2024

else:     
    if yr>=0:
        # min_yr = max(year - yr, 1900)
        # max_yr = min(year + yr, 2024)
        txt1 = 'Earthquakes from ' + str(min_yr) + " - " + str(max_yr)
    else:
            txt1 = 'Earthquakes ' + str(year)
st.subheader(txt1)



df['lat'] = df['Latitude']
df['lon'] = df['Longitude']
df['yr'] = df['Date']
df['yr'] = df['yr'].apply(lambda x: x.split('/')[-1])
df["yr"] = pd.to_numeric(df["yr"])
df['mg'] = df['Magnitude']
# df['mg'] = df['mg'].apply(lambda x: 2**x)
df['mg'] = df['mg'].apply(lambda x: round(10.*(x-5.5),1))

# st.header('Data Header')
    

# df_flt = df.loc[df['yr'] == year]
df_flt = df.loc[(df['yr'] >= min_yr) & (df['yr'] <= max_yr) & (df['Magnitude'] >= minMag) & (df['Magnitude'] < maxMag)]

df2 = df_flt[['lat','lon','Magnitude','Date','mg']]



colorArr=np.empty(len(df2.index))
for el in colorArr:
     el='red'
fig = px.scatter_mapbox(df2, lat="lat", lon="lon", title='Eathquakes', size='mg',
                        hover_data=['lat','lon','Magnitude','Date'], color_discrete_sequence=[" #915C83"],
                        # hover_data=['lat','lon','Magnitude','Date'], color_discrete_sequence=["darkred"],
                        # hover_data=['lat','lon','Magnitude'], color_discrete_sequence=["darkred"],
                        # hover_data=['lat','lon','Magnitude'], color_discrete_sequence=["darkviolet"],
                        center=dict(lon=-8.674051848928324, lat=39.63074957184749), size_max=12, zoom=0.)

fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)

# st.map(df2)

txt2 = 'Earthquakes worldwide per year: ' + str(minMag) + ' ≤ M ≤ ' + str(maxMag)
st.subheader(txt2)
# st.write(df_flt.head())

# chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

# st.bar_chart(chart_data)

m6 = np.zeros(52)
m7 = np.zeros(52)
m8 = np.zeros(125)

ymin=1900

for index, row in df.iterrows():
    # print(row['lat'], row['lon'], 'yr = ', row['yr'])
    yr1 = row['yr']
    if row['Magnitude'] >= minMag and row['Magnitude'] <= maxMag:
        #  print('Mag > 8', yr1)
        # m8[yr1-1965] +=1
        m8[yr1-ymin] +=1
   
print(len(m8), " - ", len(range(1900, 2024, 1)))

chart_data = pd.DataFrame(
#    {"col1": list(range(1965, 2017, 1)), "col2": np.random.randn(52), "col3": np.random.randn(52)}
#    {"year": list(range(1965, 2017, 1)),"number of earthquakes": m8}
      {"year": list(range(1900, 2025, 1)),"number of earthquakes": m8}
)

st.bar_chart(
   chart_data, x="year", y=["number of earthquakes"], color=["#FF0000"]  # Optional
)

st.subheader('Dataset')
st.write(df_flt.head(200))

# st.write(df2.head())
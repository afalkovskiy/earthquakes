import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px

# st.subheader('Earthquake interactive map by A.F.')
txt1 = 'Earthquake Interactive Map version 6'
st.subheader(txt1)
st.write('Alex Falkovskiy, Feb 29 2024')

col1, col2, col3, col4, col5 = st.columns(5)




# df = pd.read_csv("./data/database2.csv")
df = pd.read_csv("./data/Significant_Earthquakes_new1.csv")
# df = pd.read_csv("./data/a1.csv")

with col1:
      # Year slider
    year = st.slider("Select year", min_value=1900, max_value=2024, value=1970,  step=1)
    # st.text("year = " + str(year))
with col2:    
    yrInterval = st.slider("Interval of years", min_value=0, max_value=10, value=0,  step=1)
    # yrRange = st.slider("Select year range", min_value=year, max_value=2024, value=(year,year),  step=1)
    # min_yr = yrRange[0]
    # max_yr = yrRange[1]
    min_yr = year
    max_yr = min(year + yrInterval, 2024)
    yr=min_yr
    # st.text("year range = " + str(yr))
with col3:    
    # minMag = st.slider("Select minimum magnitude", min_value=5.5, max_value=10., value=6.,  step=0.25)
    # st.text("min magnitude = " + str(minMag))

    minMaxM = st.slider('Magnitude range for earthquakes', 5.5, 10.0, (6.0, 10.0), step=0.1)
    minMagSel = minMaxM[0]
    maxMagSel = minMaxM[1]
    # st.write('Values:', minMag, maxMag)

with col4: shaw_all = st.checkbox('All years')

with col5: eventType = st.selectbox(
    'Select type of event',
    ('earthquake', 'nuclear explosion'))
     
if eventType == 'earthquake':
    eventTxt = 'Earthquakes'
    minMag = minMagSel
    maxMag = maxMagSel
if eventType == 'nuclear explosion':
    eventTxt = 'Nuclear explosions'
    minMag = 5.5
    maxMag = 10.
# if eventType == 'volcanic eruption':
#     eventTxt = 'Volcanic eruptions'


if shaw_all:
    if eventType == 'nuclear explosion':
        txt1 = 'Nuclear explosions from 1900-2024: M ≥ 5.5'
    else:    
        txt1 = eventTxt + ' from 1900-2024'+ ": " + str(minMagSel) + ' ≤ M ≤ ' + str(maxMagSel)
    min_yr = 1900
    max_yr = 2024

else:     
    if yrInterval>0:
        # min_yr = max(year - yr, 1900)
        # max_yr = min(year + yr, 2024)
        txt1 = eventTxt + ' from ' + str(min_yr) + " - " + str(max_yr) + ": " + str(minMagSel) + ' ≤ M ≤ ' + str(maxMagSel)
    else:
            txt1 = eventTxt + ' ' + str(year) + ": " + str(minMag) + ' ≤ M ≤ ' + str(maxMag)
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
df_flt = df.loc[(df['yr'] >= min_yr) & (df['yr'] <= max_yr) & (df['Magnitude'] >= minMag) & (df['Magnitude'] < maxMag)
                & (df['Type'] == eventType)]

df2 = df_flt[['lat','lon','Magnitude','Date','mg']]
df_flt3 = df.loc[(df['Magnitude'] >= 5.5) & (df['Magnitude'] < maxMag) & (df['Type'] == eventType)]
df3 = df_flt3[['lat','lon','Magnitude','Date','mg','yr']]



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


# chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

# st.bar_chart(chart_data)

m6 = np.zeros(52)
m7 = np.zeros(125)
m8 = np.zeros(125)

ymin=1900

for index, row in df.iterrows():
    # print(row['lat'], row['lon'], 'yr = ', row['yr'])
    yr1 = row['yr']
    if row['Magnitude'] >= minMagSel and row['Magnitude'] <= maxMagSel:
        #  print('Mag > 8', yr1)
        # m8[yr1-1965] +=1
        m7[yr1-ymin] +=1
   
print('All events ', len(m7), " - ", len(range(1900, 2024, 1)))

for index, row in df3.iterrows():
    # print(row['lat'], row['lon'], 'yr = ', row['yr'])
    yr1 = row['yr']
    # if row['Magnitude'] >= minMag and row['Magnitude'] <= maxMag:
    if row['Magnitude'] >= 5.5 and row['Magnitude'] <= maxMag:
        #  print('Mag > 8', yr1)
        # m8[yr1-1965] +=1
        m8[yr1-ymin] +=1
   
print(len(m8), " - ", len(range(1900, 2024, 1)))

if eventType == 'earthquake':
    txt2 ="Earthquakes worldwide per year: 5.5 ≤ M ≤ 10.0"
else:
    txt2 = eventTxt + ' worldwide per year: ' + str(minMag) + ' ≤ M ≤ ' + str(maxMag)
st.subheader(txt2)

chart_data = pd.DataFrame(
#    {"col1": list(range(1965, 2017, 1)), "col2": np.random.randn(52), "col3": np.random.randn(52)}
#    {"year": list(range(1965, 2017, 1)),"number of earthquakes": m8}
      {"year": list(range(1900, 2025, 1)),"number of events": m8}
)

chart_data2 = pd.DataFrame(
#    {"col1": list(range(1965, 2017, 1)), "col2": np.random.randn(52), "col3": np.random.randn(52)}
#    {"year": list(range(1965, 2017, 1)),"number of earthquakes": m8}
      {"year": list(range(1900, 2025, 1)),"number of events": m7}
)

colorSel = "#FF0000"
if eventType == 'nuclear explosion':
    colorSel = '#818589'
st.bar_chart(
   chart_data, x="year", y=["number of events"], color=[colorSel]  # Optional
)

txt3 ='Earthquakes worldwide per year: ' + str(minMagSel) + ' ≤ M ≤ ' + str(maxMagSel)
st.subheader(txt3)

st.bar_chart(
   chart_data2, x="year", y=["number of events"], color=["#FF0000"]  # Optional
)

st.subheader('Dataset')
st.write(df_flt.head(200))

# st.write(df2.head())
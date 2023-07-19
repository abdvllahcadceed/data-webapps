import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Page Title
#image = Image.open('nba-logo.jpg')

#st.image(image, use_column_width=True)

st.title('US NBA Player Stats Explorer')

st.markdown("""
	This App Performs Simple Web Scraping of US NBA Player Stats Data!
	* Application built in `Python` + `Streamlit` + `GitHub` by [Abdullahi M. Cadceed](https://twitter.com/@abdullahcadceed)
	* **Data Source:** [Basket Ball Reference](https://www.basketball-reference.com)
	""")

st.sidebar.header('User Input Features')
seleceted_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2023))))

# Web Scraping of NBA Player Stats
@st.cache_data
def load_data(year):
	url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
	html = pd.read_html(url, header = 0)
	df = html[0]
	raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating header in content
	raw = raw.fillna(0)
	playerstats = raw.drop(['Rk'], axis=1)
	return playerstats
playerstats = load_data(seleceted_year)

# Sidebar - Team Selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position Selection
unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering Data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of the Selected Team(s)')
st.write('Data Dimensions: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns')
st.dataframe(df_selected_team)

# Download NBA Player Stats Data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
	csv = df.to_csv(index=False)
	b64 = base64.b64encode(csv.encode()).decode() # strings <> bytes conversion
	href = f'<a href="data:file/csv,base64,{b64}" download="playerstats.csv">Click to Here Download CSV File</a>'
	return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap Visualization
if st.button('Click Here to See the Heatmap Visualization'):
	st.header('Intercorrelation Matrix Heatmap')
	df_selected_team.to_csv('output.csv', index=False)
	df = pd.read_csv(output.csv)

	corr = df.corr()
	mask = np.zero_like(corr)
	mask[np.trui_indicies_form(mask)] = True
	with sns.axes_style("white"):
		f, ax = plt.subplots(figsize=(6, 6))
		ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
	st.pyplot()






































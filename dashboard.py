import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# st.text("Bismillah Success with Allah ^-^")
st.title("Bike Sharing Data Dashboard")

# Read CSV file
day_df = pd.read_csv('data/day.csv')
day_df['dteday'] = pd.to_datetime(day_df['dteday'])


# prepare the processed data for visualization
# count the total number of bike rentals for each season
def create_season_count_df(df):
    season_count = df.groupby('season')['cnt'].sum().reset_index()
    return season_count

def create_weathersit_count_df(df):
    season_count = df.groupby('weathersit')['cnt'].sum().reset_index()
    return season_count

def create_monthly_rentals_with_season(df):
    df['month_year'] = df['dteday'].dt.to_period('M')
    monthly_day_df = df.groupby('month_year')['cnt'].sum().reset_index()
    season_mapping = {
        1: 'Spring',
        2: 'Summer',
        3: 'Fall',
        4: 'Winter'
    }
    df['season_name'] = df['season'].map(season_mapping)
    dominant_season_per_month = df.groupby(['month_year', 'season_name']).size().reset_index(name='count')
    dominant_season_per_month_df = dominant_season_per_month.loc[dominant_season_per_month.groupby('month_year')['count'].idxmax()].reset_index(drop=True)
    dominant_season_per_month_df = dominant_season_per_month_df[['month_year', 'season_name']]
    monthly_rentals_with_season = pd.merge(monthly_day_df, dominant_season_per_month_df, on='month_year', how='left')
    return monthly_rentals_with_season

# Craft dashboard elements
# Sidebar settings
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://cdn-icons-png.flaticon.com/512/2913/2913090.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# prepare the data for visualization
season_count_df = create_season_count_df(day_df)
monthly_rentals_with_season_df = create_monthly_rentals_with_season(day_df)
weathersit_count_df = create_weathersit_count_df(day_df)

# chart 1
st.subheader("Bike Rentals According to Season")
plt.figure(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=season_count_df, palette='viridis')
plt.title('Total Bike Rentals by Season')
plt.xlabel('Season')
plt.ylabel('Total Rentals')
plt.xticks(ticks=[0, 1, 2, 3], labels=['Spring', 'Summer', 'Fall', 'Winter'], rotation=45)
plt.grid(axis='y', linestyle='--')
plt.tight_layout()
st.pyplot(plt)

# chart 2
st.subheader("Monthly Bike Rentals with Season")
plt.figure(figsize=(12, 6))

# Plot the overall trend line in grey, without individual markers
sns.lineplot(
    x=monthly_rentals_with_season_df['month_year'].astype(str),
    y=monthly_rentals_with_season_df['cnt']/1000,
    color='grey', # Set the line color to grey
    marker=None, # No markers for this line plot
    legend=False, # Don't show a legend entry for the grey line
    ax=plt.gca() # Plot on the current axes
)

# Plot the markers, colored by season
sns.scatterplot(
    x=monthly_rentals_with_season_df['month_year'].astype(str),
    y=monthly_rentals_with_season_df['cnt']/1000,
    hue=monthly_rentals_with_season_df['season_name'], # Color points by season
    marker='o', # Set marker style to 'o'
    s=80, # Increase marker size for better visibility
    zorder=2, # Ensure points are drawn on top of the line
    ax=plt.gca() # Plot on the current axes
)

plt.title('Monthly Bike Rentals (from day_df)')
plt.xlabel('Month-Year')
plt.ylabel('Total Rentals (K)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

# # chart 3
# st.subheader("Correlation Matrix")
# plt.figure(figsize=(10, 8))
# numeric_df = day_df.select_dtypes(include=[np.number])
# correlation_matrix = numeric_df.corr()
# sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f', square=True)
# plt.title('Correlation Matrix of Bike Sharing Data')
# plt.tight_layout()
# st.pyplot(plt)

# chart 4
st.subheader("Bike Rentals According by Weekday")
plt.figure(figsize=(8,5))
sns.barplot(x='weekday', y='cnt', hue='weekday', data=day_df)
plt.title("Count of Rentals by Weekday")
plt.xlabel("Weekday")
plt.ylabel("Count of Rentals")
plt.tight_layout()
st.pyplot(plt)

# chart 5
st.subheader("Bike Rentals According to Weather Situation")
plt.figure(figsize=(10, 6))
sns.barplot(x='weathersit', y='cnt', data=weathersit_count_df, palette='viridis')
plt.title('Total Bike Rentals by Weather Situation')
plt.xlabel('Weather Situation')
plt.ylabel('Total Rentals')
plt.xticks(ticks=[0, 1, 2, 3], labels=['1', '2', '3', '4'])
plt.grid(axis='y', linestyle='--')
plt.tight_layout()
st.pyplot(plt)

# Weather situation details legend
st.markdown("""
**Weather Situation Details:**
- **1:** Clear, Few clouds, Partly cloudy, Partly cloudy
- **2:** Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
- **3:** Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
- **4:** Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
""")

footer_html = """
<style>
/* Center footer inside Streamlit's main block container (excludes sidebar) */
.block-container .footer {
    position: relative;
    margin: 16px auto 24px;
    max-width: 1100px;
    text-align: center;
    color: #6c757d;
    padding: 8px 0;
    font-size: 14px;
    left: 0;
    bottom: 0;
    pointer-events: none;
}
</style>
<div class="footer">Dashboard created by Risma Faoziya :)</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)



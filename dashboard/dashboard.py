import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# st.text("Bismillah Success with Allah ^-^")
st.title("Bike Sharing Data Dashboard")

# Read CSV file
main_df = pd.read_csv('./dashboard/main_df.csv')
main_df['dteday'] = pd.to_datetime(main_df['dteday'])


# prepare the processed data for visualization
# count the total number of bike rentals for each season
# question 1
def create_season_count_df(df):
    season_count = df.groupby('season_name')['cnt'].sum().reset_index().sort_values(by='cnt', ascending=False)
    return season_count

# question 2
def create_monthly_rentals_with_season(df):
    df['month_year'] = df['dteday'].dt.to_period('M')
    monthly_hour_df = df.groupby('month_year')['cnt'].sum().reset_index()

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
    monthly_rentals_with_season = pd.merge(monthly_hour_df, dominant_season_per_month_df, on='month_year', how='left')
    return monthly_rentals_with_season

# question 3
def create_weekday_count_df(df):
    weekday_count = df.groupby('weekday')['cnt'].sum().reset_index().sort_values(by='cnt', ascending=False)
    return weekday_count


# question 4
def create_weathersit_count_df(df):
    weathersit_count = df.groupby('weathersit')['cnt'].sum().reset_index().sort_values(by='cnt', ascending=False)
    return weathersit_count

# question 5
def create_hour_count_df(df):
    hour_count = df.groupby('hr')['cnt'].sum().reset_index().sort_values(by='cnt', ascending=False)
    return hour_count


# Craft dashboard elements
# Sidebar settings
min_date = main_df["dteday"].min()
max_date = main_df["dteday"].max()
 
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
season_count_df = create_season_count_df(main_df)
monthly_rentals_with_season_df = create_monthly_rentals_with_season(main_df)
weekday_count_df = create_weekday_count_df(main_df)
weathersit_count_df = create_weathersit_count_df(main_df)
hour_count_df = create_hour_count_df(main_df)

# chart 1
st.subheader("Bike Rentals According to Season")
plt.figure(figsize=(10, 6))
sns.barplot(x='season_name', y='cnt', data=season_count_df, palette='viridis')
plt.title('Total Bike Rentals by Season')
plt.xlabel('Season')
plt.ylabel('Total Rentals')
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

# chart 3
st.subheader("Bike Rentals According by Weekday")
plt.figure(figsize=(10, 6))
sns.barplot(x='weekday', y='cnt', data=weekday_count_df, palette='viridis', order=weekday_count_df['weekday'])
plt.title('Total Bike Rentals by Weekday')
plt.xlabel('Weekday')
plt.ylabel('Total Rentals')
plt.grid(axis='y', linestyle='--')
plt.tight_layout()
st.pyplot(plt)

# chart 4
st.subheader("Bike Rentals According to Weather Situation")
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='weathersit', y='cnt', data=weathersit_count_df, palette='viridis')
plt.title('Total Bike Rentals by Weather Situation')
plt.xlabel('Weather Situation')
plt.ylabel('Total Rentals')
plt.xticks(ticks=[0, 1, 2, 3], labels=['1', '2', '3', '4'])
plt.grid(axis='y', linestyle='--')

# Add count labels above the bars
for p in ax.patches:
    ax.annotate(f'{p.get_height():.0f}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', 
                xytext=(0, 10), 
                textcoords='offset points')

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

# chart 5
st.subheader("Bike Rentals According to Hour of the Day")
plt.figure(figsize=(10, 6))
sns.barplot(x='hr', y='cnt', data=hour_count_df.head(5), palette='viridis')
plt.title('Top 5 Total Bike Rentals by Hour')
plt.xlabel('Hour')
plt.ylabel('Total Rentals')
plt.grid(axis='y', linestyle='--')
plt.tight_layout()
st.pyplot(plt)

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



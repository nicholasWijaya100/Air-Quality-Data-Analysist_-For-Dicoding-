import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data (replace 'your_data.csv' with the actual file name)
combined_df = pd.read_csv('combined_data.csv')

# Convert 'year' and 'month' to datetime format for proper ordering
combined_df['date'] = pd.to_datetime(combined_df[['year', 'month']].assign(day=1))

# Define minimum and maximum dates
min_date = pd.to_datetime('2013-03-01')
max_date = pd.to_datetime('2017-02-28')

# Streamlit app
st.title('Air Quality Report From March 2013 to February 2017')

# Introduction
st.write(
    "This report provides insights into the air quality from March 2013 to February 2017. "
    "You can use the date picker to explore the mean temperature, AQI, and correlation matrix."
)

# Date picker for selecting the date range
start_date_temp = st.date_input('Select Start Date', min_date, min_value=min_date, max_value=max_date, key='start_date')
end_date_temp = st.date_input('Select End Date', max_date, min_value=min_date, max_value=max_date, key='end_date')

# Convert selected dates to datetime64[ns]
start_date_temp = pd.to_datetime(start_date_temp)
end_date_temp = pd.to_datetime(end_date_temp)

# Filter the DataFrame based on the selected date range for temperature
filtered_df_temp = combined_df[(combined_df['date'] >= start_date_temp) & (combined_df['date'] <= end_date_temp)]

# Group by 'date' and calculate the mean temperature
mean_temp_by_month = filtered_df_temp.groupby(['date'], as_index=False)['TEMP'].mean()

# Plotting temperature using seaborn
fig_temp, ax_temp = plt.subplots(figsize=(12, 6))
sns.lineplot(x='date', y='TEMP', data=mean_temp_by_month, marker='o', ax=ax_temp)
plt.title('Mean Temperature Over Time')
plt.xlabel('')
plt.ylabel('Temperature (°C)')
plt.xticks(rotation=45)

# Display the temperature plot in the Streamlit app
st.pyplot(fig_temp)

# Filter the DataFrame based on the selected date range for AQI
filtered_df_aqi = combined_df[(combined_df['date'] >= start_date_temp) & (combined_df['date'] <= end_date_temp)]

# Group by 'year' and calculate the mean AQI for each year
mean_aqi_by_year = filtered_df_aqi.groupby('year')['AQI_PM25'].mean().reset_index()

# Plotting AQI using seaborn
fig_aqi, ax_aqi = plt.subplots(figsize=(10, 6))
sns.lineplot(x='year', y='AQI_PM25', data=mean_aqi_by_year, marker='o', color='b', ax=ax_aqi)
ax_aqi.set_title(f'Mean AQI Over the Years ({start_date_temp.year}-{end_date_temp.year})')
ax_aqi.set_xlabel('')
ax_aqi.set_ylabel('Air Quality Index')
ax_aqi.grid(True)
ax_aqi.set_ylim(bottom=0, top=300)

# Display the AQI plot in the Streamlit app
st.pyplot(fig_aqi)

# Select relevant columns for correlation heatmap
selected_columns = ['O3', 'SO2', 'NO2', 'CO']
correlation_df = combined_df[selected_columns]

# Calculate the correlation matrix
correlation_matrix = correlation_df.corr()

# Create a heatmap to visualize the correlation matrix
fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax_corr)
ax_corr.set_title('Correlation Matrix of O3, SO2, NO2, and CO Levels')

# Display the correlation heatmap in the Streamlit app
st.pyplot(fig_corr)

# Additional information or conclusion
st.write(
    "The provided visualizations offer a comprehensive view of the air quality data, including temperature trends, AQI variations, and correlations between different pollutants."
)
import streamlit as st
from data_processing2 import fetch_data, clean_and_prepare_data, consistent_missing_value_strategy, min_max_scaling, feature_engineering, merge_datasets
from EDA2 import compare_top_performers, global_benchmarks, plot_correlation_matrix
from streamlit_visualizations2 import plot_distribution, plot_time_series, plot_choropleth

# Fetch and process the data
datasets = fetch_data()
cleaned_datasets = {name: clean_and_prepare_data(df) for name, df in datasets.items()}
cleaned_datasets = {name: consistent_missing_value_strategy(df) for name, df in cleaned_datasets.items()}
cleaned_datasets = {name: min_max_scaling(df) for name, df in cleaned_datasets.items()}
feature_engineered_datasets = feature_engineering(cleaned_datasets)
merged_df = merge_datasets(feature_engineered_datasets)

# Dashboard Title
st.markdown("# Global Health Metrics Dashboard")

# Display Merged DataFrame
st.markdown("##### Merged DataFrame")
st.write(merged_df)

# Visualization Sections
sections = [
    ("Life Expectancy", ["Distribution of Life Expectancy", "Time Series Analysis", "Choropleth Map"]),
    ("Infant Mortality", ["Distribution of Infant Mortality", "Time Series Analysis", "Choropleth Map"]),
    ("Obesity", ["Distribution of Obesity", "Time Series Analysis", "Choropleth Map"]),
    ("Hypertension", ["Distribution of Hypertension", "Time Series Analysis", "Choropleth Map"]),
    ("Water Access", ["Distribution of Water Access", "Time Series Analysis", "Choropleth Map"]),
    ("Sanitation Access", ["Distribution of Sanitation Access", "Time Series Analysis", "Choropleth Map"])
]

for name, vis_types in sections:
    st.markdown(f"### {name}")
    if "Distribution of Life Expectancy" in vis_types or f"Distribution of {name}" in vis_types:
        st.markdown(f"#### Distribution of {name}")
        plot_distribution(cleaned_datasets[name], name)
    if "Time Series Analysis" in vis_types or f"Time Series Analysis of {name}" in vis_types:
        st.markdown(f"#### Time Series Analysis of {name}")
        plot_time_series(cleaned_datasets[name], name)
    if "Choropleth Map" in vis_types or f"Choropleth Map of {name}" in vis_types:
        st.markdown(f"#### Choropleth Map of {name}")
        plot_choropleth(cleaned_datasets[name], name)

# Merged Health Data Section
st.markdown("### Merged Health Data")

st.markdown("#### Correlation Matrix")
plot_correlation_matrix(merged_df)

st.markdown("#### Comparison by Country")
compare_top_performers(merged_df, 'Country')

st.markdown("#### Comparison by Continent")
compare_top_performers(merged_df, 'Continent')

# Top-Performing Regions by Continent
st.markdown("#### Comparison of Top-Performing Regions by Continent")
risk_factors = ['NumericValue_Obesity', 'NumericValue_Hypertension', 'NumericValue_Water_Access', 'NumericValue_Sanitation_Access']
for risk_factor in risk_factors:
    risk_factor_name = risk_factor.split('_')[-1]
    st.markdown(f"#### Comparison of Top-Performing Regions ({risk_factor_name}) with Global Benchmarks")
    benchmark_data = global_benchmarks(merged_df)
    comparison_df = merged_df.groupby('Continent')[[risk_factor]].mean().subtract(benchmark_data.get(risk_factor, 0))
    st.bar_chart(comparison_df)

# Global Health Metrics Menu
st.markdown("### Global Health Metrics Menu")

# Country, Continent, and Year Range Selection
selected_country = st.selectbox('Select a Country', options=merged_df['Country'].dropna().unique())
selected_continent = st.selectbox('Select a Continent', options=merged_df['Continent'].dropna().unique())
year_range = st.slider('Select Year Range', min_value=int(merged_df['TimeDim'].min()), max_value=int(merged_df['TimeDim'].max()), value=(2000, 2020))

# Filter Data based on selections and remove NaN values
filtered_df = merged_df[(merged_df['Country'] == selected_country) & 
                        (merged_df['Continent'] == selected_continent) & 
                        (merged_df['TimeDim'] >= year_range[0]) & 
                        (merged_df['TimeDim'] <= year_range[1])].dropna()

# Display the filtered data
st.write(f"Filtered data for {selected_country}, {selected_continent} from {year_range[0]} to {year_range[1]}:")
st.write(filtered_df)

# Plot the filtered data
if st.checkbox('Show Choropleth Map'):
    plot_choropleth(filtered_df, f"Choropleth Map for {selected_country}, {selected_continent}")

if st.checkbox('Show Time Series'):
    plot_time_series(filtered_df, f"Time Series for {selected_country}, {selected_continent}")

if st.checkbox('Show Distribution Plot'):
    plot_distribution(filtered_df, f"Distribution for {selected_country}, {selected_continent}")

if st.checkbox('Show Correlation Matrix'):
    plot_correlation_matrix(filtered_df)

if st.checkbox('Show Comparison by Country'):
    compare_top_performers(filtered_df, 'Country')

if st.checkbox('Show Comparison by Continent'):
    compare_top_performers(filtered_df, 'Continent')

# Save the filtered data to a CSV file
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="💾 Download CSV",
    data=csv,
    file_name=f"filtered_data_{selected_country}_{selected_continent}_{year_range[0]}-{year_range[1]}.csv",
    mime='text/csv'
)

import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd
import plotly.express as px

# Function to plot the distribution of a numeric value
def plot_distribution(df, title, add_title=True):
    # Check if the DataFrame is empty or missing the 'NumericValue' column
    if df.empty or 'NumericValue' not in df.columns:
        st.warning(f"Not enough data to plot distribution for {title}.")
        return
    # Create a histogram plot with KDE (Kernel Density Estimate)
    plt.figure(figsize=(12, 6))
    sns.histplot(df['NumericValue'], kde=True, bins=30)
    # Add title if required
    if add_title:
        plt.title(f'Distribution of {title}')
    plt.xlabel('Numeric Value')
    plt.ylabel('Frequency')
    # Render the plot in the Streamlit app
    st.pyplot(plt)

# Function to plot a time series analysis
def plot_time_series(df, title, add_title=True):
    # Check if the DataFrame is empty or missing required columns
    if df.empty or 'TimeDim' not in df.columns or 'NumericValue' not in df.columns:
        st.warning(f"Not enough data to plot time series for {title}.")
        return

    # Check if there are any data points to plot
    if df['NumericValue'].isnull().all() or df['TimeDim'].isnull().all():
        st.warning(f"No valid data points to plot time series for {title}.")
        return

    # Create a line plot for time series analysis
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=df, x='TimeDim', y='NumericValue', hue='Country', legend=False)
    
    # Add title if required
    if add_title:
        plt.title(f'Time Series Plot of {title} by Country')
    
    plt.xlabel('Year')
    plt.ylabel('Numeric Value')
    
    # Render the plot in the Streamlit app
    st.pyplot(plt)

# Function to plot a choropleth map
def plot_choropleth(df, title, add_title=True):
    # Check if the DataFrame is empty or missing required columns
    if df.empty or 'Country' not in df.columns or 'NumericValue' not in df.columns:
        st.warning(f"Not enough data to plot choropleth map for {title}.")
        return
    
    # Create a choropleth map using Plotly Express with ISO-3 country codes
    fig = px.choropleth(df, 
                        locations="Country", 
                        locationmode="ISO-3",  # Updated to use ISO-3 country codes
                        color="NumericValue", 
                        hover_name="Country",
                        title=f'Choropleth Map of {title}' if add_title else None,
                        color_continuous_scale=px.colors.sequential.Plasma)
    
    # Render the map in the Streamlit app
    st.plotly_chart(fig)

# Function to plot a correlation matrix
def plot_correlation_matrix(df, add_title=True):
    # Select only numeric columns and drop 'TimeDim' if it exists
    plt.figure(figsize=(12, 8))
    numeric_df = df.select_dtypes(include=[np.number]).drop(columns=['TimeDim'])
    # Calculate the correlation matrix
    corr_matrix = numeric_df.corr()
    # Create a heatmap of the correlation matrix
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
    # Add title if required
    if add_title:
        plt.title("Correlation Matrix of Health Metrics and Risk Factors")
    # Render the heatmap in the Streamlit app
    st.pyplot(plt)

# Function to compare top performers with global benchmarks
def compare_top_performers(df, group_col, add_title=True):
    # Define the columns to adjust for comparison
    adjusted_columns = [
        'Life_Expectancy',
        'NumericValue_Infant_Mortality',
        'NumericValue_Obesity',
        'NumericValue_Hypertension',
        'NumericValue_Water_Access',
        'NumericValue_Sanitation_Access'
    ]
    
    # Calculate global benchmarks for the selected columns
    global_benchmarks_data = global_benchmarks(df)
    
    # Filter out rows with missing values in the group column
    filtered_df = df.dropna(subset=[group_col])
    # Identify groups that have non-missing 'Life_Expectancy' values
    valid_groups = filtered_df.groupby(group_col)['Life_Expectancy'].apply(lambda x: x.notna().any())
    # Filter to keep only valid groups
    filtered_df = filtered_df[filtered_df[group_col].isin(valid_groups[valid_groups].index)]
    # Identify top performers within each group
    top_performers = filtered_df.loc[filtered_df.groupby(group_col)['Life_Expectancy'].idxmax()]
    # Subtract global benchmarks from top performers' data
    comparison_df = top_performers.set_index(group_col)[adjusted_columns].subtract(global_benchmarks_data)

    # Create a bar plot to compare top performers with global benchmarks
    plt.figure(figsize=(12, 8))
    comparison_df.plot(kind='bar', figsize=(12, 8))
    # Add title if required
    if add_title:
        plt.title(f'Comparison of Top-Performing {group_col} with Global Benchmarks')
    plt.ylabel('Difference from Global Benchmark')
    plt.xlabel(group_col)
    # Add a horizontal line at 0 to indicate the benchmark level
    plt.axhline(0, color='red', linestyle='--')
    plt.xticks(rotation=45)
    # Render the plot in the Streamlit app
    st.pyplot(plt)

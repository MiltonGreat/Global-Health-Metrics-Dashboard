import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# 1. Correlation Analysis
def plot_correlation_matrix(df):
    plt.figure(figsize=(12, 8))
    numeric_df = df.select_dtypes(include=[np.number]).drop(columns=['TimeDim'], errors='ignore')
    corr_matrix = numeric_df.corr()
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
    plt.title("Correlation Matrix of Health Metrics and Risk Factors")
    st.pyplot(plt)

# 2. Comparison of Top Performers
def global_benchmarks(df):
    adjusted_columns = [
        'Life_Expectancy',
        'NumericValue_Infant_Mortality',
        'NumericValue_Obesity',
        'NumericValue_Hypertension',
        'NumericValue_Water_Access',
        'NumericValue_Sanitation_Access'
    ]
    return df[adjusted_columns].mean()

def compare_top_performers(df, group_col):
    adjusted_columns = [
        'Life_Expectancy',
        'NumericValue_Infant_Mortality',
        'NumericValue_Obesity',
        'NumericValue_Hypertension',
        'NumericValue_Water_Access',
        'NumericValue_Sanitation_Access'
    ]

    global_benchmarks_data = global_benchmarks(df)

    filtered_df = df.dropna(subset=[group_col])
    valid_groups = filtered_df.groupby(group_col)['Life_Expectancy'].apply(lambda x: x.notna().any())
    filtered_df = filtered_df[filtered_df[group_col].isin(valid_groups[valid_groups].index)]
    top_performers = filtered_df.loc[filtered_df.groupby(group_col)['Life_Expectancy'].idxmax()]
    comparison_df = top_performers.set_index(group_col)[adjusted_columns].subtract(global_benchmarks_data)

    plt.figure(figsize=(12, 8))
    comparison_df.plot(kind='bar', figsize=(12, 8))
    plt.title(f'Comparison of Top-Performing {group_col} with Global Benchmarks')
    plt.ylabel('Difference from Global Benchmark')
    plt.xlabel(group_col)
    plt.axhline(0, color='red', linestyle='--')
    plt.xticks(rotation=45)
    st.pyplot(plt)

# 3. Calculate Annual Change
def calculate_annual_change(df, group_col, year_col, metric_col):
    df_sorted = df.sort_values(by=[group_col, year_col])
    df_sorted['Annual_Change'] = df_sorted.groupby(group_col)[metric_col].diff().fillna(0)
    return df_sorted

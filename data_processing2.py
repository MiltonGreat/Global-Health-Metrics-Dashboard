import requests
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import streamlit as st

# 1. Data Fetching
@st.cache_data
def fetch_data():
    url_dict = {
        "Life Expectancy": "https://ghoapi.azureedge.net/api/WHOSIS_000001",
        "Infant Mortality": "https://ghoapi.azureedge.net/api/MDG_0000000026",
        "Obesity": "https://ghoapi.azureedge.net/api/NCD_BMI_30A",
        "Hypertension": "https://ghoapi.azureedge.net/api/NCD_HYP_CONTROL_A",
        "Water Access": "https://ghoapi.azureedge.net/api/WSH_WATER_BASIC",
        "Sanitation Access": "https://ghoapi.azureedge.net/api/WSH_SANITATION_SAFELY_MANAGED"
    }

    datasets = {}
    for name, url in url_dict.items():
        response = requests.get(url)
        if response.status_code == 200:
            datasets[name] = pd.DataFrame(response.json()['value'])
        else:
            st.error(f"Failed to fetch data from {url}. Status code: {response.status_code}")
    
    return datasets

# 2. Data Cleaning
def clean_and_prepare_data(df):
    columns_to_drop = [
        'IndicatorCode', 'TimeDimType', 'Value', 'Low', 'High',
        'Id', 'DataSourceDimType', 'DataSourceDim', 'Dim2', 
        'Dim2Type', 'Dim3', 'Dim3Type', 'Comments', 'Date', 
        'TimeDimensionBegin', 'TimeDimensionEnd', 'ParentLocationCode', 
        'Dim1Type', 'Dim1', 'TimeDimensionValue'
    ]
    
    df_cleaned = df.drop(columns=columns_to_drop, errors='ignore').copy()
    df_cleaned.rename(columns={'SpatialDim': 'Country', 'ParentLocation': 'Continent'}, inplace=True)
    df_cleaned.dropna(inplace=True)
    df_cleaned.reset_index(drop=True, inplace=True)
    
    return df_cleaned

# 3. Consistent Missing Value Strategy
def consistent_missing_value_strategy(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].interpolate(method='linear').ffill().bfill()
    return df

# 4. Scaling
def min_max_scaling(df, column='NumericValue'):
    scaler = MinMaxScaler()
    df[column] = scaler.fit_transform(df[[column]])
    return df

# 5. Feature Engineering
def feature_engineering(datasets):
    def add_change_over_time(df, column='NumericValue'):
        df = df.sort_values(by=['Country', 'TimeDim'])
        df['Change_' + column] = df.groupby('Country')[column].diff().fillna(0)
        return df

    def add_interaction_features(df, interaction_terms):
        for term1, term2 in interaction_terms:
            interaction_feature_name = f'{term1}_x_{term2}'
            df[interaction_feature_name] = df[term1] * df[term2]
        return df

    def categorize_life_expectancy(df):
        bins = [0, 0.6, 0.8, 1.0]
        labels = ['Low', 'Medium', 'High']
        df['LifeExpectancyCategory'] = pd.cut(df['NumericValue'], bins=bins, labels=labels)
        return df

    interaction_terms = [('NumericValue', 'Change_NumericValue')]
    for name, df in datasets.items():
        df = add_change_over_time(df)
        df = add_interaction_features(df, interaction_terms)
        if name == 'Life Expectancy':
            df = categorize_life_expectancy(df)
        datasets[name] = df

    return datasets

# 6. Merging Datasets
def merge_datasets(datasets):
    merged_df = datasets['Life Expectancy']

    for name, df in datasets.items():
        if name != 'Life Expectancy':
            merged_df = merged_df.merge(df, on=['Country', 'TimeDim'], how='outer', suffixes=('', f'_{name.replace(" ", "_")}'))
    
    merged_df.rename(columns={'NumericValue': 'Life_Expectancy'}, inplace=True)
    
    return merged_df

# Global-Health-Metrics-Dashboard

### 1. Project Title and Description

#### Project Title: 

Interactive Global Health Dashboard: Analyzing Global Health Metrics Using WHO Data

#### Description:

This project involves developing an interactive dashboard that allows users to explore key global health metrics such as life expectancy, infant mortality, and the impact of risk factors like hypertension and alcohol use. The dashboard is built using data from the World Health Organization's Global Health Observatory (WHO GHO) API and aims to provide insights into public health outcomes across different countries and regions.

### 2. Table of Contents

- Introduction
- Project Objective
- Data Description
- Methodology
- File Descriptions
- How to Use
- Interactive Dashboard Link
- Results and Insights
- Potential Challenges
- Acknowledgements
- License

### 3. Introduction

This project aims to develop an interactive dashboard using data from the World Health Organization's Global Health Observatory (WHO GHO) API. The dashboard will track key health metrics such as life expectancy and infant mortality. This is an Exploratory Data Analysis (EDA) project, which analyze how various health risk factors, like smoking and alcohol use, impact public health outcomes globally.

### 4. Project Objective

Outline the primary objectives:
   
- Explore at the trends in life expectancy and infant mortality across different countries.
- Assess the impact of risk factors, such as hypertension and alcohol use, have on life expectancy and health outcomes.

### 5. Data Description

- Data Sources: WHO Global Health Observatory (GHO) API.

- Metrics: Life Expectancy, Infant Mortality, Obesity, Hypertension, Water Access, and Sanitation Access.

- Format: JSON format, processed into DataFrames for analysis.

### 6. Methodology

- Data Collection and Preprocessing: API setup, data fetching, cleaning, and handling missing values.

- Exploratory Data Analysis (EDA): Descriptive statistics, correlation analysis, and visualization using Matplotlib, Seaborn, and Plotly.

- Interactive Dashboard: Built using Streamlit, includes line charts, choropleth maps, and scatter plots.

### 7. File Descriptions

- app3.py: The main script for running the Streamlit app. 

- data_processing2.py: This script includes the data fetching and preprocessing functions.

- EDA2.py: This script includes the EDA functions.

- streamlit_visualization2.py: This script includes the visualization functions.

- cleaned_merged_dataset.csv: The final cleaned and merged dataset containing global health metrics.

- Global Health Metrics Dashboard.ipynb: This is the Jupyter notebooks used during the development and testing phases of the project.

- README.md: This file, which provides an overview of the project, instructions for use, and links to resources.

### 8. How to Use

Setup Instructions: Provide step-by-step instructions on how to set up the environment, install necessary dependencies, and run the project.

Use this prompt (bash) in the Command Prompt to run app3.py: streamlit run app3.py

### 9. Interactive Dashboard Link

Here is a link to deployed Streamlit app: https://global-health-metrics-dashboard-d5eeze5wyomofqsmoldyht.streamlit.app/

### 10. Results and Insights

Based on the datasets, the global average:

- Life Expectancy (71 yrs)
- Infant Mortality (140 per 100,000 people)
- Obesity (16.40%)
- Hypertension (10.57%)
- Water Access (85.31%)

Based on the feature engineering:

- Life Expectancy: shows a relatively stable and positive trend in life expectancy over time.
- Infant Mortality: This dataset shows a general decrease over time, indicating improvements in reducing infant mortality in most countries.
- Obesity: There is an increasing trend in obesity, reflecting the growing concern over obesity rates.
- Hypertension: indicates a mixed trend, with some countries seeing increases in hypertension while others see reductions.
- Water Access: Most countries show improvements in water access.
- Sanitation Access: shows a mix of trends, with some regions significantly improving sanitation access while others lag behind. 

Based on the correlaton of merged health data:

The list of countries with reductions in these health metrics suggests which countries have successfully implemented policies or interventions that have led to improvements in public health.

### 11. Potential Challenges

- Some API endpoints may have missing data for certain countries or years. This will be handled by imputing missing values where appropriate or excluding countries/regions with insufficient data.

- Creating complex interactive visualizations (e.g., choropleth maps) might take more time than anticipated. This challenge will be mitigated by focusing on essential features first, then expanding if time permits.

### 12. Acknowledgements

Global Health Observatory (World Health Organization) offers a centralized and comprehensive source of information and analyses on global health R&D activities. The Observatory monitors various health R&D related data and incorporates these in comprehensive analyses. For more information, go to: [Global Health Observatory - World Health Organization (WHO](https://www.who.int/data/gho)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pyecharts import options as opts
from pyecharts.charts import Gauge
from sqlalchemy import create_engine

# Define the database URL
db_url = "postgresql://postgres:postgres@localhost:5432/EmployeeManagement"

# Create the engine object
engine = create_engine(db_url)

# Load the data from the database tables
contract_projects_df = pd.read_sql_table('contract_projects', engine)
work_locations_df = pd.read_sql_table('work_locations', engine)
educations_df = pd.read_sql_table('educations', engine)
clearances_df = pd.read_sql_table('clearances', engine)
employees_df = pd.read_sql_table('employees', engine)

# Create dropdowns for filtering
contract_project_options = contract_projects_df['name'].tolist()
work_location_options = work_locations_df['name'].tolist()
education_options = educations_df['level'].tolist()
clearance_options = clearances_df['level'].tolist()

# Sidebar filters
st.sidebar.header('Filter Data')
selected_contract_projects = st.sidebar.multiselect('Contract Project', contract_project_options, default=contract_project_options)
selected_work_locations = st.sidebar.multiselect('Work Location', work_location_options, default=work_location_options)
selected_educations = st.sidebar.multiselect('Education Level', education_options, default=education_options)
selected_clearances = st.sidebar.multiselect('Clearance Level', clearance_options, default=clearance_options)

# Filter the data based on user selections
if selected_contract_projects:
    filtered_employees_df = employees_df[
        employees_df['contract_project_id'].isin(
            contract_projects_df.loc[contract_projects_df['name'].isin(selected_contract_projects), 'contract_project_id'].values
        )
    ]
else:
    filtered_employees_df = employees_df.copy()

if selected_work_locations:
    filtered_employees_df = filtered_employees_df[
        filtered_employees_df['work_location_id'].isin(
            work_locations_df.loc[work_locations_df['name'].isin(selected_work_locations), 'work_location_id'].values
        )
    ]

if selected_educations:
    filtered_employees_df = filtered_employees_df[
        filtered_employees_df['education_id'].isin(
            educations_df.loc[educations_df['level'].isin(selected_educations), 'education_id'].values
        )
    ]

if selected_clearances:
    filtered_employees_df = filtered_employees_df[
        filtered_employees_df['clearance_id'].isin(
            clearances_df.loc[clearances_df['level'].isin(selected_clearances), 'clearance_id'].values
        )
    ]

# Display the filtered data
st.write('Filtered Employees Data')
st.dataframe(filtered_employees_df)

# Display the total count of filtered employees
st.write(f'Total Employees: {len(filtered_employees_df)}')

# Create two columns for visualizations
col1, col2 = st.columns(2)

# Bar chart of employees per contract project
with col1:
    st.subheader('Employees per Contract Project')
    contract_project_counts = filtered_employees_df['contract_project_id'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=contract_project_counts.index, y=contract_project_counts.values)
    plt.xlabel('Contract Project')
    plt.ylabel('Count')
    st.pyplot(fig)

# Pie chart of employees per clearance level
with col2:
    st.subheader('Employees per Clearance Level')
    clearance_counts = filtered_employees_df['clearance_id'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.pie(clearance_counts.values, labels=clearance_counts.index, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    st.pyplot(fig)
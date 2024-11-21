#!/usr/bin/env python
# coding: utf-8

# # FRED Data - Consumer Price Index

# In[1]:


import requests
import pandas as pd
from sqlalchemy

# Define your API key and FRED API URLs for CPI, GDP, and Unemployment Rate
api_key = 'c081e5bfcdb59bb8856c4a91a95640c2'

# FRED API URLs for CPI, GDP, and Unemployment Rate
urls = {
    'cpi': f'https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCSL&api_key={api_key}&file_type=json',
    'gdp': f'https://api.stlouisfed.org/fred/series/observations?series_id=GDP&api_key={api_key}&file_type=json',
    'unemployment': f'https://api.stlouisfed.org/fred/series/observations?series_id=UNRATE&api_key={api_key}&file_type=json'
}

# Function to fetch data from the FRED API
def fetch_fred_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if the request fails
    return response.json()['observations']

# Fetch data for each series
cpi_data = fetch_fred_data(urls['cpi'])
gdp_data = fetch_fred_data(urls['gdp'])
unemployment_data = fetch_fred_data(urls['unemployment'])

# Convert to pandas DataFrame
def to_dataframe(data):
    return pd.DataFrame(data, columns=['date', 'value'])

# Ensure to use the correct DataFrame conversion for each data set
cpi_df = to_dataframe(cpi_data)
gdp_df = to_dataframe(gdp_data)
unemployment_df = to_dataframe(unemployment_data)

engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/fred')

# Define table names (ensure the tables already exist in your database)
table_names = {
    'cpi': 'cpi_table',
    'gdp': 'gdp_table',
    'unemployment': 'unemployment_table'
}

# Insert data into PostgreSQL using SQLAlchemy
def insert_data(df, table_name):
    # Use pandas `to_sql` method to insert data into PostgreSQL
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"Data inserted into {table_name} successfully.")

# Insert data into corresponding tables
insert_data(cpi_df, table_names['cpi'])
insert_data(gdp_df, table_names['gdp'])
insert_data(unemployment_df, table_names['unemployment'])

print("Data successfully inserted into the database.")


# In[2]:


# Sort cpi_df by date column in descending order
cpi_df = cpi_df.sort_values(by='date', ascending=False)
gdp_df = gdp_df.sort_values(by='date', ascending=False)
unemployment_df = unemployment_df.sort_values(by='date', ascending=False)

# Optionally reset the index if needed
cpi_df = cpi_df.reset_index(drop=True)
gdp_df = gdp_df.reset_index(drop=True)
unemployment_df = unemployment_df.reset_index(drop=True)


# # Streamlit 

# ## CPI 

# In[3]:


#hard code December 2023/2024
cpi_dec_date_row =  cpi_df[cpi_df['date'] == '2023-12-01']
cpi_dec_date = cpi_dec_date_row['date'].iloc[0]
cpi_dec_value = float(cpi_dec_date_row['value'].iloc[0])

#current/most recent metrics
cpi_max_date_row = cpi_df[cpi_df['date'] == cpi_df['date'].max()]
cpi_max_date = cpi_max_date_row['date'].iloc[0]
cpi_max_value = float(cpi_max_date_row['value'].iloc[0])

#delta (hard coded for now)
cpi_max_delta = round(((cpi_max_value - cpi_dec_value) / cpi_dec_value) *100, 2)


# In[4]:


#pip install streamlit
import streamlit as st


# In[5]:


st.title("Consumer Price Index (CPI)")
st.write("The Consumer Price Index (CPI) is a key economic indicator that measures the average change over time in the prices paid by urban consumers for a basket of goods and services. It is commonly used to track inflation and the cost of living. The CPI includes categories such as food, housing, transportation, and medical care, and is used by governments and central banks to make policy decisions, such as adjusting interest rates or social security payments.")
st.write("For detailed and up-to-date CPI data, you can visit the FRED CPI page provided by the Federal Reserve Economic Data (FRED) database.")


# In[6]:


st.divider()


# In[7]:


col1, col2 = st.columns(2)

with col1:
    st.metric(label="CPI December 2023", 
              value=cpi_dec_value)

with col2:
    st.metric(label="CPI Current Month", 
              value=cpi_max_value, 
              delta=f"{abs(cpi_max_delta)}%" if cpi_max_delta > 0 else f"{abs(cpi_max_delta)}%",
              delta_color="inverse"  # This inverts the arrow colors
             )


# In[16]:


import plotly.express as px

#cpi_data['date'] = pd.to_datetime(cpi_data['date'])
fig = px.line(cpi_data, x = 'date', y = 'value', title = 'Consumer Price Index (CPI)')
st.plotly_chart(fig)


# In[ ]:


st.divider()


# ## GDP 

# In[ ]:


st.title("Gross Domestic Product (GDP)")
st.write("Gross Domestic Product (GDP) measures the total value of all goods and services produced within a country over a specific period. It is a key indicator of economic health and is used by governments and central banks to guide policy decisions. GDP can be calculated using production, income, or expenditure approaches. For detailed and up-to-date data, visit the Bureau of Economic Analysis (BEA) or the Federal Reserve Economic Data (FRED) database.")


# In[ ]:


st.divider()


# #### Metrics 

# In[23]:


#hard code last date
gdp_last_date_row = gdp_df[gdp_df['date'] == '2024-07-01']
gdp_last_date = gdp_last_date_row['date'].iloc[0]
gdp_last_value = float(gdp_last_date_row['value'].iloc[0])

#current/most recent metrics
gdp_max_date_row = gdp_df[gdp_df['date'] == gdp_df['date'].max()]
gdp_max_date = gdp_max_date_row['date'].iloc[0]
gdp_max_value = float(gdp_max_date_row['value'].iloc[0])

#delta (hard coded for now)
gdp_max_delta = round(((gdp_max_value - gdp_last_value) / gdp_last_value) *100, 2)


# In[ ]:


col1, col2 = st.columns(2)

with col1:
    st.metric(label="GDP December 2023", 
              value=gdp_last_value)

with col2:
    st.metric(label="GDP Current Month", 
              value=gdp_max_value, 
              delta=f"{abs(gdp_max_delta)}%" if gdp_max_delta > 0 else f"{abs(gdp_max_delta)}%"
             )


# #### Chart

# In[ ]:


import plotly.express as px

#cpi_data['date'] = pd.to_datetime(cpi_data['date'])
fig = px.line(gdp_data, x = 'date', y = 'value', title = 'Gross Domestic Product (GDP)')
st.plotly_chart(fig)


# In[ ]:


st.divider()


# ### Unemployment 

# In[ ]:


st.title("Unemployment Rate")
st.write("The unemployment rate is a key economic indicator that measures the percentage of the labor force that is unemployed and actively seeking work. It is widely used to gauge the health of the labor market and the overall economy. A rising unemployment rate typically signals economic distress, while a low rate suggests a robust economy. Governments and policymakers monitor the unemployment rate closely to shape fiscal and monetary policies. For more detailed and up-to-date data, visit the Federal Reserve Economic Data (FRED) website.")


# In[ ]:


st.divider()


# #### Metrics

# In[ ]:


#hard code December 2023/2024
unemployment_dec_date_row = unemployment_df[unemployment_df['date'] == '2023-12-01']
unemployment_dec_date = unemployment_dec_date_row['date'].iloc[0]
unemployment_dec_value = float(unemployment_dec_date_row['value'].iloc[0])

#current/most recent metrics
unemployment_max_date_row = unemployment_df[unemployment_df['date'] == unemployment_df['date'].max()]
unemployment_max_date = unemployment_max_date_row['date'].iloc[0]
unemployment_max_value = float(unemployment_max_date_row['value'].iloc[0])

#delta (hard coded for now)
unemployment_max_delta = round(((unemployment_max_value - unemployment_dec_value) / unemployment_dec_value) * 100, 2)


# In[ ]:


col1, col2 = st.columns(2)

with col1:
    st.metric(label="Unemployment Rate December 2023", 
              value=unemployment_dec_value)

with col2:
    st.metric(label="Unemployment Rate Current Month", 
              value=unemployment_max_value, 
              delta=f"{abs(unemployment_max_delta)}%" if unemployment_max_delta > 0 else f"{abs(unemployment_max_delta)}%", 
              delta_color="inverse"  # This inverts the arrow colors
             )


# #### Chart

# In[ ]:


import plotly.express as px

#cpi_data['date'] = pd.to_datetime(cpi_data['date'])
fig = px.line(unemployment_data, x = 'date', y = 'value', title = 'Unemployment Rate')
st.plotly_chart(fig)


# In[ ]:


st.divider()


# ### News 

# In[15]:


st.title("Latest News")
st.write("Stay informed about the latest developments in the U.S. economy by exploring the latest headlines. Understand trends in consumer spending, price fluctuations, and their impacts on households and businesses. Choose a topic of interest to dive deeper into the factors shaping the U.S. economy today.")


# In[ ]:


import requests

API_KEY = '693382eb44694e848cd653f4ba8e51c4'
URL = 'https://newsapi.org/v2/top-headlines'

category = st.selectbox("Select a category", ["business", "entertainment", "general", "politics", "technology", "world", "other"])
keyword = st.selectbox("Select a topic", ["", "gas prices", "egg prices", "consumer spending", "cpi", "gdp", "unemployment", "inflation", "job market"])

if st.button("Get News"):
    params = {
        'country': 'us', # only united states
        'sortBy': 'publishedAt', #sort for most recent articles
        'category': category,  # Filter by category
        'apiKey': API_KEY
    }
    if keyword:  # Add keyword filter if a keyword is selected
        params['q'] = keyword
    
   # Fetch articles
    response = requests.get(URL, params=params)
    if response.status_code == 200:  # Check if the API call was successful
        articles = response.json().get('articles', [])[:5]  # Get the top 5 articles

        if articles:
            # Display articles
            for article in articles:
                st.write(f"**{article['title']}**")
                st.write(f"*{article['description']}*")
                st.write(article['url'])
                st.markdown("---")
        else:
            st.write("No articles found. Try a different category or topic.")
    else:
        st.write(f"Error: {response.status_code}. Unable to fetch articles.")


# In[ ]:





# In[ ]:





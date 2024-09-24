import requests
import pandas as pd
import streamlit as st

# Streamlit app
st.title("Median Household Income by County - Maryland")

# Load API key from Streamlit secrets
API_KEY = st.secrets["CENSUS_API_KEY"]

# Define the API URL
url = f"https://api.census.gov/data/2022/acs/acs5?get=NAME,B19013_001E&for=county:*&in=state:24&key={API_KEY}"

# Fetch the data
response = requests.get(url)

if response.status_code == 200:
    # Parse the response
    data = response.json()

    # Convert to a pandas DataFrame
    columns = data[0]
    rows = data[1:]
    df = pd.DataFrame(rows, columns=columns)

    # Rename columns for clarity
    df = df.rename(columns={"B19013_001E": "Median_Household_Income", "NAME": "County"})

    # Convert Median_Household_Income to a float
    df["Median_Household_Income"] = pd.to_numeric(df["Median_Household_Income"], errors='coerce')

    # Display the DataFrame in Streamlit
    st.write("### Median Household Income Data for Maryland Counties:")
    st.dataframe(df[["County", "Median_Household_Income"]])

    # Optional: Download as CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name='MD_Median_Household_Income_by_County.csv',
        mime='text/csv'
    )
else:
    st.error("Error fetching data. Please check your API key or try again later.")

import requests
import pandas as pd
import streamlit as st
import json

# Streamlit app
st.title("Median Household Income by County - Maryland")

# Load API key from Streamlit secrets
API_KEY = st.secrets["CENSUS_API_KEY"]

# Define the API URL
url = f"https://api.census.gov/data/2022/acs/acs5?get=NAME,B19013_001E&for=county:*&in=state:24&key={API_KEY}"

# Fetch the data
response = requests.get(url)

# Print out the response content for debugging
st.write("API Response Status Code:", response.status_code)
st.write("API Response Content (first 1000 characters):", response.text[:1000])

if response.status_code == 200:
    try:
        # Try to parse the response as JSON
        data = json.loads(response.text)
        
        # Convert to a pandas DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])

        # Rename columns for clarity
        df = df.rename(columns={"B19013_001E": "Median_Household_Income", "NAME": "County"})

        # Convert Median_Household_Income to a float
        df["Median_Household_Income"] = pd.to_numeric(df["Median_Household_Income"], errors='coerce')

        # Sort the DataFrame by Median_Household_Income in descending order
        df = df.sort_values("Median_Household_Income", ascending=False)

        # Display the DataFrame in Streamlit
        st.write("### Median Household Income Data for Maryland Counties:")
        st.dataframe(df[["County", "Median_Household_Income"]])

        # Create a bar chart
        st.write("### Bar Chart of Median Household Income by County")
        st.bar_chart(df.set_index("County")["Median_Household_Income"])

        # Optional: Download as CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name='MD_Median_Household_Income_by_County.csv',
            mime='text/csv'
        )
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse the response as JSON. Error: {str(e)}")
        st.write("Response content:")
        st.code(response.text)
        st.write("Please check if the API key is correct and if the API is returning valid JSON data.")
else:
    st.error(f"Failed to fetch data. Status code: {response.status_code}. Please check the API key and try again.")

# Created/Modified files during execution:
print("MD_Median_Household_Income_by_County.csv")

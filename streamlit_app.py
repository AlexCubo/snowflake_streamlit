import streamlit as st
import pandas as pd
import requests
import snowflake.connector

st.title('My Mom\'s New Healthy Diner')
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#Let's put a pick list here so the users can pick the fruit they want to include
fruit_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruit_to_show = my_fruit_list.loc[fruit_selected]

st.header('Breakfast Menu')

st.text("\U0001F963 Omega 3 and Bluberry Oatmeal") #you can probably use also st.write()
st.text("\U0001F957 Kale, Spinach and Rocket Smoothie")
st.text("\U0001F414 Hard-Boiled Free-Range Egg")
st.text("\U0001F951 \U0001F35E Avocado Toast")
st.text("\U0001F347 \U0001F350 \U0001F352 Some fruit")

st.header("\U0001F34C \U0001F353 Build Your Own Fruit Smoothie \U0001F95D \U0001F347")
#Display the table on the page
st.dataframe(fruit_to_show)

# New Section to display fruityvice api response
st.header('Fruityvice Fruit Advice!')
#create an Entry box
fruit_choice = st.text_input('What fruit would you like information about?', 'kiwi')
st.write('The user entered', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
## st.text(fruityvice_response.json()) # just writes the data to the screen, not formatted
# take the json version of the response and format it 
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
st.dataframe(fruityvice_normalized)

# Let's query our Snowflake Trial Account Metadata
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
##my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
##my_data_row = my_cur.fetchone()
##st.text("Hello from Snowflake:")
##st.text(my_data_row)

# Let's query some data instead
my_cur.execute("select * from fruit_load_list")
n_fruits = 3
my_data_row = my_cur.fetchmany(n_fruits)
st.header("The FRUIT_LOAD_LIST table contains many fruits.")
st.text('The first {} fruits are:'.format(n_fruits))
st.dataframe(my_data_row)





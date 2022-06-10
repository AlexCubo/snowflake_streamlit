import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError # library used in the Control of Flow

# help function definition
def get_fruityvice_data(fruit_choice):
  st.text("Barbun!")
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

def get_fruit_load_list(my_cnx):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from PC_RIVERY_DATABASE.PUBLIC.FRUIT_LOAD_LIST")
    return my_cur.fetchall()

def insert_row_snowflake(cnx, new_fruit):
  with cnx.cursor() as my_cur:
    my_cur.execute("insert into PC_RIVERY_DATABASE.PUBLIC.FRUIT_LOAD_LIST values ('" + new_fruit +"')")
    return "Thanks for adding " + new_fruit
  
st.title('My Mom\'s New Healthy Diner')
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

st.header('Breakfast Menu')

st.text("\U0001F963 Omega 3 and Bluberry Oatmeal") #you can probably use also st.write()
st.text("\U0001F957 Kale, Spinach and Rocket Smoothie")
st.text("\U0001F414 Hard-Boiled Free-Range Egg")
st.text("\U0001F951 \U0001F35E Avocado Toast")
st.text("\U0001F347 \U0001F350 \U0001F352 Some fruit")

st.header("\U0001F34C \U0001F353 Build Your Own Fruit Smoothie \U0001F95D \U0001F347")

#Let's put a pick list here so the users can pick the fruit they want to include
fruit_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruit_to_show = my_fruit_list.loc[fruit_selected]

#Display the table on the page
st.dataframe(fruit_to_show)

# New Section to display fruityvice api response
st.header('Fruityvice Fruit Advice!')
#create an Entry box
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error("Please select a fruit to get information")
  else:
    fruityvice_data = get_fruityvice_data(fruit_choice)
    st.dataframe(fruityvice_data)
except URLError as e:
  st.error()

st.header("View Our Fruit List - Add Your Favorites!")
# n_fruits = 3
#st.text('The first {} fruits are:'.format(n_fruits))
#st.dataframe(my_data_row)

if st.button('Fruits List'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  fruit_list = get_fruit_load_list(my_cnx)
  my_cnx.close()
  st.dataframe(fruit_list)

# stop streamlit to avoid loading unwanted data in snowflake
# all code after streamlit.stop() will be ignored
#st.stop() 
  
my_fruit = st.text_input('What fruit would you like to add?')
if st.button('Add Fruit'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  msg = insert_row_snowflake(my_cnx, my_fruit)
  my_cnx.close()
  st.text(msg)
             

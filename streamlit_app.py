import streamlit as st
import pandas as pd

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
st.dataframe(my_fruit_list)

st.title('My Parents New Healthy Diner')

st.header('Breakfast Menu')

st.text("\U0001F963 Omega 3 and Bluberry Oatmeal") #you can probably use also st.write()
st.text("\U0001F957 Kale, Spinach and Rocket Smoothie")
st.text("\U0001F414 Hard-Boiled Free-Range Egg")
st.text("\U0001F951 \U0001F35E Avocado Toast")
st.text("\U0001F347 \U0001F350 \U0001F352 Some fruit")

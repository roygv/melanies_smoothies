# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smootie will be:', name_on_order)

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Banana", "Strawberries", "Peaches"),
# )

# st.write("You selected:", option)
ingredients_list = st.multiselect("Choose up to 5 ingredeints",
                                 my_dataframe,
                                 max_selections=5)

if ingredients_list:

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

    my_insert_stmt = """ insert into smoothies.public.orders
            (ingredients, name_on_order)
            values ('""" + ingredients_string + "', '" + name_on_order + "')"
    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit')
    if time_to_insert and ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered!', icon="✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response)
st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

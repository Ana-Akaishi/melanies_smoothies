# Import python packages
import streamlit as st
import requests
import pandas as pd
## Use the col function to call the FRUIT_NAMEM column from fruit_options database
from snowflake.snowpark.functions import col

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title("Customize Your Smoothie ")
st.write("Choose the fruits you want in your custom Smmoothie!")

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be', name_on_order)

# smoothie fruit option
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)

#convert the snowpark dataframe to a pandas dataframe so we can use the loc function
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect('Choose up to 5 ingredients:',my_dataframe,max_selections=5)
    
if ingredients_list:
# Create the INGREDIENTS_STRING Variable
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '# += means "add this to what is already in the variable"
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen+ ' Nutritional Information')
        smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
    # st.write(ingredients_string)

    # Build a SQL Insert Statement & Test It
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders (customer_name, ingredients) VALUES ('{name_on_order}', '{ingredients_string}')"""

    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert = st.button('Submit Order')

    # This if statement will depend if you clicked the submit order button
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon='✅')



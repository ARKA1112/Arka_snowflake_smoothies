
# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
# Request the customer to have his name entered
import requests



# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie
    """
)



name_on_order = st.text_input("Name")
st.write(f"Your name on the order will be {name_on_order}")


#Display the fruit_options table
cnx = st.connection('snowflake')
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data = my_dataframe, use_container_width=True)

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)

ingredients_list = st.multiselect('Choose up to 5 ingredients:',
                                 my_dataframe,max_selections=5)
st.write("You can select upto 5 items")


# look up the ingredients list
if ingredients_list:

    ingredients_string = ""
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + " Nutritional Information")
        if search_on = None:
            search_on=fruit_chosen
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+search_on)
        #st.text(fruityvice_response.json())
        fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width=True)

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS,NAME_ON_ORDER) VALUES ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Form")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered! {name_on_order}', icon="✅")
#####################EOF#####################################################

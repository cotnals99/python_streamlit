from codecs import getencoder
import pandas as pd
import plotly.express as px
import streamlit as st


#basic page configuration

st.set_page_config(page_title='Sales Dashboard',
                   page_icon=':bar_chart:',
                   layout='wide')

@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io='supermarkt_sales.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000,
    )
    # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

# print(df)
# st.dataframe(df)

# sidebar
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique(),
    # default="Yangon",
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique(),
    # default="Yangon",
)

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)


# mainpage
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.title(":chart_with_upwards_trend: Sales Dashboard")
st.markdown("##")

#Top KPIs
total_Sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:"*int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales")
    st.subheader(f"US $ {total_Sales:,}")
with middle_column:
    st.subheader("Average Rating")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("---")

# Sales by product line [Bar Chart]

sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)

fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# st.plotly_chart(fig_product_sales)
# st.dataframe(sales_by_product_line)


# Sales by hour [Bar Chart]
sales_by_hour = (
    df_selection.groupby(by=["hour"]).sum()[["Total"]]
)

fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by Hour</b>",
    color_discrete_sequence=["#008333"] * len(sales_by_hour),
    template="plotly_white",
)

fig_hourly_sales.update_layout(
    xaxis=(dict(tickmode='linear')),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


# st.plotly_chart(fig_hourly_sales)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)



# Hide Streamlit style
hide_st_Style = """
            <style>
            #MainMenu {visibility:hidden;}
            header {visibility:hidden;}
            footer {visibility:hidden;}
            </style>
            """

st.markdown(hide_st_Style, unsafe_allow_html=True)


st.dataframe(df_selection)

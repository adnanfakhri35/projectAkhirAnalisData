import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime

st.header('Project Akhir Analisis Data Dicoding, made by Kemas M Adnan Fakhri S F')

def create_orders_item_orders(df1,df2):
    orders_item_orders = pd.merge(
    left = df1,
    right = df2,
    how="right",
    left_on="order_id",
    right_on="order_id")

    return orders_item_orders

def create_order_bulanan(df):
    order_bulanan = df.resample(rule="M", on="order_purchase_timestamp").agg({
    "order_id":"count",})
    order_bulanan.index = order_bulanan.index.strftime('2018-%m-%d').sort_values(ascending=False)
    order_bulanan = order_bulanan.reset_index()
    order_bulanan.rename(columns={"order_id": "order_count"}, inplace=True)

    return order_bulanan

def create_orders_products(df1,df2):
    orders_products = pd.merge(
    left = df1,
    right = df2,
    how="right",
    left_on="product_id",
    right_on="product_id")

    return orders_products

def create_product_terbanyak(df):
    product_terbanyak = df.groupby(by="product_category_name").order_id.count().sort_values(ascending=False)
    product_terbanyak_df = pd.DataFrame(product_terbanyak)

    return product_terbanyak_df

products_csv = pd.read_csv("products.csv")
orders_csv = pd.read_csv("orders.csv")
orders_item_csv = pd.read_csv("orders_item.csv")
customers_csv = pd.read_csv("customers_data.csv")

orders_item_csv_df = pd.DataFrame(orders_item_csv)

datetime_columns = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']
orders_csv.reset_index(inplace=True)
for column in datetime_columns:
    orders_csv[column] = pd.to_datetime(orders_csv[column])
    orders_csv.set_index(orders_csv[column], inplace=True)

orders_item_orders_df = create_orders_item_orders(orders_item_csv, orders_csv)
order_bulanan_df = create_order_bulanan(orders_item_orders_df)
orders_products_df = create_orders_products(orders_item_orders_df, products_csv)
product_terbanyak_df = create_product_terbanyak(orders_products_df)

st.subheader('Penjualan dalam e-commerce (2018)')

fig, ax = plt.subplots(figsize=(10, 5))
plt.title("Penjualan dalam e-commerce (2018)", loc="center", fontsize=15)

ax.plot(
    order_bulanan_df['order_purchase_timestamp'], order_bulanan_df['order_count'], marker='o', linewidth=3, color="#32CD32"
)
ax.tick_params(axis='y', labelsize=10)
ax.tick_params(axis='x', labelsize=10, rotation=45)

st.pyplot(fig)

st.subheader("Produk yang paling banyak dan sedikit terjual")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(40, 20))

colors = ["#32cd32", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="order_id", y="product_category_name", data=product_terbanyak_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jumlah terjual", fontsize=50)
ax[0].set_title("Produk paling banyak terjual", loc="center", fontsize=60)
ax[0].tick_params(axis='y', labelsize=50)
ax[0].tick_params(axis='x', labelsize=50)

sns.barplot(x="order_id", y="product_category_name", data=product_terbanyak_df.sort_values(by="order_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jumlah terjual", fontsize=50)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk yang paling sedikit terjual", loc="center", fontsize=60)
ax[1].tick_params(axis='y', labelsize=50)
ax[1].tick_params(axis='x', labelsize=50)

st.pyplot(fig)

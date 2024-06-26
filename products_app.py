import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="products-31545")
dbPRODUCTS = db.collection('products')

st.header('Nuevo registro')

availability = st.text_input('availability')
brand = st.text_input('brand')
color = st.text_input('color')
condition = st.text_input('condition')
description = st.text_input('description')
images = st.text_input('images')
language = st.text_input('language')
mpn = st.text_input('mpn')
name = st.text_input('name')
price = st.text_input('price')
scraped_at = st.text_input('scraped_at')
size_list = st.text_input('size_list')
sku = st.text_input('sku')
url = st.text_input('url')

submit = st.button('Crear nuevo registro')

#Once the item has submitted, upload it to the database
if availability and brand and color and condition and description and images and language and mpn and name and price and scraped_at and size_list and sku and url:
    doc_ref = db.collection('products').document(availability)
    doc_ref.set({
        'availability' : availability,
        'brand' : brand,
        'color' : color,
        'condition' : condition,
        'description' : description,
        'images' : images,
        'language' : language,
        'mpn' : mpn,
        'name' : name,
        'price' : price,
        'scraped_at' : scraped_at,
        'size_list' : size_list,
        'sku' : sku,
        'url' : url
    })

    st.sidebar.write('Registro insertado correctamente')

###########Proceso de lectura##############
products_ref = list(db.collection(u'products').stream())
products_dict = list(map(lambda x: x.to_dict(), products_ref))
products_dataframe = pd.DataFrame(products_dict)
st.dataframe(products_dataframe)



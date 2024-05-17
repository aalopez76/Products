import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="products-project")
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

######Busqueda#################
def loadBybrand(brand):
    brand_ref = dbPRODUCTS.where(u'brand', u'==', brand)
    currentBrand = None
    for mybrand in brand_ref.stream():
        currentBrand = mybrand
    return currentBrand

st.sidebar.subheader('Buscar marca')
brandSearch = st.sidebar.text_input('brand', key='brand_search_input')
btnFiltrar = st.sidebar.button('Buscar')

if btnFiltrar:
    doc = loadBybrand(brandSearch)
    if doc is None:
        st.sidebar.write('Marca no existe')
    else:
        st.sidebar.write(doc.to_dict())

##############Actualización#################
st.sidebar.markdown("""---""")
newbrand = st.sidebar.text_input('Actualizar Marca')
btnActualizar = st.sidebar.button('Actualizar')

if btnActualizar:
    updatebrand = loadBybrand(brandSearch)
    if updatebrand is None:
        st.sidebar.write(f"{brandSearch} no existe")
    else:
        myupdatebrand = dbPRODUCTS.document(updatebrand.id)
        myupdatebrand.update(
            {
                'brand': newbrand
            }
        )

# Eliminación
st.sidebar.markdown("""---""")
btnEliminar = st.sidebar.button('Eliminar')

if btnEliminar:
    deletebrand = loadBybrand(brandSearch)
    if deletebrand is None:
        st.sidebar.write(f"{brandSearch} no existe")
    else:
        dbPRODUCTS.document(deletebrand.id).delete()
        st.sidebar.write(f"{brandSearch} eliminado")

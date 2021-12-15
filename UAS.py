import json
import pandas as pd
#import matplotlib.pyplot as plt
import streamlit as st 

st.title('Aplikasi Data Produksi Minyak Dunia')

oil_data = pd.read_csv(r'produksi_minyak_mentah.csv')
info_negara = open(r'kode_negara_lengkap.json')
kode = json.load(info_negara)

#============Daftar Negara================
daftar_negara = list()
for negara in kode :
    print(negara["name"])
    daftar_negara.append(negara["name"])

pilih_negara = st.selectbox('Pilih Negara',daftar_negara)
pilih_kode_negara = None
for negara in kode :
	if pilih_negara == negara ["name"] :
		pilih_kode_negara = negara ["alpha-3"]
		break

st.write(pilih_negara,pilih_kode_negara)

import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st 
import random

st.title('Aplikasi Data Produksi Minyak Dunia')

oil_data = pd.read_csv(r'produksi_minyak_mentah.csv')
info_negara = open(r'kode_negara_lengkap.json')
kode = json.load(info_negara)

#============Daftar Negara================
daftar_negara = list()
for negara in kode :
    print(negara["name"])
    daftar_negara.append(negara["name"])
warna = ("r","g","b","c","m","k")
excluded = ['WLD','G20','OECD','OEU','EU28']


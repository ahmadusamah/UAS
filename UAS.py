import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st 
import random

st.title('Data Produksi Minyak Dunia')

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
#============Soal Pertama================
pilih_negara = st.selectbox('Pilih Negara',daftar_negara)
pilih_kode_negara = None
for negara in kode :
	if pilih_negara == negara ["name"] :
		pilih_kode_negara = negara ["alpha-3"]

st.write(pilih_negara,pilih_kode_negara)

data = oil_data.loc[oil_data["kode_negara"] == pilih_kode_negara]   
data["tahun"] = data["tahun"].astype(int) 
data["produksi"] = data["produksi"].astype(int)     

data.plot(kind="line", x="tahun", y="produksi",c=random.choice(warna))
plt.title("Produksi Minyak ",pilih_negara)
plt.xlabel("Tahun Produksi")
plt.ylabel("Jumlah Produksi")
plt.show()



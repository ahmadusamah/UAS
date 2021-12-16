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
#============Soal Pertama================
pilih_negara = st.selectbox('Pilih Negara',daftar_negara)
pilih_kode_negara = None
for negara in kode :
	if pilih_negara == negara ["name"] :
		pilih_kode_negara = negara ["alpha-3"]
		break

st.write(pilih_negara,pilih_kode_negara)

data = oil_data.loc[oil_data["kode_negara"] == pilih_kode_negara]
data["tahun"] = data["tahun"].astype(int) 
data["produksi"] = data["produksi"].astype(int)     
data["tahun"] = data["tahun"].astype(int) 
data["produksi"] = data["produksi"].astype(int)     

data.plot(kind="line", x="tahun", y="produksi",c=random.choice(warna))
plt.title("Produksi Minyak ",pilih_negara)
plt.xlabel("Tahun Produksi")
plt.ylabel("Jumlah Produksi")
plt.show()

#============Soal Kedua================

pilih_tahun = st.slider("Pilih tahun:", 1971, 2015, 2000)
pilih_besar = st.number_input("Banyak negara yang ingin ditampilkan:", min_value = 1, max_value = 25)
data2 = oil_data.loc[oil_data["tahun"] == pilih_tahun ]
data2 = data2.sort_values(["produksi"], ascending=[0])
data2 = data2[~data2["kode_negara"].isin(excluded)]
data2 = data2[:pilih_besar]

for x in data2.index:
    kode1 = data2["kode_negara"][x]
    for y in kode:
        kode2 = y['alpha-3']
        if kode1 == kode2 :
            data2["kode_negara"][x] = y['name']
            
data2.plot(kind="bar", x="kode_negara", y="produksi")
plt.title(pilih_besar," Negara Produsen Minyak Terbesar pada Tahun ",pilih_tahun)
plt.xlabel("Negara")
plt.ylabel("Jumlah Produksi")
plt.show()


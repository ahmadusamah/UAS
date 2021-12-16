import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st 


st.set_page_config(layout="wide")
st.title('Data Produksi Minyak Dunia')
left_col,right_col = st.columns(2)

oil_data = pd.read_csv(r'produksi_minyak_mentah.csv')
info_negara = open(r'kode_negara_lengkap.json')
kode = json.load(info_negara)

#============Daftar Negara================
daftar_negara = list()
for negara in kode :
    print(negara["name"])
    daftar_negara.append(negara["name"])
excluded = ['WLD','G20','OECD','OEU','EU28']
oil_data = oil_data[~oil_data["kode_negara"].isin(excluded)]
#============Soal Pertama================
left_col.subheader("Data Minyak")
pilih_negara = left_col.selectbox('Pilih Negara',daftar_negara)
pilih_kode_negara = None
for negara in kode :
	if pilih_negara == negara ["name"] :
		pilih_kode_negara = negara ["alpha-3"]

data = oil_data.loc[oil_data["kode_negara"] == pilih_kode_negara]      
list_tahun = list()
list_produksi = list()
for x in data.index:
	list_tahun.append(data["tahun"][x])
	list_produksi.append(data["produksi"][x])
fig, ax = plt.subplots()
ax.bar(list_tahun, list_produksi)
left_col.pyplot(fig)
#============Soal Kedua================

right_col.subheader("Produsen Minyak Terbesar")
pilih_tahun = right_col.slider("Pilih tahun:", 1971, 2015, 2000)
pilih_besar = right_col.number_input("Banyak negara yang ingin ditampilkan:", min_value = 1, max_value = 25)
data2 = oil_data.loc[oil_data["tahun"] == pilih_tahun ]
data2 = data2.sort_values(["produksi"], ascending=[0])
data2 = data2[:pilih_besar]

for x in data2.index:
    kode1 = data2["kode_negara"][x]
    for y in kode:
        kode2 = y['alpha-3']
        if kode1 == kode2 :
            data2["kode_negara"][x] = y['name']
            
list_negara = list()
list_produksi1 = list()
for x in data2.index:
	list_negara.append(data2["kode_negara"][x])
	list_produksi1.append(data2["produksi"][x])
fig, ax = plt.subplots()
ax.bar(list_negara, list_produksi1)
ax.set_xticklabels(list_negara, rotation=90)
right_col.pyplot(fig)

#============Soal Ketiga================
left_col.subheader("Jumlah Produksi Terbesar Secara Kumulatif")
pilih_besar_2 = left_col.number_input("Banyak negara yang ingin ditampilkan:", min_value = 1, max_value = 29,value = 10)
data3 = oil_data.groupby("kode_negara")["produksi"].sum()

data3 = data3.sort_values(ascending=False)
data3 = data3[:pilih_besar_2]
left_col.write(data3)
list_index = list()
list_value = list()
for index, value in data3.items():
	for y in kode:
		kode2 = y['alpha-3']
		if index == kode2 :
 			index = y['name']
			list_index.append(index)
			list_value.append(value)
fig, ax = plt.subplots()
ax.bar(list_index, list_value)
ax.set_xticklabels(list_index, rotation=90)
left_col.pyplot(fig)
#============Soal Keempat================
right_col.subheader("Info")
pilih_tahun_3 = right_col.slider("Pilih tahun:", 1971, 2015, 2001)
pilih_besar_3 = right_col.number_input("Banyak negara yang ingin ditampilkan:", min_value = 1, max_value = 26,value = 10)
data4 = oil_data.loc[oil_data["tahun"] == pilih_tahun_3]
data4 = data4.sort_values(["produksi"], ascending=[0])
st.write(data4.index)
st.write(data4.columns)

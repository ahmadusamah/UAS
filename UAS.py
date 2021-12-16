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
            
data2.plot(kind="bar", x="kode_negara", y="produksi")
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
'''
for x in data3.index:
    kode1 = data3["kode_negara"][x]
    for y in kode:
        kode2 = y['alpha-3']
        if kode1 == kode2 :
            data3["kode_negara"][x] = y['name']
data3 = data3.groupby("kode_negara")["produksi"].sum()
data3 = data3.sort_values(ascending=False)
data3 = data3[:pilih_besar]
right_col.subheader("Jumlah Total Produksi Minyak Terbesar")

list_negara3 = list()
list_produksi3 = list()
for x in data3.index:
	list_negara3.append(data3["kode_negara"][x])
	list_produksi3.append(data3["produksi"][x])
fig, ax = plt.subplots()
ax.bar(list_negara3, list_produksi3)
ax.set_xticklabels(list_negara3, rotation=90)
right_col.pyplot(fig)'''

#============Soal Keempat================
right_col.subheader("Info")
pilih_tahun_2 = right_col.slider2("Pilih tahun:", 1971, 2015, 2000)
pilih_besar_2 = right_col.number_input2("Banyak negara yang ingin ditampilkan:", min_value = 1, max_value = 25)
data4 = oil_data.loc[oil_data["tahun"] == pilih_tahun_2]
data4 = data4.sort_values(["produksi"], ascending=[0])
imax = data4["produksi"].idxmax()
right_col.write(imax)

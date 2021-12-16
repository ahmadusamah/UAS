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
left_col.header("Data Minyak")
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

right_col.header("Produsen Minyak Terbesar")
pilih_tahun = right_col.slider("Pilih tahun:", 1971, 2015, 2000)
pilih_besar = right_col.number_input("Banyak negara yang ingin ditampilkan:", min_value = 1, max_value = 40,value = 3)
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
left_col.header("Jumlah Produksi Terbesar Secara Kumulatif")
pilih_besar_2 = left_col.number_input("Banyak negara yang ingin ditampilkan:", min_value = 1, max_value = 40,value = 10)
data3 = oil_data.groupby("kode_negara")["produksi"].sum()

data3 = data3.sort_values(ascending=False)
data3 = data3[:pilih_besar_2]

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
right_col.header("Info")
pilih_tahun_3 = right_col.slider("Pilih tahun:", 1971, 2015, 2001)
right_col.subheader("Data produsen minyak")
data4 = oil_data.loc[oil_data["tahun"] == pilih_tahun_3]
data4 = data4.sort_values(["produksi"], ascending=[0])
st.write(data4.groupby("kode_negara")["produksi"].max())

st.subheader("Data Kumulatif")
data5 = oil_data.groupby("kode_negara")["produksi"].sum()

max_value, max_index, min_value, min_index = (None, )*4
nama = list()
kodenegara = list()
region = list()
subregion = list()
for index, value in data.items():
	if max_value is None or value > max_value :
		max_value = value
		max_index = index
	if min_value is None or value < min_value and value != 0 :
		min_value = value
		min_index = index
	if value == 0:
		for y in kode:
			kode2 = y['alpha-3']
			if index == kode2 :
				nama.append(y['name'])
				kodenegara.append(y["country-code"])
				region.append(y["region"])
				subregion.append(y["sub-region"])

for y in kode:
	kode2 = y['alpha-3']
	if max_index == kode2 :
		st.write('Nama Negara :',y['name'],'\nKode Negara :',y["country-code"],'\nRegion :',y["region"],'\nSub-region :',y["sub-region"],'\nTotal Produksi :',max_value)
	if min_index == kode2 :
		st.write('Nama Negara :',y['name'],'\nKode Negara :',y["country-code"],'\nRegion :',y["region"],'\nSub-region :',y["sub-region"],'\nTotal Produksi :',min_value)

tabel = {'Nama Negara':nama,'Kode Negara':kodenegara,'Region':region,'Sub-region':subregion}
df = pd.DataFrame(data = tabel)
st.dataframe(df)



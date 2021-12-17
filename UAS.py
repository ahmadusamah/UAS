import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st 
import random

st.set_page_config(layout="wide")
st.title('Data Produksi Minyak Dunia')
left_col,right_col = st.columns(2)

oil_data = pd.read_csv(r'produksi_minyak_mentah.csv')
info_negara = open(r'kode_negara_lengkap.json')
kode = json.load(info_negara)

#============Daftar Negara================
daftar_negara = list()
for negara in kode :
    daftar_negara.append(negara["name"])
excluded = ['WLD','G20','OECD','OEU','EU28']
oil_data = oil_data[~oil_data["kode_negara"].isin(excluded)]
warna = ("r","g","b","c","m","k")
#============Soal Pertama================
left_col.header("Data Minyak per Negara")
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
ax.bar(list_tahun, list_produksi, color=random.choice(warna))
left_col.pyplot(fig)
#============Soal Kedua================

right_col.header("Daftar Produsen Minyak Terbesar")
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
ax.bar(list_negara, list_produksi1, color=warna)
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
ax.bar(list_index, list_value, color=warna)
ax.set_xticklabels(list_index, rotation=90)
left_col.pyplot(fig)

#============Soal Keempat================
def tulis(y):
		st.write('Nama Negara :',y['name'])
		st.write('Kode Negara :',y["country-code"])
		st.write('Region :',y["region"])
		st.write('Sub-region :',y["sub-region"])	

st.header("Informasi Terkait Data")
pilih_tahun_3 = left_col.slider("pada tahun:", 1971, 2015, 2001)

# Untuk data pertahun
with st.expander("Data Produsen Minyak pada Tahun Tertentu"):
	st.header("Data Produsen Minyak",(pilih_tahun_3))
	data4 = oil_data.loc[oil_data["tahun"] == pilih_tahun_3]
	data4 = data4.sort_values(["produksi"], ascending=[0])
	data4 = data4.groupby("kode_negara")["produksi"].sum()
	max_value1, max_index1, min_value1, min_index1 = (None, )*4
	nama1 = list()
	kodenegara1 = list()
	region1 = list()
	subregion1 = list()
	for index, value in data4.items():
		if max_value1 is None or value > max_value1 :
			max_value1 = value
			max_index1 = index
		if min_value1 is None or value < min_value1 and value != 0 :
			min_value1 = value
			min_index1 = index
		if value == 0:
			for y in kode:
				kode2 = y['alpha-3']
				if index == kode2 :
					nama1.append(y['name'])
					kodenegara1.append(y["country-code"])
					region1.append(y["region"])
					subregion1.append(y["sub-region"])

	for y in kode:
		kode2 = y['alpha-3']
		if max_index1 == kode2 :
			st.subheader("Negara dengan Produksi Terbesar")
			tulis(y)
			st.write('Total Produksi :', max_value1)
		if min_index1 == kode2 :
			st.subheader("Negara dengan Produksi Terkecil")
			tulis(y)
			st.write('Total Produksi :', min_value1)

	st.subheader("Negara dengan 0 Produksi Minyak")		
	tabel1 = {'Nama Negara':nama1,'Kode Negara':kodenegara1,'Region':region1,'Sub-region':subregion1}
	df1 = pd.DataFrame(data = tabel1)
	st.dataframe(df1)

# Untuk data kumulatif
with st.expander("Data Produsen Minyak Sepanjang 1971-2015"):
	st.header("Data Kumulatif")
	data5 = oil_data.groupby("kode_negara")["produksi"].sum()

	max_value, max_index, min_value, min_index = (None, )*4
	nama = list()
	kodenegara = list()
	region = list()
	subregion = list()
	for index, value in data5.items():
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
			st.subheader("Negara dengan Produksi Terbesar Sepanjang 1971-2015")
			tulis(y)
			st.write('Total Produksi :', max_value1)
		if min_index == kode2 :
			st.subheader("Negara dengan Produksi Terkecil Sepanjang 1971-2015")
			tulis(y)
			st.write('Total Produksi :', min_value1)

	st.subheader("Tabel Negara dengan Total 0 Produksi Minyak Sepanjang 1971-2015")
	tabel = {'Nama Negara':nama,'Kode Negara':kodenegara,'Region':region,'Sub-region':subregion}
	df = pd.DataFrame(data = tabel)
	st.dataframe(df)




# app6.py
import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# タイトル
st.title("ペンギンデータ可視化アプリ")

# データ読み込み
df = sns.load_dataset("penguins")

# 欠損値を削除（簡易処理）
df = df.dropna()

# サイドバーで種と性別を選択
species_list = df['species'].unique()
sex_list = df['sex'].unique()

selected_species = st.sidebar.multiselect("種（species）を選んでください", species_list, default=species_list.tolist())
selected_sex = st.sidebar.multiselect("性別（sex）を選んでください", sex_list, default=sex_list.tolist())

# フィルタリング
filtered_df = df[df['species'].isin(selected_species) & df['sex'].isin(selected_sex)]

# データ表示
st.subheader("選択されたデータ")
st.dataframe(filtered_df)

# 散布図で体長×体重を表示
st.subheader("体長と体重の関係（bill_length_mm × body_mass_g）")

fig, ax = plt.subplots()
for species in selected_species:
    subset = filtered_df[filtered_df['species'] == species]
    ax.scatter(subset['bill_length_mm'], subset['body_mass_g'], label=species)
ax.set_xlabel("bill length(mm)")
ax.set_ylabel("body mass(g)")
ax.legend()
st.pyplot(fig)
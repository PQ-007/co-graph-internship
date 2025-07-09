# app5.py
import streamlit as st
import requests

st.title("アニメ検索アプリ（Jikan API）")

# 入力フォーム
title = st.text_input("アニメタイトルを入力してください", "Naruto")

if title:
    # Jikan APIを呼び出し
    url = f"https://api.jikan.moe/v4/anime?q={title}&limit=5"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        results = data.get("data", [])
        if results:
            st.subheader(f"検索結果（{len(results)}件）：")
            for anime in results:
                st.markdown(f"### {anime['title']} ({anime.get('year', '年不明')})")
                st.image(anime['images']['jpg']['image_url'], width=200)
                st.write(anime.get('synopsis', 'あらすじ情報なし'))
                st.markdown(f"[MyAnimeListで見る]({anime['url']})")
                st.divider()
        else:
            st.warning("結果が見つかりませんでした。")
    else:
        st.error(f"APIエラー：ステータスコード {response.status_code}")
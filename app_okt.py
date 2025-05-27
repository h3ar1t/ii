
import streamlit as st
from konlpy.tag import Okt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re

st.set_page_config(page_title="한국어 형태소 기반 단어 빈도 분석기", layout="centered")

st.title("📊 한국어 형태소 기반 단어 빈도 분석기")

uploaded_file = st.file_uploader("텍스트 파일을 업로드하세요", type=["txt"])
text_input = st.text_area("또는 텍스트를 직접 입력하세요", height=300)

text = ""
if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
elif text_input:
    text = text_input

if text:
    # 텍스트 전처리
    text = re.sub(r"[^가-힣\s]", "", text)

    # 형태소 분석기로 명사 추출
    okt = Okt()
    nouns = okt.nouns(text)

    # 명사 길이 1 이상만 필터링
    words = [noun for noun in nouns if len(noun) > 1]

    word_freq = Counter(words)

    st.subheader("단어 빈도 상위 20개")
    for word, freq in word_freq.most_common(20):
        st.write(f"{word}: {freq}회")

    # 워드클라우드 생성
    wc = WordCloud(font_path="NanumGothic.ttf", background_color="white", width=800, height=400)
    wc.generate_from_frequencies(word_freq)

    st.subheader("워드클라우드")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
else:
    st.info("텍스트를 입력하거나 파일을 업로드하세요.")

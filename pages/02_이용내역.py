# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# 파일 불러오기
dong_df = pd.read_csv("행정구역(동별).csv")
bike_df = pd.read_csv("따릉이 이용내역_20250607.csv")

# 동-자치구 매핑 사전 생성
dong_to_gu = dict(zip(dong_df['동'], dong_df['자치구']))

# 대여소명이 들어 있는 열(E열)의 이름 확인 및 동 추출
# 예: '성산2동_1234' → '성산2동'
bike_df['대여동'] = bike_df.iloc[:, 4].str.split('_').str[0]

# 동을 자치구로 매핑 (없는 경우 NaN)
bike_df['자치구'] = bike_df['대여동'].map(dong_to_gu)

# 자치구별 이용 횟수 집계
gu_usage = bike_df['자치구'].value_counts().reset_index()
gu_usage.columns = ['자치구', '이용횟수']

# Streamlit UI 구성
st.title("서울시 자치구별 따릉이 이용 현황 (2025-06-07 기준)")

fig = px.bar(
    gu_usage.sort_values('이용횟수', ascending=False),
    x='자치구',
    y='이용횟수',
    title='자치구별 따릉이 대여 횟수',
    labels={'이용횟수': '이용 횟수', '자치구': '자치구'},
    color='이용횟수',
    color_continuous_scale='Viridis'
)

st.plotly_chart(fig)


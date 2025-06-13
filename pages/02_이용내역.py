import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 불러오기 (euc-kr 인코딩)
gu_dong_df = pd.read_csv("행정구역(동별).csv", encoding='euc-kr')
bike_df = pd.read_csv("따릉이 이용내역_20250607.csv", encoding='euc-kr')

# 동 → 자치구 매핑 딕셔너리 생성
dong_to_gu = dict(zip(gu_dong_df['동'], gu_dong_df['자치구']))

# 대여소명(E열)에서 동 이름 추출 (예: "신사동_101" → "신사동")
e_col = bike_df.columns[4]  # E열
bike_df['대여_동'] = bike_df[e_col].astype(str).str.split('_').str[0]

# 동 → 자치구 매핑
bike_df['대여_자치구'] = bike_df['대여_동'].map(dong_to_gu)

# 자치구별 대여 횟수 집계
gu_counts = bike_df['대여_자치구'].value_counts().reset_index()
gu_counts.columns = ['자치구', '대여 횟수']

# Streamlit 앱 UI
st.title("🚲 서울시 자치구별 따릉이 대여 횟수 (2025년 6월 7일 기준)")

# Plotly 막대 그래프
fig = px.bar(
    gu_counts,
    x='자치구',
    y='대여 횟수',
    title='자치구별 따릉이 대여 횟수',
    labels={'대여 횟수': '이용 횟수'},
    color='대여 횟수',
    color_continuous_scale='Blues',
)

fig.update_layout(xaxis_title='자치구', yaxis_title='대여 횟수')

st.plotly_chart(fig)

# 자치구별 데이터 테이블 출력
st.subheader("📋 자치구별 대여 횟수 데이터")
st.dataframe(gu_counts)

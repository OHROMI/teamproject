import streamlit as st
import pandas as pd
import plotly.express as px
import chardet

# 인코딩 자동 감지 함수
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(100000))
    return result['encoding']

# 파일 경로
gu_file = "행정구역(동별).csv"
bike_file = "따릉이 이용내역_20250607.csv"

# 인코딩 감지
gu_encoding = detect_encoding(gu_file)
bike_encoding = detect_encoding(bike_file)

# CSV 파일 불러오기
gu_dong_df = pd.read_csv(gu_file, encoding=gu_encoding)
bike_df = pd.read_csv(bike_file, encoding=bike_encoding)

# 동 -> 자치구 매핑 사전 생성
dong_to_gu = dict(zip(gu_dong_df['동'], gu_dong_df['자치구']))

# E열에서 동 이름 추출 (예: "신사동_101" -> "신사동")
e_col = bike_df.columns[4]  # E열
bike_df['대여_동'] = bike_df[e_col].astype(str).str.split('_').str[0]

# 동 이름을 자치구로 매핑
bike_df['대여_자치구'] = bike_df['대여_동'].map(dong_to_gu)

# 자치구별 대여 횟수 집계
gu_counts = bike_df['대여_자치구'].value_counts().reset_index()
gu_counts.columns = ['자치구', '대여 횟수']

# Streamlit 앱 UI
st.title("📊 서울시 자치구별 따릉이 대여 횟수 (2025년 6월 7일)")

# Plotly 막대 그래프
fig = px.bar(
    gu_counts,
    x='자치구',
    y='대여 횟수',
    title='자치구별 따릉이 대여 횟수',
    labels={'대여 횟수': '이용 횟수'},
    color='대여 횟수',
    color_continuous_scale='Viridis',
)

fig.update_layout(xaxis_title='자치구', yaxis_title='대여 횟수')
st.plotly_chart(fig)

# 데이터 테이블 표시
st.subheader("📋 자치구별 대여 횟수 데이터")
st.dataframe(gu_counts)

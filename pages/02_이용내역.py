import streamlit as st
import pandas as pd
import plotly.express as px

st.title("서울시 자치구별 따릉이 이용 현황 (2025-06-07 기준)")

# --------------------------
# 1. 파일 불러오기
# --------------------------
try:
    dong_df = pd.read_csv("행정구역(동별).csv", encoding='utf-8')
except Exception:
    dong_df = pd.read_csv("행정구역(동별).csv", encoding='euc-kr')

try:
    bike_df = pd.read_csv("따릉이 이용내역_20250607.csv", encoding='utf-8')
except Exception:
    bike_df = pd.read_csv("따릉이 이용내역_20250607.csv", encoding='euc-kr')

# --------------------------
# 2. 실제 열 이름 확인
# --------------------------
st.subheader("📋 행정구역(동별) 열 이름 확인")
st.write(dong_df.columns)

st.subheader("📋 따릉이 이용내역 열 이름 확인")
st.write(bike_df.columns)

# --------------------------
# 3. 열 이름 맞추기
# --------------------------
# 사용자가 올린 파일에 따라 자동으로 컬럼 이름 추출
dong_col_names = dong_df.columns.tolist()
dong_col_gu = dong_col_names[0]  # 자치구
dong_col_dong = dong_col_names[1]  # 동

dong_to_gu = dict(zip(dong_df[dong_col_dong], dong_df[dong_col_gu]))

# --------------------------
# 4. 따릉이 데이터에서 E열 = 5번째 열 사용
# --------------------------
if bike_df.shape[1] < 5:
    st.error("❌ CSV 파일의 5번째 열(E열)이 존재하지 않습니다.")
    st.stop()

# 대여소명 → 동 추출
bike_df['대여동'] = bike_df.iloc[:, 4].astype(str).str.split('_').str[0]

# --------------------------
# 5. 동 → 자치구 매핑
# --------------------------
bike_df['자치구'] = bike_df['대여동'].map(dong_to_gu)

# --------------------------
# 6. 자치구별 이용 횟수 집계
# --------------------------
gu_usage = bike_df['자치구'].value_counts().reset_index()
gu_usage.columns = ['자치구', '이용횟수']

# --------------------------
# 7. 시각화
# --------------------------
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

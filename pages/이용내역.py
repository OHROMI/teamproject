import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 파일 업로드
st.title("서울시 따릉이 이용 현황 (자치구 기준 시각화)")

# 데이터 불러오기
bike_file = '따릉이 이용내역_20250607.csv'
dong_file = '행정구역(동별).csv'

# 따릉이 이용내역 불러오기
bike_df = pd.read_csv(bike_file)

# 행정구역 데이터 불러오기
dong_df = pd.read_csv(dong_file)

# 1. 따릉이 데이터에서 대여소 위치 동 이름 추출 (E열 기준)
bike_df['동이름'] = bike_df.iloc[:, 4].str.split('_').str[0]

# 2. 동 → 자치구 매핑 (dong_df에는 '자치구', '행정동' 컬럼이 있다고 가정)
dong_to_gu = dict(zip(dong_df['행정동'], dong_df['자치구']))

# 3. 따릉이 데이터에 자치구 정보 추가
bike_df['자치구'] = bike_df['동이름'].map(dong_to_gu)

# 4. 자치구별 이용 건수 집계
gu_usage = bike_df['자치구'].value_counts().sort_values(ascending=False)

# 5. 시각화
st.subheader("자치구별 따릉이 이용 횟수")
fig, ax = plt.subplots(figsize=(10, 6))
gu_usage.plot(kind='bar', ax=ax, color='skyblue')
ax.set_xlabel("자치구")
ax.set_ylabel("이용 횟수")
ax.set_title("2025년 6월 7일 기준 자치구별 따릉이 이용 횟수")
st.pyplot(fig)

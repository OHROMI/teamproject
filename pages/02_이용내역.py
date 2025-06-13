import streamlit as st
import pandas as pd
import plotly.express as px

st.title("서울시 자치구별 시간대별 따릉이 대여 현황 (2025-06-07 기준)")

# -------------------
# 1. CSV 불러오기
# -------------------
# 행정구역
try:
    dong_df = pd.read_csv("행정구역(동별).csv", encoding='utf-8')
except:
    dong_df = pd.read_csv("행정구역(동별).csv", encoding='euc-kr')

# 따릉이 이용내역
try:
    bike_df = pd.read_csv("따릉이 이용내역_20250607.csv", encoding='utf-8')
except:
    bike_df = pd.read_csv("따릉이 이용내역_20250607.csv", encoding='euc-kr')

# -------------------
# 2. 자치구 매핑
# -------------------
dong_col_gu, dong_col_dong = dong_df.columns[:2]
dong_to_gu = dict(zip(dong_df[dong_col_dong], dong_df[dong_col_gu]))

bike_df['대여동'] = bike_df.iloc[:, 4].astype(str).str.split('_').str[0]
bike_df['자치구'] = bike_df['대여동'].map(dong_to_gu)

# -------------------
# 3. 시간대 추출 (C열: 3번째 열 기준 HHMM)
# -------------------
bike_df['대여시각'] = bike_df.iloc[:, 2].astype(str).str.zfill(4)  # 4자리로 채우기 (ex. 905 → 0905)
bike_df['대여시간대'] = bike_df['대여시각'].str[:2].astype(int)     # 앞 2자리 → 시각

# -------------------
# 4. 자치구 선택
# -------------------
available_gus = bike_df['자치구'].dropna().unique().tolist()
selected_gu = st.selectbox("자치구 선택", sorted(available_gus))

# -------------------
# 5. 시간대별 대여 횟수
# -------------------
gu_filtered = bike_df[bike_df['자치구'] == selected_gu]
hourly_usage = gu_filtered['대여시간대'].value_counts().sort_index().reset_index()
hourly_usage.columns = ['시간대', '대여횟수']

# 0~23시까지 누락된 시간 보완
all_hours = pd.DataFrame({'시간대': list(range(24))})
hourly_usage = pd.merge(all_hours, hourly_usage, how='left', on='시간대').fillna(0)
hourly_usage['대여횟수'] = hourly_usage['대여횟수'].astype(int)

# -------------------
# 6. 시각화
# -------------------
fig = px.bar(
    hourly_usage,
    x='시간대',
    y='대여횟수',
    title=f"{selected_gu} 시간대별 따릉이 대여 횟수",
    labels={'시간대': '대여 시각 (시)', '대여횟수': '이용 횟수'},
    color='대여횟수',
    color_continuous_scale='Blues'
)
fig.update_layout(xaxis=dict(tickmode='linear'))

st.plotly_chart(fig)

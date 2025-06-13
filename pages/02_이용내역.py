import streamlit as st
import pandas as pd
import plotly.express as px

def try_read_csv(filepath, encodings=['utf-8', 'cp949', 'euc-kr']):
    for enc in encodings:
        try:
            return pd.read_csv(filepath, encoding=enc), enc
        except Exception:
            continue
    raise ValueError(f"파일을 열 수 없습니다: {filepath}")

# 파일 경로
gu_file = "행정구역(동별).csv"
bike_file = "따릉이 이용내역_20250607.csv"

# 파일 읽기
gu_dong_df, gu_encoding = try_read_csv(gu_file)
bike_df, bike_encoding = try_read_csv(bike_file)

# Streamlit에 인코딩 정보 출력
st.sidebar.markdown(f"🗂️ 자치구 파일 인코딩: `{gu_encoding}`")
st.sidebar.markdown(f"🗂️ 따릉이 파일 인코딩: `{bike_encoding}`")

# ⚠️ 컬럼명 확인 출력
st.subheader("📌 자치구 파일의 컬럼명")
st.write(gu_dong_df.columns.tolist())

# 📌 여기서 '동'과 '자치구'가 존재하는지 확인
# 만약 다르면 아래처럼 컬럼명을 수정
expected_columns = ['자치구', '동']
if not all(col in gu_dong_df.columns for col in expected_columns):
    # 예: 컬럼 이름에 공백이 있는 경우
    gu_dong_df.columns = gu_dong_df.columns.str.strip()  # 공백 제거
    st.write("✅ 공백 제거 후 컬럼명:", gu_dong_df.columns.tolist())

# 다시 확인
if not all(col in gu_dong_df.columns for col in expected_columns):
    st.error("❌ '자치구' 또는 '동' 컬럼이 존재하지 않습니다. 컬럼명을 확인해주세요.")
    st.stop()

# 동 → 자치구 매핑
dong_to_gu = dict(zip(gu_dong_df['동'], gu_dong_df['자치구']))

# 대여소명(E열)에서 동 이름 추출
e_col = bike_df.columns[4]
bike_df['대여_동'] = bike_df[e_col].astype(str).str.split('_').str[0]

# 자치구 매핑
bike_df['대여_자치구'] = bike_df['대여_동'].map(dong_to_gu)

# 자치구별 대여 횟수 집계
gu_counts = bike_df['대여_자치구'].value_counts().reset_index()
gu_counts.columns = ['자치구', '대여 횟수']

# 시각화
st.title("🚲 서울시 자치구별 따릉이 대여 현황 (2025년 6월 7일)")

fig = px.bar(
    gu_counts,
    x='자치구',
    y='대여 횟수',
    title='자치구별 따릉이 대여 횟수',
    color='대여 횟수',
    color_continuous_scale='Plasma'
)
st.plotly_chart(fig)

st.subheader("📋 자치구별 대여 횟수 테이블")
st.dataframe(gu_counts)

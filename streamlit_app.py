import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# 1. 基本设置
# -------------------------------
st.set_page_config(
    page_title="테니스 선수 경력 통계 분석",
    page_icon="🎾",
    layout="wide"
)

# -------------------------------
# 2. 제목
# -------------------------------
st.title("🎾 테니스 선수의 직업 경력 통계 분석")
st.write("프로 테니스 선수들의 출전 수, 승률, 대满贯 우승 등을 시각화하여 한눈에 분석할 수 있는 대시보드입니다.")

# -------------------------------
# 3. 예시 데이터 생성
# -------------------------------
players = {
    "선수명": ["노바크 조코비치", "라파엘 Nadal", "로저 페더러", "세라나 윌리엄스", "마리아 샤라포바", "이수민"],
    "국가": ["세르비아", "스페인", "스위스", "미국", "러시아", "한국"],
    "나이": [36, 37, 42, 42, 36, 28],
    "대满贯 우승": [24, 22, 20, 23, 5, 0],
    "경기 출전 수": [1600, 1500, 1520, 1100, 800, 200],
    "승률(%)": [83, 82, 82, 84, 79, 65],
    "최고 랭킹": [1, 1, 1, 1, 1, 50]
}

df = pd.DataFrame(players)

# -------------------------------
# 4. 사이드바 추가
# -------------------------------
st.sidebar.header("⚙️ 필터 설정")

# 국가 선택
country_filter = st.sidebar.multiselect(
    "국가 선택:",
    options=df["국가"].unique(),
    default=df["국가"].unique()
)

# 선수 검색
search_name = st.sidebar.text_input("선수 검색 (예: 조코비치)")

# 정렬 옵션
sort_option = st.sidebar.selectbox(
    "정렬 기준:",
    ["대满贯 우승", "승률(%)", "경기 출전 수", "최고 랭킹"]
)

# 데이터 보이기 여부
show_table = st.sidebar.checkbox("선수 데이터 표시", value=True)

# 그래프 선택
graph_type = st.sidebar.radio(
    "그래프 종류 선택:",
    ["대满贯 우승 비교", "승률 비교", "경기 출전 수 비교", "국가 분포"]
)

# -------------------------------
# 5. 필터 적용
# -------------------------------
filtered_df = df[df["국가"].isin(country_filter)]

if search_name:
    filtered_df = filtered_df[filtered_df["선수명"].str.contains(search_name)]

filtered_df = filtered_df.sort_values(by=sort_option, ascending=False)

# -------------------------------
# 6. 데이터 테이블 표시
# -------------------------------
if show_table:
    st.subheader("📋 선수 기본 데이터")
    st.dataframe(filtered_df, use_container_width=True)

# -------------------------------
# 7. 선택된 그래프 출력
# -------------------------------
if graph_type == "대满贯 우승 비교":
    st.subheader("🏆 선수별 대满贯 우승 수")
    fig = px.bar(filtered_df, x="선수명", y="대满贯 우승", color="국가", text="대满贯 우승")
    st.plotly_chart(fig, use_container_width=True)

elif graph_type == "승률 비교":
    st.subheader("📈 선수별 승률 비교")
    fig = px.line(filtered_df, x="선수명", y="승률(%)", markers=True, color="국가")
    st.plotly_chart(fig, use_container_width=True)

elif graph_type == "경기 출전 수 비교":
    st.subheader("🎾 선수별 경기 출전 수")
    fig = px.bar(filtered_df, x="선수명", y="경기 출전 수", color="선수명")
    st.plotly_chart(fig, use_container_width=True)

elif graph_type == "국가 분포":
    st.subheader("🌍 국가별 선수 분포")
    fig = px.pie(filtered_df, names="국가", title="선수 국적 분포")
    st.plotly_chart(fig, use_container_width=True)


import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="국가별 MBTI 분석",
    page_icon="🌍",
    layout="wide"
)

# 제목
st.title("🌍 국가별 MBTI 유형 분석")
st.write("국가를 선택하고 해당 국가의 MBTI 비율을 확인해 보세요!")

st.divider()

# CSV 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "mbti_country.csv"

# CSV 불러오기
@st.cache_data
def load_data():
    encodings = ["utf-8-sig", "cp949", "euc-kr"]

    for encoding in encodings:
        try:
            return pd.read_csv(CSV_PATH, encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise ValueError("CSV 인코딩을 확인해 주세요.")

try:
    df = load_data()

except FileNotFoundError:
    st.error("CSV 파일을 찾을 수 없습니다.")
    st.info("CSV 파일을 파이썬 파일의 상위 폴더에 넣어주세요.")
    st.stop()

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# 데이터 열 확인
st.subheader("📊 데이터 확인")

st.caption("CSV 파일의 국가 및 MBTI 데이터 구조를 확인합니다.")

st.dataframe(df.head(), use_container_width=True)

# 데이터 열 이름
columns = df.columns.tolist()

# 국가 열 자동 탐색
country_candidates = ["Country", "country", "국가", "나라"]
country_col = next(
    (col for col in country_candidates if col in columns),
    columns[0]
)

# MBTI 열 자동 탐색
mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

available_mbti = [m for m in mbti_types if m in columns]

if len(available_mbti) != 16:
    st.error(
        "CSV 파일에서 MBTI 16개 열을 모두 찾을 수 없습니다. "
        "열 이름을 확인해 주세요."
    )
    st.write("현재 열 이름:", columns)
    st.stop()

# 국가 선택
countries = sorted(df[country_col].dropna().unique().tolist())

if not countries:
    st.error("CSV에 국가 데이터가 없습니다.")
    st.stop()

st.subheader("🌏 국가 선택")

selected_country = st.selectbox(
    "분석할 국가를 선택하세요.",
    countries
)

# 선택 국가 데이터
country_data = df[df[country_col] == selected_country]

if country_data.empty:
    st.warning("선택한 국가의 데이터가 없습니다.")
    st.stop()

# 국가별 MBTI 비율 추출
values = country_data.iloc[0][available_mbti]

values = pd.to_numeric(values, errors="coerce")

if values.isna().any():
    st.error("MBTI 비율 데이터에 숫자가 아닌 값이 있습니다.")
    st.stop()

# 내림차순 정렬
result = pd.DataFrame({
    "MBTI": available_mbti,
    "비율": values.values
})

result = result.sort_values(
    by="비율",
    ascending=False
).reset_index(drop=True)

# 1위 유형
top_mbti = result.iloc[0]["MBTI"]
top_ratio = result.iloc[0]["비율"]

# 상단 주요 정보
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("선택 국가", selected_country)

with col2:
    st.metric("가장 높은 MBTI", top_mbti)

with col3:
    st.metric("최고 비율", f"{top_ratio:.2f}%")

st.divider()

# 그래프
st.subheader("📈 MBTI 유형별 비율")

# 그래프 색상
colors = [
    "#16A34A" if mbti == top_mbti
    else f"rgba(59, 130, 246, {max(0.25, 0.9 - i * 0.045)})"
    for i, mbti in enumerate(result["MBTI"])
]

fig = go.Figure()

# 전체 MBTI 꺾은선 그래프
fig.add_trace(go.Scatter(
    x=result["MBTI"],
    y=result["비율"],
    mode="lines+markers",
    name="MBTI 비율",
    line=dict(
        color="#60A5FA",
        width=3
    ),
    marker=dict(
        size=11,
        color=colors,
        line=dict(
            color="white",
            width=1.5
        )
    ),
    customdata=result[["비율"]].values,
    hovertemplate=(
        "<b>MBTI: %{x}</b><br>"
        "비율: %{y:.2f}%<extra></extra>"
    )
))

# 1위 MBTI 강조
fig.add_trace(go.Scatter(
    x=[top_mbti],
    y=[top_ratio],
    mode="markers+text",
    name="1위 MBTI",
    marker=dict(
        color="#16A34A",
        size=19,
        symbol="star",
        line=dict(color="white", width=2)
    ),
    text=[f"1위 {top_mbti}"],
    textposition="top center",
    textfont=dict(
        color="#16A34A",
        size=13
    ),
    hovertemplate=(
        "<b>🥇 1위 MBTI</b><br>"
        "%{x}<br>"
        "비율: %{y:.2f}%<extra></extra>"
    )
))

fig.update_layout(
    title=f"{selected_country}의 MBTI 유형별 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    template="plotly_white",
    height=520,
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    margin=dict(l=30, r=30, t=80, b=40)
)

fig.update_xaxes(
    showgrid=False
)

fig.update_yaxes(
    showgrid=True,
    gridcolor="rgba(150,150,150,0.2)",
    rangemode="tozero"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# 순위표
st.subheader("🏆 MBTI 비율 순위")

result.index = result.index + 1
result.index.name = "순위"

st.dataframe(
    result.style.format({"비율": "{:.2f}%"}),
    use_container_width=True
)

# 다운로드 기능
csv_data = result.to_csv(
    index=True,
    encoding="utf-8-sig"
)

st.download_button(
    label="📥 분석 결과 CSV 다운로드",
    data=csv_data,
    file_name=f"{selected_country}_MBTI_analysis.csv",
    mime="text/csv"
)

st.caption("※ MBTI 비율은 제공된 CSV 데이터에 기반합니다.")

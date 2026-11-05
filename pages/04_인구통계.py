
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# 페이지 설정
st.set_page_config(
    page_title="대한민국 연령별 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 대한민국 연령별 인구 분석")
st.caption("행정구역, 성별, 연도를 선택하여 연령대별 인구수를 확인하세요.")


# CSV 파일 불러오기
@st.cache_data
def load_data():

    # pages 폴더의 상위 폴더에서 CSV 파일 찾기
    csv_path = Path(__file__).resolve().parent.parent / "population.csv"

    if not csv_path.exists():
        st.error("population.csv 파일을 찾을 수 없습니다.")
        st.stop()

    data = None
    last_error = None

    # 한글 인코딩 처리
    for encoding in ["cp949", "utf-8-sig", "euc-kr", "utf-8"]:
        try:
            data = pd.read_csv(
                csv_path,
                encoding=encoding
            )
            break

        except UnicodeDecodeError as error:
            last_error = error

    if data is None:
        raise ValueError(f"CSV 인코딩 오류: {last_error}")

    # 행정구역 이름 정리
    data["행정구역"] = (
        data["행정구역"]
        .astype(str)
        .str.replace(r"\s*\(\d+\)\s*$", "", regex=True)
        .str.strip()
    )

    # 숫자 데이터 쉼표 제거 및 숫자 변환
    for column in data.columns:

        if column != "행정구역":
            data[column] = pd.to_numeric(
                data[column]
                .astype(str)
                .str.replace(",", "", regex=False),
                errors="coerce"
            )

    return data


# 데이터 읽기
try:
    df = load_data()

except Exception as error:
    st.error(f"데이터를 불러올 수 없습니다: {error}")
    st.stop()


# 성별 설정
sex_options = {
    "전체": "거주자",
    "남성": "남_거주자",
    "여성": "여_거주자"
}

# 연령대 설정
age_columns = [
    "0~9세",
    "10~19세",
    "20~29세",
    "30~39세",
    "40~49세",
    "50~59세",
    "60~69세",
    "70~79세",
    "80~89세",
    "90~99세",
    "100세 이상"
]

# 연도 설정
years = ["2024", "2025"]


# 선택 메뉴
regions = df["행정구역"].dropna().tolist()

if not regions:
    st.error("행정구역 데이터가 없습니다.")
    st.stop()

col1, col2, col3 = st.columns(3)

with col1:
    selected_region = st.selectbox(
        "🏙️ 행정구역 선택",
        regions
    )

with col2:
    selected_sex = st.selectbox(
        "👥 성별 선택",
        list(sex_options.keys())
    )

with col3:
    selected_year = st.selectbox(
        "📅 연도 선택",
        years,
        index=1
    )


# 선택한 행정구역 데이터
selected_row = df[
    df["행정구역"] == selected_region
].iloc[0]

sex_key = sex_options[selected_sex]

# 연령대별 인구 데이터 추출
values = []

for age in age_columns:

    column_name = f"{selected_year}년_{sex_key}_{age}"

    if column_name not in df.columns:
        st.error(f"데이터 열을 찾을 수 없습니다: {column_name}")
        st.stop()

    value = selected_row[column_name]

    values.append(
        0 if pd.isna(value) else int(value)
    )


# 인구 합계
total_population = sum(values)

st.subheader(
    f"{selected_region} · {selected_year}년 · {selected_sex}"
)

metric1, metric2 = st.columns(2)

with metric1:
    st.metric(
        "연령대별 인구 합계",
        f"{total_population:,}명"
    )

with metric2:
    st.metric(
        "연령대 구간",
        f"{len(age_columns)}개"
    )


# 꺾은선 그래프 생성
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=age_columns,
        y=values,
        mode="lines+markers",
        name="인구수",

        # 핫핑크 색상
        line=dict(
            color="#FF1493",
            width=3
        ),

        marker=dict(
            color="#FF1493",
            size=8
        ),

        hovertemplate=(
            "%{x}<br>"
            "인구수: %{y:,.0f}명"
            "<extra></extra>"
        )
    )
)


# 세로축 최대값 설정
max_value = max(values) if values else 0

y_axis_max = max(
    100000,
    ((max_value // 100000) + 1) * 100000
)


# 그래프 디자인
fig.update_layout(
    template="plotly_white",
    height=560,

    xaxis_title="나이",
    yaxis_title="인구수 (명)",

    hovermode="x unified",
    showlegend=False,

    font=dict(
        family="Arial, sans-serif",
        size=13
    ),

    margin=dict(
        l=25,
        r=25,
        t=35,
        b=35
    )
)


# 가로축: 10살 단위 구분선
fig.update_xaxes(
    type="category",
    categoryorder="array",
    categoryarray=age_columns,
    showgrid=True,
    gridcolor="#E8E8E8",
    gridwidth=1,
    tickangle=0
)


# 세로축: 10만 명 단위 구분선
fig.update_yaxes(
    rangemode="tozero",
    range=[0, y_axis_max],

    tickmode="linear",
    tick0=0,
    dtick=100000,

    tickformat=",",

    showgrid=True,
    gridcolor="#DCDCDC",
    gridwidth=1,

    zeroline=True
)


# 그래프 출력
st.plotly_chart(
    fig,
    use_container_width=True
)


# 데이터 표 출력
with st.expander("📋 연령대별 인구 데이터 확인"):

    result = pd.DataFrame({
        "연령대": age_columns,
        "인구수": values
    })

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True
    )


st.caption(
    "자료: population.csv | 그래프 색상: 핫핑크"
)

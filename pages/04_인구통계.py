
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="대한민국 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 대한민국 인구 분석 대시보드")


# 1. CSV 데이터 불러오기
@st.cache_data
def load_data():
    csv_path = Path(__file__).resolve().parent.parent / "population.csv"

    if not csv_path.exists():
        raise FileNotFoundError("population.csv 파일을 찾을 수 없습니다.")

    data = None

    for encoding in ["cp949", "utf-8-sig", "euc-kr", "utf-8"]:
        try:
            data = pd.read_csv(csv_path, encoding=encoding)
            break
        except UnicodeDecodeError:
            continue

    if data is None:
        raise ValueError("CSV 인코딩을 읽을 수 없습니다.")

    data["행정구역"] = (
        data["행정구역"].astype(str)
        .str.replace(r"\s*\(\d+\)\s*$", "", regex=True)
        .str.strip()
    )

    for col in data.columns:
        if col != "행정구역":
            data[col] = pd.to_numeric(
                data[col].astype(str).str.replace(",", ""),
                errors="coerce"
            )

    return data


try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 오류: {e}")
    st.stop()


# 기본 설정
YEARS = ["2024", "2025"]

AGES = [
    "0~9세", "10~19세", "20~29세",
    "30~39세", "40~49세", "50~59세",
    "60~69세", "70~79세", "80~89세",
    "90~99세", "100세 이상"
]

PINK = "#FF1493"
GREEN = "#16A34A"


def pop_col(year, sex, age):
    return f"{year}년_{sex}_{age}"


def total_col(year):
    return f"{year}년_거주자_총인구수"


# 전국을 제외한 지역 데이터
region_df = df[
    ~df["행정구역"].str.contains("전국", na=False)
].copy()


# ------------------------------------------------
# 1. 연령대별 남녀 인구 꺾은선 그래프
# ------------------------------------------------

st.header("1. 연령대별 남녀 인구 비교")
st.write("남성은 핫핑크, 여성은 초록색으로 표시됩니다.")

c1, c2 = st.columns(2)

with c1:
    region = st.selectbox(
        "행정구역 선택",
        df["행정구역"].tolist()
    )

with c2:
    year = st.selectbox(
        "연도 선택",
        YEARS,
        index=1
    )

row = df[df["행정구역"] == region].iloc[0]

male_values = []
female_values = []

for age in AGES:
    male_col = pop_col(year, "남_거주자", age)
    female_col = pop_col(year, "여_거주자", age)

    if male_col not in df.columns or female_col not in df.columns:
        st.error("성별 인구 데이터 열을 찾을 수 없습니다.")
        st.stop()

    male = row[male_col]
    female = row[female_col]

    male_values.append(0 if pd.isna(male) else int(male))
    female_values.append(0 if pd.isna(female) else int(female))


fig = go.Figure()

# 남성 그래프
fig.add_trace(go.Scatter(
    x=AGES,
    y=male_values,
    mode="lines+markers",
    name="남성",
    line=dict(color=PINK, width=3),
    marker=dict(color=PINK, size=8)
))

# 여성 그래프
fig.add_trace(go.Scatter(
    x=AGES,
    y=female_values,
    mode="lines+markers",
    name="여성",
    line=dict(color=GREEN, width=3),
    marker=dict(color=GREEN, size=8)
))

max_value = max(male_values + female_values)
y_max = max(100000, (max_value // 100000 + 1) * 100000)

fig.update_layout(
    template="plotly_white",
    height=550,
    xaxis_title="나이",
    yaxis_title="인구수 (명)",
    hovermode="x unified",
    legend_title="성별"
)

fig.update_xaxes(
    type="category",
    categoryorder="array",
    categoryarray=AGES,
    showgrid=True,
    gridcolor="#E8E8E8"
)

fig.update_yaxes(
    range=[0, y_max],
    tickmode="linear",
    tick0=0,
    dtick=100000,
    tickformat=",",
    showgrid=True,
    gridcolor="#DCDCDC"
)

st.plotly_chart(fig, use_container_width=True)

m1, m2, m3 = st.columns(3)

m1.metric("남성 인구 합계", f"{sum(male_values):,}명")
m2.metric("여성 인구 합계", f"{sum(female_values):,}명")
m3.metric(
    "남녀 인구 차이",
    f"{abs(sum(male_values)-sum(female_values)):,}명"
)


st.divider()


# ------------------------------------------------
# 2. 연령대별 인구가 가장 많은 지역
# ------------------------------------------------

st.header("2. 연령대별 인구 최다 지역 분석")
st.write("원하는 연령대와 성별을 선택해 인구가 많은 지역을 확인하세요.")

r1, r2, r3 = st.columns(3)

with r1:
    rank_year = st.selectbox(
        "분석 연도",
        YEARS,
        index=1,
        key="rank_year"
    )

with r2:
    selected_age = st.selectbox(
        "연령대 선택",
        AGES,
        index=6
    )

with r3:
    selected_sex = st.selectbox(
        "성별 선택",
        ["전체", "남성", "여성"]
    )

sex_key = {
    "전체": "거주자",
    "남성": "남_거주자",
    "여성": "여_거주자"
}[selected_sex]

column = pop_col(rank_year, sex_key, selected_age)

if column not in region_df.columns:
    st.error(f"데이터 열이 없습니다: {column}")
    st.stop()

ranking = region_df[
    ["행정구역", column]
].copy()

ranking = ranking.rename(
    columns={column: "인구수"}
)

ranking["인구수"] = ranking["인구수"].fillna(0)

ranking = ranking.sort_values(
    "인구수",
    ascending=False
)

top_region = ranking.iloc[0]

st.metric(
    "해당 연령대 인구가 가장 많은 지역",
    top_region["행정구역"],
    f"{int(top_region['인구수']):,}명"
)

# 상위 10개 지역
top10 = ranking.head(10).sort_values(
    "인구수",
    ascending=True
)

bar_fig = px.bar(
    top10,
    x="인구수",
    y="행정구역",
    orientation="h",
    text="인구수",
    title=f"{rank_year}년 {selected_age} {selected_sex} TOP 10",
    color_discrete_sequence=[PINK]
)

bar_fig.update_traces(
    texttemplate="%{text:,.0f}명",
    textposition="outside",
    cliponaxis=False
)

bar_fig.update_layout(
    template="plotly_white",
    height=500,
    xaxis_title="인구수 (명)",
    yaxis_title="행정구역",
    showlegend=False
)

bar_fig.update_xaxes(
    showgrid=True,
    gridcolor="#E5E5E5",
    tickformat=","
)

st.plotly_chart(
    bar_fig,
    use_container_width=True
)

with st.expander("전체 지역 순위표 보기"):
    ranking_display = ranking.copy()
    ranking_display["인구수"] = ranking_display["인구수"].map(
        lambda x: f"{int(x):,}명"
    )
    ranking_display.insert(
        0, "순위", range(1, len(ranking_display) + 1)
    )
    st.dataframe(
        ranking_display,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ------------------------------------------------
# 3. 추가 기능: 2024년과 2025년 인구 증감 분석
# ------------------------------------------------

st.header("3. 지역별 인구 증감 분석")
st.write("2024년과 2025년을 비교하여 인구 증가와 감소를 확인합니다.")

col24 = total_col("2024")
col25 = total_col("2025")

if col24 not in region_df.columns or col25 not in region_df.columns:
    st.warning("인구 증감 분석에 필요한 열이 없습니다.")

else:
    change_df = region_df[
        ["행정구역", col24, col25]
    ].copy()

    change_df = change_df.rename(
        columns={
            col24: "2024년 인구",
            col25: "2025년 인구"
        }
    )

    change_df["인구 증감"] = (
        change_df["2025년 인구"]
        - change_df["2024년 인구"]
    )

    change_df["증감률(%)"] = (
        change_df["인구 증감"]
        / change_df["2024년 인구"] * 100
    ).replace([float("inf"), -float("inf")], 0).fillna(0)

    sorted_df = change_df.sort_values(
        "인구 증감",
        ascending=False
    )

    increased = sorted_df.iloc[0]
    decreased = sorted_df.iloc[-1]

    c1, c2 = st.columns(2)

    c1.metric(
        "인구 증가 1위",
        increased["행정구역"],
        f"{int(increased['인구 증감']):+,}명"
    )

    c2.metric(
        "인구 감소 1위",
        decreased["행정구역"],
        f"{int(decreased['인구 증감']):+,}명"
    )

    chart_df = sorted_df.sort_values(
        "인구 증감",
        ascending=True
    )

    colors = [
        GREEN if value >= 0 else PINK
        for value in chart_df["인구 증감"]
    ]

    change_fig = go.Figure()

    change_fig.add_trace(go.Bar(
        x=chart_df["인구 증감"],
        y=chart_df["행정구역"],
        orientation="h",
        marker_color=colors,
        text=chart_df["인구 증감"],
        texttemplate="%{text:+,.0f}명",
        textposition="outside",
        cliponaxis=False
    ))

    change_fig.update_layout(
        template="plotly_white",
        height=600,
        title="2024년 대비 2025년 지역별 인구 증감",
        xaxis_title="인구 증감 (명)",
        yaxis_title="행정구역",
        showlegend=False
    )

    change_fig.update_xaxes(
        zeroline=True,
        showgrid=True,
        gridcolor="#E5E5E5",
        tickformat="+,"
    )

    st.plotly_chart(
        change_fig,
        use_container_width=True
    )

    with st.expander("지역별 인구 증감 상세표"):
        detail = change_df.sort_values(
            "인구 증감",
            ascending=False
        ).copy()

        detail["2024년 인구"] = detail["2024년 인구"].map(
            lambda x: f"{int(x):,}명"
        )

        detail["2025년 인구"] = detail["2025년 인구"].map(
            lambda x: f"{int(x):,}명"
        )

        detail["인구 증감"] = detail["인구 증감"].map(
            lambda x: f"{int(x):+,}명"
        )

        detail["증감률(%)"] = detail["증감률(%)"].map(
            lambda x: f"{x:+.2f}%"
        )

        st.dataframe(
            detail,
            use_container_width=True,
            hide_index=True
        )


st.divider()

st.caption(
    "자료: population.csv | "
    "인코딩: CP949 우선 적용 | "
    "그래프: Plotly"
)

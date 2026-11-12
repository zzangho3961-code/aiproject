
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from pathlib import Path

# --------------------------------
# 페이지 설정
# --------------------------------
st.set_page_config(
    page_title="월별 평균기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 평균기온 예측 프로그램")
st.caption("과거 기상 데이터를 이용한 선형회귀 기온 예측")

# --------------------------------
# CSV 파일 불러오기
# --------------------------------
@st.cache_data
def load_data():
    file_path = Path(__file__).parent / "temperature.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            "temperature.csv 파일을 찾을 수 없습니다."
        )

    for encoding in ["cp949", "utf-8-sig", "euc-kr"]:
        try:
            data = pd.read_csv(file_path, encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError("CSV 파일의 인코딩을 확인해주세요.")

    required_columns = ["일시", "평균기온(℃)"]

    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"CSV에 {col} 열이 없습니다.")

    # 날짜 변환
    data["날짜"] = pd.to_datetime(
        data["일시"],
        format="%b-%y",
        errors="coerce"
    )

    data["평균기온(℃)"] = pd.to_numeric(
        data["평균기온(℃)"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["날짜", "평균기온(℃)"]
    ).copy()

    data["연도"] = data["날짜"].dt.year
    data["월"] = data["날짜"].dt.month

    return data.sort_values("날짜")


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터 불러오기 오류: {e}")
    st.stop()


# --------------------------------
# 사용자 입력
# --------------------------------
st.subheader("📅 예측 조건 설정")

col1, col2 = st.columns(2)

with col1:
    selected_month = st.selectbox(
        "예측할 월을 선택하세요",
        list(range(1, 13)),
        format_func=lambda x: f"{x}월"
    )

with col2:
    selected_year = st.number_input(
        "예측할 연도를 입력하세요",
        min_value=int(df["연도"].max()) + 1,
        max_value=2100,
        value=int(df["연도"].max()) + 1,
        step=1
    )


# --------------------------------
# 선택한 월의 데이터 추출
# --------------------------------
month_data = df[
    df["월"] == selected_month
].copy()

month_data = month_data.sort_values("연도")

if len(month_data) < 2:
    st.error("선형회귀를 수행하기 위한 데이터가 부족합니다.")
    st.stop()


# --------------------------------
# 선형회귀 모델 학습
# --------------------------------
X = month_data[["연도"]]
y = month_data["평균기온(℃)"]

model = LinearRegression()
model.fit(X, y)

# 과거 데이터 예측값
month_data["회귀예측기온"] = model.predict(X)

# 사용자가 선택한 미래 연도의 기온 예측
future_X = pd.DataFrame({
    "연도": [int(selected_year)]
})

predicted_temp = model.predict(future_X)[0]

# 회귀식
slope = model.coef_[0]
intercept = model.intercept_
r2 = model.score(X, y)


# --------------------------------
# 예측 결과 표시
# --------------------------------
st.divider()
st.subheader("🔮 기온 예측 결과")

result1, result2, result3 = st.columns(3)

with result1:
    st.metric(
        "예측 연도",
        f"{selected_year}년 {selected_month}월"
    )

with result2:
    st.metric(
        "예측 평균기온",
        f"{predicted_temp:.2f} ℃"
    )

with result3:
    st.metric(
        "결정계수 (R²)",
        f"{r2:.3f}"
    )

st.info(
    f"{selected_year}년 {selected_month}월의 "
    f"예측 평균기온은 {predicted_temp:.2f}℃입니다."
)


# --------------------------------
# 그래프 데이터 생성
# --------------------------------
# 회귀선을 부드럽게 표시하기 위한 연도 범위
line_years = np.linspace(
    month_data["연도"].min(),
    selected_year,
    300
)

line_X = pd.DataFrame({
    "연도": line_years
})

line_temps = model.predict(line_X)

# --------------------------------
# 그래프
# --------------------------------
st.subheader(
    f"📈 {selected_month}월 평균기온 및 미래 예측 그래프"
)

fig = go.Figure()

# 실제 관측 데이터
fig.add_trace(go.Scatter(
    x=month_data["연도"],
    y=month_data["평균기온(℃)"],
    mode="markers",
    name="실제 평균기온",
    marker=dict(
        size=9,
        color="#2196F3"
    ),
    hovertemplate=
    "%{x}년<br>실제 평균기온: %{y:.2f}℃<extra></extra>"
))

# 선형회귀 직선
fig.add_trace(go.Scatter(
    x=line_years,
    y=line_temps,
    mode="lines",
    name="선형회귀 예측선",
    line=dict(
        color="#FF7043",
        width=3
    ),
    hovertemplate=
    "연도: %{x:.1f}<br>회귀 예측: %{y:.2f}℃<extra></extra>"
))

# 미래 예측 지점
fig.add_trace(go.Scatter(
    x=[selected_year],
    y=[predicted_temp],
    mode="markers+text",
    name="미래 예측기온",
    marker=dict(
        size=15,
        color="#D500F9",
        symbol="star"
    ),
    text=[f"{predicted_temp:.2f}℃"],
    textposition="top center",
    hovertemplate=
    "%{x}년<br>예측 평균기온: %{y:.2f}℃<extra></extra>"
))

# 과거 마지막 연도와 미래 연도 구분
fig.add_vline(
    x=int(df["연도"].max()),
    line_dash="dash",
    line_color="gray",
    annotation_text="실제 데이터 마지막 연도",
    annotation_position="top"
)

fig.update_layout(
    xaxis_title="연도",
    yaxis_title="평균기온 (℃)",
    hovermode="x unified",
    template="plotly_white",
    height=600,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

fig.update_xaxes(
    dtick=1,
    showgrid=True
)

fig.update_yaxes(
    showgrid=True,
    ticksuffix="℃"
)

st.plotly_chart(fig, use_container_width=True)


# --------------------------------
# 선형회귀 알고리즘 설명
# --------------------------------
st.divider()

st.subheader("🧠 선형회귀 알고리즘이란?")

st.markdown("""
선형회귀(Linear Regression)는 과거 데이터를 분석하여
변수 사이의 선형적인 관계를 찾아내고, 이를 이용해
미래의 값을 예측하는 머신러닝 알고리즘입니다.

이번 프로그램에서는 과거의 **연도(X)** 와
**평균기온(Y)** 의 관계를 학습하여 미래 기온을 예측합니다.
""")

st.latex(r"y = ax + b")

st.markdown(f"""
- **X (독립변수)** : 연도
- **Y (종속변수)** : 평균기온
- **a (기울기)** : 연도가 1년 증가할 때 예측기온의 변화량
- **b (절편)** : 회귀 직선의 절편

### 현재 선택한 월의 회귀식

""")

st.latex(
    rf"\hat{{y}} = {slope:.4f}x + ({intercept:.4f})"
)

st.markdown(f"""
현재 선택한 {selected_month}월의 회귀식은 위와 같습니다.

기울기(a)는 **{slope:.4f}** 이며,
이는 연도가 1년 증가할 때 모델이 예측하는
평균기온의 변화량을 의미합니다.

결정계수(R²)는 **{r2:.3f}** 입니다.
이는 과거 데이터에서 회귀 모델이 기온 변동을
얼마나 설명하는지 나타내는 지표입니다.

### 📊 그래프 보는 방법

1. **파란색 점** : 실제로 관측된 과거 평균기온입니다.
2. **주황색 선** : 실제 데이터에 가장 잘 맞도록 학습한 선형회귀 직선입니다.
3. **보라색 별** : 회귀 직선을 연장하여 계산한 미래 예측기온입니다.
4. **회색 점선** : 실제 기상 데이터와 미래 예측 영역의 경계입니다.

### ⚙️ 선형회귀는 어떻게 작동할까?

① 과거의 같은 월에 해당하는 평균기온 데이터를 수집합니다.

② 각 연도를 X값, 평균기온을 Y값으로 설정합니다.

③ 여러 실제 데이터 점과의 오차 제곱합이 최소가 되는
회귀 직선을 계산합니다.

④ 계산된 직선의 기울기와 절편을 이용하여
사용자가 입력한 미래 연도의 기온을 예측합니다.

⑤ 예측된 값을 그래프에 별도로 표시합니다.

**주의:** 기온은 장기적인 기후 변화뿐 아니라 계절적·자연적
변동의 영향을 받습니다. 선형회귀는 과거의 선형적인 추세가
미래에도 이어진다고 가정하므로 실제 기온과 차이가 발생할 수 있습니다.
이 결과는 참고용 통계 예측값입니다.
""")

# --------------------------------
# 데이터 정보
# --------------------------------
with st.expander("📁 분석에 사용된 실제 데이터 확인"):
    st.write(
        f"전체 데이터 기간: "
        f"{df['연도'].min()}년 ~ {df['연도'].max()}년"
    )

    st.write(
        f"선택한 월의 분석 데이터 수: {len(month_data)}개"
    )

    st.dataframe(
        month_data[
            ["연도", "월", "평균기온(℃)", "회귀예측기온"]
        ].reset_index(drop=True),
        use_container_width=True
    )

st.caption(
    "🌡️ 본 프로그램은 temperature.csv의 실제 관측 데이터를 "
    "기반으로 선형회귀 예측을 수행합니다."
)

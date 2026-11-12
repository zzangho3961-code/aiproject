
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------
st.set_page_config(
    page_title="월별 평균기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 평균기온 예측 프로그램")
st.write("과거 기온 데이터를 분석하고 미래의 평균기온을 예측합니다.")

# --------------------------------------------------
# CSV 파일 불러오기
# pages 폴더의 상위 폴더에서 temperature.csv 찾기
# --------------------------------------------------
@st.cache_data
def load_data():
    file_path = Path(__file__).parent.parent / "temperature.csv"

    if not file_path.exists():
        st.error("temperature.csv 파일을 찾을 수 없습니다.")
        st.info("temperature.csv 파일을 pages 폴더의 상위 폴더에 넣어주세요.")
        st.stop()

    encodings = ["cp949", "utf-8-sig", "euc-kr"]
    data = None

    for encoding in encodings:
        try:
            data = pd.read_csv(file_path, encoding=encoding)
            break
        except UnicodeDecodeError:
            continue

    if data is None:
        st.error("CSV 파일 인코딩을 읽을 수 없습니다.")
        st.stop()

    required_columns = ["일시", "평균기온(℃)"]

    for col in required_columns:
        if col not in data.columns:
            st.error(f"CSV 파일에 '{col}' 열이 없습니다.")
            st.write("현재 CSV 열:", list(data.columns))
            st.stop()

    # 날짜 변환
    data["일시"] = pd.to_datetime(
        data["일시"],
        format="%b-%y",
        errors="coerce"
    )

    # 기온 숫자 변환
    data["평균기온(℃)"] = pd.to_numeric(
        data["평균기온(℃)"],
        errors="coerce"
    )

    # 결측치 제거
    data = data.dropna(
        subset=["일시", "평균기온(℃)"]
    ).copy()

    data["연도"] = data["일시"].dt.year
    data["월"] = data["일시"].dt.month

    return data.sort_values("일시")


df = load_data()

if df.empty:
    st.error("분석할 수 있는 기온 데이터가 없습니다.")
    st.stop()

# --------------------------------------------------
# 회귀분석 함수
# --------------------------------------------------
def calculate_r2(actual, predicted):
    actual = np.array(actual)
    predicted = np.array(predicted)

    ss_res = np.sum((actual - predicted) ** 2)
    ss_tot = np.sum((actual - np.mean(actual)) ** 2)

    if ss_tot == 0:
        return 0

    return 1 - (ss_res / ss_tot)


def linear_regression(years, temperatures, target_year):
    # 선형회귀: y = ax + b
    slope, intercept = np.polyfit(years, temperatures, 1)

    predicted = slope * target_year + intercept
    fitted = slope * years + intercept

    r2 = calculate_r2(temperatures, fitted)

    return predicted, fitted, r2, slope, intercept


def polynomial_regression(years, temperatures, target_year):
    # 연도를 중심화하여 수치 안정성 개선
    center = np.mean(years)
    centered_years = years - center

    # 2차 다항회귀
    coefficients = np.polyfit(
        centered_years,
        temperatures,
        2
    )

    predicted = np.polyval(
        coefficients,
        target_year - center
    )

    fitted = np.polyval(
        coefficients,
        centered_years
    )

    r2 = calculate_r2(temperatures, fitted)

    return predicted, fitted, r2, coefficients, center


def knn_regression(years, temperatures, target_year, k=5):
    # 목표 연도와 가까운 과거 연도 k개 선택
    distances = np.abs(years - target_year)

    nearest_indices = np.argsort(distances)[:min(k, len(years))]

    predicted = np.mean(temperatures[nearest_indices])

    fitted = []

    # 각 과거 연도에 대해서도 KNN 예측값 계산
    for year in years:
        distance = np.abs(years - year)
        indices = np.argsort(distance)[:min(k, len(years))]
        fitted.append(np.mean(temperatures[indices]))

    fitted = np.array(fitted)
    r2 = calculate_r2(temperatures, fitted)

    return predicted, fitted, r2, nearest_indices


# --------------------------------------------------
# 사용자 입력
# --------------------------------------------------
st.subheader("📅 예측 조건 선택")

col1, col2 = st.columns(2)

with col1:
    selected_month = st.selectbox(
        "예측할 월을 선택하세요",
        list(range(1, 13)),
        format_func=lambda x: f"{x}월"
    )

with col2:
    last_year = int(df["연도"].max())

    selected_year = st.number_input(
        "예측할 연도를 입력하세요",
        min_value=last_year + 1,
        max_value=2100,
        value=last_year + 1,
        step=1
    )

# --------------------------------------------------
# 선택한 월 데이터 추출
# --------------------------------------------------
monthly_data = df[df["월"] == selected_month].copy()

monthly_data = monthly_data.sort_values("연도")

if len(monthly_data) < 3:
    st.warning("선택한 월의 데이터가 3개 미만이어서 예측하기 어렵습니다.")
    st.stop()

years = monthly_data["연도"].to_numpy(dtype=float)
temperatures = monthly_data["평균기온(℃)"].to_numpy(dtype=float)

# --------------------------------------------------
# 세 가지 알고리즘 계산
# --------------------------------------------------
linear_result = linear_regression(
    years, temperatures, selected_year
)

poly_result = polynomial_regression(
    years, temperatures, selected_year
)

knn_result = knn_regression(
    years, temperatures, selected_year
)

results = {
    "선형회귀": {
        "prediction": linear_result[0],
        "fitted": linear_result[1],
        "r2": linear_result[2]
    },
    "다항회귀": {
        "prediction": poly_result[0],
        "fitted": poly_result[1],
        "r2": poly_result[2]
    },
    "KNN": {
        "prediction": knn_result[0],
        "fitted": knn_result[1],
        "r2": knn_result[2]
    }
}

# --------------------------------------------------
# 알고리즘 선택
# --------------------------------------------------
st.divider()
st.subheader("🧠 예측 알고리즘 선택")

selected_model = st.selectbox(
    "사용할 예측 알고리즘을 선택하세요",
    ["선형회귀", "다항회귀", "KNN"]
)

result = results[selected_model]
prediction = result["prediction"]
fitted = result["fitted"]

# --------------------------------------------------
# 예측 결과
# --------------------------------------------------
st.subheader("🔮 예측 결과")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "예측 연도",
        f"{selected_year}년"
    )

with col2:
    st.metric(
        "예측 평균기온",
        f"{prediction:.2f} ℃"
    )

with col3:
    st.metric(
        "모델 R²",
        f"{result['r2']:.3f}"
    )

# --------------------------------------------------
# 그래프
# --------------------------------------------------
st.subheader(f"📈 {selected_month}월 평균기온 변화 및 예측")

fig = go.Figure()

# 실제 기온 데이터
fig.add_trace(
    go.Scatter(
        x=years,
        y=temperatures,
        mode="lines+markers",
        name="실제 평균기온",
        line=dict(width=2),
        marker=dict(size=6)
    )
)

# 모델이 학습한 곡선
fig.add_trace(
    go.Scatter(
        x=years,
        y=fitted,
        mode="lines",
        name=f"{selected_model} 학습 결과",
        line=dict(dash="dash", width=3)
    )
)

# 미래 예측 지점
fig.add_trace(
    go.Scatter(
        x=[selected_year],
        y=[prediction],
        mode="markers+text",
        name="미래 예측기온",
        marker=dict(size=14, symbol="star"),
        text=[f"{prediction:.2f}℃"],
        textposition="top center"
    )
)

# 마지막 실제 연도 표시
fig.add_vline(
    x=int(max(years)),
    line_dash="dot",
    annotation_text="실제 데이터 마지막 연도"
)

fig.update_layout(
    title=f"{selected_month}월 평균기온 예측 ({selected_model})",
    xaxis_title="연도",
    yaxis_title="평균기온 (℃)",
    hovermode="x unified",
    template="plotly_white",
    legend_title="데이터 구분"
)

st.plotly_chart(fig, use_container_width=True)

st.caption(
    "실선은 실제 관측 기온, 점선은 모델의 과거 데이터 학습 결과, "
    "별표는 선택한 연도의 예측값입니다."
)

# --------------------------------------------------
# 알고리즘 비교
# --------------------------------------------------
st.divider()
st.subheader("⚖️ 세 가지 알고리즘 예측 결과 비교")

comparison = pd.DataFrame({
    "알고리즘": list(results.keys()),
    "예측 평균기온(℃)": [
        results[name]["prediction"]
        for name in results
    ],
    "R²": [
        results[name]["r2"]
        for name in results
    ]
})

st.dataframe(
    comparison.style.format({
        "예측 평균기온(℃)": "{:.2f}",
        "R²": "{:.3f}"
    }),
    use_container_width=True,
    hide_index=True
)

bar_fig = go.Figure()

bar_fig.add_trace(
    go.Bar(
        x=comparison["알고리즘"],
        y=comparison["예측 평균기온(℃)"],
        text=[
            f"{value:.2f}℃"
            for value in comparison["예측 평균기온(℃)"]
        ],
        textposition="outside"
    )
)

bar_fig.update_layout(
    title=f"{selected_year}년 {selected_month}월 알고리즘별 예측기온",
    xaxis_title="알고리즘",
    yaxis_title="예측 평균기온 (℃)",
    template="plotly_white"
)

st.plotly_chart(bar_fig, use_container_width=True)

# --------------------------------------------------
# 알고리즘 작동 원리 설명
# --------------------------------------------------
st.divider()
st.subheader("📚 선택한 알고리즘은 어떻게 작동할까?")

if selected_model == "선형회귀":
    st.markdown("""
    ### ① 선형회귀 (Linear Regression)

    과거 연도와 평균기온 사이의 관계를 직선으로 표현하는 방법입니다.

    **작동 원리**
    1. 과거 연도를 x축, 평균기온을 y축으로 설정합니다.
    2. 실제 데이터와 가장 잘 맞는 직선을 찾습니다.
    3. 직선의 기울기와 절편을 계산합니다.
    4. 미래 연도를 직선의 식에 넣어 예측합니다.

    **수학 공식**

    `y = ax + b`

    - a: 직선의 기울기
    - b: y절편
    - x: 연도
    - y: 예측 평균기온

    그래프에서 점선이 직선 형태로 나타나는 것이 특징입니다.
    """)

    st.write(f"기울기: {linear_result[3]:.5f}")
    st.write(f"절편: {linear_result[4]:.5f}")

elif selected_model == "다항회귀":
    st.markdown("""
    ### ② 다항회귀 (Polynomial Regression)

    직선이 아닌 곡선으로 데이터의 변화 추세를 분석하는 방법입니다.

    **작동 원리**
    1. 과거 연도와 평균기온 데이터를 수집합니다.
    2. 데이터의 변화에 맞는 2차 곡선을 계산합니다.
    3. 곡선의 계수를 구합니다.
    4. 미래 연도를 곡선의 식에 넣어 예측합니다.

    **수학 공식**

    `y = ax² + bx + c`

    - a, b, c: 곡선을 결정하는 계수
    - x: 연도
    - y: 예측 평균기온

    그래프에서 점선이 곡선 형태로 나타날 수 있습니다.
    """)

    st.write(
        "계수:",
        [round(float(value), 6) for value in poly_result[3]]
    )

elif selected_model == "KNN":
    st.markdown("""
    ### ③ KNN 회귀 (K-Nearest Neighbors Regression)

    예측하려는 연도와 가까운 과거 연도들의 기온을 참고하는 방법입니다.

    **작동 원리**
    1. 예측할 연도를 정합니다.
    2. 과거 연도 중 예측 연도와 가까운 5개 연도를 찾습니다.
    3. 선택된 5개 연도의 평균기온을 계산합니다.
    4. 계산한 평균을 미래 기온으로 예측합니다.

    **수학 공식**

    `예측값 = 가까운 K개 데이터의 평균`

    KNN은 직선이나 곡선을 만드는 대신 가까운 과거 데이터의 값을 활용합니다.
    """)

    st.write("사용한 이웃 데이터 개수: 5개")
    st.write(
        "참고한 과거 연도:",
        [int(years[i]) for i in knn_result[3]]
    )

# --------------------------------------------------
# 주의사항
# --------------------------------------------------
st.info("""
📌 **예측 시 주의사항**

- 기온은 여러 기후 요인의 영향을 받으므로 예측값이 실제 기온과 다를 수 있습니다.
- 선형회귀는 장기적인 직선 추세를 가정합니다.
- 다항회귀는 장기 예측에서 곡선이 지나치게 커질 수 있습니다.
- KNN은 가까운 과거 데이터의 평균을 사용하므로 먼 미래를 예측할 때 변화가 충분히 반영되지 않을 수 있습니다.
- R²는 현재 학습 데이터에 대한 적합도를 나타내며 미래 예측의 정확도를 보장하지 않습니다.
""")

# --------------------------------------------------
# 원본 데이터 확인
# --------------------------------------------------
with st.expander("📂 선택한 월의 과거 기온 데이터 확인하기"):
    st.dataframe(
        monthly_data[["일시", "연도", "월", "평균기온(℃)"]],
        use_container_width=True,
        hide_index=True
    )

st.success("분석이 완료되었습니다! 🌡️")

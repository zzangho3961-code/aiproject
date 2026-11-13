
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# ----------------------------------
# 1. 페이지 설정
# ----------------------------------

st.set_page_config(
    page_title="Iris 품종 예측",
    page_icon="🌸",
    layout="wide"
)

st.title("🌸 Iris 붓꽃 품종 예측 AI")
st.write("꽃잎의 길이와 너비를 입력하면 머신러닝이 붓꽃 품종을 예측합니다.")

st.divider()

# ----------------------------------
# 2. 데이터 불러오기
# ----------------------------------

@st.cache_data
def load_data():
    file_path = Path(__file__).resolve().parent / "Iris.csv"

    if not file_path.exists():
        raise FileNotFoundError("Iris.csv 파일을 찾을 수 없습니다.")

    try:
        data = pd.read_csv(file_path, encoding="cp949")
    except UnicodeDecodeError:
        data = pd.read_csv(file_path, encoding="utf-8-sig")

    return data


try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 파일 오류: {e}")
    st.stop()

# 필요한 컬럼 확인
required_columns = ["꽃잎길이", "꽃잎너비", "품종"]

if not all(col in df.columns for col in required_columns):
    st.error("CSV 파일의 컬럼명을 확인해주세요.")
    st.stop()

df = df.dropna(subset=required_columns)

# ----------------------------------
# 3. 학습 데이터 설정
# ----------------------------------

X = df[["꽃잎길이", "꽃잎너비"]]
y = df["품종"]

# Random Forest 모델
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42
)

# 5겹 교차검증
scores = cross_val_score(
    model,
    X,
    y,
    cv=5,
    scoring="accuracy"
)

# 전체 데이터 학습
model.fit(X, y)

# ----------------------------------
# 4. 입력 범위 설정
# ----------------------------------

min_length = float(df["꽃잎길이"].min())
max_length = float(df["꽃잎길이"].max())

min_width = float(df["꽃잎너비"].min())
max_width = float(df["꽃잎너비"].max())

st.subheader("📏 꽃잎 크기 입력")

st.info(
    f"""
    입력 가능한 범위를 확인하세요.

    🌱 꽃잎 길이: {min_length} ~ {max_length} cm

    🌱 꽃잎 너비: {min_width} ~ {max_width} cm
    """
)

col1, col2 = st.columns(2)

with col1:
    petal_length = st.number_input(
        "꽃잎 길이 (cm)",
        min_value=min_length,
        max_value=max_length,
        value=4.5,
        step=0.1
    )

with col2:
    petal_width = st.number_input(
        "꽃잎 너비 (cm)",
        min_value=min_width,
        max_value=max_width,
        value=1.3,
        step=0.1
    )

# ----------------------------------
# 5. 품종 예측
# ----------------------------------

if st.button("🔍 붓꽃 품종 예측하기", type="primary",
             use_container_width=True):

    input_data = pd.DataFrame(
        [[petal_length, petal_width]],
        columns=["꽃잎길이", "꽃잎너비"]
    )

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    st.divider()

    st.subheader("🎯 AI 예측 결과")

    st.success(f"예측된 붓꽃 품종: {prediction}")

    # 품종별 확률
    probability_df = pd.DataFrame({
        "품종": model.classes_,
        "예측 확률 (%)": probabilities * 100
    })

    probability_df = probability_df.sort_values(
        "예측 확률 (%)",
        ascending=False
    )

    st.write("### 품종별 예측 확률")

    st.bar_chart(
        probability_df.set_index("품종")
    )

    st.dataframe(
        probability_df.style.format({
            "예측 확률 (%)": "{:.2f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

    # ----------------------------------
    # 6. 분류 영역 시각화
    # ----------------------------------

    st.divider()
    st.subheader("📊 머신러닝 분류 영역 시각화")

    # 그래프 영역 생성
    x_min = min_length - 0.3
    x_max = max_length + 0.3
    y_min = min_width - 0.2
    y_max = max_width + 0.2

    xx, yy = np.meshgrid(
        np.arange(x_min, x_max, 0.02),
        np.arange(y_min, y_max, 0.02)
    )

    grid = pd.DataFrame({
        "꽃잎길이": xx.ravel(),
        "꽃잎너비": yy.ravel()
    })

    # 각 좌표의 품종 예측
    Z = model.predict(grid)

    # 품종별 숫자 변환
    class_names = list(model.classes_)

    class_to_number = {
        name: i for i, name in enumerate(class_names)
    }

    Z_number = np.array([
        class_to_number[name] for name in Z
    ]).reshape(xx.shape)

    # 그래프 색상
    colors = ["#FFD166", "#74B9FF", "#DDA0DD"]

    fig, ax = plt.subplots(figsize=(11, 7))

    # 배경 분류 영역
    ax.contourf(
        xx,
        yy,
        Z_number,
        levels=np.arange(-0.5, len(class_names) + 0.5, 1),
        colors=colors,
        alpha=0.35
    )

    # 기존 데이터 표시
    for i, species in enumerate(class_names):

        subset = df[df["품종"] == species]

        ax.scatter(
            subset["꽃잎길이"],
            subset["꽃잎너비"],
            color=colors[i],
            edgecolors="black",
            s=55,
            alpha=0.85,
            label=species
        )

    # 사용자 입력 위치 (초록색 별)
    ax.scatter(
        petal_length,
        petal_width,
        marker="*",
        color="limegreen",
        edgecolors="black",
        linewidths=1.2,
        s=450,
        label="Your Input",
        zorder=10
    )

    # 입력 위치 설명
    ax.annotate(
        f"Your Input\n({petal_length:.1f}, {petal_width:.1f})",
        xy=(petal_length, petal_width),
        xytext=(15, 15),
        textcoords="offset points",
        fontsize=10,
        fontweight="bold",
        color="darkgreen",
        arrowprops=dict(
            arrowstyle="->",
            color="green"
        )
    )

    ax.set_xlabel("Petal Length (cm)", fontsize=12)
    ax.set_ylabel("Petal Width (cm)", fontsize=12)

    ax.set_title(
        "Iris Random Forest Classification",
        fontsize=15,
        fontweight="bold"
    )

    ax.legend()
    ax.grid(alpha=0.2)

    st.pyplot(fig)
    plt.close(fig)

    # ----------------------------------
    # 7. 분류 이유 설명
    # ----------------------------------

    st.subheader("💡 왜 이 품종으로 분류되었을까?")

    st.write(
        f"""
        입력한 꽃잎 길이는 **{petal_length:.1f}cm**,
        꽃잎 너비는 **{petal_width:.1f}cm**입니다.

        랜덤 포레스트는 기존 붓꽃 데이터의 꽃잎 크기 패턴을
        학습한 여러 의사결정나무의 결과를 종합합니다.

        그 결과 가장 높은 예측 확률을 가진 품종은
        **{prediction}**입니다.
        """
    )

    st.caption(
        "그래프의 배경색은 해당 위치에서 모델이 예측한 품종을 "
        "나타냅니다. 예측 확률은 모델의 추정값이며 실제 확률을 "
        "보장하지 않습니다."
    )

    # ----------------------------------
    # 8. 모델 성능
    # ----------------------------------

    st.divider()
    st.subheader("📈 머신러닝 모델 성능")

    accuracy = scores.mean() * 100

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "5겹 교차검증 평균 정확도",
            f"{accuracy:.2f}%"
        )

    with c2:
        st.metric(
            "학습 데이터 개수",
            f"{len(df)}개"
        )

    st.caption(
        "정확도는 5겹 교차검증으로 측정했습니다. "
        "모델 성능은 입력 특성과 데이터 구성에 따라 달라질 수 있습니다."
    )

# ----------------------------------
# 9. 데이터 정보
# ----------------------------------

with st.expander("📚 Iris 데이터 정보 확인"):

    st.write("전체 데이터 미리보기")
    st.dataframe(df, use_container_width=True)

    st.write("품종별 데이터 개수")
    st.bar_chart(df["품종"].value_counts())

    st.write("기초 통계 분석")
    st.dataframe(df.describe(), use_container_width=True)

st.divider()

st.caption("🌸 Iris AI Classification | Random Forest")

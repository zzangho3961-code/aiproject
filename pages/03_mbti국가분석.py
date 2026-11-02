
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# -------------------------
# 페이지 설정
# -------------------------
st.set_page_config(
    page_title="세계 국가별 MBTI 분석",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 세계 국가별 MBTI 분석")
st.markdown("국가를 선택하면 해당 국가의 MBTI 분포를 확인할 수 있습니다.")
st.divider()

# -------------------------
# 데이터 불러오기
# -------------------------
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

try:
    df = load_data()

    mbti_columns = [
        col for col in df.columns if col != "Country"
    ]

    # 국가 선택
    country_list = sorted(df["Country"].dropna().unique())

    selected_country = st.selectbox(
        "🌏 분석할 국가를 선택하세요.",
        country_list
    )

    # 선택한 국가 데이터
    country_data = df[
        df["Country"] == selected_country
    ].iloc[0]

    # MBTI 비율 계산 및 정렬
    mbti_data = pd.DataFrame({
        "MBTI": mbti_columns,
        "비율": [
            country_data[col] * 100
            for col in mbti_columns
        ]
    })

    mbti_data = mbti_data.sort_values(
        "비율",
        ascending=False
    ).reset_index(drop=True)

    # -------------------------
    # 최고 비율 MBTI
    # -------------------------
    first_mbti = mbti_data.iloc[0]["MBTI"]
    first_value = mbti_data.iloc[0]["비율"]

    st.subheader(f"📊 {selected_country} MBTI 분석")

    col1, col2, col3 = st.columns(3)

    col1.metric("🌍 분석 국가", selected_country)
    col2.metric("🏆 가장 높은 MBTI", first_mbti)
    col3.metric("📈 최고 비율", f"{first_value:.2f}%")

    st.success(
        f"🏆 {selected_country}에서 가장 높은 비율을 차지하는 "
        f"MBTI는 {first_mbti}입니다!"
    )

    st.divider()

    # -------------------------
    # 막대그래프 색상 설정
    # -------------------------
    st.subheader("🧠 MBTI 16가지 유형별 비율")

    colors = ["#FF3030"]

    blue_gradient = [
        mcolors.to_hex(
            plt.colormaps["Blues"](value)
        )
        for value in [
            0.85 - i * (0.85 - 0.25) / 14
            for i in range(15)
        ]
    ]

    colors.extend(blue_gradient)

    # -------------------------
    # 그래프 그리기
    # -------------------------
    fig, ax = plt.subplots(figsize=(13, 6))

    bars = ax.bar(
        mbti_data["MBTI"],
        mbti_data["비율"],
        color=colors,
        edgecolor="white",
        linewidth=1
    )

    # 막대 위에 비율 표시
    for bar, value in zip(
        bars,
        mbti_data["비율"]
    ):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.15,
            f"{value:.2f}%",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold"
        )

    ax.set_title(
        f"{selected_country} MBTI Distribution",
        fontsize=17,
        fontweight="bold",
        pad=20
    )

    ax.set_xlabel("MBTI Type", fontsize=12)
    ax.set_ylabel("Percentage (%)", fontsize=12)

    ax.set_ylim(
        0,
        mbti_data["비율"].max() * 1.18
    )

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    ax.set_axisbelow(True)

    plt.xticks(fontsize=10)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    # -------------------------
    # 순위표
    # -------------------------
    st.divider()

    st.subheader("🏅 MBTI 비율 순위")

    ranking = mbti_data.copy()
    ranking.index = ranking.index + 1
    ranking.index.name = "순위"

    ranking = ranking.rename(
        columns={"비율": "비율 (%)"}
    )

    st.dataframe(
        ranking,
        use_container_width=True
    )

    st.caption(
        "※ 제공된 CSV 데이터의 비율을 백분율로 환산한 결과입니다."
    )

except FileNotFoundError:
    st.error(
        "CSV 파일을 찾을 수 없습니다. "
        "app.py와 같은 폴더에 CSV 파일을 넣어주세요."
    )

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")


import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="월별 기온분석",
    page_icon="🌡️",
    layout="wide"
)

# 제목
st.title("🌡️ 월별 기온분석")
st.write("원하는 월을 선택하면 전체 연도의 최고기온과 최저기온을 비교합니다.")

# CSV 파일 불러오기
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("temperature.csv", encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv("temperature.csv", encoding="utf-8-sig")

    # 날짜에서 월과 연도 추출
    df["월"] = df["일시"].str.split("-").str[0]
    year_text = df["일시"].str.split("-").str[1].astype(int)

    # 데이터의 연도 범위에 맞춰 2자리 연도를 4자리로 변환
    # 07~99는 1907~1999, 00~26은 2000~2026
    df["연도"] = year_text.apply(
        lambda y: 1900 + y if y >= 7 else 2000 + y
    )

    # 기온 데이터 숫자 변환
    df["최고기온(℃)"] = pd.to_numeric(
        df["최고기온(℃)"], errors="coerce"
    )
    df["최저기온(℃)"] = pd.to_numeric(
        df["최저기온(℃)"], errors="coerce"
    )

    return df


try:
    df = load_data()

    # 월 선택
    month_dict = {
        "1월": "Jan",
        "2월": "Feb",
        "3월": "Mar",
        "4월": "Apr",
        "5월": "May",
        "6월": "Jun",
        "7월": "Jul",
        "8월": "Aug",
        "9월": "Sep",
        "10월": "Oct",
        "11월": "Nov",
        "12월": "Dec"
    }

    selected_month = st.selectbox(
        "📅 분석할 월을 선택하세요.",
        list(month_dict.keys())
    )

    month_code = month_dict[selected_month]

    # 선택한 월의 데이터만 추출
    filtered_df = df[df["월"] == month_code].copy()

    # 연도별 데이터 정리
    # 같은 연도에 중복 자료가 있으면 최고기온은 최댓값,
    # 최저기온은 최솟값으로 집계
    result = (
        filtered_df.groupby("연도")
        .agg({
            "최고기온(℃)": "max",
            "최저기온(℃)": "min"
        })
        .reset_index()
        .sort_values("연도")
    )

    # 결측값 제거
    result = result.dropna(
        subset=["최고기온(℃)", "최저기온(℃)"]
    )

    st.divider()

    if not result.empty:

        # 그래프 생성
        fig = go.Figure()

        # 최고기온 그래프 - 핫핑크
        fig.add_trace(go.Scatter(
            x=result["연도"],
            y=result["최고기온(℃)"],
            mode="lines+markers",
            name="최고기온",
            line=dict(
                color="#FF1493",
                width=3
            ),
            marker=dict(size=7)
        ))

        # 최저기온 그래프 - 코발트 블루
        fig.add_trace(go.Scatter(
            x=result["연도"],
            y=result["최저기온(℃)"],
            mode="lines+markers",
            name="최저기온",
            line=dict(
                color="#0047AB",
                width=3
            ),
            marker=dict(size=7)
        ))

        # 그래프 레이아웃
        fig.update_layout(
            title="월별 기온분석",
            xaxis_title="연도",
            yaxis_title="온도 (℃)",
            legend_title="기온 구분",
            hovermode="x unified",
            template="plotly_white",
            height=550
        )

        # 그래프 출력
        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # 분석 데이터 표시
        st.subheader("📊 선택한 월의 기온 데이터")
        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.warning("선택한 월에 표시할 데이터가 없습니다.")

except FileNotFoundError:
    st.error("temperature.csv 파일을 찾을 수 없습니다. app.py와 같은 폴더에 넣어주세요.")

except Exception as e:
    st.error(f"데이터 처리 중 오류가 발생했습니다: {e}")

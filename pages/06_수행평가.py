
import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="오늘 뭐 먹지?",
    page_icon="🍽️",
    layout="centered"
)

# 제목
st.title("🍽️ 오늘 뭐 먹지?")
st.subheader("오늘의 메뉴 고민은 여기서 끝!")
st.write("좋아하는 음식 종류를 선택하면 맛있는 메뉴 2가지를 추천해 줄게 😋")

st.divider()

# 음식 데이터
food_data = {
    "한식 🇰🇷": [
        {
            "name": "김치찌개",
            "emoji": "🍲",
            "taste": "매콤하고 칼칼하면서 김치의 깊은 감칠맛이 특징이야.",
            "difficulty": "쉬움",
            "reason": "한국인이 즐겨 먹는 대표적인 집밥 메뉴로 든든하게 먹기 좋아!"
        },
        {
            "name": "제육볶음",
            "emoji": "🥩",
            "taste": "매콤달콤한 양념과 돼지고기의 고소한 맛이 잘 어울려.",
            "difficulty": "보통",
            "reason": "밥과 함께 먹기 좋고 매콤한 고기 요리를 좋아한다면 추천!"
        },
        {
            "name": "비빔밥",
            "emoji": "🥗",
            "taste": "다양한 나물과 고추장의 조화로 새콤달콤하고 고소해.",
            "difficulty": "보통",
            "reason": "여러 가지 재료를 한 번에 즐길 수 있는 균형 잡힌 메뉴야."
        },
        {
            "name": "불고기",
            "emoji": "🥩",
            "taste": "달콤짭짤한 간장 양념과 부드러운 소고기의 풍미가 좋아.",
            "difficulty": "보통",
            "reason": "호불호가 비교적 적고 남녀노소 즐기기 좋은 음식이야."
        },
        {
            "name": "순두부찌개",
            "emoji": "🍲",
            "taste": "부드러운 순두부와 얼큰한 국물이 매력적이야.",
            "difficulty": "보통",
            "reason": "따뜻하고 얼큰한 국물 요리가 생각날 때 딱 좋아!"
        },
        {
            "name": "간장찜닭",
            "emoji": "🍗",
            "taste": "달콤짭짤한 간장 소스와 닭고기, 당면의 조화가 좋아.",
            "difficulty": "보통",
            "reason": "여러 명이 함께 먹기 좋고 든든한 한 끼로 추천해!"
        }
    ],

    "양식 🇮🇹": [
        {
            "name": "까르보나라",
            "emoji": "🍝",
            "taste": "치즈와 계란의 고소함, 베이컨의 짭짤함이 조화를 이뤄.",
            "difficulty": "보통",
            "reason": "꾸덕하고 진한 크림감과 치즈 풍미를 좋아한다면 추천!"
        },
        {
            "name": "마르게리타 피자",
            "emoji": "🍕",
            "taste": "토마토의 산미와 모차렐라 치즈, 바질 향이 잘 어울려.",
            "difficulty": "보통",
            "reason": "이탈리아를 대표하는 클래식 피자로 재료 본연의 맛을 즐길 수 있어!"
        },
        {
            "name": "라자냐",
            "emoji": "🍽️",
            "taste": "고기 라구와 베샤멜 소스, 치즈가 층층이 어우러져.",
            "difficulty": "어려움",
            "reason": "여러 소스의 깊은 풍미를 한 번에 느낄 수 있는 요리야."
        },
        {
            "name": "봉골레 파스타",
            "emoji": "🍝",
            "taste": "마늘과 올리브오일, 조개의 시원한 감칠맛이 특징이야.",
            "difficulty": "보통",
            "reason": "깔끔하면서도 해산물의 풍미가 살아 있는 파스타를 원한다면 추천!"
        },
        {
            "name": "스테이크",
            "emoji": "🥩",
            "taste": "고기의 육즙과 구운 표면의 고소한 풍미가 매력적이야.",
            "difficulty": "어려움",
            "reason": "고기 본연의 맛과 레스토랑 분위기를 즐기고 싶을 때 좋아!"
        },
        {
            "name": "감바스 알 아히요",
            "emoji": "🍤",
            "taste": "마늘 향이 가득한 올리브오일과 새우의 감칠맛이 특징이야.",
            "difficulty": "쉬움",
            "reason": "바삭한 빵과 함께 먹으면 풍미가 더욱 살아나!"
        }
    ],

    "일식 🇯🇵": [
        {
            "name": "돈카츠",
            "emoji": "🍱",
            "taste": "바삭한 튀김옷과 촉촉한 돼지고기의 조화가 좋아.",
            "difficulty": "보통",
            "reason": "바삭한 식감과 든든한 한 끼를 동시에 즐길 수 있어!"
        },
        {
            "name": "연어덮밥",
            "emoji": "🍣",
            "taste": "부드러운 연어와 밥, 간장 소스의 담백한 조화가 특징이야.",
            "difficulty": "쉬움",
            "reason": "신선한 해산물과 깔끔한 맛을 좋아한다면 추천!"
        },
        {
            "name": "규동",
            "emoji": "🥘",
            "taste": "달콤짭짤한 간장 양념이 소고기와 밥에 잘 어울려.",
            "difficulty": "쉬움",
            "reason": "간편하면서도 든든하게 먹을 수 있는 일본식 덮밥이야."
        },
        {
            "name": "라멘",
            "emoji": "🍜",
            "taste": "진한 육수와 쫄깃한 면, 차슈의 풍미가 매력적이야.",
            "difficulty": "보통",
            "reason": "진하고 깊은 국물 맛을 좋아하는 사람에게 추천!"
        },
        {
            "name": "오코노미야키",
            "emoji": "🥞",
            "taste": "양배추와 반죽의 고소함에 달콤짭짤한 소스가 더해져.",
            "difficulty": "보통",
            "reason": "다양한 토핑을 곁들여 색다른 일본식 요리를 즐길 수 있어!"
        },
        {
            "name": "가라아게",
            "emoji": "🍗",
            "taste": "간장과 생강으로 밑간한 닭고기를 바삭하게 튀긴 요리야.",
            "difficulty": "보통",
            "reason": "바삭하고 육즙 가득한 닭고기를 좋아한다면 추천!"
        }
    ],

    "중식 🇨🇳": [
        {
            "name": "마파두부",
            "emoji": "🌶️",
            "taste": "두반장의 매콤함과 두부의 부드러운 식감이 조화를 이뤄.",
            "difficulty": "보통",
            "reason": "매콤하면서도 깊은 감칠맛을 즐기고 싶을 때 좋아!"
        },
        {
            "name": "탕수육",
            "emoji": "🥢",
            "taste": "바삭한 튀김과 새콤달콤한 소스가 잘 어울려.",
            "difficulty": "보통",
            "reason": "중식 대표 메뉴로 바삭한 식감을 좋아한다면 추천!"
        },
        {
            "name": "짜장면",
            "emoji": "🍜",
            "taste": "춘장의 구수하고 달콤짭짤한 맛이 면과 잘 어울려.",
            "difficulty": "보통",
            "reason": "친숙하고 든든한 중식 메뉴를 먹고 싶을 때 추천!"
        },
        {
            "name": "짬뽕",
            "emoji": "🍲",
            "taste": "얼큰한 국물에 해산물과 채소의 감칠맛이 더해져.",
            "difficulty": "보통",
            "reason": "얼큰하고 시원한 국물 요리가 당기는 날에 딱이야!"
        },
        {
            "name": "깐풍기",
            "emoji": "🍗",
            "taste": "바삭한 닭고기에 매콤새콤한 소스가 더해져.",
            "difficulty": "어려움",
            "reason": "일반적인 치킨과 다른 중식 특유의 강렬한 풍미를 느낄 수 있어!"
        },
        {
            "name": "양장피",
            "emoji": "🥗",
            "taste": "해산물과 채소, 겨자소스의 톡 쏘는 맛이 특징이야.",
            "difficulty": "어려움",
            "reason": "다양한 식감과 산뜻한 겨자 풍미를 즐기고 싶을 때 추천!"
        }
    ]
}

# 음식 종류 선택
st.subheader("🥢 어떤 음식이 먹고 싶어?")

food_type = st.radio(
    "음식 종류를 선택해 줘!",
    ["한식 🇰🇷", "양식 🇮🇹", "일식 🇯🇵", "중식 🇨🇳"],
    horizontal=True
)

st.divider()

# 추천 버튼
st.subheader("🎲 오늘의 메뉴 추천")

if "recommended_foods" not in st.session_state:
    st.session_state.recommended_foods = None

if st.button("✨ 메뉴 2가지 추천받기!", use_container_width=True):

    st.session_state.recommended_foods = random.sample(
        food_data[food_type], 2
    )
    st.session_state.selected_type = food_type

# 추천 결과
if st.session_state.recommended_foods is not None:

    if st.session_state.selected_type == food_type:

        st.success("오늘의 추천 메뉴가 도착했어! 🎉")

        for i, food in enumerate(
            st.session_state.recommended_foods, 1
        ):

            st.markdown(f"### {i}. {food['emoji']} {food['name']}")

            st.info(
                f"💡 **추천 이유**\n\n{food['reason']}"
            )

            st.write(f"😋 **맛:** {food['taste']}")

            st.write(
                f"👨‍🍳 **조리 난이도:** {food['difficulty']}"
            )

            st.divider()

        st.caption("마음에 드는 메뉴가 있으면 오늘 도전해 봐! 😎")

    else:
        st.info("음식 종류를 바꾸고 추천 버튼을 눌러 새로운 메뉴를 만나 봐!")

else:
    st.write("버튼을 누르면 선택한 종류에서 메뉴 2가지를 랜덤으로 추천해 줄게! 🎁")

# 하단 문구
st.divider()

st.markdown(
    """
    ### 🍴 오늘의 요리 한마디

    맛있는 음식은 사람을 행복하게 만들어!

    오늘도 맛있는 한 끼 먹자 😋
    """
)

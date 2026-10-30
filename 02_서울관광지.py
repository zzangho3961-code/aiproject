
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

# 서울 관광지 데이터
places = [
    {"rank": 1, "name": "명동", "eng": "Myeongdong",
     "lat": 37.5636, "lon": 126.9850,
     "category": "쇼핑 · K-뷰티",
     "desc": "화장품, 패션 매장과 길거리 음식으로 유명한 서울 대표 쇼핑 거리입니다.",
     "english": "A popular shopping district famous for cosmetics, fashion and street food."},

    {"rank": 2, "name": "N서울타워", "eng": "N Seoul Tower",
     "lat": 37.5512, "lon": 126.9882,
     "category": "전망 · 랜드마크",
     "desc": "서울의 아름다운 전경을 감상할 수 있는 대표적인 관광 명소입니다.",
     "english": "A famous landmark offering panoramic views of Seoul."},

    {"rank": 3, "name": "코엑스", "eng": "COEX",
     "lat": 37.5116, "lon": 127.0592,
     "category": "쇼핑 · 전시",
     "desc": "쇼핑몰과 별마당도서관, 다양한 전시 공간이 있는 복합문화공간입니다.",
     "english": "A large complex with shopping, the Starfield Library and exhibitions."},

    {"rank": 4, "name": "강남역", "eng": "Gangnam Station",
     "lat": 37.4979, "lon": 127.0276,
     "category": "쇼핑 · 도심",
     "desc": "다양한 음식점과 카페, 쇼핑 매장이 모여 있는 번화가입니다.",
     "english": "A lively area filled with restaurants, cafes and shops."},

    {"rank": 5, "name": "홍대", "eng": "Hongdae",
     "lat": 37.5563, "lon": 126.9236,
     "category": "문화 · 공연",
     "desc": "거리 공연과 음악, 개성 있는 카페와 상점으로 유명합니다.",
     "english": "A lively area known for music, street performances and cafes."},

    {"rank": 6, "name": "경복궁", "eng": "Gyeongbokgung Palace",
     "lat": 37.5796, "lon": 126.9770,
     "category": "역사 · 전통문화",
     "desc": "조선 시대 왕궁으로 한국의 역사와 전통 건축을 볼 수 있습니다.",
     "english": "The main royal palace of the Joseon Dynasty."},

    {"rank": 7, "name": "광장시장", "eng": "Gwangjang Market",
     "lat": 37.5700, "lon": 126.9997,
     "category": "전통시장 · 음식",
     "desc": "빈대떡과 김밥 등 다양한 한국 길거리 음식을 맛볼 수 있습니다.",
     "english": "A traditional market famous for Korean street food."},

    {"rank": 8, "name": "DDP", "eng": "Dongdaemun Design Plaza",
     "lat": 37.5671, "lon": 127.0095,
     "category": "건축 · 디자인",
     "desc": "독특한 건축물과 디자인 전시를 감상할 수 있는 공간입니다.",
     "english": "A landmark known for unique architecture and design exhibitions."},

    {"rank": 9, "name": "북촌한옥마을", "eng": "Bukchon Hanok Village",
     "lat": 37.5826, "lon": 126.9830,
     "category": "전통문화 · 산책",
     "desc": "한국의 전통 한옥과 옛 주거 문화를 경험할 수 있는 마을입니다.",
     "english": "A village featuring traditional Korean houses."},

    {"rank": 10, "name": "남대문시장", "eng": "Namdaemun Market",
     "lat": 37.5592, "lon": 126.9777,
     "category": "전통시장 · 쇼핑",
     "desc": "의류와 잡화, 다양한 먹거리를 판매하는 서울의 전통시장입니다.",
     "english": "A historic market selling clothes, accessories and Korean food."}
]

st.title("🗺️ 서울 관광지 TOP 10")
st.subheader("Top 10 Tourist Attractions in Seoul")
st.write("외국인 관광객을 위한 서울 대표 관광지 안내 지도입니다.")

st.info("관광지 추천 목록이며 공식 방문객 순위는 아닙니다.")

# 검색 기능
search = st.text_input("🔍 관광지 검색")

filtered_places = [
    p for p in places
    if search.lower() in (
        p["name"] + p["eng"] + p["category"]
    ).lower()
]

col1, col2 = st.columns([1, 2])

with col1:
    st.header("📍 관광지 목록")

    if filtered_places:
        selected_name = st.selectbox(
            "관광지를 선택하세요",
            [p["name"] for p in filtered_places]
        )

        selected = next(
            p for p in filtered_places
            if p["name"] == selected_name
        )

        st.subheader(f'{selected["rank"]}위. {selected["name"]}')
        st.write(f'**영어 이름:** {selected["eng"]}')
        st.write(f'**종류:** {selected["category"]}')
        st.write(selected["desc"])

        st.markdown("**English Description**")
        st.write(selected["english"])

        google_url = (
            f'https://www.google.com/maps/search/?api=1&query='
            f'{selected["lat"]},{selected["lon"]}'
        )
        st.link_button("Google 지도에서 보기", google_url)

        st.divider()

        for p in filtered_places:
            st.write(f'{p["rank"]}위 | {p["name"]}')
    else:
        st.warning("검색 결과가 없습니다.")

with col2:
    st.header("🌏 서울 관광 지도")

    map_seoul = folium.Map(
        location=[37.5665, 126.9780],
        zoom_start=12
    )

    for p in filtered_places:
        popup = f"""
        <b>{p['rank']}위. {p['name']}</b><br>
        {p['eng']}<br>
        {p['category']}<br>
        {p['desc']}
        """

        folium.Marker(
            location=[p["lat"], p["lon"]],
            popup=folium.Popup(popup, max_width=250),
            tooltip=p["name"],
            icon=folium.Icon(
                color="red" if (
                    filtered_places and
                    p["name"] == selected_name
                ) else "blue",
                icon="info-sign"
            )
        ).add_to(map_seoul)

    if filtered_places:
        map_seoul.location = [
            selected["lat"], selected["lon"]
        ]
        map_seoul.zoom_start = 14 if search else 12

    st_folium(
        map_seoul,
        width=None,
        height=600,
        returned_objects=[]
    )

st.divider()
st.caption("Seoul Tourist Map | 서울 관광 안내 프로젝트")

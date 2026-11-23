
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="ONE PIECE × MBTI",
    page_icon="🏴‍☠️",
    layout="centered"
)

# 제목
st.title("🏴‍☠️ ONE PIECE × MBTI")
st.subheader("나와 닮은 원피스 캐릭터는 누구일까?")
st.write(
    "나의 MBTI를 선택하고 원피스 캐릭터와 "
    "나에게 어울리는 미래의 진로를 찾아보자! ⚓"
)

st.divider()

# MBTI별 캐릭터 및 진로 데이터
mbti_data = {
    "ISTJ": {
        "character": "로브 루치",
        "emoji": "🐆",
        "description": "원칙과 규율을 중요하게 생각하며 맡은 일은 철저하게 수행하는 성격이야. 냉철하고 책임감이 강하며 계획적으로 행동하는 편이야.",
        "reason": "체계적이고 규칙을 중시하는 모습이 ISTJ의 특징과 닮았어.",
        "careers": [
            {
                "name": "경찰관 및 수사관",
                "major": "경찰행정학과, 법학과",
                "personality": "책임감이 강하고 규칙을 잘 지키며 논리적으로 문제를 해결하는 사람"
            },
            {
                "name": "회계사",
                "major": "회계학과, 경영학과",
                "personality": "꼼꼼하고 정확하며 숫자와 자료를 체계적으로 관리하는 사람"
            }
        ]
    },

    "ISFJ": {
        "character": "쵸파",
        "emoji": "🦌",
        "description": "다른 사람을 돕는 것을 좋아하고 따뜻한 마음을 가진 캐릭터야. 동료들을 소중하게 생각하고 맡은 역할에 최선을 다해.",
        "reason": "배려심과 책임감이 강한 모습이 ISFJ와 잘 어울려.",
        "careers": [
            {
                "name": "의료인",
                "major": "간호학과, 의예과, 의학과",
                "personality": "공감 능력이 뛰어나고 세심하며 다른 사람을 돕는 것을 좋아하는 사람"
            },
            {
                "name": "사회복지사",
                "major": "사회복지학과",
                "personality": "배려심이 많고 인내심이 있으며 사람들과 소통하는 것을 좋아하는 사람"
            }
        ]
    },

    "INFJ": {
        "character": "니코 로빈",
        "emoji": "📚",
        "description": "지적 호기심이 풍부하고 깊이 생각하는 성격이야. 역사와 지식에 관심이 많으며 자신만의 가치관이 뚜렷해.",
        "reason": "깊은 사고력과 탐구심, 독립적인 성향이 INFJ와 닮았어.",
        "careers": [
            {
                "name": "심리상담사",
                "major": "심리학과, 상담학과",
                "personality": "상대방의 감정을 잘 이해하고 깊이 생각하며 공감할 수 있는 사람"
            },
            {
                "name": "역사학 연구원",
                "major": "사학과, 역사교육과",
                "personality": "호기심이 많고 자료를 분석하며 역사적 사실을 탐구하는 사람"
            }
        ]
    },

    "INTJ": {
        "character": "트라팔가 로",
        "emoji": "⚔️",
        "description": "냉철한 판단력과 전략적인 사고를 가진 캐릭터야. 목표를 이루기 위해 미리 계획하고 상황을 분석하는 능력이 뛰어나.",
        "reason": "독립적이고 분석적이며 전략을 중요하게 생각하는 점이 INTJ와 비슷해.",
        "careers": [
            {
                "name": "전략기획가",
                "major": "경영학과, 경제학과",
                "personality": "분석력이 뛰어나고 장기적인 계획을 세우는 것을 좋아하는 사람"
            },
            {
                "name": "소프트웨어 개발자",
                "major": "컴퓨터공학과, 소프트웨어학과",
                "personality": "논리적이고 집중력이 뛰어나며 복잡한 문제를 해결하는 사람"
            }
        ]
    },

    "ISTP": {
        "character": "롤로노아 조로",
        "emoji": "⚔️",
        "description": "말보다는 행동으로 보여주는 실전형 캐릭터야. 혼자서 문제를 해결하는 것을 좋아하고 위기 상황에서도 침착한 편이야.",
        "reason": "독립적이고 실용적이며 행동력이 뛰어난 점이 ISTP와 닮았어.",
        "careers": [
            {
                "name": "기계공학 기술자",
                "major": "기계공학과, 메카트로닉스공학과",
                "personality": "기계를 다루는 것을 좋아하고 실습과 문제 해결에 강한 사람"
            },
            {
                "name": "요리사",
                "major": "조리학과, 호텔조리학과",
                "personality": "손재주가 좋고 집중력이 뛰어나며 직접 만들고 완성하는 것을 좋아하는 사람"
            }
        ]
    },

    "ISFP": {
        "character": "상디",
        "emoji": "🍳",
        "description": "요리 실력이 뛰어나고 다른 사람을 배려하는 따뜻한 마음을 가지고 있어. 자신만의 기술과 감각을 중요하게 생각해.",
        "reason": "섬세한 감각과 예술적인 표현력, 배려심이 ISFP와 잘 어울려.",
        "careers": [
            {
                "name": "셰프 및 파티시에",
                "major": "호텔조리학과, 제과제빵학과",
                "personality": "창의적이고 미적 감각이 뛰어나며 요리와 음식에 대한 열정이 있는 사람"
            },
            {
                "name": "디자이너",
                "major": "시각디자인학과, 산업디자인학과",
                "personality": "감각적이고 창의적이며 자신만의 아이디어를 표현하는 것을 좋아하는 사람"
            }
        ]
    },

    "INFP": {
        "character": "우솝",
        "emoji": "🎯",
        "description": "상상력이 풍부하고 감수성이 뛰어난 캐릭터야. 때로는 겁이 많지만 소중한 사람들을 위해 용기를 내는 따뜻한 마음을 가지고 있어.",
        "reason": "풍부한 상상력과 감수성, 자신만의 개성을 중요하게 생각하는 점이 INFP와 닮았어.",
        "careers": [
            {
                "name": "작가 및 웹툰 작가",
                "major": "문예창작학과, 만화애니메이션학과",
                "personality": "상상력이 풍부하고 자신의 생각과 감정을 창작물로 표현하는 사람"
            },
            {
                "name": "콘텐츠 기획자",
                "major": "미디어커뮤니케이션학과, 문화콘텐츠학과",
                "personality": "창의적이고 새로운 아이디어를 생각해 내는 것을 좋아하는 사람"
            }
        ]
    },

    "INTP": {
        "character": "베가펑크",
        "emoji": "🧠",
        "description": "과학과 기술에 대한 호기심이 엄청나게 많은 천재 과학자야. 새로운 원리를 탐구하고 기존의 틀을 깨는 아이디어를 만들어 내.",
        "reason": "논리적 사고와 지적 호기심, 독창적인 발상이 INTP의 특징과 닮았어.",
        "careers": [
            {
                "name": "과학자 및 연구원",
                "major": "물리학과, 화학과, 생명과학과",
                "personality": "탐구심이 강하고 논리적으로 생각하며 새로운 지식을 발견하는 것을 좋아하는 사람"
            },
            {
                "name": "데이터 분석가",
                "major": "통계학과, 데이터사이언스학과",
                "personality": "자료를 분석하고 논리적인 근거를 찾아내는 것을 좋아하는 사람"
            }
        ]
    },

    "ESTP": {
        "character": "포트거스 D. 에이스",
        "emoji": "🔥",
        "description": "행동력이 뛰어나고 자신감이 넘치는 캐릭터야. 새로운 상황에 빠르게 적응하고 직접 경험하면서 문제를 해결하는 편이야.",
        "reason": "활동적이고 도전적이며 순간적인 판단력이 뛰어난 점이 ESTP와 닮았어.",
        "careers": [
            {
                "name": "스포츠 지도자",
                "major": "체육학과, 스포츠과학과",
                "personality": "활동적이고 도전 정신이 강하며 사람들을 이끄는 것을 좋아하는 사람"
            },
            {
                "name": "사업가",
                "major": "경영학과, 창업학과",
                "personality": "추진력이 있고 새로운 기회를 빠르게 발견하며 실행하는 사람"
            }
        ]
    },

    "ESFP": {
        "character": "몽키 D. 루피",
        "emoji": "🍖",
        "description": "자유롭고 활발하며 친구들과 함께하는 것을 좋아해. 자신이 원하는 목표를 향해 거침없이 나아가고 주변 사람들에게 긍정적인 에너지를 전달해.",
        "reason": "활발한 에너지와 낙천적인 성격, 사람들과 어울리는 것을 좋아하는 점이 ESFP와 닮았어.",
        "careers": [
            {
                "name": "방송인 및 크리에이터",
                "major": "방송영상학과, 미디어커뮤니케이션학과",
                "personality": "표현력이 풍부하고 사람들과 소통하는 것을 즐기는 사람"
            },
            {
                "name": "이벤트 기획자",
                "major": "광고홍보학과, 이벤트학과",
                "personality": "활발하고 사교적이며 새로운 경험과 활동을 기획하는 것을 좋아하는 사람"
            }
        ]
    },

    "ENFP": {
        "character": "보아 행콕",
        "emoji": "💖",
        "description": "자신감이 넘치고 감정 표현이 풍부한 캐릭터야. 자신이 소중하게 생각하는 사람과 목표에 강한 애정을 보여줘.",
        "reason": "열정적이고 감정 표현이 풍부하며 자신만의 개성이 뚜렷한 점이 ENFP와 닮았어.",
        "careers": [
            {
                "name": "광고 및 마케팅 기획자",
                "major": "광고홍보학과, 경영학과",
                "personality": "창의적이고 아이디어가 풍부하며 사람들의 관심을 끄는 것을 좋아하는 사람"
            },
            {
                "name": "공연 및 문화 기획자",
                "major": "문화콘텐츠학과, 공연예술학과",
                "personality": "열정적이고 새로운 경험을 즐기며 다양한 사람들과 협력하는 사람"
            }
        ]
    },

    "ENTP": {
        "character": "프랑키",
        "emoji": "🔧",
        "description": "독창적인 아이디어와 뛰어난 창의력을 가진 캐릭터야. 새로운 것을 만드는 것을 즐기고 남들과 다른 방식으로 문제를 해결해.",
        "reason": "새로운 아이디어를 떠올리고 도전을 즐기는 모습이 ENTP와 닮았어.",
        "careers": [
            {
                "name": "제품 개발자",
                "major": "산업디자인학과, 기계공학과",
                "personality": "창의적이고 호기심이 많으며 새로운 제품을 만드는 것을 좋아하는 사람"
            },
            {
                "name": "창업가",
                "major": "경영학과, 창업학과",
                "personality": "도전 정신이 강하고 새로운 사업 아이디어를 생각하는 것을 좋아하는 사람"
            }
        ]
    },

    "ESTJ": {
        "character": "네펠타리 비비",
        "emoji": "👑",
        "description": "책임감이 강하고 공동체를 위해 행동하는 캐릭터야. 목표를 위해 적극적으로 노력하고 사람들을 이끄는 능력이 있어.",
        "reason": "책임감과 조직력, 목표를 이루려는 추진력이 ESTJ와 잘 어울려.",
        "careers": [
            {
                "name": "경영 관리자",
                "major": "경영학과, 행정학과",
                "personality": "조직적이고 책임감이 강하며 사람들을 효율적으로 이끄는 사람"
            },
            {
                "name": "공무원",
                "major": "행정학과, 정치외교학과",
                "personality": "성실하고 체계적이며 공공의 목표를 위해 일하는 것을 중요하게 생각하는 사람"
            }
        ]
    },

    "ESFJ": {
        "character": "나미",
        "emoji": "🍊",
        "description": "현실적인 판단력이 뛰어나고 동료들을 잘 챙기는 캐릭터야. 주변 상황을 꼼꼼하게 살피며 팀을 위해 적극적으로 행동해.",
        "reason": "사교성과 책임감, 주변 사람들을 챙기는 모습이 ESFJ와 닮았어.",
        "careers": [
            {
                "name": "호텔리어",
                "major": "호텔경영학과, 관광경영학과",
                "personality": "친절하고 사교적이며 사람들에게 좋은 서비스를 제공하는 것을 좋아하는 사람"
            },
            {
                "name": "교사",
                "major": "교육학과, 사범대학",
                "personality": "배려심이 있고 의사소통 능력이 뛰어나며 다른 사람의 성장을 돕는 사람"
            }
        ]
    },

    "ENFJ": {
        "character": "징베",
        "emoji": "🌊",
        "description": "신뢰감이 있고 책임감이 강하며 다른 사람들을 이끌어 주는 캐릭터야. 동료들을 배려하고 갈등 상황에서도 침착하게 행동해.",
        "reason": "공감 능력과 리더십, 공동체를 생각하는 마음이 ENFJ와 닮았어.",
        "careers": [
            {
                "name": "교육 전문가",
                "major": "교육학과, 교육심리학과",
                "personality": "공감 능력이 뛰어나고 다른 사람의 성장을 돕는 것을 좋아하는 사람"
            },
            {
                "name": "인사 관리자",
                "major": "경영학과, 심리학과",
                "personality": "소통 능력이 뛰어나고 갈등을 조정하며 사람들과 협력하는 사람"
            }
        ]
    },

    "ENTJ": {
        "character": "샹크스",
        "emoji": "🍷",
        "description": "강한 카리스마와 리더십을 가진 캐릭터야. 중요한 순간에 과감하게 결정을 내리고 자신이 중요하게 생각하는 가치를 지켜.",
        "reason": "결단력과 리더십, 목표를 향한 추진력이 ENTJ와 닮았어.",
        "careers": [
            {
                "name": "기업 CEO",
                "major": "경영학과, 경제학과",
                "personality": "리더십이 강하고 결단력이 있으며 조직의 목표를 이끌어 가는 사람"
            },
            {
                "name": "프로젝트 매니저",
                "major": "산업공학과, 경영학과",
                "personality": "계획을 세우고 문제를 해결하며 여러 사람과 협력하는 사람"
            }
        ]
    }
}

# MBTI 선택
st.subheader("🔍 나의 MBTI를 선택해 봐!")

mbti_list = list(mbti_data.keys())

selected_mbti = st.selectbox(
    "나의 MBTI는?",
    mbti_list,
    index=mbti_list.index("ISTJ")
)

# 결과 출력
if st.button("🏴‍☠️ 나의 원피스 캐릭터 확인하기", use_container_width=True):

    result = mbti_data[selected_mbti]

    st.divider()

    st.success(f"당신의 MBTI는 {selected_mbti}!")

    st.header(
        f"{result['emoji']} 당신과 닮은 캐릭터는?"
    )

    st.title(result["character"])

    st.write("### ✨ 캐릭터 성격 분석")
    st.write(result["description"])

    st.info(f"💡 **MBTI 선정 이유:** {result['reason']}")

    st.divider()

    st.header("🚀 나에게 어울리는 미래의 진로")

    st.write(
        "캐릭터의 성격과 MBTI 특징을 참고해 "
        "어울릴 만한 진로 두 가지를 추천했어!"
    )

    for i, career in enumerate(result["careers"], 1):

        st.subheader(
            f"🎯 추천 진로 {i}. {career['name']}"
        )

        st.write(
            f"🎓 **관련 학과:** {career['major']}"
        )

        st.write(
            f"🙋 **이런 사람에게 적합해:** "
            f"{career['personality']}"
        )

        st.divider()

    st.caption(
        "※ 원피스 캐릭터와 MBTI의 연결은 재미를 위한 "
        "비공식 해석이야. MBTI만으로 실제 성격이나 "
        "진로가 결정되는 것은 아니야!"
    )

# 하단 안내
st.write("")
st.caption("🏴‍☠️ ONE PIECE × MBTI | 나만의 해적단과 진로 찾기!")


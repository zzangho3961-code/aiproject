import streamlit as st
st.title('나의 첫 웹 서비스 만들기!')
a=st.text_input('이름을 입력해주세요!')
b=st.selectbox('종하하는 음식을 선택해 주세요!',['치킨','피자','족발'])
if st.button('인사말 생성'):
st.write('반갑습니다!')
st.info(a+'문장호 왕자님 안녕하세요!')
st.warning(b+'를 선호하시는군요! 저도 좋아합니다')
st.error('제가 편히 모시겠습니다!')
st.balloons()

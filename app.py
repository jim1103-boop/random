import random
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍱")

# 제목 및 설명
st.title("🍱 오늘의 점심 메뉴 추천기")
st.write("버튼을 눌러 오늘 점심 메뉴를 결정해 보세요!")

# 추천할 메뉴 리스트 (원하는 메뉴를 자유롭게 추가/수정하세요)
lunch_menus = [
    "김치찌개",
    "된장찌개",
    "제육볶음",
    "돈가스",
    "초밥",
    "짜장면",
    "짬뽕",
    "쌀국수",
    "햄버거",
    "파스타",
    "비빔밥",
    "국밥",
    "샌드위치",
    "마라탕",
    "칼국수",
]

# 구분선
st.divider()

# 버튼 생성 및 클릭 이벤트 처리
if st.button("🎲 오늘의 메뉴 추천받기", use_container_width=True):
    # 리스트에서 랜덤으로 1개 선택
    selected_menu = random.choice(lunch_menus)

    # 결과 출력
    st.success(f"오늘의 추천 메뉴는 **{selected_menu}**입니다! 🎉")
    st.balloons()  # 축하 풍선 효과

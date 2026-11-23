import pandas as pd
import streamlit as st

# 1. 시작: 페이지 기본 설정
st.set_page_config(page_title="중화 반응 탐구 시뮬레이터", page_icon="🧪", layout="centered")

# 2. 리스트 선언: 선택하지 않은 이온의 개수(1~10개) 리스트로 정의
unselected_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# 함수(def) 및 조건 판단(if-elif-else) 정의
def calculate(h: int, oh: int) -> tuple[int, str]:
    """수소 이온(h)과 수산화 이온(oh) 개수를 받아 물 분자 수와 액성을 리턴"""
    if h > oh:
        water = oh
        acidity = "🔴 산성"
    elif h < oh:
        water = h
        acidity = "🔵 염기성"
    else:
        water = h
        acidity = "🟢 중성"
    return water, acidity


# 이온 선택 버튼 스타일 설정
st.markdown(
    """
<style>
div[data-testid="column"] button {
    height: 75px;
    font-size: 20px !important;
    font-weight: bold !important;
    border-radius: 14px !important;
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("🧪 산·염기 중화 반응 탐구 시뮬레이터")
st.latex(r"\text{H}^+ + \text{OH}^- \longrightarrow \text{H}_2\text{O}")

if "selected_ion" not in st.session_state:
    st.session_state.selected_ion = "수소 이온 (H⁺)"

# 3. 입력받기: 수소/수산화 이온 선택 및 슬라이더로 이온 수 입력(1~10)
with st.container(border=True):
    st.markdown("##### 1️⃣ 기준 이온 선택")
    col1, col2 = st.columns(2)
    is_h = st.session_state.selected_ion == "수소 이온 (H⁺)"

    if col1.button("🔴 수소 이온 (H⁺)", use_container_width=True, type="primary" if is_h else "secondary"):
        st.session_state.selected_ion = "수소 이온 (H⁺)"
        st.rerun()

    if col2.button("🔵 수산화 이온 (OH⁻)", use_container_width=True, type="primary" if not is_h else "secondary"):
        st.session_state.selected_ion = "수산화 이온 (OH⁻)"
        st.rerun()

    st.write("")
    st.markdown("##### 2️⃣ 기준 이온 개수 선택 (1 ~ 10개)")
    input_count = st.slider("이온 개수", 1, 10, 5, label_visibility="collapsed")

    st.write("")
    clicked = st.button("🔍 알아보기", type="primary", use_container_width=True)

# 4. 버튼 클릭 시: 리스트를 순회하며 calculate(h, oh) 실행
if clicked:
    results = []
    other_ion_col = "OH⁻" if is_h else "H⁺"

    for other_count in unselected_list:
        if is_h:
            h = input_count
            oh = other_count
        else:
            h = other_count
            oh = input_count

        # 함수 실행 및 결과 받기
        water, acidity = calculate(h, oh)

        results.append({
            other_ion_col: other_count,
            "생성된 물 분자 수": water,
            "혼합 용액의 액성": acidity,
        })

    # 5. 출력: 표 형태로 구성하여 화면에 출력
    df = pd.DataFrame(results)

    st.write("")
    with st.container(border=True):
        st.subheader(f"📊 실험 결과 ({st.session_state.selected_ion} {input_count}개 기준)")

        m1, m2, m3 = st.columns(3)
        m1.metric("기준 이온 수", f"{input_count}개")
        m2.metric("최대 생성 물 분자", f"{df['생성된 물 분자 수'].max()}개")
        m3.metric(f"중화점 (필요한 {other_ion_col})", f"{input_count}개")

        st.divider()

        tab1, tab2 = st.tabs(["📋 반응 데이터 표", "📈 물 분자 생성량 그래프"])

        with tab1:
            st.dataframe(df, use_container_width=True, hide_index=True)

        with tab2:
            st.caption(f"넣어준 {other_ion_col} 개수에 따른 생성된 물 분자(H₂O) 수 변화")
            chart_data = df.set_index(other_ion_col)[["생성된 물 분자 수"]]
            st.line_chart(chart_data)
            st.info(f"💡 **{other_ion_col}가 {input_count}개**일 때 완전히 중화되며, 이후에는 기준 이온이 모두 소모되어 물 분자 수가 더 이상 증가하지 않습니다.")

import pandas as pd
import streamlit as st

st.set_page_config(page_title="중화 반응 탐구 시뮬레이터", page_icon="🧪", layout="centered")


# 1. 핵심 중화 반응 계산 함수 (사용자 설계 로직)
def calculate(h: int, oh: int) -> tuple[int, str]:
    """수소 이온(h)과 수산화 이온(oh) 개수를 받아 생성된 물 분자 수와 액성을 반환합니다."""
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


# 이온 선택 버튼 스타일
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

# 상단 헤더 및 화학 반응식 안내
st.title("🧪 산·염기 중화 반응 탐구 시뮬레이터")
st.latex(r"\text{H}^+ + \text{OH}^- \longrightarrow \text{H}_2\text{O}")

if "selected_ion" not in st.session_state:
    st.session_state.selected_ion = "수소 이온 (H⁺)"

# 2. 실험 조건 설정 카드
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
    st.markdown("##### 2️⃣ 기준 이온 개수 설정 (0 ~ 10개)")
    input_count = st.slider("이온 개수", 0, 10, 5, label_visibility="collapsed")

    st.write("")
    clicked = st.button("🔍 실험 결과 알아보기", type="primary", use_container_width=True)

# 3. 실험 결과 분석 영역
if clicked:
    results = []
    other_ion_col = "OH⁻" if is_h else "H⁺"

    for other_count in range(1, 11):
        h = input_count if is_h else other_count
        oh = other_count if is_h else input_count
        water, acidity = calculate(h, oh)

        results.append({
            other_ion_col: other_count,
            "생성된 물 분자 수": water,
            "혼합 용액의 액성": acidity,
        })

    df = pd.DataFrame(results)

    st.write("")
    with st.container(border=True):
        st.subheader(f"📊 실험 결과 ({st.session_state.selected_ion} {input_count}개 기준)")

        # 상단 핵심 지표 요약 (중화점 & 최대 물 분자 수)
        m1, m2, m3 = st.columns(3)
        m1.metric("기준 이온 수", f"{input_count}개")
        m2.metric("최대 생성 물 분자", f"{df['생성된 물 분자 수'].max()}개")
        neutral_point = f"{input_count}개" if 1 <= input_count <= 10 else "없음 (0개)"
        m3.metric("중화점 (필요한 " + other_ion_col + ")", neutral_point)

        st.divider()

        # 탭(Tab)으로 데이터 표와 그래프를 깔끔하게 분리하여 제공
        tab1, tab2 = st.tabs(["📋 반응 데이터 표", "📈 물 분자 생성량 그래프"])

        with tab1:
            st.dataframe(df, use_container_width=True, hide_index=True)

        with tab2:
            st.caption(f"넣어준 {other_ion_col} 개수에 따른 생성된 물 분자(H₂O) 수 변화")
            chart_data = df.set_index(other_ion_col)[["생성된 물 분자 수"]]
            st.line_chart(chart_data)
            if 1 <= input_count <= 10:
                st.info(f"💡 **{other_ion_col}가 {input_count}개**일 때 완전히 중화되며, 이후에는 기준 이온이 모두 소모되어 물 분자 수가 더 이상 증가하지 않습니다.")

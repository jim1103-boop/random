import pandas as pd
import streamlit as st


# 1. 계획하신 calculate(h, oh) 함수
def calculate(h, oh):
    if h > oh:
        water = oh
        acidity = "산성"
    elif h < oh:
        water = h
        acidity = "염기성"
    elif h == oh:
        water = h
        acidity = "중성"
    return water, acidity


# 이온 선택 버튼만 큼직하게 키우는 CSS 스타일
st.markdown(
    """
<style>
div[data-testid="column"] div.stButton > button {
    height: 80px;
    font-size: 22px;
    font-weight: bold;
    border-radius: 12px;
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("🧪 중화 반응 계산기")

# 선택 상태를 기억하기 위한 session_state 초기화
if "selected_ion" not in st.session_state:
    st.session_state.selected_ion = "수소 이온 (H⁺)"

# 2. 이온 선택 (큼직한 네모 버튼)
st.write("### 1. 기준이 될 이온을 선택하세요")
col1, col2 = st.columns(2)

with col1:
    btn_type1 = (
        "primary"
        if st.session_state.selected_ion == "수소 이온 (H⁺)"
        else "secondary"
    )
    if st.button("🔴 수소 이온 (H⁺)", use_container_width=True, type=btn_type1):
        st.session_state.selected_ion = "수소 이온 (H⁺)"
        st.rerun()

with col2:
    btn_type2 = (
        "primary"
        if st.session_state.selected_ion == "수산화 이온 (OH⁻)"
        else "secondary"
    )
    if st.button(
        "🔵 수산화 이온 (OH⁻)", use_container_width=True, type=btn_type2
    ):
        st.session_state.selected_ion = "수산화 이온 (OH⁻)"
        st.rerun()

# 3. 이온 개수 입력
st.write("### 2. 이온 개수를 입력하세요")
input_count = st.number_input(
    "개수 입력",
    min_value=1,
    max_value=20,
    value=5,
    step=1,
    label_visibility="collapsed",
)

st.write("")  # 여백 추가

# 4. [알아보기] 버튼을 눌렀을 때만 아래 계산 및 출력 실행
if st.button("🔍 알아보기", type="primary", use_container_width=True):
    unselected_list = list(range(1, 11))
    results = []

    for other_count in unselected_list:
        if st.session_state.selected_ion == "수소 이온 (H⁺)":
            h = input_count
            oh = other_count
        else:
            h = other_count
            oh = input_count

        water, acidity = calculate(h, oh)

        results.append({
            "수소 이온(H⁺) 수": h,
            "수산화 이온(OH⁻) 수": oh,
            "생성된 물 분자 수": water,
            "혼합 용액의 액성": acidity,
        })

    st.divider()
    st.write(
        f"### 📊 결과 ({st.session_state.selected_ion} {input_count}개 기준)"
    )
    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True, hide_index=True)

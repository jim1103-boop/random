import time
import altair as alt
import pandas as pd
import streamlit as st

# 1. 시작: 페이지 기본 설정
st.set_page_config(
    page_title="중화 반응 탐구 시뮬레이터", page_icon="🧪", layout="centered"
)

# 2. 리스트 선언: 선택하지 않은 이온의 개수(1~10개) 리스트로 정의
unselected_list = list(range(1, 11))


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


# 이온 선택 버튼 & 떨어지는 물방울(💧) 애니메이션 CSS
st.markdown(
    """
<style>
div[data-testid="column"] button {
    height: 75px;
    font-size: 20px !important;
    font-weight: bold !important;
    border-radius: 14px !important;
}

@keyframes dropFall {
    0% { transform: translateY(-10vh) scale(0.8); opacity: 1; }
    100% { transform: translateY(105vh) scale(1.2); opacity: 0; }
}
.water-drop {
    position: fixed;
    top: -5%;
    font-size: 28px;
    z-index: 9999;
    pointer-events: none;
    animation: dropFall 1.6s ease-in forwards;
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

    if col1.button(
        "🔴 수소 이온 (H⁺)",
        use_container_width=True,
        type="primary" if is_h else "secondary",
    ):
        st.session_state.selected_ion = "수소 이온 (H⁺)"
        st.rerun()

    if col2.button(
        "🔵 수산화 이온 (OH⁻)",
        use_container_width=True,
        type="primary" if not is_h else "secondary",
    ):
        st.session_state.selected_ion = "수산화 이온 (OH⁻)"
        st.rerun()

    st.write("")
    st.markdown("##### 2️⃣ 기준 이온 개수 선택 (1 ~ 10개)")
    input_count = st.slider(
        "이온 개수", 1, 10, 5, label_visibility="collapsed"
    )

    st.write("")
    clicked = st.button("🔍 알아보기", type="primary", use_container_width=True)

# 4. 버튼 클릭 시: 물방울 애니메이션 + calculate(h, oh) 실행
if clicked:
    # 게이지 바가 차오르는 짧은 반응 연출
    progress_bar = st.progress(0, text="🧪 H⁺와 OH⁻가 만나 물 분자를 생성하는 중...")
    for percent in range(0, 101, 25):
        time.sleep(0.1)
        progress_bar.progress(percent, text="🧪 H⁺와 OH⁻가 만나 물 분자를 생성하는 중...")
    progress_bar.empty()

    # 화면 위에서 파란 물방울(💧)들이 떨어지는 효과
    drops_html = "".join(
        f'<div class="water-drop" style="left:{left}%; animation-delay:{delay}s;">💧</div>'
        for left, delay in [
            (10, 0.0), (22, 0.15), (35, 0.05), (48, 0.2),
            (60, 0.1), (73, 0.25), (85, 0.05), (92, 0.18),
        ]
    )
    st.markdown(drops_html, unsafe_allow_html=True)
    st.toast("물(H₂O) 분자 생성 완료!", icon="💧")

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

    # 5. 출력: 표 및 인터랙티브 그래프 출력
    df = pd.DataFrame(results)

    st.write("")
    with st.container(border=True):
        st.subheader(
            f"📊 실험 결과 ({st.session_state.selected_ion} {input_count}개 기준)"
        )

        m1, m2, m3 = st.columns(3)
        m1.metric("기준 이온 수", f"{input_count}개")
        m2.metric("최대 생성 물 분자", f"{df['생성된 물 분자 수'].max()}개")
        m3.metric(f"중화점 (필요한 {other_ion_col})", f"{input_count}개")

        st.divider()

        tab1, tab2 = st.tabs(["📋 반응 데이터 표", "📈 물 분자 생성량 그래프"])

        with tab1:
            st.dataframe(df, use_container_width=True, hide_index=True)

        with tab2:
            st.caption(
                "그래프의 각 점을 누르거나 마우스를 올리면 혼합 용액의 액성을 확인할 수 있습니다."
            )

            line = (
                alt.Chart(df)
                .mark_line(color="#888888")
                .encode(
                    x=alt.X(
                        f"{other_ion_col}:Q",
                        scale=alt.Scale(domain=[1, 10]),
                        axis=alt.Axis(
                            tickMinStep=1, title=f"넣어준 {other_ion_col} 수 (개)"
                        ),
                    ),
                    y=alt.Y(
                        "생성된 물 분자 수:Q",
                        scale=alt.Scale(domain=[0, 10]),
                        axis=alt.Axis(
                            tickMinStep=1, title="생성된 물 분자 수 (개)"
                        ),
                    ),
                )
            )

            points = (
                alt.Chart(df)
                .mark_circle(size=140)
                .encode(
                    x=f"{other_ion_col}:Q",
                    y="생성된 물 분자 수:Q",
                    color=alt.Color(
                        "혼합 용액의 액성:N",
                        scale=alt.Scale(
                            domain=["🔴 산성", "🟢 중성", "🔵 염기성"],
                            range=["#FF4B4B", "#21C354", "#1C83E1"],
                        ),
                        legend=alt.Legend(title="액성"),
                    ),
                    tooltip=[
                        alt.Tooltip(
                            other_ion_col, title=f"{other_ion_col} 수 (개)"
                        ),
                        alt.Tooltip(
                            "생성된 물 분자 수", title="생성된 물 분자 수 (개)"
                        ),
                        alt.Tooltip(
                            "혼합 용액의 액성", title="혼합 용액의 액성"
                        ),
                    ],
                )
            )

            st.altair_chart(
                (line + points).interactive(), use_container_width=True
            )
            st.info(
                f"💡 **{other_ion_col}가 {input_count}개**일 때 중화점(🟢 중성)에 도달하며, 이후에는 기준 이온이 모두 소모되어 물 분자 수가 더 이상 증가하지 않습니다."
            )

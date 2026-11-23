import math
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


# 이온 선택 버튼 & 화면 전체로 퍼지는 물방울(💧) + 중화열(🔥) 애니메이션 CSS
st.markdown(
    """
<style>
div[data-testid="column"] button {
    height: 75px;
    font-size: 20px !important;
    font-weight: bold !important;
    border-radius: 14px !important;
}

/* 물방울과 불꽃이 화면 전체로 퍼지는 애니메이션 */
@keyframes fullScreenBurst {
    0% {
        transform: translate(-50%, -50%) scale(0.4);
        opacity: 1;
    }
    75% {
        opacity: 1;
    }
    100% {
        transform: translate(calc(-50% + var(--dx)), calc(-50% + var(--dy))) scale(1.8);
        opacity: 0;
    }
}

.reaction-burst {
    position: fixed;
    left: 50%;
    top: 50%;
    font-size: 40px;
    z-index: 9999;
    pointer-events: none;
    animation: fullScreenBurst 1.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* 중화열로 인해 화면 전체가 잠깐 따뜻하게 붉어졌다 식는 열기 파동 */
@keyframes heatWave {
    0% {
        opacity: 0;
    }
    30% {
        opacity: 1;
    }
    100% {
        opacity: 0;
    }
}

.heat-overlay {
    position: fixed;
    inset: 0;
    background: radial-gradient(circle at center, rgba(255, 87, 34, 0.35) 0%, rgba(255, 152, 0, 0.15) 55%, transparent 100%);
    z-index: 9998;
    pointer-events: none;
    animation: heatWave 1.8s ease-out forwards;
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("🧪 산·염기 중화 반응 탐구 시뮬레이터")
st.latex(r"\text{H}^+ + \text{OH}^- \longrightarrow \text{H}_2\text{O} + \text{열(중화열)}")

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

# 4. 버튼 클릭 시: 게이지 100% 완료 후 물방울(💧)과 중화열(🔥)이 화면 전체로 퍼짐
if clicked:
    progress_bar = st.progress(0, text="🧪 H⁺와 OH⁻가 반응하는 중... (0%)")
    for percent in range(1, 101):
        time.sleep(0.012)
        progress_bar.progress(
            percent, text=f"🧪 H⁺와 OH⁻가 반응하는 중... ({percent}%)"
        )

    time.sleep(0.2)
    progress_bar.empty()

    # 화면 전체에 따뜻한 열기 배경(heat-overlay) + 물방울(💧)과 열(🔥) 입자 36개 확산
    burst_divs = ['<div class="heat-overlay"></div>']
    for ring_idx, (count, dist_x, dist_y, delay) in enumerate([
        (10, 22, 22, 0.0),    # 안쪽 원
        (12, 38, 38, 0.08),   # 중간 원
        (14, 55, 55, 0.15),   # 바깥쪽 큰 원
    ]):
        for i in range(count):
            angle = (2 * math.pi / count) * i + (ring_idx * 0.3)
            dx = f"{math.cos(angle) * dist_x:.1f}vw"
            dy = f"{math.sin(angle) * dist_y:.1f}vh"
            # 물방울(💧)과 열(🔥)이 번갈아 가며 퍼짐
            icon = "💧" if i % 2 == 0 else "🔥"
            burst_divs.append(
                f'<div class="reaction-burst" style="--dx:{dx}; --dy:{dy}; animation-delay:{delay}s;">{icon}</div>'
            )

    st.markdown("".join(burst_divs), unsafe_allow_html=True)
    st.toast("중화 반응 완료! 물(H₂O) 분자와 중화열이 발생했습니다.", icon="🔥")

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
                        scale=alt.Scale(domain=(1, 10)),
                        axis=alt.Axis(
                            tickMinStep=1, title=f"넣어준 {other_ion_col} 수 (개)"
                        ),
                    ),
                    y=alt.Y(
                        "생성된 물 분자 수:Q",
                        scale=alt.Scale(domain=(0, 10)),
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
                f"💡 **{other_ion_col}가 {input_count}개**일 때 중화점(🟢 중성)에 도달하며, 중화열 발생량도 최대가 됩니다."
            )

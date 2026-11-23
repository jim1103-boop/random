import pandas as pd
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="중화 반응 시뮬레이터", page_icon="🧪")

st.title("🧪 산·염기 중화 반응 시뮬레이터")
st.write(
    "기준 이온의 개수를 입력하면, 반대 이온(1개~10개)과 반응했을 때 생성되는 **물 분자 수**와 **혼합 용액의 액성**을 계산합니다."
)

st.divider()

# 1. 사용자 입력 영역
col1, col2 = st.columns(2)

with col1:
    ion_type = st.radio(
        "기준 이온 종류를 선택하세요:", ("수소 이온 (H⁺)", "수산화 이온 (OH⁻)")
    )

with col2:
    ion_count = st.number_input(
        "기준 이온의 개수를 입력하세요:", min_value=1, max_value=20, value=5, step=1
    )

# 반대 이온 이름 설정
opposite_ion = (
    "수산화 이온 (OH⁻)" if ion_type == "수소 이온 (H⁺)" else "수소 이온 (H⁺)"
)

st.subheader(
    f"📊 {ion_type} {ion_count}개에 {opposite_ion}을 섞었을 때의 변화"
)

# 2. 데이터 계산 (반대 이온 1개 ~ 10개)
results = []

for opp_count in range(1, 11):
    # 물 분자 수는 두 이온 중 적은 쪽의 개수만큼 생성됨
    water_molecules = min(ion_count, opp_count)

    # 액성 판별
    if ion_count == opp_count:
        acidity = "중성 🟢"
        remaining = "없음 (0개)"
    elif ion_count > opp_count:
        acidity = "산성 🔴" if ion_type == "수소 이온 (H⁺)" else "염기성 🔵"
        remaining = f"{ion_type.split()[0]} {ion_count - opp_count}개"
    else:
        acidity = "염기성 🔵" if ion_type == "수소 이온 (H⁺)" else "산성 🔴"
        remaining = f"{opposite_ion.split()[0]} {opp_count - ion_count}개"

    results.append({
        f"넣어준 {opposite_ion} 수": f"{opp_count}개",
        "생성된 물(H₂O) 분자 수": water_molecules,
        "혼합 용액의 액성": acidity,
        "반응 후 남은 이온": remaining,
    })

df = pd.DataFrame(results)

# 3. 결과 출력 (표 & 그래프)
st.dataframe(df, use_container_width=True, hide_index=True)

st.subheader("📈 넣어준 이온 수에 따른 물 분자 생성량")
# 그래프용 데이터프레임 인덱스 설정
chart_df = df.set_index(f"넣어준 {opposite_ion} 수")[["생성된 물(H₂O) 분자 수"]]
st.bar_chart(chart_df)

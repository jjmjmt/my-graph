import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 기본 설정 (와이드 레이아웃 적용)
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간", page_icon="🎬", layout="wide"
)


# 데이터 로드 및 전처리 (캐싱을 통한 성능 최적화)
@st.cache_data
def load_data():
    """GitHub에서 박스오피스 CSV 데이터를 불러오고 날짜 형식을 변환하는 함수"""
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

    # CSV 데이터 읽기 (날짜 열을 문자열로 읽어서 처리)
    df = pd.read_csv(url, dtype={"날짜": str, "영화코드": str})

    # 날짜 열(YYYYMMDD 8자리 문자열)을 datetime 객체로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")

    return df


def main():
    st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
    st.caption(
        "박스오피스 데이터를 바탕으로 시간에 따른 영화 데이터의 변화를 탐색합니다."
    )

    # 데이터 불러오기
    try:
        df = load_data()
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return

    st.markdown("---")

    # ==========================================
    # 구역 1: 특정 영화의 날짜별 일관객 변화
    # ==========================================
    st.header("1. 영화별 일일 관객수 추이")

    # 드롭다운 선택을 위한 전체 영화 목록 추출 (영화명 기준 정렬)
    movie_list = sorted(df["영화명"].dropna().unique())

    # 영화 선택 드롭다운 (기본값 설정)
    selected_movie = st.selectbox(
        "조회할 영화를 선택하세요:",
        options=movie_list,
        index=0 if movie_list else None,
    )

    if selected_movie:
        # 선택한 영화의 데이터만 필터링 후 날짜순 정렬
        movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")

        # Plotly 선 그래프 생성
        fig = px.line(
            movie_df,
            x="날짜",
            y="일관객",
            title=f"'{selected_movie}' 날짜별 일일 관객수 변화",
            labels={"날짜": "날짜", "일관객": "일일 관객수(명)"},
            markers=True,  # 데이터 지점에 마커 표시
        )

        # 마우스오버(Hover) 툴팁 포맷 및 스타일 설정
        fig.update_traces(
            hovertemplate="<b>날짜</b>: %{x|%Y-%m-%d}<br><b>일관객수</b>: %{y:,}명<extra></extra>"
        )

        # 레이아웃 미세 조정
        fig.update_layout(
            xaxis_title="날짜",
            yaxis_title="관객수(명)",
            hovermode="x unified",
        )

        # Streamlit에 그래프 출력
        st.plotly_chart(fig, use_container_width=True)

        # 인사이트 문구 작성 영역 (작성용 템플릿)
        st.info(
            "💡 **이 그래프로 알 수 있는 것**\n\n"
            "여기에 분석 내용을 작성하세요. (예: 개봉 초기에 관객수가 집중되었는지, 주말에 반응이 크게 오르는지 등)"
        )

    st.markdown("---")

    # ==========================================
    # 구역 2: 추후 그래프 추가 영역 (예시 구조)
    # ==========================================
    st.header("2. [추가 예정] 시간에 따른 그래프 구역")
    st.text(
        "이곳에 두 번째 그래프(예: 상위 N개 영화의 누적관객 추이 비교 등)가 추가될 수 있습니다."
    )

    # st.info("💡 **이 그래프로 알 수 있는 것**\n\n여기에 분석 내용을 작성하세요.")


if __name__ == "__main__":
    main()
  
# ==========================================
    # 구역 2: 기간 내 관객수 TOP 5 영화 비교
    # ==========================================
    st.header("2. 관객수 TOP 5 영화의 일일 관객수 비교")

    # 전체 기간 동안 일관객 합계가 가장 높은 영화 상위 5개 추출
    top5_movies = (
        df.groupby("영화명")["일관객"]
        .sum()
        .nlargest(5)
        .index.tolist()
    )

    # 상위 5개 영화 데이터만 필터링 후 날짜순 정렬
    top5_df = df[df["영화명"].isin(top5_movies)].sort_values("날짜")

    # Plotly 다중 선 그래프 생성 (color 옵션으로 영화별 구분)
    fig2 = px.line(
        top5_df,
        x="날짜",
        y="일관객",
        color="영화명",
        title="기간 내 관객수 TOP 5 영화의 일일 관객수 추이",
        labels={
            "날짜": "날짜",
            "일관객": "일일 관객수(명)",
            "영화명": "영화 제목",
        },
    )

    # 마우스오버 툴팁 포맷 및 레이아웃 설정
    fig2.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>날짜: %{x|%Y-%m-%d}<br>관객수: %{y:,}명<extra></extra>"
    )

    fig2.update_layout(
        xaxis_title="날짜",
        yaxis_title="관객수(명)",
        hovermode="x unified",
        legend_title_text="영화 제목 (클릭 시 켜기/끄기)",
    )

    # Streamlit 화면에 그래프 출력
    st.plotly_chart(fig2, use_container_width=True)

    # 인사이트 문구 작성 영역
    st.info(
        "💡 **이 그래프로 알 수 있는 것**\n\n"
        "여기에 분석 내용을 작성하세요. (예: TOP 5 영화들의 흥행 시기가 겹치는지, 최전성기 관객수 차이는 어느 정도인지 등)"
    )

st.markdown("---")

    # ==========================================
    # 구역 3: 날짜별 10위권 일관객 합계 (영역 그래프)
    # ==========================================
    st.header("3. 날짜별 TOP 10 총 관객수 추이")

    # 날짜별 일관객 합계 계산
    daily_total = df.groupby("날짜")["일관객"].sum().reset_index()

    # 관객수가 가장 컸던 상위 3일 추출
    top3_days = daily_total.nlargest(3, "일관객")

    # Plotly 영역 그래프(Area Chart) 생성
    fig3 = px.area(
        daily_total,
        x="날짜",
        y="일관객",
        title="날짜별 TOP 10 일일 총 관객수 변화",
        labels={"날짜": "날짜", "일관객": "총 관객수(명)"},
    )

    # 상위 3일에 주석(Annotation) 추가
    for idx, row in top3_days.iterrows():
        date_str = row["날짜"].strftime("%Y-%m-%d")
        fig3.add_annotation(
            x=row["날짜"],
            y=row["일관객"],
            text=f"🏆 Top {top3_days.index.get_loc(idx) + 1}<br>{date_str}<br>({row['일관객']:,}명)",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#EF553B",
            ax=0,
            ay=-40,
            bgcolor="#FFFFFF",
            bordercolor="#EF553B",
            borderwidth=1,
            borderpad=4,
            opacity=0.9,
        )

    # Hover 포맷 및 레이아웃 설정
    fig3.update_traces(
        hovertemplate="<b>날짜</b>: %{x|%Y-%m-%d}<br><b>TOP 10 총 관객수</b>: %{y:,}명<extra></extra>"
    )

    fig3.update_layout(
        xaxis_title="날짜",
        yaxis_title="총 관객수(명)",
        hovermode="x unified",
    )

    # Streamlit에 그래프 출력
    st.plotly_chart(fig3, use_container_width=True)

    # 인사이트 문구 작성 영역
    st.info(
        "💡 **이 그래프로 알 수 있는 것**\n\n"
        "여기에 분석 내용을 작성하세요. (예: 연중 극장가 최고 성수기 시점, 명절/연휴 시즌의 관객 폭발력 등)"
    )

st.markdown("---")

    # ==========================================
    # 구역 4: 기간 내 관객수 TOP 10 (가로 막대그래프)
    # ==========================================
    st.header("4. 기간 내 누적 관객수 TOP 10")

    # 영화별로 일관객 합계 및 10위권 진입 일수(데이터 행 수) 집계
    top10_summary = (
        df.groupby("영화명")
        .agg(총관객수=("일관객", "sum"), 진입일수=("날짜", "count"))
        .reset_index()
    )

    # 총 관객수 기준 상위 10개 영화 추출
    top10_df = top10_summary.nlargest(10, "총관객수")

    # 관객수가 많은 영화가 그래프 위에 오도록 정렬 (Plotly y축은 아래에서 위로 그려짐)
    top10_df = top10_df.sort_values("총관객수", ascending=True)

    # Plotly 가로 막대그래프(px.bar orientation="h") 생성
    fig4 = px.bar(
        top10_df,
        x="총관객수",
        y="영화명",
        orientation="h",
        title="기간 내 총 관객수 TOP 10 영화",
        labels={"총관객수": "총 관객수(명)", "영화명": "영화 제목"},
        custom_data=["진입일수"],  # Hover 툴팁에 활용할 추가 데이터
        text_auto=",.0f",  # 막대 끝에 숫자 표시 (천 단위 쉼표)
    )

    # Hover 툴팁 설정 (마우스 올렸을 때 10위권 진입 일수 표시)
    fig4.update_traces(
        hovertemplate="<b>%{y}</b><br>총 관객수: %{x:,}명<br>10위권 진입 일수: %{customdata[0]}일<extra></extra>",
        textposition="outside",
    )

    fig4.update_layout(
        xaxis_title="총 관객수(명)",
        yaxis_title="영화 제목",
    )

    # Streamlit에 그래프 출력
    st.plotly_chart(fig4, use_container_width=True)

    # 인사이트 문구 작성 영역
    st.info(
        "💡 **이 그래프로 알 수 있는 것**\n\n"
        "여기에 분석 내용을 작성하세요. (예: 진입 일수가 적음에도 단기간에 관객을 많이 모은 영화, 롱런한 영화 비교 등)"
    )

st.markdown("---")

    # ==========================================
    # 구역 5: 월×요일별 일관객 합계 (히트맵)
    # ==========================================
    st.header("5. 월 및 요일별 관객수 분포")

    # 월, 요일 정보 추출
    df_heatmap = df.copy()
    df_heatmap["월"] = df_heatmap["날짜"].dt.month
    df_heatmap["요일_num"] = df_heatmap["날짜"].dt.dayofweek  # 0:월 ~ 6:일

    # 요일 이름을 월요일부터 일요일 순서로 매핑
    weekday_map = {
        0: "월요일",
        1: "화요일",
        2: "수요일",
        3: "목요일",
        4: "금요일",
        5: "토요일",
        6: "일요일",
    }
    df_heatmap["요일"] = df_heatmap["요일_num"].map(weekday_map)

    # 월과 요일별 일관객 합계 집계 및 피벗 테이블 생성
    heatmap_data = df_heatmap.pivot_table(
        index="월", columns="요일", values="일관객", aggfunc="sum"
    ).fillna(0)

    # 요일 순서를 월요일~일요일로 고정
    weekday_order = [
        "월요일",
        "화요일",
        "수요일",
        "목요일",
        "금요일",
        "토요일",
        "일요일",
    ]
    heatmap_data = heatmap_data.reindex(columns=weekday_order)

    # Plotly 히트맵 생성 (색이 진할수록 관객수 증가 - Viridis 컬러스케일)
    fig5 = px.imshow(
        heatmap_data,
        labels=dict(x="요일", y="월", color="총 관객수(명)"),
        x=weekday_order,
        y=[f"{m}월" for m in heatmap_data.index],
        color_continuous_scale="Viridis",
        title="월 및 요일별 일관객 합계 히트맵",
        aspect="auto",
    )

    # Hover 툴팁 포맷 설정
    fig5.update_traces(
        hovertemplate="<b>%{y} %{x}</b><br>총 관객수: %{z:,}명<extra></extra>"
    )

    fig5.update_layout(
        xaxis_title="요일",
        yaxis_title="월",
    )

    # Streamlit에 그래프 출력
    st.plotly_chart(fig5, use_container_width=True)

    # 인사이트 문구 작성 영역
    st.info(
        "💡 **이 그래프로 알 수 있는 것**\n\n"
        "여기에 분석 내용을 작성하세요. (예: 특정 월의 주말 집중도, 평일 관객수가 가장 높은 달 등)"
    )

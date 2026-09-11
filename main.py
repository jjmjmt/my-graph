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


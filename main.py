import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("---")

# 2. 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # '날짜' 열을 문자열로 바꾼 뒤 진짜 날짜형(datetime)으로 변환
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 데 실패했습니다: {e}")
    st.stop()


# ==========================================
# 구역 1: 영화별 일관객 변화 (선 그래프)
# ==========================================
st.header("📈 1. 영화별 일관객수 변화 추이")
st.markdown("선택한 영화의 일별 관객수 변화를 시간 순서대로 확인합니다.")

# 영화 선택 드롭다운 (가나다순 정렬)
movie_list = sorted(df['영화명'].unique())
selected_movie = st.selectbox("🎥 분석할 영화를 선택하세요", movie_list)

# 선택한 영화 데이터 필터링 및 날짜순 정렬
movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')

if not movie_df.empty:
    # 플롯리 선 그래프 생성
    fig = px.line(
        movie_df, 
        x='날짜', 
        y='일관객',
        title=f"[{selected_movie}] 일관객수 변화",
        labels={'날짜': '상영 날짜', '일관객': '일일 관객 수(명)'},
        markers=True # 데이터 포인트 표시
    )
    
    # 마우스 오버(호버) 툴팁 설정
    fig.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>관객수:</b> %{y:,}명<extra></extra>"
    )
    
    # 레이아웃 조정 (천 단위 콤마 등)
    fig.update_layout(yaxis_tickformat=",d")
    
    # 스트림릿에 그래프 출력
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("해당 영화의 데이터가 없습니다.")

# 인사이트 기록 구역
st.info("💡 **이 그래프로 알 수 있는 것:**여기에 그래프를 보고 발견한 유의미한 분석 내용을 한 문장으로 적어주세요.")


# ==========================================
# 구역 2: (향후 추가될 그래프 자리)
# ==========================================
st.markdown("---")
st.header("⏳ 2. 다음 분석 그래프 (준비 중)")
st.caption("새로운 시간 관련 영화 분석 그래프가 여기에 추가될 예정입니다.")

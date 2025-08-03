import streamlit as st
import json
import os
from fair_trade_rag import FairTradeRAG
from law_data_collector import LawDataCollector

# Streamlit Cloud에서 secrets 사용
if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# 페이지 설정
st.set_page_config(
    page_title="공정거래 법령 분석 시스템",
    page_icon="⚖️",
    layout="wide"
)

# 사이드바
st.sidebar.title("⚖️ 공정거래 법령 분석")
st.sidebar.markdown("---")

# 메인 기능 선택
page = st.sidebar.selectbox(
    "기능 선택",
    ["🏠 홈", "📊 데이터 수집", "🔍 케이스 분석", "📋 법령 요약", "⚙️ 설정"]
)

def home_page():
    """홈 페이지"""
    st.title("공정거래 법령 분석 시스템")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 시스템 개요")
        st.markdown("""
        이 시스템은 공정거래 관련 법령들을 분석하여 
        기업의 공정거래 케이스를 평가하는 AI 도구입니다.
        
        **주요 기능:**
        - 📊 법령 데이터 수집 및 저장
        - 🔍 케이스별 법적 분석
        - 📋 법령 요약 및 설명
        - ⚖️ 위반 가능성 평가
        """)
    
    with col2:
        st.subheader("📈 지원 법령")
        st.markdown("""
        **핵심 법령:**
        - 공정거래법
        - 하도급법
        - 상생협력법
        
        **관련 법령:**
        - 독점규제 및 공정거래에 관한 법률
        - 하도급거래 공정화에 관한 법률
        - 대·중소기업 상생협력 촉진에 관한 법률
        """)
    
    st.markdown("---")
    
    # 시스템 상태 확인
    st.subheader("🔧 시스템 상태")
    
    # 데이터 파일 확인
    if os.path.exists("fair_trade_laws.json"):
        with open("fair_trade_laws.json", 'r', encoding='utf-8') as f:
            laws = json.load(f)
        st.success(f"✅ 법령 데이터 로드됨 ({len(laws)}개 법령)")
    else:
        st.warning("⚠️ 법령 데이터가 없습니다. '데이터 수집' 페이지에서 데이터를 수집해주세요.")
    
    # 벡터 DB 확인
    if os.path.exists("chroma_db"):
        st.success("✅ 벡터 데이터베이스 준비됨")
    else:
        st.warning("⚠️ 벡터 데이터베이스가 없습니다. '케이스 분석' 페이지에서 초기화해주세요.")

def data_collection_page():
    """데이터 수집 페이지"""
    st.title("📊 법령 데이터 수집")
    st.markdown("---")
    
    st.markdown("""
    국가법령정보센터에서 공정거래 관련 법령들을 수집합니다.
    """)
    
    if st.button("🚀 데이터 수집 시작", type="primary"):
        with st.spinner("법령 데이터를 수집하고 있습니다..."):
            try:
                collector = LawDataCollector()
                laws = collector.collect_fair_trade_laws()
                
                if laws:
                    collector.save_laws_to_file(laws)
                    st.success(f"✅ {len(laws)}개의 법령을 성공적으로 수집했습니다!")
                    
                    # 수집된 법령 목록 표시
                    st.subheader("📋 수집된 법령 목록")
                    for i, law in enumerate(laws, 1):
                        with st.expander(f"{i}. {law['title']}"):
                            st.write(f"**키워드:** {law.get('keyword', 'N/A')}")
                            st.write(f"**조문 수:** {len(law.get('articles', []))}")
                            st.write(f"**URL:** {law.get('url', 'N/A')}")
                else:
                    st.error("❌ 데이터 수집에 실패했습니다.")
                    
            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")

def case_analysis_page():
    """케이스 분석 페이지"""
    st.title("🔍 케이스 분석")
    st.markdown("---")
    
    # RAG 시스템 초기화
    try:
        rag = FairTradeRAG()
        st.success("✅ RAG 시스템이 준비되었습니다.")
    except Exception as e:
        st.error(f"❌ RAG 시스템 초기화 실패: {str(e)}")
        return
    
    # 법령 데이터 확인
    laws = rag.load_law_data()
    if not laws:
        st.warning("⚠️ 법령 데이터가 없습니다. 먼저 데이터를 수집해주세요.")
        return
    
    # 벡터 DB 초기화
    if st.button("🔄 벡터 데이터베이스 초기화"):
        with st.spinner("벡터 데이터베이스를 생성하고 있습니다..."):
            try:
                documents = rag.prepare_documents(laws)
                rag.create_vector_database(documents)
                st.success("✅ 벡터 데이터베이스가 생성되었습니다!")
            except Exception as e:
                st.error(f"❌ 벡터 데이터베이스 생성 실패: {str(e)}")
    
    st.markdown("---")
    
    # 케이스 입력
    st.subheader("📝 케이스 입력")
    
    # 예시 케이스들
    example_cases = {
        "하도급 대금 삭감": """
        A기업은 자동차 부품 제조업체로, B기업으로부터 하도급 작업을 받아왔습니다. 
        최근 B기업이 갑자기 하도급 대금을 30% 삭감하겠다고 통보했고, 
        계약서에는 "원청의 요청에 따라 단가 조정 가능"이라는 조항이 있습니다. 
        A기업은 이에 반대했지만 B기업은 "계약서에 명시되어 있다"며 강행하려고 합니다.
        """,
        "독점적 지위 남용": """
        대기업 C는 특정 시장에서 80% 이상의 점유율을 가지고 있습니다. 
        최근 C기업이 중소기업 D에게 "우리 제품만 사용하라"며 
        다른 업체 제품 사용을 금지하고, 이를 어길 경우 거래 중단을 위협하고 있습니다.
        """,
        "불공정 거래 조건": """
        대기업 E는 중소기업 F와 거래하면서 다음과 같은 조건을 제시했습니다:
        - 90일 후 지급 조건 (기존 30일에서 변경)
        - 품질 보증금 20% 예치 요구
        - 계약 해지 시 30일 전 통보
        F기업은 이러한 조건들이 너무 까다롭다고 생각합니다.
        """
    }
    
    selected_example = st.selectbox(
        "예시 케이스 선택 (선택사항):",
        ["직접 입력"] + list(example_cases.keys())
    )
    
    if selected_example != "직접 입력":
        case_description = st.text_area(
            "케이스 설명:",
            value=example_cases[selected_example],
            height=200
        )
    else:
        case_description = st.text_area(
            "케이스 설명:",
            placeholder="분석하고 싶은 공정거래 관련 케이스를 자세히 설명해주세요...",
            height=200
        )
    
    if st.button("🔍 분석 시작", type="primary") and case_description.strip():
        with st.spinner("케이스를 분석하고 있습니다..."):
            try:
                analysis_result = rag.analyze_case(case_description)
                
                st.subheader("📊 분석 결과")
                st.markdown(analysis_result)
                
                # 분석 결과 다운로드
                st.download_button(
                    label="📥 분석 결과 다운로드",
                    data=analysis_result,
                    file_name="공정거래_케이스_분석.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"❌ 분석 중 오류 발생: {str(e)}")

def law_summary_page():
    """법령 요약 페이지"""
    st.title("📋 법령 요약")
    st.markdown("---")
    
    try:
        rag = FairTradeRAG()
    except Exception as e:
        st.error(f"❌ RAG 시스템 초기화 실패: {str(e)}")
        return
    
    # 요약 옵션
    summary_type = st.radio(
        "요약 유형 선택:",
        ["전체 법령 요약", "특정 법령 요약"]
    )
    
    if summary_type == "특정 법령 요약":
        law_name = st.text_input(
            "법령명 입력:",
            placeholder="예: 공정거래법, 하도급법, 상생협력법"
        )
        
        if st.button("📋 요약 생성", type="primary") and law_name.strip():
            with st.spinner("법령을 요약하고 있습니다..."):
                try:
                    summary = rag.get_law_summary(law_name)
                    st.subheader(f"📋 {law_name} 요약")
                    st.markdown(summary)
                except Exception as e:
                    st.error(f"❌ 요약 생성 중 오류 발생: {str(e)}")
    
    else:
        if st.button("📋 전체 요약 생성", type="primary"):
            with st.spinner("전체 법령을 요약하고 있습니다..."):
                try:
                    summary = rag.get_law_summary()
                    st.subheader("📋 전체 법령 요약")
                    st.markdown(summary)
                except Exception as e:
                    st.error(f"❌ 요약 생성 중 오류 발생: {str(e)}")

def settings_page():
    """설정 페이지"""
    st.title("⚙️ 설정")
    st.markdown("---")
    
    st.subheader("🔑 OpenAI API 키 설정")
    
    # API 키 입력
    api_key = st.text_input(
        "OpenAI API 키:",
        type="password",
        help="OpenAI API 키를 입력하세요. 환경변수 OPENAI_API_KEY로도 설정 가능합니다."
    )
    
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        st.success("✅ API 키가 설정되었습니다.")
    
    st.markdown("---")
    
    st.subheader("🗂️ 데이터 관리")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ 법령 데이터 삭제"):
            if os.path.exists("fair_trade_laws.json"):
                os.remove("fair_trade_laws.json")
                st.success("✅ 법령 데이터가 삭제되었습니다.")
            else:
                st.warning("⚠️ 삭제할 법령 데이터가 없습니다.")
    
    with col2:
        if st.button("🗑️ 벡터 DB 삭제"):
            import shutil
            if os.path.exists("chroma_db"):
                shutil.rmtree("chroma_db")
                st.success("✅ 벡터 데이터베이스가 삭제되었습니다.")
            else:
                st.warning("⚠️ 삭제할 벡터 데이터베이스가 없습니다.")
    
    st.markdown("---")
    
    st.subheader("📊 시스템 정보")
    
    # 파일 상태 확인
    if os.path.exists("fair_trade_laws.json"):
        file_size = os.path.getsize("fair_trade_laws.json") / 1024  # KB
        st.info(f"📄 법령 데이터 파일: {file_size:.1f} KB")
    
    if os.path.exists("chroma_db"):
        st.info("📊 벡터 데이터베이스: 준비됨")
    else:
        st.warning("📊 벡터 데이터베이스: 없음")

# 페이지 라우팅
if page == "🏠 홈":
    home_page()
elif page == "📊 데이터 수집":
    data_collection_page()
elif page == "🔍 케이스 분석":
    case_analysis_page()
elif page == "📋 법령 요약":
    law_summary_page()
elif page == "⚙️ 설정":
    settings_page() 

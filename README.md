# ⚖️ 공정거래 법령 분석 시스템

AI를 활용한 공정거래 관련 법령 분석 및 케이스 평가 시스템입니다.

## 🌟 주요 기능

- **📊 법령 데이터 수집**: 국가법령정보센터에서 공정거래 관련 법령 자동 수집
- **🔍 케이스 분석**: AI를 통한 실제 사례의 법적 분석 및 위반 가능성 평가  
- **📋 법령 요약**: 복잡한 법령을 이해하기 쉽게 요약
- **⚖️ 전문가 수준 분석**: GPT를 활용한 상세한 법적 검토

## 🚀 라이브 데모

**배포된 웹사이트**: [여기에 Streamlit Cloud URL이 들어갑니다]

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **AI/ML**: OpenAI GPT-3.5, LangChain, ChromaDB
- **데이터 수집**: BeautifulSoup, Requests
- **임베딩**: Sentence Transformers

## 📋 지원 법령

- 독점규제 및 공정거래에 관한 법률 (공정거래법)
- 하도급거래 공정화에 관한 법률 (하도급법)  
- 대·중소기업 상생협력 촉진에 관한 법률 (상생협력법)

## 🔧 로컬 실행

### 필수 조건
- Python 3.8 이상
- OpenAI API 키

### 설치 및 실행
```bash
# 리포지토리 클론
git clone https://github.com/[사용자명]/fair-trade-law-analyzer.git
cd fair-trade-law-analyzer

# 패키지 설치
pip install -r requirements.txt

# 환경변수 설정 (PowerShell)
$env:OPENAI_API_KEY="your_api_key_here"

# 앱 실행
streamlit run fair_trade_app.py
```

## 📖 사용 방법

1. **데이터 수집**: "📊 데이터 수집" 페이지에서 법령 데이터 수집
2. **시스템 초기화**: "🔍 케이스 분석" 페이지에서 벡터 데이터베이스 초기화
3. **케이스 분석**: 실제 사례를 입력하여 AI 법령 분석 수행

## 🔐 보안

- API 키는 Streamlit Cloud Secrets로 안전하게 관리
- 개인정보나 민감한 데이터는 저장하지 않음

## 📝 라이선스

MIT License

## 👥 기여

이슈 및 풀 리퀘스트를 환영합니다!

## 📧 연락처

프로젝트 관련 문의: [soyeun.lee@sk.com]

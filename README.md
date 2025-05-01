# My RAGBot SaaS

설치 및 실행 가이드
my-ragbot-saas/
├── backend/                       # FastAPI 서버
│   ├── libs/                      # 🔧 공통 라이브러리 (RAG, 결제, 로깅 등)
│   │   ├── rag_lib/               # RAG 전용 모듈
│   │   ├── billing_lib/           # (추후) 결제 연동 모듈
│   │   └── analytics_lib/         # (추후) 사용 통계 모듈
│   │
│   ├── services/                  # 🧩 비즈니스 로직
│   │   ├── auth_service.py        # 회원가입·로그인
│   │   ├── site_service.py        # 사이트 등록·설치 코드 관리
│   │   ├── chat_service.py        # 채팅 흐름 제어, DB 저장 호출
│   │   ├── billing_service.py     # (추후) 과금 로직
│   │   └── analytics_service.py   # (추후) 통계 로직
│   │
│   ├── app/                       # FastAPI 앱 본체
│   │   ├── __init__.py
│   │   ├── main.py                # 앱 생성, CORS, StaticFiles, 라우터 포함
│   │   ├── config.py              # 설정 관리 (.env → pydantic Settings)
│   │   ├── models.py              # SQLAlchemy ORM (User, Site, Document, Chat…)
│   │   ├── schemas.py             # Pydantic 스키마 (요청·응답)
│   │   ├── crud.py                # 단순 CRUD 헬퍼 (UserCRUD, SiteCRUD…)
│   │   └── routes/                # 엔드포인트 모음
│   │       ├── auth.py            # /login, /register
│   │       ├── site.py            # /site, /site/{id}/settings
│   │       ├── chat.py            # /chat (위젯 연동)
│   │       ├── upload.py          # /site/{id}/upload (TXT → rag_lib.ingest)
│   │       └── widget.py          # 위젯 정적 파일 서빙
│   │
│   ├── widget/                    # 고객이 삽입할 파일 모음
│   │   ├── chatbot.js             # iframe 생성 스크립트
│   │   ├── chatbox.html           # iframe 내 UI + fetch 로직
│   │   └── chatbox.css            # 채팅창 스타일
│   │
│   ├── Dockerfile                 # 컨테이너 빌드 스크립트
│   ├── requirements.txt           # Python 패키지 목록
│   └── scripts/
│       └── init_db.py             # DB 생성·시드 스크립트
│
├── frontend/                      # 관리자 페이지 (Jinja2 + Tailwind)
│   ├── templates/
│   │   ├── base.html              # 전체 레이아웃
│   │   ├── login.html             # 로그인 폼
│   │   ├── dashboard.html         # 사이트 목록·키 복사
│   │   ├── settings.html          # 챗봇 세팅 (첫인사, 버튼 위치)
│   │   └── upload.html            # TXT 업로드 폼
│   └── static/
│       └── styles.css             # Tailwind 기반 커스텀 스타일
│
├── .env.example                   # DATABASE_URL, OPENAI_KEY 등
├── docker-compose.yml             # (선택) PG + API 연동
└── README.md                      # 설치·실행·배포 가이드...




단계별 개발 로드맵
단계	기간(예상)	주요 목표	산출물 / 검증 포인트
0. 개발 환경 셋업	0.5일	가상환경, .env, DB(→ SQLite), FastAPI 프로젝트 생성	uvicorn main:app --reload → GET /ping 확인
1. Auth & Site Service	2일	회원가입/로그인, 사이트 등록·SiteKey 발급 로직 완성	/register → /login → /site 테스트
2. rag_lib 모듈화	2~3일	libs/rag_lib/ 설계·구현 (인터페이스→FAISS→OpenAI→RAGService)	단위 테스트로 RAGService.query() 검증
3. Chat 연동 & DB 저장	1일	/chat 엔드포인트 → chat_service 호출 → DB 저장	Postman: POST /chat → 답변 / DB에 기록 확인
4. 관리자 UI (Jinja2)	1.5일	로그인·대시보드·세팅·업로드 템플릿 완성	브라우저로 해당 페이지 진입 & 기능 동작 확인
5. 위젯 제작 & 통합	1일	widget/* 파일 작성 → /widget StaticFiles 서빙 설정	데모 HTML에 설치 코드 붙이고 챗봇 작동 테스트
6. RAG 진짜 구현	2~3일	TXT 업로드 → rag_lib.ingest_documents() → 문맥 기반 답변으로 고도화	업로드 후 관련 문서가 답변에 활용되는지 검증
7. 테스트 & CI/CD	1~2일	pytest 작성, GitHub Actions, Docker-compose 배포 환경 완성	PR마다 테스트 통과, docker-compose up 확인
8. 베타 배포 & 피드백	0.5~1일	ngrok 또는 VPS에 띄우고 초기 사용자 피드백 수집	실사용 환경에서 버그/유저 피드백 확보
총 예상기간: 약 2주 후 MVP 배포
(매일 4–6시간 집중 개발, 학습 시간 포함 기준)


유지보수·확장 전략
모듈화

새로운 기능은 libs/, services/, routes/에 각각 추가

예) billing_lib, billing_service.py, routes/billing.py

버전 관리

Git 브랜치 전략 (feature/, bugfix/, main)

Semantic Versioning (태그: v0.1.0 → v0.2.0)

문서화

README.md에 “기능 사양” 섹션 추가

각 모듈별 docstring, FastAPI 자동 생성 Swagger

테스트

핵심 로직(RAG, Auth, Billing…)은 반드시 단위 테스트

API는 통합 테스트(TestClient)

CI/CD

GitHub Actions ▶︎ Docker Hub ▶︎ Cloud Deploy

👏 마무리
총 예상 소요: 약 2주(MVP) + 지속적 업데이트

학습 포인트:

FastAPI 라우터·의존성 주입

SQLAlchemy ORM & Alembic(추후)

Jinja2 템플릿 기초

간단한 JS로 iframe 위젯 제작

앞으로 할 일

환경 셋업 & FastAPI 튜토리얼

모듈별 코드 스켈레톤 작성

단계별 테스트 → 커밋 → 배포

이 플랜대로 천천히, 그래도 꾸준히만 나아가면
“완전 처음 해보는” FastAPI+Front-end 조합이더라도
충분히 MVP 완성 → 수익화까지 도달할 수 있어.
화이팅! 🚀
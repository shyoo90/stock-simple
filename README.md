# Stock Simple

## 프로젝트 개요
240728 Stock Simple은 주식 정보를 검색하고 표시하는 간단한 웹 애플리케이션입니다. 이 애플리케이션은 Next.js, Tailwind CSS, React, TypeScript 및 Docker를 사용하여 구축되었습니다.

## 주요 기능
- 주식 정보를 실시간으로 검색
- 검색어와 일치하는 주식 정보를 드롭다운 목록으로 표시
- Docker를 사용하여 백엔드와 프론트엔드 서비스를 함께 실행

## 프로젝트 구조
```
project-root/
│
├── backend/
│ ├── app/
│ │ ├── main.py
│ │ ├── requirements.txt
│ │ └── ...
│ └── Dockerfile
│
├── frontend-react/
│ ├── src/
│ │ ├── app/
│ │ │ ├── layout.tsx
│ │ │ ├── page.tsx
│ │ │ └── api/
│ │ │ └── stocks/
│ │ │ └── route.ts
│ │ ├── styles/
│ │ │ └── globals.css
│ ├── public/
│ │ └── ...
│ ├── Dockerfile
│ ├── tailwind.config.ts
│ ├── postcss.config.js
│ └── package.json
│
└── docker-compose.yml
```

## 설치 및 실행 방법

### 필수 구성 요소
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 로컬에서 실행
1. 이 repository를 클론합니다:
    ```bash
    git clone https://github.com/yourusername/240728_stock_simple.git
    cd 240728_stock_simple
    ```

2. Docker Compose로 모든 서비스를 시작합니다:
    ```bash
    docker-compose up --build
    ```

3. 브라우저에서 [http://localhost:3000](http://localhost:3000)에 접속하여 애플리케이션을 확인합니다.

## 환경 변수 설정
프로젝트에서 사용하는 환경 변수는 `.env` 파일에 설정할 수 있습니다. 예를 들어, PostgreSQL 데이터베이스 설정은 다음과 같습니다:

POSTGRES_DB=stock_db
POSTGRES_USER=stock_user
POSTGRES_PASSWORD=your_password


## 주요 파일 및 디렉토리
- `backend/`: 백엔드 애플리케이션 소스 코드
- `frontend-react/`: 프론트엔드 애플리케이션 소스 코드
- `docker-compose.yml`: Docker Compose 설정 파일
- `.env`: 환경 변수 파일

## 기여
기여를 환영합니다! 이 프로젝트에 기여하려면 이 repository를 포크하고 새로운 기능이나 버그 수정을 위한 브랜치를 생성한 후, Pull Request를 제출하세요.

1. 이 repository를 포크합니다.
2. 새로운 기능 브랜치를 생성합니다:
    ```bash
    git checkout -b feature/새로운기능
    ```
3. 변경 사항을 커밋합니다:
    ```bash
    git commit -m 'Add 새로운 기능'
    ```
4. 브랜치를 푸시합니다:
    ```bash
    git push origin feature/새로운기능
    ```
5. Pull Request를 제출합니다.

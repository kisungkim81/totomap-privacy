# SportsToto 판매점 데이터 업데이트 가이드

이 문서는 SportsToto 판매점 데이터를 업데이트하는 방법을 설명합니다.

## 📋 목차

- [사전 요구사항](#사전-요구사항)
- [업데이트 절차](#업데이트-절차)
- [문제 해결](#문제-해결)
- [참고사항](#참고사항)

## 🔧 사전 요구사항

### 필수 소프트웨어
- Python 3.7 이상
- Git

### 필수 Python 라이브러리
```bash
pip install requests beautifulsoup4
```

## 📖 업데이트 절차

### 1단계: 저장소 준비

```bash
# totomap-privacy 저장소로 이동
cd D:\androidProject\totomap-privacy

# 최신 코드 가져오기
git pull origin main
```

### 2단계: 데이터 수집 스크립트 실행

```bash
# 판매점 데이터 수집 (약 1-2분 소요)
python update_stores.py
```

**실행 결과:**
- `sportstoto_stores.csv` 파일이 생성/업데이트됩니다
- 약 6,462개의 판매점 정보가 수집됩니다
- 진행 상황이 콘솔에 표시됩니다

### 3단계: 데이터 검증

스크립트가 자동으로 데이터를 검증하며, 다음 정보를 출력합니다:
- 총 수집된 판매점 수
- 데이터 품질 (누락된 정보 체크)
- 샘플 데이터 미리보기

### 4단계: Git Commit 및 Push

```bash
# 변경사항 확인
git status

# CSV 파일 스테이징
git add sportstoto_stores.csv

# 커밋 (날짜 포함 권장)
git commit -m "판매점 데이터 업데이트: YYYY-MM-DD

- 전국 6,XXX개 판매점 정보 업데이트
- SportsToto 공식 사이트 최신 데이터 반영"

# GitHub에 푸시
git push origin main
```

### 5단계: 앱 배포 (선택사항)

앱을 다시 배포하여 최신 데이터를 사용자에게 제공합니다.

## 🔍 전체 과정 한눈에 보기

```bash
# 1. 저장소 이동 및 업데이트
cd D:\androidProject\totomap-privacy
git pull origin main

# 2. 데이터 수집
python update_stores.py

# 3. 변경사항 커밋 및 푸시
git add sportstoto_stores.csv
git commit -m "판매점 데이터 업데이트: $(date +%Y-%m-%d)"
git push origin main
```

## ⚠️ 문제 해결

### 문제: "requests 모듈을 찾을 수 없습니다"

**해결방법:**
```bash
pip install requests beautifulsoup4
```

### 문제: "수집된 데이터가 없습니다"

**원인:**
- 네트워크 연결 문제
- SportsToto 웹사이트 구조 변경
- 웹사이트 접근 제한

**해결방법:**
1. 인터넷 연결 확인
2. https://www.sportstoto.co.kr/find_store.php 웹사이트 직접 접속 확인
3. 방화벽/안티바이러스 설정 확인

### 문제: "수집된 판매점 수가 예상보다 적습니다"

**해결방법:**
1. 스크립트를 다시 실행해보세요
2. 서버 응답 시간이 느릴 경우 `time.sleep(0.3)`을 `time.sleep(0.5)`로 증가

### 문제: Git push 시 권한 오류

**해결방법:**
```bash
# GitHub 인증 정보 확인
git config --list | grep user

# 필요시 인증 정보 재설정
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 📝 참고사항

### 데이터 구조

CSV 파일은 다음 4개의 컬럼으로 구성됩니다:

| 컬럼 | 설명 | 예시 |
|------|------|------|
| Name | 판매점 이름 | 씨티마트 |
| Address | 전체 주소 | 서울 강남구 도산대로 49길 8 |
| Latitude | 위도 | 37.5233511349545 |
| Longitude | 경도 | 127.037425209409 |

### 업데이트 주기 권장

- **정기 업데이트**: 월 1회
- **긴급 업데이트**: 앱 사용자 피드백 시
- **계절별 업데이트**: 분기별 1회 (판매점 폐업/신규 개점 반영)

### 데이터 출처

- **소스**: https://www.sportstoto.co.kr/find_store.php
- **제공**: 국민체육진흥공단 스포츠토토
- **갱신 주기**: SportsToto 웹사이트 기준

### 스크립트 동작 원리

1. SportsToto 웹사이트에서 페이지별로 데이터 요청
2. JavaScript 코드 내 JSON 데이터 추출
3. 유니코드 이스케이프 시퀀스 디코딩
4. CSV 형식으로 저장

### 주의사항

- ⚠️ 스크립트는 웹 스크래핑을 사용하므로 웹사이트 구조 변경 시 수정 필요
- ⚠️ 과도한 요청을 방지하기 위해 페이지 간 0.3초 지연 적용
- ⚠️ 저작권 및 이용약관 준수 필요
- ⚠️ 개인적/비상업적 용도로만 사용 권장

## 📞 문의

문제가 계속되거나 추가 도움이 필요한 경우:
1. GitHub Issues에 문의
2. 스크립트 로그 확인
3. 웹사이트 접속 가능 여부 확인

---

**마지막 업데이트**: 2025-10-16
**버전**: 1.0.0

# 로또 판매점 데이터 수집 가이드

## ⚠️ 중요 안내

동행복권 로또 사이트(https://dhlottery.co.kr)는 강력한 anti-scraping 보호 기능을 사용합니다:
- 일반 HTTP 요청으로는 데이터 수집 불가
- 복잡한 세션 관리 및 쿠키 인증 필요
- JavaScript 동적 렌더링 사용

**결론**: 자동 스크래핑보다는 아래 방법들을 권장합니다.

---

## 📋 방법 1: 수동 데이터 수집 (가장 확실한 방법)

### 1단계: 동행복권 사이트 접속
```
https://dhlottery.co.kr/store.do?method=sellerInfo645
```

### 2단계: 브라우저에서 직접 데이터 수집
1. **시/도 선택** (예: 서울특별시)
2. **구/군 선택** (예: 강남구) - 선택 안하면 전체 검색
3. **검색 버튼 클릭**
4. **결과 복사**:
   - 테이블 전체 선택 (Ctrl+A)
   - 복사 (Ctrl+C)
   - Excel 또는 Google Sheets에 붙여넣기
5. **모든 페이지 반복**
6. **전체 시/도에 대해 반복**

### 3단계: CSV 변환
Excel 파일을 다음 형식의 CSV로 저장:
```csv
Name,Address,Latitude,Longitude,Phone
서울복권방,서울 강남구 테헤란로 123,,,02-123-4567
```

### 4단계: Geocoding으로 좌표 추가
좌표가 없는 경우 `add_coordinates.py` 스크립트 사용

---

## 🤖 방법 2: Kakao Local Search API (추천 - 자동화)

### 장점
- ✅ 완전 자동화
- ✅ 좌표 포함
- ✅ 전화번호 포함

### 단점
- ⚠️ "로또" 키워드 검색이므로 실제 판매점이 아닌 곳도 포함될 수 있음
- ⚠️ Kakao API 키 필요

### 사용 방법

#### 1단계: Kakao API 키 발급
1. https://developers.kakao.com/ 접속
2. 내 애플리케이션 > 애플리케이션 추가하기
3. REST API 키 복사

#### 2단계: 환경변수 설정
```bash
# Windows
set KAKAO_API_KEY=your_rest_api_key

# Linux/Mac
export KAKAO_API_KEY=your_rest_api_key
```

#### 3단계: 스크립트 실행
```bash
cd scripts/lotto
python scrape_kakao_api.py
```

결과: `lotto_stores.csv` 파일 생성 (좌표 포함)

---

## 🌐 방법 3: Selenium 자동화 (고급)

### 장점
- ✅ 공식 사이트에서 직접 수집
- ✅ 가장 정확한 데이터

### 단점
- ⚠️ Selenium 및 ChromeDriver 설치 필요
- ⚠️ 실행 시간 오래 걸림

### 사용 방법

#### 1단계: 패키지 설치
```bash
pip install selenium webdriver-manager
```

#### 2단계: 스크립트 실행
```bash
cd scripts/lotto
python scrape_with_selenium.py
```

결과: `lotto_stores.csv` 파일 생성 (좌표 없음)

#### 3단계: 좌표 추가 (선택사항)
```bash
set KAKAO_API_KEY=your_rest_api_key
python add_coordinates.py
```

결과: `lotto_stores_with_coords.csv` 파일 생성

---

## 방법 4: Geocoding API로 좌표 추가

### Geocoding API 설정

#### Kakao Geocoding
```python
import requests

def get_coordinates(address):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": "KakaoAK YOUR_API_KEY"}
    params = {"query": address}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if data['documents']:
        return (data['documents'][0]['y'], data['documents'][0]['x'])
    return ('', '')
```

#### Naver Geocoding
```python
import requests

def get_coordinates(address):
    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": "YOUR_CLIENT_ID",
        "X-NCP-APIGW-API-KEY": "YOUR_CLIENT_SECRET"
    }
    params = {"query": address}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if data['addresses']:
        return (data['addresses'][0]['y'], data['addresses'][0]['x'])
    return ('', '')
```

## 데이터 형식

### CSV 구조
```csv
Name,Address,Latitude,Longitude
롯데슈퍼 서울역점,서울 중구 한강대로 405,37.5547125,126.9707878
GS25 강남역점,서울 강남구 강남대로 지하 396,37.4979972,127.0276228
```

### 필수 컬럼
- **Name**: 판매점 이름
- **Address**: 전체 주소
- **Latitude**: 위도 (빈 값 가능)
- **Longitude**: 경도 (빈 값 가능)

## 자동화 스크립트 (실험적)

`update_lotto_stores.py` 스크립트는 실험적 기능입니다.
동행복권 사이트의 정책에 따라 작동하지 않을 수 있습니다.

```bash
python update_lotto_stores.py
```

## 업데이트 주기

- **권장**: 분기별 1회 (3개월)
- **이유**: 로또 판매점은 자주 변경되지 않음

## 데이터 출처

- **공식 사이트**: https://dhlottery.co.kr
- **판매점 찾기**: https://dhlottery.co.kr/store.do?method=sellerInfo645

## 문의

데이터 수집 관련 문의:
- Email: kisungkim81@gmail.com
- GitHub: https://github.com/kisungkim81/totomap-privacy

---

**마지막 업데이트**: 2025-10-16

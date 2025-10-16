# 로또 판매점 데이터 수집 가이드

## ⚠️ 중요 안내

동행복권 로또 사이트는 복잡한 인증 및 세션 관리를 사용하여 자동화된 데이터 수집이 제한적입니다.

현재는 다음 두 가지 방법을 권장합니다:

## 방법 1: 수동 데이터 수집 (권장)

### 1단계: 동행복권 사이트 접속
```
https://dhlottery.co.kr/store.do?method=sellerInfo645
```

### 2단계: 지역별로 검색하여 엑셀 다운로드
1. 시/도 선택
2. 구/군 선택
3. 검색 버튼 클릭
4. 결과를 복사하여 엑셀로 저장

### 3단계: CSV 변환
엑셀 파일을 다음 형식의 CSV로 변환:
```csv
Name,Address,Latitude,Longitude
판매점명,주소,,
```

### 4단계: Geocoding으로 좌표 추가
- Kakao Geocoding API 또는
- Naver Geocoding API 사용

## 방법 2: API 사용 (고급)

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

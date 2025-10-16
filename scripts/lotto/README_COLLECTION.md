# 로또 판매점 데이터 수집 스크립트

이 디렉토리에는 전국 로또 판매점 데이터를 수집하는 스크립트가 포함되어 있습니다.

## 📊 최종 수집 결과

- **총 판매점**: 12,805개
- **좌표 정보**: 12,804개 (99.99%)
- **데이터 출처**: https://www.fullayer.com/lottostore/fo/lottostorelist
- **수집일**: 2025년 10월

## 🚀 스크립트 설명

### 1. collect_by_detailed_region.py

**주요 수집 스크립트** - 전국 세부 지역별로 데이터를 수집합니다.

**기능:**
- 서울 25개 구, 부산 16개 구/군, 대구 9개 구/군 등 164개 지역 검색
- 각 지역별로 페이지네이션을 통해 전체 데이터 수집
- 좌표 정보(위도/경도) 자동 추출
- 중복 제거 기능

**실행 방법:**
```bash
python collect_by_detailed_region.py
```

**출력:**
- `app/src/main/assets/lotto_stores.csv` - CSV 형식의 판매점 데이터

### 2. collect_remaining_stores.py

**추가 수집 스크립트** - 누락된 판매점을 찾기 위한 보조 스크립트입니다.

**기능:**
- 기존 CSV 파일 로드
- 추가 키워드(읍/면/동, 편의점 이름 등)로 검색
- 중복되지 않은 새로운 판매점만 추가
- 기존 CSV에 자동으로 병합

**실행 방법:**
```bash
python collect_remaining_stores.py
```

## 📋 CSV 파일 형식

```csv
Name,Address,Latitude,Longitude
대치타운 중앙,서울 강남구 역삼로69길 28 1층 101호,37.503523,127.054147
수서 원스토어,서울 강남구 밤고개로1길 10 지하1층 제비 138호,37.488024,127.101844
```

**컬럼 설명:**
- `Name`: 판매점 이름
- `Address`: 전체 주소
- `Latitude`: 위도 (지도 표시용)
- `Longitude`: 경도 (지도 표시용)

## 🔧 필요한 패키지

```bash
pip install requests beautifulsoup4
```

## 📝 수집 전략

1. **세부 지역 검색**:
   - 광역시/도 → 구/군 → 시 단위로 세분화
   - 각 지역별로 개별 검색 수행
   - 페이지네이션 한계를 우회

2. **중복 제거**:
   - (Name, Address) 튜플로 고유성 판단
   - 메모리 효율적인 set 자료구조 사용

3. **좌표 추출**:
   - JavaScript `mapModal()` 함수에서 좌표 파싱
   - 정규표현식으로 경도/위도 추출

## ⚠️ 주의사항

- 서버 부하 방지를 위해 요청 간 0.15~0.3초 딜레이 포함
- 너무 빈번한 요청 시 IP 차단 가능성 있음
- 데이터 수집은 공개된 정보만 대상으로 함

## 🔄 데이터 업데이트

정기적으로 데이터를 업데이트하려면:

```bash
# 1. 전체 수집 (처음부터)
python collect_by_detailed_region.py

# 2. 추가 수집 (기존 데이터에서 누락 찾기)
python collect_remaining_stores.py
```

## 📞 문의

데이터 수집 관련 문의: [GitHub Issues](https://github.com/kisungkim81/totomap-privacy/issues)

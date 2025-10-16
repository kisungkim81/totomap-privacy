# 로또 판매점 데이터 수집 빠른 시작 가이드

## 🚀 가장 빠른 방법: Kakao API (권장)

### 1분 설정

```bash
# 1. Kakao API 키 발급: https://developers.kakao.com/
# 2. 환경변수 설정
set KAKAO_API_KEY=your_rest_api_key

# 3. 스크립트 실행
cd D:\androidProject\totomap-privacy\scripts\lotto
python scrape_kakao_api.py
```

결과: `../../lotto_stores.csv` 파일 생성 (좌표 포함!)

---

## ⚠️ 문제 발생 시

### 동행복권 사이트 직접 스크래핑 불가능
- 사이트에 강력한 anti-scraping 보호 기능 있음
- `update_lotto_stores.py` 및 `scrape_lotto_advanced.py`는 작동하지 않음

### 해결 방법
1. **Kakao API 사용** (위 방법) - 가장 쉬움
2. **Selenium 사용** - 브라우저 자동화
3. **수동 수집** - 가장 확실함

---

## 📊 현재 상태

### ✅ 이미 생성된 파일
- `lotto_stores.csv` - 34개 샘플 판매점 (전국 주요 편의점)

### 📝 사용 가능한 스크립트

| 스크립트 | 상태 | 설명 |
|---------|------|------|
| `scrape_kakao_api.py` | ✅ 권장 | Kakao API로 "로또" 검색 |
| `scrape_with_selenium.py` | ⚠️ 고급 | Selenium으로 공식 사이트 자동화 |
| `add_coordinates.py` | ✅ 유틸 | 주소에 좌표 추가 |
| `create_sample_data.py` | ✅ 완료 | 샘플 데이터 생성 (이미 실행됨) |
| `update_lotto_stores.py` | ❌ 작동 안 함 | 사이트 보호로 인해 실패 |

---

## 📖 자세한 가이드

전체 옵션 및 상세 설명은 `README_LOTTO.md` 참조

---

**마지막 업데이트**: 2025-10-16

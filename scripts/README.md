# 판매점 데이터 업데이트 스크립트

이 폴더에는 각 복권 앱의 판매점 데이터를 업데이트하는 스크립트들이 포함되어 있습니다.

## 📁 폴더 구조

```
scripts/
├── README.md                           # 이 파일
├── toto/                               # 스포츠토토 관련
│   ├── update_stores.py               # 스포츠토토 판매점 업데이트
│   ├── update_and_push.bat            # Windows 자동화
│   └── update_and_push.sh             # Linux/Mac 자동화
└── lotto/                              # 로또 관련
    ├── update_lotto_stores.py         # 로또 판매점 업데이트
    ├── update_and_push.bat            # Windows 자동화
    └── update_and_push.sh             # Linux/Mac 자동화
```

## 🚀 사용 방법

### 스포츠토토 판매점 업데이트

#### Windows
```bash
cd scripts/toto
update_and_push.bat
```

#### Linux/Mac
```bash
cd scripts/toto
./update_and_push.sh
```

#### 수동 실행
```bash
cd scripts/toto
python update_stores.py
```

### 로또 판매점 업데이트

#### Windows
```bash
cd scripts/lotto
update_and_push.bat
```

#### Linux/Mac
```bash
cd scripts/lotto
./update_and_push.sh
```

#### 수동 실행
```bash
cd scripts/lotto
python update_lotto_stores.py
```

## 📊 데이터 출처

| 앱 | 데이터 출처 | 파일명 |
|---|---|---|
| 토토어디 (TotoApp) | https://www.sportstoto.co.kr/find_store.php | sportstoto_stores.csv |
| 로또어디 (LottoApp) | https://dhlottery.co.kr/store.do?method=sellerInfo645 | lotto_stores.csv |

## ⚙️ 필수 요구사항

### Python 라이브러리
```bash
pip install requests beautifulsoup4
```

### 시스템 요구사항
- Python 3.7 이상
- Git (푸시 기능 사용 시)
- 인터넷 연결

## 📝 CSV 파일 형식

모든 CSV 파일은 동일한 형식을 사용합니다:

```csv
Name,Address,Latitude,Longitude
판매점명,주소,위도,경도
```

### 예시
```csv
Name,Address,Latitude,Longitude
씨티마트,서울 강남구 도산대로 49길 8,37.5233511349545,127.037425209409
GS25 서초타운점,서울 서초구 서초대로52길 23,37.4927684540547,127.014870982049
```

## 🔄 업데이트 주기

### 권장 주기
- **정기 업데이트**: 월 1회
- **긴급 업데이트**: 사용자 피드백 발생 시
- **계절별 업데이트**: 분기별 1회

### 예상 소요 시간
| 작업 | 스포츠토토 | 로또 |
|---|---|---|
| 데이터 수집 | 1-2분 | 5-10분 |
| Git 푸시 | 10초 | 10초 |
| **총 소요** | **약 2분** | **약 10분** |

## ⚠️ 주의사항

1. **웹 스크래핑 제한**
   - 과도한 요청 방지를 위해 요청 간 지연 시간 적용
   - 웹사이트 구조 변경 시 스크립트 수정 필요

2. **좌표 정보**
   - 스포츠토토: 웹사이트에서 좌표 정보 제공 (자동 수집)
   - 로또: 좌표 정보 미제공 (Geocoding API 필요)

3. **데이터 정확성**
   - 공식 웹사이트 데이터를 그대로 수집
   - 데이터 품질은 원본 사이트에 의존

4. **저작권**
   - 비상업적 용도로만 사용
   - 각 웹사이트의 이용약관 준수 필요

## 🐛 문제 해결

### 데이터 수집 실패
```bash
# 네트워크 연결 확인
ping www.sportstoto.co.kr
ping dhlottery.co.kr

# 웹사이트 직접 접속 확인
```

### Python 라이브러리 오류
```bash
# 라이브러리 재설치
pip install --upgrade requests beautifulsoup4
```

### Git 푸시 실패
```bash
# Git 상태 확인
git status

# 원격 저장소 확인
git remote -v

# 인증 정보 확인
git config --list | grep user
```

## 📞 문의

문제가 지속되거나 개선 사항이 있는 경우:
- GitHub Issues: https://github.com/kisungkim81/totomap-privacy/issues
- Email: kisungkim81@gmail.com

---

**마지막 업데이트**: 2025-10-16
**버전**: 1.0.0

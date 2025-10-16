# 🚀 빠른 시작 가이드

## 판매점 데이터 업데이트 (30초 완료)

### Windows 사용자

1. `totomap-privacy` 폴더로 이동
2. `update_and_push.bat` 더블클릭
3. 완료!

```bash
# 또는 명령 프롬프트에서:
cd D:\androidProject\totomap-privacy
update_and_push.bat
```

### Mac/Linux 사용자

```bash
cd /path/to/totomap-privacy
chmod +x update_and_push.sh
./update_and_push.sh
```

### 수동 실행 (세부 제어가 필요한 경우)

```bash
# 1. 데이터 수집
python update_stores.py

# 2. Git 커밋 및 푸시
git add sportstoto_stores.csv
git commit -m "판매점 데이터 업데이트: 2025-10-16"
git push origin main
```

## 📁 생성된 파일들

```
totomap-privacy/
├── sportstoto_stores.csv      # 판매점 데이터 (6,462개)
├── update_stores.py            # 데이터 수집 스크립트
├── update_and_push.bat         # Windows 자동화 스크립트
├── update_and_push.sh          # Linux/Mac 자동화 스크립트
├── README_UPDATE.md            # 상세 가이드
└── QUICK_START.md             # 이 파일
```

## ⏱️ 예상 소요 시간

- 데이터 수집: 1-2분
- Git 푸시: 10초
- **총 소요 시간: 약 2분**

## ✅ 성공 확인

스크립트 실행 후 다음이 표시되면 성공:

```
[성공] 전국 모든 판매점 데이터를 성공적으로 수집했습니다!
[성공] CSV 파일 저장 완료: sportstoto_stores.csv
업데이트 완료!
```

## 🔄 업데이트 주기

- **권장**: 월 1회
- **긴급**: 사용자 피드백 시
- **정기**: 분기별 1회

## 📞 문제 발생 시

자세한 내용은 `README_UPDATE.md` 참고

---

**마지막 업데이트**: 2025-10-16

#!/bin/bash

# ========================================
# SportsToto 판매점 데이터 자동 업데이트
# ========================================

echo ""
echo "========================================"
echo "SportsToto 판매점 데이터 업데이트 시작"
echo "========================================"
echo ""

# 현재 디렉토리 확인
echo "[1/5] 저장소 확인 중..."
if [ ! -f "sportstoto_stores.csv" ]; then
    echo "[오류] totomap-privacy 저장소 디렉토리에서 실행해주세요."
    exit 1
fi

# Git 최신 상태로 업데이트
echo ""
echo "[2/5] Git 저장소 업데이트 중..."
git pull origin main
if [ $? -ne 0 ]; then
    echo "[경고] Git pull 실패. 계속 진행합니다..."
fi

# Python 스크립트 실행
echo ""
echo "[3/5] 판매점 데이터 수집 중... (1-2분 소요)"
python3 update_stores.py
if [ $? -ne 0 ]; then
    echo "[오류] 데이터 수집 실패."
    exit 1
fi

# 변경사항 확인
echo ""
echo "[4/5] 변경사항 확인 중..."
git status

# 사용자 확인
echo ""
read -p "변경사항을 커밋하고 푸시하시겠습니까? (Y/N): " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "작업을 취소했습니다."
    exit 0
fi

# Git commit 및 push
echo ""
echo "[5/5] Git 커밋 및 푸시 중..."

TODAY=$(date +%Y-%m-%d)

git add sportstoto_stores.csv
git commit -m "판매점 데이터 업데이트: $TODAY"
git push origin main

if [ $? -ne 0 ]; then
    echo "[오류] Git push 실패. 수동으로 푸시해주세요."
    exit 1
fi

echo ""
echo "========================================"
echo "업데이트 완료!"
echo "========================================"
echo ""

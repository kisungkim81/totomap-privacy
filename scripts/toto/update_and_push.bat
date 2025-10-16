@echo off
REM ========================================
REM SportsToto 판매점 데이터 자동 업데이트
REM ========================================

echo.
echo ========================================
echo SportsToto 판매점 데이터 업데이트 시작
echo ========================================
echo.

REM 현재 디렉토리 확인
echo [1/5] 저장소 확인 중...
if not exist "sportstoto_stores.csv" (
    echo [오류] totomap-privacy 저장소 디렉토리에서 실행해주세요.
    pause
    exit /b 1
)

REM Git 최신 상태로 업데이트
echo.
echo [2/5] Git 저장소 업데이트 중...
git pull origin main
if errorlevel 1 (
    echo [경고] Git pull 실패. 계속 진행합니다...
)

REM Python 스크립트 실행
echo.
echo [3/5] 판매점 데이터 수집 중... (1-2분 소요)
python update_stores.py
if errorlevel 1 (
    echo [오류] 데이터 수집 실패.
    pause
    exit /b 1
)

REM 변경사항 확인
echo.
echo [4/5] 변경사항 확인 중...
git status

REM 사용자 확인
echo.
set /p CONFIRM="변경사항을 커밋하고 푸시하시겠습니까? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo 작업을 취소했습니다.
    pause
    exit /b 0
)

REM Git commit 및 push
echo.
echo [5/5] Git 커밋 및 푸시 중...

REM 날짜 가져오기
for /f "tokens=1-3 delims=/-" %%a in ('date /t') do (
    set YEAR=%%c
    set MONTH=%%a
    set DAY=%%b
)

git add sportstoto_stores.csv
git commit -m "판매점 데이터 업데이트: %YEAR%-%MONTH%-%DAY%"
git push origin main

if errorlevel 1 (
    echo [오류] Git push 실패. 수동으로 푸시해주세요.
    pause
    exit /b 1
)

echo.
echo ========================================
echo 업데이트 완료!
echo ========================================
echo.
pause

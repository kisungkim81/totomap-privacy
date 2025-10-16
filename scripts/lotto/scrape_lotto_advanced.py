#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
동행복권 로또 판매점 데이터 수집 스크립트 (개선 버전)

웹페이지 분석 결과:
- AJAX endpoint: /store.do?method=sellerInfo645Result
- POST 방식으로 데이터 요청
- 지역별로 반복 수집 필요

작성일: 2025-10-16
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
from typing import List, Dict

# 17개 시도 코드
SIDO_CODES = {
    '서울': '11',
    '부산': '26',
    '대구': '27',
    '인천': '28',
    '광주': '29',
    '대전': '30',
    '울산': '31',
    '세종': '36',
    '경기': '41',
    '강원': '42',
    '충북': '43',
    '충남': '44',
    '전북': '45',
    '전남': '46',
    '경북': '47',
    '경남': '48',
    '제주': '50'
}

def get_stores_by_sido(sido_name: str, sido_code: str) -> List[Dict]:
    """
    특정 시도의 모든 로또 판매점을 수집합니다.
    """
    print(f"\n[{sido_name}] 데이터 수집 중...")

    url = "https://dhlottery.co.kr/store.do?method=sellerInfo645Result"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://dhlottery.co.kr',
        'Referer': 'https://dhlottery.co.kr/store.do?method=sellerInfo645',
        'Connection': 'keep-alive'
    }

    stores = []
    page = 1
    max_pages = 100  # 안전장치

    session = requests.Session()

    # 먼저 메인 페이지 방문하여 세션 생성
    try:
        session.get('https://dhlottery.co.kr/store.do?method=sellerInfo645', headers=headers, timeout=10)
        time.sleep(1)
    except Exception as e:
        print(f"  [오류] 메인 페이지 접속 실패: {e}")
        return []

    while page <= max_pages:
        data = {
            'method': 'sellerInfo645Result',
            'searchType': '3',  # 전체 검색
            'sltSIDO2': sido_code,
            'rtlrSttus': '001',  # 판매점 상태
            'nowPage': str(page)
        }

        try:
            response = session.post(url, headers=headers, data=data, timeout=15)

            if response.status_code != 200:
                print(f"  [오류] HTTP {response.status_code}")
                break

            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')

            # 판매점 테이블 찾기
            table = soup.find('table')
            if not table:
                if page == 1:
                    print(f"  [경고] 테이블을 찾을 수 없습니다")
                break

            rows = table.find_all('tr')[1:]  # 헤더 제외

            if not rows:
                break

            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    name = cols[0].get_text(strip=True)
                    address = cols[1].get_text(strip=True)
                    phone = cols[2].get_text(strip=True) if len(cols) > 2 else ''

                    if name and address:
                        stores.append({
                            'name': name,
                            'address': address,
                            'phone': phone
                        })

            print(f"  페이지 {page}: {len(rows)}개 발견 (누적: {len(stores)}개)")

            # 다음 페이지가 있는지 확인
            next_button = soup.find('a', text='다음')
            if not next_button or len(rows) == 0:
                break

            page += 1
            time.sleep(0.5)  # 서버 부하 방지

        except Exception as e:
            print(f"  [오류] 페이지 {page} 수집 실패: {e}")
            break

    print(f"[{sido_name}] 완료: 총 {len(stores)}개 판매점")
    return stores

def save_to_csv(stores: List[Dict], filename: str = '../../lotto_stores.csv'):
    """
    수집한 데이터를 CSV 파일로 저장합니다.
    """
    print(f"\nCSV 파일 저장 중: {filename}")

    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Address', 'Latitude', 'Longitude', 'Phone'])

        for store in stores:
            writer.writerow([
                store['name'],
                store['address'],
                '',  # Latitude - 나중에 Geocoding API로 채울 수 있음
                '',  # Longitude
                store.get('phone', '')
            ])

    print(f"✓ 저장 완료: {len(stores)}개 판매점")

def main():
    print("=" * 70)
    print("                동행복권 로또 판매점 데이터 수집")
    print("=" * 70)
    print(f"\n수집 대상: 전국 17개 시도")
    print("=" * 70)

    all_stores = []

    for sido_name, sido_code in SIDO_CODES.items():
        stores = get_stores_by_sido(sido_name, sido_code)
        all_stores.extend(stores)
        time.sleep(1)  # 시도 간 대기

    print("\n" + "=" * 70)
    print(f"[완료] 총 {len(all_stores)}개 판매점 수집 완료")
    print("=" * 70)

    if all_stores:
        save_to_csv(all_stores)
        print("\n✓ 데이터 수집 및 저장이 성공적으로 완료되었습니다!")
    else:
        print("\n[경고] 수집된 데이터가 없습니다.")
        print("[안내] 네트워크 상태 또는 웹사이트 구조를 확인해주세요.")

if __name__ == "__main__":
    main()

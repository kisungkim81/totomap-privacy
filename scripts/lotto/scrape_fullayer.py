#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fullayer 로또 판매점 데이터 수집 스크립트

사이트: https://www.fullayer.com/lottostore/fo/lottostorelist
총 14,450개 판매점

작성일: 2025-10-16
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import json
from typing import List, Dict

BASE_URL = "https://www.fullayer.com/lottostore/fo/lottostorelist"

def get_store_list(page=1):
    """
    페이지별 판매점 리스트 수집
    """
    # 페이지 URL (GET 파라미터 사용)
    url = f"{BASE_URL}?page={page}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code != 200:
            print(f"  [오류] HTTP {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        # tbody에서 tr 찾기
        tbody = soup.find('tbody')
        if not tbody:
            return []

        rows = tbody.find_all('tr')

        stores = []
        for row in rows:
            try:
                cols = row.find_all('td')
                if len(cols) < 4:
                    continue

                # 이름 (첫 번째 td의 a 태그)
                name_link = cols[0].find('a')
                name = name_link.get_text(strip=True) if name_link else ''

                # 전화번호 (두 번째 td의 a 태그)
                phone_link = cols[1].find('a')
                phone = phone_link.get_text(strip=True) if phone_link else ''

                # 주소 (세 번째 td)
                address = cols[2].get_text(strip=True)

                # 좌표 (네 번째 td의 a 태그 onclick에서 추출)
                map_link = cols[3].find('a', {'onclick': True})
                lng, lat = '', ''

                if map_link:
                    onclick = map_link.get('onclick', '')
                    # mapModal('이름','경도', '위도') 형식
                    if 'mapModal' in onclick:
                        parts = onclick.split("'")
                        if len(parts) >= 5:
                            lng = parts[3].strip()
                            lat = parts[5].strip()

                if name and address:
                    stores.append({
                        'name': name,
                        'phone': phone,
                        'address': address,
                        'lat': lat,
                        'lng': lng
                    })

            except Exception as e:
                print(f"    [경고] 행 처리 오류: {e}")
                continue

        return stores

    except Exception as e:
        print(f"  [오류] 페이지 {page} 수집 실패: {e}")
        return []

def collect_all_stores():
    """
    모든 판매점 데이터 수집
    """
    print("=" * 70)
    print("        Fullayer 로또 판매점 데이터 수집")
    print("=" * 70)
    print(f"\n예상 판매점 수: 약 14,450개")
    print("페이지당 약 20개씩 수집")
    print("=" * 70)

    all_stores = []
    page = 1
    max_pages = 750  # 최대 750페이지 (14,450 / 20)

    while page <= max_pages:
        print(f"\n[페이지 {page}] 수집 중...")

        stores = get_store_list(page)

        if not stores:
            print(f"  더 이상 데이터가 없습니다.")
            break

        all_stores.extend(stores)
        print(f"  {len(stores)}개 수집 (누적: {len(all_stores)}개)")

        # 100페이지마다 진행상황 표시
        if page % 100 == 0:
            print(f"\n>>> 진행률: {page}/750 페이지 ({page*100//750}%)")

        page += 1
        time.sleep(0.3)  # 서버 부하 방지

    return all_stores

def save_to_csv(stores: List[Dict], filename: str = '../../lotto_stores.csv'):
    """
    CSV 파일로 저장
    """
    print(f"\nCSV 파일 저장: {filename}")

    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Address', 'Latitude', 'Longitude', 'Phone'])

        for store in stores:
            writer.writerow([
                store['name'],
                store['address'],
                store.get('lat', ''),
                store.get('lng', ''),
                store.get('phone', '')
            ])

    print(f"완료: {len(stores)}개 판매점")

def main():
    stores = collect_all_stores()

    print("\n" + "=" * 70)
    print(f"[완료] 총 {len(stores)}개 판매점 수집 완료")
    print("=" * 70)

    if stores:
        save_to_csv(stores)

        # 좌표 포함 여부 확인
        with_coords = sum(1 for s in stores if s.get('lat') and s.get('lng'))
        print(f"\n통계:")
        print(f"  - 총 판매점: {len(stores)}개")
        print(f"  - 좌표 포함: {with_coords}개 ({with_coords*100//len(stores)}%)")
        print(f"  - 좌표 없음: {len(stores)-with_coords}개")
    else:
        print("\n[경고] 수집된 데이터가 없습니다.")

if __name__ == "__main__":
    main()

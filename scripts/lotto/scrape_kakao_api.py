#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kakao 로컬 검색 API를 사용한 로또 판매점 수집

Kakao Local API로 "로또 판매점" 키워드 검색하여 데이터 수집

Requirements:
1. Kakao Developers에서 앱 생성 및 REST API 키 발급
   https://developers.kakao.com/
2. 환경변수 설정:
   set KAKAO_API_KEY=your_rest_api_key

작성일: 2025-10-16
"""

import requests
import csv
import time
import os
from typing import List, Dict

KAKAO_API_KEY = os.environ.get('KAKAO_API_KEY', '')

# 전국 주요 도시 좌표 (검색 기준점)
SEARCH_LOCATIONS = [
    {'name': '서울', 'x': 126.9784, 'y': 37.5665},
    {'name': '부산', 'x': 129.0756, 'y': 35.1796},
    {'name': '대구', 'x': 128.6014, 'y': 35.8714},
    {'name': '인천', 'x': 126.7052, 'y': 37.4563},
    {'name': '광주', 'x': 126.8526, 'y': 35.1595},
    {'name': '대전', 'x': 127.3845, 'y': 36.3504},
    {'name': '울산', 'x': 129.3114, 'y': 35.5384},
    {'name': '세종', 'x': 127.2890, 'y': 36.4800},
    {'name': '수원', 'x': 127.0286, 'y': 37.2636},
    {'name': '성남', 'x': 127.1388, 'y': 37.4449},
    {'name': '춘천', 'x': 127.7306, 'y': 37.8813},
    {'name': '청주', 'x': 127.4895, 'y': 36.6424},
    {'name': '천안', 'x': 127.1138, 'y': 36.8151},
    {'name': '전주', 'x': 127.1480, 'y': 35.8242},
    {'name': '목포', 'x': 126.3922, 'y': 34.8118},
    {'name': '포항', 'x': 129.3656, 'y': 36.0190},
    {'name': '창원', 'x': 128.6811, 'y': 35.2279},
    {'name': '제주', 'x': 126.5312, 'y': 33.4996},
]

def search_lotto_stores_kakao(location: Dict, keyword: str = "로또") -> List[Dict]:
    """
    특정 위치 기준으로 로또 판매점 검색
    """
    if not KAKAO_API_KEY:
        print("❌ KAKAO_API_KEY가 설정되지 않았습니다.")
        return []

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}

    stores = []
    page = 1
    max_page = 45  # Kakao API 최대 45페이지

    print(f"\n[{location['name']}] 검색 중...")

    while page <= max_page:
        params = {
            'query': keyword,
            'x': location['x'],
            'y': location['y'],
            'radius': 20000,  # 20km 반경
            'page': page,
            'size': 15  # 페이지당 15개
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code != 200:
                print(f"  [오류] HTTP {response.status_code}")
                break

            data = response.json()
            documents = data.get('documents', [])

            if not documents:
                break

            for doc in documents:
                store = {
                    'name': doc.get('place_name', ''),
                    'address': doc.get('road_address_name') or doc.get('address_name', ''),
                    'phone': doc.get('phone', ''),
                    'lat': doc.get('y', ''),
                    'lng': doc.get('x', ''),
                    'category': doc.get('category_name', '')
                }

                # 중복 제거 (이름+주소 기준)
                if store['name'] and store['address']:
                    if not any(s['name'] == store['name'] and s['address'] == store['address'] for s in stores):
                        stores.append(store)

            print(f"  페이지 {page}: {len(documents)}개 (누적: {len(stores)}개)")

            # 마지막 페이지 확인
            if data['meta']['is_end']:
                break

            page += 1
            time.sleep(0.1)  # API 호출 제한 준수

        except Exception as e:
            print(f"  [오류] 페이지 {page} 검색 실패: {e}")
            break

    print(f"[{location['name']}] 완료: {len(stores)}개")
    return stores

def collect_all_stores() -> List[Dict]:
    """
    전국 모든 위치에서 로또 판매점 검색
    """
    all_stores = []
    seen = set()  # 중복 제거용

    for location in SEARCH_LOCATIONS:
        stores = search_lotto_stores_kakao(location)

        for store in stores:
            key = (store['name'], store['address'])
            if key not in seen:
                all_stores.append(store)
                seen.add(key)

        time.sleep(0.5)

    return all_stores

def save_to_csv(stores: List[Dict], filename: str = '../../lotto_stores.csv'):
    """
    CSV 파일로 저장
    """
    print(f"\nCSV 파일 저장: {filename}")

    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Address', 'Latitude', 'Longitude', 'Phone', 'Category'])

        for store in stores:
            writer.writerow([
                store['name'],
                store['address'],
                store['lat'],
                store['lng'],
                store['phone'],
                store.get('category', '')
            ])

    print(f"✓ 저장 완료: {len(stores)}개 판매점")

def main():
    print("=" * 70)
    print("       로또 판매점 데이터 수집 (Kakao Local Search API)")
    print("=" * 70)

    if not KAKAO_API_KEY:
        print("\n❌ KAKAO_API_KEY 환경변수가 설정되지 않았습니다.")
        print("\n설정 방법:")
        print("  Windows: set KAKAO_API_KEY=your_rest_api_key")
        print("  Linux/Mac: export KAKAO_API_KEY=your_rest_api_key")
        print("\nAPI 키 발급: https://developers.kakao.com/")
        return

    print(f"\n검색 대상 지역: {len(SEARCH_LOCATIONS)}개")
    print("=" * 70)

    stores = collect_all_stores()

    print("\n" + "=" * 70)
    print(f"총 {len(stores)}개 판매점 수집 완료")
    print("=" * 70)

    if stores:
        save_to_csv(stores)
        print("\n✓ 완료!")
        print("\n참고:")
        print("- 이 방법은 '로또' 키워드로 검색된 모든 장소를 포함합니다")
        print("- 실제 판매점이 아닌 곳도 포함될 수 있습니다")
        print("- 더 정확한 데이터는 동행복권 공식 사이트 수동 수집을 권장합니다")
    else:
        print("\n❌ 데이터 수집 실패")

if __name__ == "__main__":
    main()

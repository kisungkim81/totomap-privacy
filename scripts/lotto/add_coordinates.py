#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CSV 파일의 주소에 좌표 추가 스크립트

Kakao Maps Geocoding API를 사용하여 주소를 좌표로 변환합니다.

사용법:
1. Kakao Developers에서 API 키 발급: https://developers.kakao.com/
2. 환경변수 설정: set KAKAO_API_KEY=your_api_key
3. 실행: python add_coordinates.py

작성일: 2025-10-16
"""

import csv
import time
import requests
import os
from typing import Tuple, Optional

KAKAO_API_KEY = os.environ.get('KAKAO_API_KEY', '')

def get_coordinates_kakao(address: str) -> Tuple[str, str]:
    """
    Kakao Geocoding API로 주소를 좌표로 변환
    """
    if not KAKAO_API_KEY:
        return ('', '')

    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"query": address}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        data = response.json()

        if data.get('documents'):
            doc = data['documents'][0]
            lat = doc['y']  # 위도
            lng = doc['x']  # 경도
            return (lat, lng)

    except Exception as e:
        print(f"  [오류] 좌표 변환 실패: {address} - {e}")

    return ('', '')

def add_coordinates_to_csv(input_file: str = '../../lotto_stores.csv',
                          output_file: str = '../../lotto_stores_with_coords.csv'):
    """
    CSV 파일에 좌표 추가
    """
    if not KAKAO_API_KEY:
        print("❌ KAKAO_API_KEY 환경변수가 설정되지 않았습니다.")
        print("\n설정 방법:")
        print("  Windows: set KAKAO_API_KEY=your_api_key")
        print("  Linux/Mac: export KAKAO_API_KEY=your_api_key")
        print("\nAPI 키 발급: https://developers.kakao.com/")
        return

    print(f"입력 파일: {input_file}")
    print(f"출력 파일: {output_file}")

    stores = []
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stores.append(row)

    print(f"\n총 {len(stores)}개 판매점")
    print("좌표 변환 중...\n")

    processed = 0
    for i, store in enumerate(stores, 1):
        address = store['Address']

        # 좌표가 이미 있으면 건너뛰기
        if store.get('Latitude') and store.get('Longitude'):
            print(f"[{i}/{len(stores)}] 건너뛰기 (좌표 존재): {address}")
            continue

        lat, lng = get_coordinates_kakao(address)

        if lat and lng:
            store['Latitude'] = lat
            store['Longitude'] = lng
            print(f"[{i}/{len(stores)}] ✓ {address} -> ({lat}, {lng})")
            processed += 1
        else:
            print(f"[{i}/{len(stores)}] ✗ {address}")

        # API 호출 제한 방지 (무료: 300,000회/일, 초당 30회)
        time.sleep(0.05)  # 20 requests/sec

    # 결과 저장
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['Name', 'Address', 'Latitude', 'Longitude', 'Phone']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stores)

    print(f"\n✓ 완료: {processed}개 좌표 추가")
    print(f"✓ 저장: {output_file}")

def main():
    print("=" * 70)
    print("              로또 판매점 좌표 추가 (Kakao Geocoding)")
    print("=" * 70)
    print()

    add_coordinates_to_csv()

if __name__ == "__main__":
    main()

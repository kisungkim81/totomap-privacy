#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SportsToto 판매점 데이터 업데이트 스크립트

이 스크립트는 SportsToto 공식 웹사이트에서 전국 모든 판매점 정보를 수집하여
CSV 파일로 저장합니다.

사용법:
    python update_stores.py

출력:
    - sportstoto_stores.csv: 전국 판매점 데이터 (Name, Address, Latitude, Longitude)

작성일: 2025-10-16
최종 수정일: 2025-10-16
"""

import requests
import json
import csv
import re
import codecs
import time
from typing import List, Dict
from datetime import datetime

# 설정
BASE_URL = "https://www.sportstoto.co.kr/find_store.php"
OUTPUT_FILE = "sportstoto_stores.csv"
EXPECTED_TOTAL = 6462  # 예상 판매점 수
PAGE_SIZE = 50  # 페이지당 판매점 수


def scrape_page(page: int = 1) -> List[Dict]:
    """
    특정 페이지의 판매점 데이터를 가져옵니다.

    Args:
        page: 페이지 번호 (1부터 시작)

    Returns:
        판매점 정보 리스트
    """
    url = f"{BASE_URL}?page={page}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'

        # JavaScript에서 JSON 배열 추출
        pattern = r'var address_json = JSON\.parse\("(\[.+?\])"\);'
        match = re.search(pattern, response.text, re.DOTALL)

        stores = []

        if match:
            json_raw = match.group(1)

            # 이스케이프 처리
            json_string = json_raw.replace('\\"', '"')

            # 유니코드 이스케이프를 실제 문자로 변환
            def decode_unicode_escapes(s):
                s = s.replace('\\\\u', '\\u')
                try:
                    return codecs.decode(s, 'unicode-escape')
                except:
                    return s

            json_string = decode_unicode_escapes(json_string)

            try:
                stores_data = json.loads(json_string)

                for store in stores_data:
                    # 주소 조합 (addr1~addr4)
                    address_parts = []
                    for i in range(1, 5):
                        addr_part = store.get(f'addr{i}', '').strip()
                        if addr_part:
                            address_parts.append(addr_part)

                    full_address = ' '.join(address_parts)

                    stores.append({
                        'name': store.get('name', ''),
                        'address': full_address,
                        'latitude': store.get('y_axis', ''),
                        'longitude': store.get('x_axis', '')
                    })

            except json.JSONDecodeError as e:
                print(f"[오류] 페이지 {page} JSON 파싱 실패: {e}")

        return stores

    except Exception as e:
        print(f"[오류] 페이지 {page} 데이터 수집 실패: {e}")
        return []


def scrape_all_stores() -> List[Dict]:
    """
    모든 페이지의 판매점 정보를 수집합니다.

    Returns:
        전체 판매점 정보 리스트
    """
    print("\n" + "=" * 70)
    print("SportsToto 전국 판매점 데이터 수집 시작")
    print(f"수집 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")

    all_stores = []
    page = 1
    max_pages = (EXPECTED_TOTAL + PAGE_SIZE - 1) // PAGE_SIZE + 5  # 여유있게

    while page <= max_pages:
        print(f"[진행] 페이지 {page} 처리 중...", end=' ', flush=True)

        stores = scrape_page(page)

        if not stores:
            print(f"데이터 없음 - 수집 종료")
            break

        all_stores.extend(stores)
        print(f"완료 ({len(stores)}개 수집, 총 {len(all_stores)}개)")

        # 더 이상 새로운 데이터가 없으면 중단
        if len(stores) < PAGE_SIZE or len(all_stores) >= EXPECTED_TOTAL:
            print(f"\n[완료] 모든 데이터 수집 완료!")
            break

        page += 1
        time.sleep(0.3)  # 서버 부하 방지

    print("=" * 70)
    return all_stores


def save_to_csv(stores: List[Dict], filename: str = OUTPUT_FILE) -> bool:
    """
    판매점 데이터를 CSV 파일로 저장합니다.

    Args:
        stores: 판매점 정보 리스트
        filename: 출력 파일명

    Returns:
        성공 여부
    """
    if not stores:
        print("[경고] 저장할 데이터가 없습니다.")
        return False

    try:
        print(f"\n[저장] {len(stores)}개의 판매점 정보를 {filename}에 저장 중...")

        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)

            # 헤더 작성
            writer.writerow(['Name', 'Address', 'Latitude', 'Longitude'])

            # 데이터 작성
            for store in stores:
                writer.writerow([
                    store.get('name', ''),
                    store.get('address', ''),
                    store.get('latitude', ''),
                    store.get('longitude', '')
                ])

        print(f"[성공] CSV 파일 저장 완료: {filename}")
        return True

    except Exception as e:
        print(f"[오류] CSV 파일 저장 실패: {e}")
        return False


def validate_data(stores: List[Dict]) -> None:
    """
    수집된 데이터를 검증하고 결과를 출력합니다.

    Args:
        stores: 판매점 정보 리스트
    """
    print("\n" + "=" * 70)
    print("데이터 검증 결과")
    print("=" * 70)
    print(f"총 수집 판매점 수: {len(stores)}개")
    print(f"예상 판매점 수: {EXPECTED_TOTAL}개")

    if len(stores) >= EXPECTED_TOTAL - 10:
        print(f"[성공] 전국 모든 판매점 데이터를 성공적으로 수집했습니다!")
    elif len(stores) >= EXPECTED_TOTAL - 100:
        print(f"[주의] 대부분의 판매점 데이터를 수집했습니다. (차이: {EXPECTED_TOTAL - len(stores)}개)")
    else:
        print(f"[경고] 일부 데이터가 누락되었을 수 있습니다. (부족: {EXPECTED_TOTAL - len(stores)}개)")

    # 데이터 품질 체크
    empty_names = sum(1 for s in stores if not s.get('name'))
    empty_addresses = sum(1 for s in stores if not s.get('address'))
    empty_coords = sum(1 for s in stores if not s.get('latitude') or not s.get('longitude'))

    print(f"\n데이터 품질:")
    print(f"  - 이름 누락: {empty_names}개")
    print(f"  - 주소 누락: {empty_addresses}개")
    print(f"  - 좌표 누락: {empty_coords}개")

    if stores:
        print(f"\n데이터 샘플 (처음 3개):")
        for i, store in enumerate(stores[:3], 1):
            print(f"  {i}. {store.get('name', 'N/A')} - {store.get('address', 'N/A')}")

    print("=" * 70)


def main():
    """
    메인 실행 함수
    """
    print("\n" + "=" * 70)
    print(" " * 15 + "SportsToto 판매점 데이터 업데이트")
    print("=" * 70)

    # 1. 데이터 수집
    stores = scrape_all_stores()

    # 2. 데이터 검증
    if stores:
        validate_data(stores)

        # 3. CSV 파일 저장
        if save_to_csv(stores):
            print(f"\n[완료] 업데이트 완료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"[정보] 다음 단계: Git commit 및 push를 진행하세요.")
        else:
            print(f"\n[오류] 파일 저장에 실패했습니다.")
    else:
        print("\n[오류] 수집된 데이터가 없습니다.")
        print("[안내] 네트워크 연결 또는 웹사이트 접근을 확인해주세요.")

    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

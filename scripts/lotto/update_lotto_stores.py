#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
로또 판매점 데이터 업데이트 스크립트

이 스크립트는 동행복권 공식 웹사이트에서 전국 모든 로또 판매점 정보를 수집하여
CSV 파일로 저장합니다.

사용법:
    python update_lotto_stores.py

출력:
    - lotto_stores.csv: 전국 로또 판매점 데이터 (Name, Address, Latitude, Longitude)

작성일: 2025-10-16
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import re
from typing import List, Dict
from datetime import datetime

# 설정
BASE_URL = "https://dhlottery.co.kr"
SEARCH_URL = f"{BASE_URL}/store.do?method=sellerInfo645Result"
OUTPUT_FILE = "lotto_stores.csv"

# 시도 코드 매핑 (동행복권 사이트 기준)
SIDO_MAP = {
    "서울": "11",
    "부산": "26",
    "대구": "27",
    "인천": "28",
    "광주": "29",
    "대전": "30",
    "울산": "31",
    "세종": "36",
    "경기": "41",
    "강원": "42",
    "충북": "43",
    "충남": "44",
    "전북": "45",
    "전남": "46",
    "경북": "47",
    "경남": "48",
    "제주": "50"
}


def get_gugun_list(sido_code: str) -> List[Dict]:
    """
    특정 시/도의 구/군 목록을 가져옵니다.

    Args:
        sido_code: 시/도 코드

    Returns:
        구/군 정보 리스트
    """
    url = f"{BASE_URL}/store.do?method=searchGUGUN"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': f'{BASE_URL}/store.do?method=sellerInfo645'
    }

    params = {
        'sltSIDO2': sido_code
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.encoding = 'euc-kr'

        soup = BeautifulSoup(response.text, 'html.parser')
        options = soup.find_all('option')

        gugun_list = []
        for option in options:
            value = option.get('value', '').strip()
            text = option.get_text().strip()
            if value and value != 'all':
                gugun_list.append({'code': value, 'name': text})

        return gugun_list

    except Exception as e:
        print(f"[오류] 구/군 목록 조회 실패 (시/도: {sido_code}): {e}")
        return []


def search_stores(sido_code: str = '', gugun_code: str = '', page: int = 1) -> Dict:
    """
    판매점을 검색합니다.

    Args:
        sido_code: 시/도 코드
        gugun_code: 구/군 코드
        page: 페이지 번호

    Returns:
        판매점 정보 딕셔너리
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': f'{BASE_URL}/store.do?method=sellerInfo645',
        'X-Requested-With': 'XMLHttpRequest'
    }

    params = {
        'rtlrSttus': '001',  # 판매점 상태
        'nowPage': page,
        'sltSIDO2': sido_code,
        'sltGUGUN2': gugun_code
    }

    try:
        response = requests.get(SEARCH_URL, headers=headers, params=params, timeout=30)
        response.encoding = 'euc-kr'

        soup = BeautifulSoup(response.text, 'html.parser')

        # 판매점 테이블 파싱
        stores = []
        rows = soup.select('table tbody tr')

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                store = {
                    'name': cols[1].get_text(strip=True),
                    'address': cols[2].get_text(strip=True),
                    'phone': cols[3].get_text(strip=True),
                    'latitude': '',
                    'longitude': ''
                }
                stores.append(store)

        # 총 페이지 수 확인
        pagination = soup.select('.paginate')
        total_pages = 1
        if pagination:
            page_links = pagination[0].select('a')
            if page_links:
                # 마지막 페이지 번호 추출
                for link in page_links:
                    onclick = link.get('onclick', '')
                    match = re.search(r'goPage\((\d+)\)', onclick)
                    if match:
                        page_num = int(match.group(1))
                        total_pages = max(total_pages, page_num)

        return {
            'stores': stores,
            'total_pages': total_pages,
            'current_page': page
        }

    except Exception as e:
        print(f"[오류] 판매점 검색 실패 (페이지 {page}): {e}")
        return {'stores': [], 'total_pages': 0, 'current_page': page}


def geocode_address(address: str) -> tuple:
    """
    주소를 좌표로 변환합니다 (Kakao Geocoding API 사용 가능)

    Args:
        address: 주소

    Returns:
        (위도, 경도) 튜플
    """
    # TODO: Kakao 또는 Naver Geocoding API를 사용하여 좌표 변환
    # 현재는 빈 문자열 반환
    return ('', '')


def scrape_all_stores() -> List[Dict]:
    """
    전국 모든 로또 판매점 정보를 수집합니다.

    Returns:
        전체 판매점 정보 리스트
    """
    print("\n" + "=" * 70)
    print("동행복권 로또 판매점 데이터 수집 시작")
    print(f"수집 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")

    all_stores = []

    # 각 시/도별로 수집
    for sido_name, sido_code in SIDO_MAP.items():
        print(f"\n[{sido_name}] 지역 수집 시작...")

        # 구/군 목록 가져오기
        gugun_list = get_gugun_list(sido_code)

        if not gugun_list:
            # 구/군이 없으면 시/도 전체 검색
            print(f"  - {sido_name} 전체 검색 중...")
            page = 1
            while True:
                result = search_stores(sido_code=sido_code, page=page)
                stores = result['stores']

                if not stores:
                    break

                all_stores.extend(stores)
                print(f"    페이지 {page}: {len(stores)}개 수집 (총 {len(all_stores)}개)")

                if page >= result['total_pages']:
                    break

                page += 1
                time.sleep(0.3)
        else:
            # 각 구/군별로 검색
            for gugun in gugun_list:
                print(f"  - {gugun['name']} 검색 중...")
                page = 1

                while True:
                    result = search_stores(
                        sido_code=sido_code,
                        gugun_code=gugun['code'],
                        page=page
                    )
                    stores = result['stores']

                    if not stores:
                        break

                    all_stores.extend(stores)
                    print(f"    페이지 {page}: {len(stores)}개 수집 (총 {len(all_stores)}개)")

                    if page >= result['total_pages']:
                        break

                    page += 1
                    time.sleep(0.3)

        print(f"[{sido_name}] 완료")
        time.sleep(0.5)

    print("\n" + "=" * 70)
    print(f"[완료] 총 {len(all_stores)}개 판매점 수집 완료")
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

    # 데이터 품질 체크
    empty_names = sum(1 for s in stores if not s.get('name'))
    empty_addresses = sum(1 for s in stores if not s.get('address'))

    print(f"\n데이터 품질:")
    print(f"  - 이름 누락: {empty_names}개")
    print(f"  - 주소 누락: {empty_addresses}개")
    print(f"  - 좌표 정보: 미수집 (Geocoding API 필요)")

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
    print(" " * 20 + "로또 판매점 데이터 업데이트")
    print("=" * 70)

    # 1. 데이터 수집
    stores = scrape_all_stores()

    # 2. 데이터 검증
    if stores:
        validate_data(stores)

        # 3. CSV 파일 저장
        if save_to_csv(stores):
            print(f"\n[완료] 업데이트 완료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"[정보] 좌표 정보를 추가하려면 Geocoding API를 설정하세요.")
        else:
            print(f"\n[오류] 파일 저장에 실패했습니다.")
    else:
        print("\n[오류] 수집된 데이터가 없습니다.")
        print("[안내] 네트워크 연결 또는 웹사이트 접근을 확인해주세요.")

    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

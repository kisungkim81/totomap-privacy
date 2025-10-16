import requests
from bs4 import BeautifulSoup
import csv
import time
import re

# 읍/면/동 레벨의 추가 검색어
ADDITIONAL_KEYWORDS = [
    '읍', '면', '동', '가', '리',
    '로또', '복권', '편의점', 'GS25', 'CU', '세븐일레븐', '이마트24',
    '마트', '슈퍼', '문방구', '분식', '카페',
    # 자주 누락되는 작은 도시/군
    '고성', '양구', '인제', '철원', '화천', '홍천', '횡성', '평창', '정선', '영월',
    '단양', '괴산', '증평', '음성', '진천', '옥천', '영동', '보은',
    '금산', '부여', '서천', '청양', '홍성', '예산', '태안',
    '고창', '부안', '순창', '임실', '장수', '진안', '무주',
    '강진', '고흥', '곡성', '구례', '담양', '무안', '보성', '신안', '영광', '영암', '완도', '장성', '장흥', '진도', '함평', '해남', '화순',
    '고령', '군위', '봉화', '성주', '영덕', '영양', '예천', '울릉', '울진', '의성', '청도', '청송', '칠곡',
    '거창', '고성', '남해', '산청', '의령', '창녕', '하동', '함안', '함양', '합천'
]

def load_existing_stores():
    """기존 CSV 파일에서 이미 수집된 판매점 로드"""
    existing = set()
    try:
        with open('app/src/main/assets/lotto_stores.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row['Name'], row['Address'])
                existing.add(key)
    except:
        pass
    return existing

def collect_remaining_stores():
    """추가 키워드로 누락된 판매점 수집"""

    base_url = "https://www.fullayer.com/lottostore/fo/lottostorelist"

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.fullayer.com/lottostore/fo/lottostorelist',
    })

    # 기존 데이터 로드
    existing_stores = load_existing_stores()
    print(f"기존 수집된 판매점: {len(existing_stores):,}개")

    new_stores = []

    print("="*60)
    print(f"추가 키워드 검색으로 누락 판매점 수집")
    print(f"총 {len(ADDITIONAL_KEYWORDS)}개 키워드 검색")
    print("="*60)

    for idx, keyword in enumerate(ADDITIONAL_KEYWORDS, 1):
        print(f"\n[{idx:3d}/{len(ADDITIONAL_KEYWORDS)}] '{keyword}' 검색 중...")

        page = 1
        max_pages = 100
        keyword_count = 0

        while page <= max_pages:
            try:
                data = {
                    's_pagenum': str(page),
                    's_pagesize': '20',
                    's_like_lts_name': '',
                    's_like_lts_addr': keyword,
                    's_like_lts_place2': '',
                }

                response = session.post(base_url, data=data, timeout=30)
                soup = BeautifulSoup(response.text, 'html.parser')

                table = soup.find('table')
                if not table:
                    break

                tbody = table.find('tbody')
                if not tbody:
                    break

                rows = tbody.find_all('tr')
                if not rows:
                    break

                page_count = 0
                for row in rows:
                    try:
                        cols = row.find_all('td')
                        if len(cols) >= 3:
                            name = cols[0].get_text(strip=True)
                            phone = cols[1].get_text(strip=True)
                            address = cols[2].get_text(strip=True)

                            longitude = ''
                            latitude = ''

                            map_btn = cols[3].find('a') if len(cols) > 3 else None
                            if map_btn and map_btn.has_attr('onclick'):
                                onclick = map_btn['onclick']
                                coords = re.findall(r"mapModal\([^,]+,\s*'([^']+)',\s*'([^']+)'", onclick)
                                if coords:
                                    longitude = coords[0][0]
                                    latitude = coords[0][1]

                            if name and address:
                                # 중복 체크 (기존 + 새로운)
                                key = (name, address)
                                if key not in existing_stores:
                                    # 이미 new_stores에 있는지도 체크
                                    if key not in [(s['name'], s['address']) for s in new_stores]:
                                        new_stores.append({
                                            'name': name,
                                            'phone': phone,
                                            'address': address,
                                            'latitude': latitude,
                                            'longitude': longitude
                                        })
                                        page_count += 1
                                        keyword_count += 1
                    except Exception as e:
                        continue

                if page_count == 0:
                    break

                page += 1
                time.sleep(0.1)

            except Exception as e:
                break

        if keyword_count > 0:
            print(f"  → '{keyword}': +{keyword_count}개 (누적 신규: {len(new_stores):,}개)")

        time.sleep(0.2)

    return new_stores, existing_stores

def main():
    new_stores, existing_stores = collect_remaining_stores()

    print(f"\n{'='*60}")
    print(f"추가 수집된 판매점: {len(new_stores):,}개")
    print(f"기존 판매점: {len(existing_stores):,}개")
    print(f"전체 판매점: {len(existing_stores) + len(new_stores):,}개")
    print('='*60)

    if new_stores:
        # 기존 CSV에 추가
        output_file = 'app/src/main/assets/lotto_stores.csv'

        # 기존 데이터 읽기
        existing_data = []
        with open(output_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_data.append(row)

        # 새 데이터 추가하여 다시 쓰기
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['Name', 'Address', 'Latitude', 'Longitude']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            # 기존 데이터
            for store in existing_data:
                writer.writerow(store)

            # 신규 데이터
            for store in new_stores:
                writer.writerow({
                    'Name': store['name'],
                    'Address': store['address'],
                    'Latitude': store['latitude'],
                    'Longitude': store['longitude']
                })

        print(f"\n데이터가 {output_file}에 업데이트되었습니다.")

        # 통계 정보
        all_stores = existing_data + [{'Latitude': s['latitude'], 'Longitude': s['longitude']} for s in new_stores]
        with_coords = sum(1 for s in all_stores if s.get('Latitude') and s.get('Longitude'))
        print(f"좌표 정보 있음: {with_coords:,}개 ({with_coords/len(all_stores)*100:.1f}%)")
    else:
        print("\n추가로 수집된 판매점이 없습니다.")

if __name__ == "__main__":
    main()

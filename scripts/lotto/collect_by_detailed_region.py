import requests
from bs4 import BeautifulSoup
import csv
import time
import re

# 서울 전체 구
SEOUL_GU = [
    '강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구',
    '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구',
    '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구'
]

# 부산 전체 구/군
BUSAN_GU = [
    '강서구', '금정구', '기장군', '남구', '동구', '동래구', '부산진구', '북구',
    '사상구', '사하구', '서구', '수영구', '연제구', '영도구', '중구', '해운대구'
]

# 대구 전체 구/군
DAEGU_GU = [
    '군위군', '남구', '달서구', '달성군', '동구', '북구', '서구', '수성구', '중구'
]

# 인천 전체 구/군
INCHEON_GU = [
    '강화군', '계양구', '남동구', '동구', '미추홀구', '부평구', '서구', '연수구', '옹진군', '중구'
]

# 광주 전체 구
GWANGJU_GU = [
    '광산구', '남구', '동구', '북구', '서구'
]

# 대전 전체 구
DAEJEON_GU = [
    '대덕구', '동구', '서구', '유성구', '중구'
]

# 울산 전체 구/군
ULSAN_GU = [
    '남구', '동구', '북구', '울주군', '중구'
]

# 경기도 주요 시/군
GYEONGGI_SI = [
    '가평군', '고양시', '과천시', '광명시', '광주시', '구리시', '군포시', '김포시',
    '남양주시', '동두천시', '부천시', '성남시', '수원시', '시흥시', '안산시', '안성시',
    '안양시', '양주시', '양평군', '여주시', '연천군', '오산시', '용인시', '의왕시',
    '의정부시', '이천시', '파주시', '평택시', '포천시', '하남시', '화성시'
]

# 기타 지역 (시/군 단위로)
OTHER_REGIONS = [
    '세종특별자치시',
    '강원', '춘천', '원주', '강릉', '동해', '태백', '속초', '삼척',
    '충북', '청주', '충주', '제천',
    '충남', '천안', '공주', '보령', '아산', '서산', '논산', '계룡', '당진',
    '전북', '전주', '군산', '익산', '정읍', '남원', '김제',
    '전남', '목포', '여수', '순천', '나주', '광양',
    '경북', '포항', '경주', '김천', '안동', '구미', '영주', '영천', '상주', '문경', '경산',
    '경남', '창원', '진주', '통영', '사천', '김해', '밀양', '거제', '양산',
    '제주', '제주시', '서귀포'
]

def collect_by_detailed_search():
    """세부 지역(구/군/시)별로 검색하여 모든 데이터 수집"""

    base_url = "https://www.fullayer.com/lottostore/fo/lottostorelist"

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.fullayer.com/lottostore/fo/lottostorelist',
    })

    all_stores = []

    # 모든 검색 키워드 준비
    all_search_keywords = (
        [f"서울 {gu}" for gu in SEOUL_GU] +
        [f"부산 {gu}" for gu in BUSAN_GU] +
        [f"대구 {gu}" for gu in DAEGU_GU] +
        [f"인천 {gu}" for gu in INCHEON_GU] +
        [f"광주 {gu}" for gu in GWANGJU_GU] +
        [f"대전 {gu}" for gu in DAEJEON_GU] +
        [f"울산 {gu}" for gu in ULSAN_GU] +
        [f"경기 {si}" for si in GYEONGGI_SI] +
        OTHER_REGIONS
    )

    print("="*60)
    print(f"세부 지역별 검색으로 전체 로또 판매점 수집")
    print(f"총 {len(all_search_keywords)}개 지역 검색")
    print("="*60)

    for idx, keyword in enumerate(all_search_keywords, 1):
        print(f"\n[{idx:3d}/{len(all_search_keywords)}] {keyword} 검색 중...")

        page = 1
        max_pages = 500
        region_count = 0

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
                                # 중복 체크
                                key = (name, address)
                                if key not in [(s['name'], s['address']) for s in all_stores]:
                                    all_stores.append({
                                        'name': name,
                                        'phone': phone,
                                        'address': address,
                                        'latitude': latitude,
                                        'longitude': longitude
                                    })
                                    page_count += 1
                                    region_count += 1
                    except Exception as e:
                        continue

                if page_count == 0:
                    break

                if page % 5 == 0:
                    print(f"  페이지 {page}: +{page_count}개 (지역: {region_count}개, 누적: {len(all_stores):,}개)")

                page += 1
                time.sleep(0.15)

            except Exception as e:
                print(f"  페이지 {page} 오류: {e}")
                break

        if region_count > 0:
            print(f"  → {keyword}: {region_count}개 수집 완료")

        time.sleep(0.3)

    return all_stores

def main():
    stores = collect_by_detailed_search()

    print(f"\n{'='*60}")
    print(f"총 {len(stores):,}개 판매점 수집 완료!")
    print('='*60)

    if stores:
        # CSV 파일로 저장
        output_file = 'app/src/main/assets/lotto_stores.csv'
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['Name', 'Address', 'Latitude', 'Longitude']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for store in stores:
                writer.writerow({
                    'Name': store['name'],
                    'Address': store['address'],
                    'Latitude': store['latitude'],
                    'Longitude': store['longitude']
                })

        print(f"\n데이터가 {output_file}에 저장되었습니다.")

        # 통계 정보
        with_coords = sum(1 for s in stores if s['latitude'] and s['longitude'])
        print(f"좌표 정보 있음: {with_coords:,}개 ({with_coords/len(stores)*100:.1f}%)")

if __name__ == "__main__":
    main()

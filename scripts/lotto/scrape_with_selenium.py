#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Selenium을 사용한 로또 판매점 데이터 수집

Requirements:
    pip install selenium

Chrome WebDriver 필요:
    https://chromedriver.chromium.org/downloads
    또는
    pip install webdriver-manager

작성일: 2025-10-16
"""

import csv
import time
from typing import List, Dict

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select, WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
except ImportError:
    print("❌ Selenium이 설치되지 않았습니다.")
    print("설치 명령: pip install selenium webdriver-manager")
    exit(1)

# 17개 시도 코드
SIDO_CODES = {
    '서울특별시': '11',
    '부산광역시': '26',
    '대구광역시': '27',
    '인천광역시': '28',
    '광주광역시': '29',
    '대전광역시': '30',
    '울산광역시': '31',
    '세종특별자치시': '36',
    '경기도': '41',
    '강원도': '42',
    '충청북도': '43',
    '충청남도': '44',
    '전라북도': '45',
    '전라남도': '46',
    '경상북도': '47',
    '경상남도': '48',
    '제주특별자치도': '50'
}

def setup_driver():
    """
    Chrome WebDriver 설정
    """
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service

        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 백그라운드 실행
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=service, options=options)
        print("✓ Chrome WebDriver 설정 완료 (webdriver-manager)")
        return driver
    except:
        # webdriver-manager 없이 시도
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        try:
            driver = webdriver.Chrome(options=options)
            print("✓ Chrome WebDriver 설정 완료")
            return driver
        except Exception as e:
            print(f"❌ Chrome WebDriver 실행 실패: {e}")
            print("\n해결 방법:")
            print("1. Chrome WebDriver 다운로드: https://chromedriver.chromium.org/")
            print("2. 또는 webdriver-manager 설치: pip install webdriver-manager")
            return None

def scrape_lotto_stores_selenium() -> List[Dict]:
    """
    Selenium을 사용하여 로또 판매점 데이터 수집
    """
    driver = setup_driver()
    if not driver:
        return []

    all_stores = []

    try:
        url = "https://dhlottery.co.kr/store.do?method=sellerInfo645"
        print(f"\n접속 중: {url}")
        driver.get(url)
        time.sleep(2)

        # 시/도 선택
        sido_select = Select(driver.find_element(By.ID, "sltSIDO2"))

        for sido_name in SIDO_CODES.keys():
            print(f"\n[{sido_name}] 검색 중...")

            try:
                # 시/도 선택
                sido_select.select_by_visible_text(sido_name)
                time.sleep(1)

                # 검색 버튼 클릭
                search_btn = driver.find_element(By.CSS_SELECTOR, "a[href*='javascript:$.searchList']")
                search_btn.click()
                time.sleep(2)

                # 결과 테이블 파싱
                page = 1
                while True:
                    try:
                        # 테이블 찾기
                        table = driver.find_element(By.CSS_SELECTOR, "table.tbl_data")
                        rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # 헤더 제외

                        if not rows:
                            break

                        for row in rows:
                            cols = row.find_elements(By.TAG_NAME, "td")
                            if len(cols) >= 3:
                                name = cols[0].text.strip()
                                address = cols[1].text.strip()
                                phone = cols[2].text.strip()

                                if name and address:
                                    all_stores.append({
                                        'name': name,
                                        'address': address,
                                        'phone': phone
                                    })

                        print(f"  페이지 {page}: {len(rows)}개 (누적: {len(all_stores)}개)")

                        # 다음 페이지
                        try:
                            next_btn = driver.find_element(By.LINK_TEXT, "다음")
                            next_btn.click()
                            time.sleep(1)
                            page += 1
                        except NoSuchElementException:
                            break

                    except NoSuchElementException:
                        break

                print(f"[{sido_name}] 완료: {len(all_stores)}개")

            except Exception as e:
                print(f"  [오류] {sido_name} 검색 실패: {e}")
                continue

    finally:
        driver.quit()

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
                '',  # Latitude
                '',  # Longitude
                store.get('phone', '')
            ])

    print(f"✓ 저장 완료: {len(stores)}개 판매점")

def main():
    print("=" * 70)
    print("        동행복권 로또 판매점 데이터 수집 (Selenium)")
    print("=" * 70)

    stores = scrape_lotto_stores_selenium()

    if stores:
        print(f"\n총 {len(stores)}개 판매점 수집 완료")
        save_to_csv(stores)
        print("\n✓ 완료!")
    else:
        print("\n❌ 데이터 수집 실패")

if __name__ == "__main__":
    main()

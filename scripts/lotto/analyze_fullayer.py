#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fullayer 사이트 구조 분석
"""

import requests
from bs4 import BeautifulSoup

url = "https://www.fullayer.com/lottostore/fo/lottostorelist"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

print("페이지 요청 중...")
response = requests.get(url, headers=headers)

print(f"상태 코드: {response.status_code}")
print(f"응답 길이: {len(response.text)} bytes")

soup = BeautifulSoup(response.text, 'html.parser')

# 테이블 찾기
tables = soup.find_all('table')
print(f"\n테이블 개수: {len(tables)}")

# tbody 찾기
tbodies = soup.find_all('tbody')
print(f"tbody 개수: {len(tbodies)}")

if tbodies:
    tbody = tbodies[0]
    rows = tbody.find_all('tr')
    print(f"첫 번째 tbody의 행 개수: {len(rows)}")

    if rows:
        print(f"\n첫 번째 행:")
        print(rows[0].prettify()[:500])

# onclick이 있는 tr 찾기
onclick_rows = soup.find_all('tr', {'onclick': True})
print(f"\nonclick이 있는 tr 개수: {len(onclick_rows)}")

if onclick_rows:
    print(f"\n첫 번째 onclick 행:")
    print(onclick_rows[0].prettify()[:500])

# form 찾기
forms = soup.find_all('form')
print(f"\nform 개수: {len(forms)}")

if forms:
    form = forms[0]
    print(f"\n첫 번째 form:")
    print(f"  action: {form.get('action')}")
    print(f"  method: {form.get('method')}")
    print(f"  id: {form.get('id')}")

# script 태그에서 AJAX URL 찾기
scripts = soup.find_all('script')
print(f"\nscript 태그 개수: {len(scripts)}")

for i, script in enumerate(scripts[:3]):
    if script.string and ('ajax' in script.string.lower() or 'dataList' in script.string):
        print(f"\n[Script {i}]:")
        print(script.string[:500])

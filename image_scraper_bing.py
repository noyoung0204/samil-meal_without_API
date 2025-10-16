import json
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re

# 메뉴 리스트
menu_list = [
  "대패제육덮밥", "미소장국", "새우까스", "배추김치", "컵과일",
  "핫치즈오야꼬동", "콩나물국", "근대된장무침", "만두탕수", "나박김치", "참쌀약과",
  "간장돼지불고기", "고로케", "케찹", "배추김치", "쿠앤크케이크",
  "김치알밥", "꼬치어묵국", "아몬드멸치볶음", "양념감자", "치폴레폭립", "백김치", "펑리수휘낭시에",
  "참치마요덮밥", "우동국물", "찰도그롤", "알감자콘버터구이", "배추김치", "레드자몽음료",
  "아욱된장국", "수육", "무생채", "부추무침", "약고추장", "보쌈김치", "과일푸딩", "야채스틱", "상추", "쌈장",
  "참치유부롤초밥", "치아바타샌드위치", "후레이크샐러드", "흑임자드레싱", "분모자로제떡볶이", "불고기피자", "백김치", "딸기우유",
  "찰보리밥", "김치찌개", "간장찜닭", "건파래볶음", "츠쿠네", "배추겉절이",
  "육개장", "계란찜", "미니돈까스", "석박지", "과일코너", "초코볼",
  "토마토스파게티", "치킨샐러드", "끌레도르아이스크림", "단무지오이피클", "갈릭바게트",
  "차조밥", "된장찌개", "츄러스떡맛탕", "훈제돈육구이", "무쌈", "배추김치", "망고음료",
  "카레소스", "완두콩밥", "양배추샐러드", "지코바닭다리구이", "배추김치", "마카롱",
  "미소부타동", "유부맑은국", "하와이안샐러드", "에그참치브리또", "배추김치", "허쉬크림파이",
  "수수밥", "돈육짜글이찌개", "꼬치없는소떡", "단호박옥수수치즈구이", "배추겉절이", "옥수수라떼", "요구르트",
  "햄야채볶음밥", "김치우동", "시리얼과일샐러드", "닭꼬치튀김", "배추김치", "사과음료",
  "흑미밥", "조랭이떡국", "오코노미야키카츠", "배추김치", "미니딸기롤케이크", "야채스틱",
  "양송이스프", "하트버거", "콘슬로우", "회오리감자", "이온음료"
]

# Bing 이미지 검색 함수
def get_bing_image_url(query):
    headers = {
        "User-Agent": UserAgent().random
    }
    url = f"https://www.bing.com/images/search?q={query}+음식&form=HDRSC3"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    image_elements = soup.find_all("a", {"class": "iusc"})
    for img in image_elements:
        m = img.get("m")
        if m:
            match = re.search(r'"murl":"(.*?)"', m)
            if match:
                return match.group(1)
    return None

# 이미지 수집 및 파일 저장
def main():
    results = {}
    for menu in menu_list:
        print(f"🔍 검색 중: {menu}")
        img_url = get_bing_image_url(menu)
        results[menu] = img_url
    print("✅ 이미지 수집 완료")

    # 결과 HTML 저장
    html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>급식 이미지</title>
        <style>
            body { font-family: sans-serif; background: #f4f4f4; padding: 30px; }
            .item { margin: 20px 0; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
            img { max-width: 300px; border-radius: 12px; }
        </style>
    </head>
    <body>
        <h1>🍱 급식 이미지 자동 수집 결과</h1>
    """
    for menu, img_url in results.items():
        if img_url:
            html += f"""
            <div class="item">
                <h2>{menu}</h2>
                <img src="{img_url}" alt="{menu}">
            </div>
            """
        else:
            html += f"""
            <div class="item">
                <h2>{menu}</h2>
                <p>❌ 이미지 없음</p>
            </div>
            """
    html += "</body></html>"

    with open("menu_images.html", "w", encoding="utf-8") as f:
        f.write(html)

    # JS에 쓸 JSON 파일 저장
    with open("image_map.js", "w", encoding="utf-8") as f:
        f.write("const imageMap = ")
        json.dump(results, f, ensure_ascii=False, indent=2)
        f.write(";")

    print("✅ HTML 및 image_map.js 파일 생성 완료")

if __name__ == "__main__":
    main()

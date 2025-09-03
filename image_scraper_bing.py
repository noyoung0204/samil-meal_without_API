import json
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re

# 메뉴 리스트
menu_list = [
    "혼합잡곡밥", "소고기미역국", "매콤돼지갈비찜", "콘샐러드", "배추김치", "딸기케이크",
    "흑미밥", "건새우아욱된장국", "크림떡볶이", "쌈닭파채무침*쌈무", "배추김치",
    "현미밥", "참치마요무침*김구이", "북어콩나물국", "등갈비바베큐구이", "배추김치", "황금카스테라빵",
    "차조밥", "근대된장국", "제육볶음", "삼색전", "배추겉절이", "패션후르츠라떼", "양배추쌈", "오이스틱", "쌈장",
    "우동국물", "푸실리루끌라샐러드", "지코바 치밥", "배추김치", "초코마들렌", "별별소떡",
    "기장밥", "소고기무국", "숙주나물", "소시지볶음", "멕시코식콘립", "배추김치", "리치캐모마일음료", "꿀자몽블랙티음료",
    "콘크림스프", "감말랭이과일샐러드", "고구마치즈롤까스", "배추김치", "오레오와플",
    "찰보리밥", "우거지된장국", "스크램블에그", "매콤푸삼볶음", "배추겉절이", "수제고르곤졸라또띠아",
    "밥버거", "계란국", "오이고추된장무침", "지파이", "슈니첼", "까두기", "리얼블랙케이크",
    "비빔밥", "팽이버섯장국", "단호박범벅", "약고추장", "핫도그", "백김치", "초코우유",
    "차수수밥", "쑥갓어묵국", "오리고기김치볶음", "햄감자구이", "총각김치", "라임아이스티", "야채스틱",
    "햄치즈크로플버거", "그린샐러드”키위드레싱", "나시고랭볶음밥", "카다이프 새우튀김", "배추김치", "생크림요거트", "수박음료",
    "유부맑은국", "쫄면무침", "돈까스덮밥", "배추김치", "망고스틱", "후르츠마카로니샐러드",
    "전주 베테랑 칼국수", "오징어 초무침", "수원왕갈비통닭/후라이드통닭", "석박지", "과일코너", "쿨피스",
    "김밥볶음밥", "부산식 물떡볶이", "오징어튀김", "야채튀김", "배추김치", "황금란", "샤인애플 음료",
    "혼합잡곡밥", "청경채무침", "갈릭버터닭다리살구이", "폴더 와플",
    "삼각주먹밥", "풀드포크버거", "그래놀라샐러드", "웨지감자", "크런치 바",
    "완두콩밥", "자장소스", "버터진미채구이", "탕수육", "깍두기", "젤리블리",
    "차조밥", "근대된장국", "돼지갈비찜", "(자율)샐러드*딸기드레싱", "도토리묵무침", "배추김치", "설빙아이스크림",
    "후리가케밥", "참치양념", "비빔면", "고기만두", "유린기", "배추김치", "포카리스웨트"
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

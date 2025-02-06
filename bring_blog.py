
# 네이버 검색 API 예제 - 블로그 검색
import os
import urllib.request
import json
from dotenv import load_dotenv

# .env 파일을 읽어 환경변수로 설정
load_dotenv()


tags = ['#우리FIS아카데미', "우리FISA", "#AI엔지니어링","#K디지털트레이닝","#우리에프아이에스","#글로벌소프트웨어캠퍼스"]
encTags = [urllib.parse.quote(tag) for tag in tags]
query = '&'.join([f"q={term}" for term in encTags])

client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")

# url 생성
url = "https://openapi.naver.com/v1/search/blog?query=" + query + "&display=5" + "&sort=sim"

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
else:
    print("Error Code:" + rescode)

# 결과를 파일로 저장
with open('blog_search_result.json', 'w') as f:
    f.write(response_body.decode('utf-8'))

# JSON 파일 읽기
with open('blog_search_result.json', 'r') as f:
    json_data = f.read()

    # JSON 파싱
    data = json.loads(json_data)

    # Markdown 파일 생성
    with open('README.md', 'w', encoding='utf-8') as f:
        # Markdown 헤더 작성
        f.write(f"# AI_엔지니어링 학습일지챌린지! 네이버블로그 엿보기\n\n")
        f.write(f"마지막 업데이트: {data['lastBuildDate']}\n")
        f.write(f"표시 블로그 수: {data['display']}\n\n")
        f.write(f"---\n\n")

        for i, item in enumerate(data['items'], 1):
            f.write(f"## {i}. {item['title']}\n")
            f.write(f"- 블로그: [{item['bloggername']}]({item['bloggerlink']})\n")
            f.write(f"- 링크: {item['link']}\n")
            f.write(f"- 포스팅 날짜: {item['postdate'][:4]}-{item['postdate'][4:6]}-{item['postdate'][6:]}\n")
            f.write(f"- 부분글: {item['description']}\n\n")

    print("Markdown 파일이 생성되었습니다.")
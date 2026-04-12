import requests
import xml.etree.ElementTree as ET
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def get_trending_keywords():
    """
    구글 트렌드 일간 급상승 검색어(한국) RSS 패치를 통해
    오늘 날짜의 강력한 실시간 트렌드 키워드들을 추출합니다.
    (웹 크롤링 차단이 없는 가장 안정적인 방법)
    """
    url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=KR"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        trends = []
        
        # XML에서 최근 급상승 검색어 추출
        for item in root.findall(".//item"):
            title = item.find("title")
            if title is not None and title.text:
                trends.append(title.text)
                
        if not trends:
            return ["스마트폰 거치대", "무선 충전기", "홈트레이닝 기구"]
            
        # 상위 10개만 리턴
        return trends[:10]
        
    except Exception as e:
        print(f"[Error] 트렌드 크롤링 실패: {e}")
        return ["스탠바이미 가성비", "캠핑용 랜턴", "단백질 보충제"]

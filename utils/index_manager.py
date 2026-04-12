import os
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

def request_google_indexing(url):
    """
    Google Indexing API를 통해 URL의 생성, 업데이트 내역을 즉시 알립니다.
    """
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "service_account.json")
    if not os.path.exists(creds_path):
        print(f"[Warning] {creds_path} 파일을 찾을 수 없어 Google Indexing을 생략합니다.")
        return False
        
    try:
        credentials = service_account.Credentials.from_service_account_file(
            creds_path, scopes=["https://www.googleapis.com/auth/indexing"]
        )
        service = build("indexing", "v3", credentials=credentials)
        response = service.urlNotifications().publish(
            body={"url": url, "type": "URL_UPDATED"}
        ).execute()
        print(f"[Success] Google Indexing 요청 완료: {response}")
        return True
    except Exception as e:
        print(f"[Error] Google Indexing API 통신 오류: {e}")
        return False

def request_indexnow(url):
    """
    IndexNow (Bing, Naver 등) API를 통해 URL 생성을 구글 외 검색엔진에 알립니다.
    """
    host = os.environ.get("BLOG_HOST", "myblog.github.io")
    key = os.environ.get("BING_API_KEY", "your_bing_indexnow_key") # 사이트에 등록한 텍스트 파일명과 동일해야 함
    
    endpoint = "https://api.indexnow.org/indexnow"
    payload = {
        "host": host,
        "key": key,
        "keyLocation": f"https://{host}/{key}.txt",
        "urlList": [url]
    }
    
    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"[Success] IndexNow 핑 전송 완료!")
            return True
        else:
            print(f"[Warn] IndexNow 응답 문제: {response.status_code}")
            return False
    except Exception as e:
        print(f"[Error] IndexNow 통신 오류: {e}")
        return False

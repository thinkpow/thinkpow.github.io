import os
import time
import hmac
import hashlib
import requests
import urllib.parse
from tenacity import retry, wait_exponential, stop_after_attempt

def generate_hmac(method, url, secret_key, access_key):
    path, *query = url.split("?")
    datetime = time.strftime('%y%m%d', time.gmtime()) + 'T' + time.strftime('%H%M%S', time.gmtime()) + 'Z'
    message = datetime + method + path + (query[0] if query else "")
    signature = hmac.new(bytes(secret_key, "utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"CEA algorithm=HmacSHA256, access-key={access_key}, signed-date={datetime}, signature={signature}"

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def get_coupang_products(keyword, limit=3):
    """
    쿠팡 파트너스 API를 이용하여 실제 키워드 기반 인기 상품 데이터를 가져옵니다.
    """
    access_key = os.environ.get("COUPANG_ACCESS_KEY")
    secret_key = os.environ.get("COUPANG_SECRET_KEY")
    
    if not access_key or not secret_key or access_key == "쿠팡_액세스키":
        print("[Warn] 쿠팡 API 키가 없습니다. API를 호출하지 못했습니다.")
        return []
        
    domain = "https://api-gateway.coupang.com"
    # 쿠팡 상품 검색 API
    url_path = f"/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword={urllib.parse.quote(keyword)}&limit={limit}"
    
    auth = generate_hmac("GET", url_path, secret_key, access_key)
    headers = {
        "Authorization": auth,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(domain + url_path, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        products = []
        for item in data.get("data", {}).get("productData", []):
            products.append({
                "productName": item.get("productName", ""),
                "productPrice": item.get("productPrice", 0),
                "productUrl": item.get("productUrl", ""),
                "productImage": item.get("productImage", "")
            })
        return products
    except Exception as e:
        print(f"[Error] 쿠팡 API 통신 실패: {e}")
        return []

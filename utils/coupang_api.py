import os
import time
import hmac
import hashlib
import json
import urllib.request
import urllib.parse
import urllib.error
from tenacity import retry, wait_exponential, stop_after_attempt

def generate_hmac(method, url, secret_key, access_key):
    path, *query = url.split("?")
    datetime = time.strftime('%y%m%d', time.gmtime()) + 'T' + time.strftime('%H%M%S', time.gmtime()) + 'Z'
    message = datetime + method + path + (query[0] if query else "")
    signature = hmac.new(bytes(secret_key, "utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"CEA algorithm=HmacSHA256, access-key={access_key}, signed-date={datetime}, signature={signature}"

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def get_coupang_products(keyword, limit=5):
    """
    쿠팡 파트너스 API를 이용하여 실제 키워드 기반 인기 상품 데이터를 가져옵니다.
    """
    access_key = os.environ.get("COUPANG_ACCESS_KEY", "").strip()
    secret_key = os.environ.get("COUPANG_SECRET_KEY", "").strip()
    
    if not access_key or not secret_key or access_key == "쿠팡_액세스키":
        print("[Warn] 쿠팡 API 키가 없습니다. API를 호출하지 못했습니다.")
        return []
        
    domain = "https://api-gateway.coupang.com"
    url_path = f"/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword={urllib.parse.quote(keyword)}&limit={limit}"
    
    auth = generate_hmac("GET", url_path, secret_key, access_key)
    
    req = urllib.request.Request(domain + url_path)
    req.add_header("Authorization", auth)
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0")
    
    try:
        res = urllib.request.urlopen(req, timeout=10)
        data = json.loads(res.read().decode("utf-8"))
        
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
        print(f"[Error] 쿠팡 API 통신 실패 (키/IP 미승인 등): {e}")
        # API 실패로 인해 AI가 가짜 이미지를 생성해 엑스박스가 뜨는 것을 방지
        fallback_data = []
        for i in range(1, limit + 1):
            fallback_data.append({
                "productName": f"[{keyword}] 추천 가성비 아이템 {i}",
                "productPrice": 29900 + (i * 1000),
                "productUrl": "https://link.coupang.com/a/dummy",
                "productImage": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80"
            })
        return fallback_data

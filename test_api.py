from dotenv import load_dotenv
load_dotenv()
import urllib.request
import urllib.parse
import urllib.error
import os
import time
import hmac
import hashlib
import json

access_key = os.environ.get('COUPANG_ACCESS_KEY', '').strip()
secret_key = os.environ.get('COUPANG_SECRET_KEY', '').strip()
keyword = '노트북'
domain = 'https://api-gateway.coupang.com'
url_path = '/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword=' + urllib.parse.quote(keyword) + '&limit=5'

path, *qn = url_path.split('?')
dt = time.strftime('%y%m%d', time.gmtime()) + 'T' + time.strftime('%H%M%S', time.gmtime()) + 'Z'
msg = dt + 'GET' + path + (qn[0] if qn else '')
sig = hmac.new(bytes(secret_key, 'utf-8'), msg.encode('utf-8'), hashlib.sha256).hexdigest()
auth = f'CEA algorithm=HmacSHA256, access-key={access_key}, signed-date={dt}, signature={sig}'

req = urllib.request.Request(domain + url_path)
req.add_header('Authorization', auth)
req.add_header('Content-Type', 'application/json')
req.add_header('User-Agent', 'Mozilla/5.0')

try:
    res = urllib.request.urlopen(req)
    print('SUCCESS:', res.read().decode('utf-8')[:300])
except urllib.error.URLError as e:
    print('ERROR:', e.reason)
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))

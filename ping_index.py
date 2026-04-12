import os
from dotenv import load_dotenv
from utils.index_manager import request_indexnow, request_google_indexing

def main():
    load_dotenv()
    if not os.path.exists('latest_posted_url.txt'):
        print('[Error] latest_posted_url.txt 파일을 찾을 수 없어 핑을 생략합니다.')
        return

    with open('latest_posted_url.txt', 'r', encoding='utf-8') as f:
        final_url = f.read().strip()

    print(f'>> 핑 전송 시작 (대상 URL: {final_url})')
    request_indexnow(final_url)
    request_google_indexing(final_url)
    print('>> 성공적으로 색인 핑 전송을 마쳤습니다!')

if __name__ == '__main__':
    main()

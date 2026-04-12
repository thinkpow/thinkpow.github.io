import os
import datetime
from dotenv import load_dotenv
from crewai import Crew, Process

from agents import create_scout_agent, create_analyst_agent, create_writer_agent, create_visualizer_agent
from tasks import task_extract_trends, task_select_products, task_write_post, task_create_sns_content

from utils.naver_api import get_trending_keywords
from utils.coupang_api import get_coupang_products
from utils.index_manager import request_indexnow

def main():
    # 1. 환경 설정
    load_dotenv()
    if not os.environ.get("GOOGLE_API_KEY"):
        print("[!] GOOGLE_API_KEY가 설정되지 않았습니다. .env 파일을 확인해주세요.")
        return

    print("🚀 [Discerning Review Agent] 자동화 파이프라인 시작 🚀")

    # 2. 외부 API 데이터 수집 (사전 Context 확보)
    print("\n[Step 1] 네이버/외부 트렌드 스캔 중...")
    trends = get_trending_keywords()
    print(f"👉 확인된 트렌드: {trends}")

    # 3. 에이전트 및 태스크 초기화
    scout = create_scout_agent()
    analyst = create_analyst_agent()
    writer = create_writer_agent()
    visualizer = create_visualizer_agent()

    t_trends = task_extract_trends(scout)
    t_trends.description += f"\n\n* 조사된 데이터: {trends}"
    
    t_products = task_select_products(analyst)
    # 첫번째 태스크 결과와 별도로, 크루 실행 중 동적으로 API를 주입하는 대신
    # 여기서는 임의로 첫번째 요소 기반으로 데이터를 가져와 컨텍스트로 전달
    target_keyword = trends[0] 
    print(f"\n[Step 2] 쿠팡 스캔 중 (키워드: {target_keyword})...")
    products_info = get_coupang_products(target_keyword)
    t_products.description += f"\n\n* 조사된 상품 데이터:\n{products_info}"

    t_write = task_write_post(writer)
    t_sns = task_create_sns_content(visualizer)

    # 4. Crew 구성 및 킥오프
    print("\n[Step 3] AI Crew 활동 개시 (사고 과정 시뮬레이션)...")
    crew = Crew(
        agents=[scout, analyst, writer, visualizer],
        tasks=[t_trends, t_products, t_write, t_sns],
        process=Process.sequential, # 선형 파이프라인
        verbose=True
    )

    crew_result = crew.kickoff()

    # 5. 결과물 정리 및 파일 시스템 저장
    print("\n[Step 4] 산출물 로컬 저장 중...")
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    clean_keyword = target_keyword.replace(' ', '-')
    
    os.makedirs("_posts", exist_ok=True)
    post_filename = f"_posts/{today_date}-{clean_keyword}.md"
    
    # 최근 CrewAI는 task.output.raw 형태로 값을 반환합니다.
    blog_body = t_write.output.raw if hasattr(t_write.output, 'raw') else str(t_write.output)
    sns_body = t_sns.output.raw if hasattr(t_sns.output, 'raw') else str(t_sns.output)

    with open(post_filename, "w", encoding="utf-8") as f:
        f.write(blog_body)
    
    with open("sns_contents.txt", "w", encoding="utf-8") as f:
        f.write("=== SNS 파생 콘텐츠 (영상/카드뉴스) ===\n\n")
        f.write(sns_body)

    print(f"✅ 블로그 작성 완료: {post_filename}")
    print(f"✅ SNS 스크립트 작성 완료: sns_contents.txt")

    # 6. Indexing 작업 
    print("\n[Step 5] 포스트 색인 요청...")
    # 예시 URL (실제 배포 사이트 구조에 맞춰 수정 필요)
    blog_host = os.environ.get("BLOG_HOST", "myusername.github.io")
    final_url = f"https://{blog_host}/{today_date.replace('-','/')}/{clean_keyword}.html"
    
    # 깃헙 배포가 끝난 뒤에 호출되는 것이 이상적이나, 우선 핑을 전송해 둠
    request_indexnow(final_url)

    print("\n🚀 모든 운영 자동화 파이프라인이 성공적으로 끝났습니다.")

if __name__ == "__main__":
    main()

from crewai import Task

def task_extract_trends(scout_agent):
    return Task(
        description="""사전 조사된 급상승 검색어 목록 데이터가 주어집니다. 
        이 중 쇼핑 전환율과 콘텐츠 작성 매력도가 가장 높을 것으로 예상되는 핵심 키워드 1개를 고르세요. 
        이유도 1줄로 짧게 덧붙이세요.""",
        expected_output="선정된 1개의 핵심 키워드 및 간략한 이유",
        agent=scout_agent
    )

def task_select_products(analyst_agent):
    return Task(
        description="""선정된 트렌드 키워드를 바탕으로 조사된 쿠팡 상품들(5개) 중, 
        가장 좋은 상품 2개를 '메인 리뷰용'으로 확정하고, 나머지 3개는 '추가 추천 상품용'으로 분류하십시오.
        [주의] 상품 이미지 링크는 반드시 원본 데이터의 `productImage` (thumbnail...coupangcdn.com 형태)를 그대로 사용하십시오.
        상품별명, 가격, 장점 요약, productImage 링크, 수익화 URL 리스트를 명확히 분리해 반환하세요.""",
        expected_output="엄선된 상품 2개의 핵심 속성과 원본 수익화 링크 구조 리스트",
        agent=analyst_agent
    )

def task_write_post(writer_agent):
    return Task(
        description="""전달받은 5개의 상품 정보를 활용하여 지갑을 열게 만드는 구매 가이드를 작성하세요.
        
        [필수 규칙]
        1. Jekyll 호환용 yaml Front-matter를 최상단에 작성 (title, date, categories, tags)
        2. [이미지 에러 방지] 쿠팡 데이터는 상품당 단 1개의 `productImage` 링크만 제공합니다. 따라서 메인 리뷰 상품(1, 2번) 설명 시 **해당 상품별로 제공된 productImage 1개만** 정확히 마크다운 문법(`![alt](이미지주소)`)으로 삽입하고, 절대로 가짜 이미지 주소(via.placeholder.com 등)를 지어내어 여러 장을 그리도록 하지 말 것.
        3. 모든 상품 링크는 제공된 쿠팡 수익화 URL(`[상품 보러가기](url)`)을 사용할 것.
        4. [추가 추천] 메인 상품 2개의 상세 리뷰가 끝난 뒤 문서 하단에 '💡 리뷰언니의 추가 추천 상품 BEST 3' 등과 같은 섹션을 만들어, 나머지 3개 상품의 이름, 가격, 간단 특징, 수익화 URL을 짤막하게 리스트 형태로 보여줄 것.
        5. 마지막 줄에는 반드시: "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다." 기입.
        6. 오직 마크다운 텍스트 원문만 텍스트로 출력! 절대 ```markdown 이나 ```yaml 코드블럭으로 문서를 통째로 감싸지 말 것.
        """,
        expected_output="완성된 마크다운 포스팅 원문",
        agent=writer_agent
    )

def task_create_sns_content(visualizer_agent):
    return Task(
        description="""블로그 포스팅의 핵심 내용을 바탕으로 아래 2가지 SNS 콘텐츠를 기획하세요:
        1. 유튜브 쇼츠/틱톡용 15초 분량 스크립트 (시선을 강탈하는 훅 강제 포함, 대사 위주)
        2. 인스타그램 카드뉴스 4컷 (각 컷별 들어갈 텍스트와, 배경 이미지 생성을 위한 Midjourney 스타일 영문 프롬프트)
        결과물은 마크다운으로 정리해 반환하세요.
        """,
        expected_output="숏폼 스크립트 및 카드뉴스 프롬프트 텍스트",
        agent=visualizer_agent
    )

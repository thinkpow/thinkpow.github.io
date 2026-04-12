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
        description="""선정된 트렌드 키워드를 바탕으로 조사된 여러 쿠팡 상품들 중, 
        가장 리뷰가 좋고 가성비가 훌륭해 구매 전환을 일으킬 수 있는 최정예 상품 2개를 확정하십시오.
        상품명, 가격, 장점 요약, 상품 이미지 링크, 그리고 수익화 URL을 정리해 반환하세요.""",
        expected_output="엄선된 상품 2개의 핵심 속성과 원본 수익화 링크 구조 리스트",
        agent=analyst_agent
    )

def task_write_post(writer_agent):
    return Task(
        description="""전달받은 2개의 상품 정보를 활용하여, 방문자가 결국 지갑을 열게 만드는 구매 가이드 블로그를 작성하세요.
        
        [필수 규칙]
        1. Jekyll/Hugo 호환용 yaml Front-matter를 최상단에 작성 (title, date, categories, tags)
        2. 마크다운(`![alt텍스트](이미지주소)`)을 이용해 상품 이미지를 콘텐츠 사이에 자연스럽게 배치할 것
        3. 모든 상품 링크는 제공된 쿠팡 수익화 링크(`[상품 보러가기](url)`)를 사용할 것
        4. 문서 맨 밑단에는 반드시 다음 문구를 추가할 것: 
           "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."
        5. 오직 마크다운 형식의 결과물만 출력할 것.
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

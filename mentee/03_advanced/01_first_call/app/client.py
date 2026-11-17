"""Day22 · 첫 실제 응답 | PPT 6~13 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""

"""
Responses API의 첫 요청 생성부터 응답 처리,
결과 요약 및 안전성 검증까지 수행하는 함수들을 구현한다.

API 호출에 필요한 요청 형식을 구성하고,
출력 데이터가 허용된 정보만 포함하도록 검증한다.
"""

def make_first_request(model, instructions, question, selected, *, structured=False):
    # TODO D22-01-A01: 첫 요청의 model·instructions·input·출력 상한·store를 완성하세요.
    # 입력·완료 기준: 입력은 전달받은 값입니다. 새 질문·임의 모델을 하드코딩하지 않으며 JSON Schema는 다음 교시입니다.
    # BEGIN D22-01-A01

    # Responses API 요청 데이터 생성
    # - model : 사용할 모델
    # - instructions : 시스템 지시문
    # - input : 사용자 질문
    # - max_output_tokens : 최대 출력 길이 제한
    # - store=False : 응답 저장 비활성화
    request = {"model": model, "instructions": instructions, "input": question,
               "reasoning": {"effort": "none"}, "max_output_tokens": 1200,
               "store": False, "service_tier": "default"}
    return request
    # model은 전달값, input은 question, 출력 상한1200, store=False
    # raise NotImplementedError("D22-01-A01: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-01-A01

def create_response(client, request, stream=False):
    # TODO D22-01-A02: Responses API를 한 번 호출하고 반환값을 돌려주세요.
    # 입력·완료 기준: 키를 직접 문자열로 쓰지 않습니다. 한 함수 호출은 create 한 번만 수행합니다.
    # BEGIN D22-01-A02

    # 요청 딕셔너리를 API 호출 형식으로 변환
    options = dict(request)  # 힌트: 이미 만든 요청 딕셔너리
    # Responses API 호출
    # - stream 여부에 따라 일반 응답 또는 스트리밍 응답 생성
    response = client.responses.create(**options, stream=stream)  # 힌트: client.responses.create(**options, stream=stream)
    return response
    # raise NotImplementedError("D22-01-A02: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-01-A02

def make_view(result):
    # TODO D22-01-A03: 키 없이 source·model·종료 상태·응답 ID를 요약하세요.
    # 입력·완료 기준: 미실행이면 response_id는 None입니다. 0이나 가짜 응답 ID를 채우지 않습니다.
    # BEGIN D22-01-A03

    # 마지막 실행 결과 조회
    # - 실행 이력이 없으면 빈 객체 사용
    last = result.get("attempts", [])[-1] if result.get("attempts") else {}
    # 화면 출력용 요약 데이터 생성
    # - 실행 모드
    # - 사용 모델
    # - 실행 상태
    # - 응답 ID
    summary = {"source_mode": result["source_mode"], "model": result.get("model"), "run_status": result["run_status"], "response_id": last.get("response_id")}
    return summary
    # 힌트: result와 last에서 같은 필드명을 읽습니다.
    # raise NotImplementedError("D22-01-A03: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-01-A03

def setting_cases():
    # TODO D22-01-A04: 키 미설정과 모델 접근 오류의 차이를 모의 비교표에 적으세요.
    # 입력·완료 기준: 반복 실제 호출로 오류를 만들지 않습니다. 모델 접근 거부는 403/404 등 공급자 원인을 봅니다.
    # BEGIN D22-01-A04

    # 대표 오류 상황 비교 데이터
    # - missing_key : API 키 미설정
    # - model_denied : 모델 접근 권한 없음
    cases = [{"case":"missing_key", "where":"local_settings", "new_api_send_count":0},
            {"case":"model_denied", "where":"provider_permission", "simulated_send_count":1}]  # 각 행에 case·where·전송 수를 구분합니다.
    return cases
    # raise NotImplementedError("D22-01-A04: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-01-A04

def check_safe_view(view):
    # TODO D22-01-A05: 기록할 필드를 허용 목록으로 제한하는 assertion을 완성하세요.
    # 입력·완료 기준: 설정 객체 전체를 JSON에 넣지 않습니다. 필드 허용 목록은 내용의 전면적 비밀 탐지기가 아닙니다.
    # BEGIN D22-01-A05

    # JSON 출력 허용 필드 목록
    allowed = {"source_mode","model","run_status","response_id"}
    # 허용된 필드만 포함되는지 검증
    assert set(view) == allowed
    # 인증 정보 포함 여부 검증
    assert "api_key" not in view and "Authorization" not in view
    return True
    # raise NotImplementedError("D22-01-A05: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-01-A05

"""
Responses API 요청 객체를 생성하고,
create 호출을 통해 실제 응답을 반환하도록 구현하였다.

또한 실행 결과를 화면 출력용 데이터로 요약하고,
대표 오류 상황 비교 데이터 제공 및 허용 필드 기반의 안전성 검증 기능을 추가하였다.
"""
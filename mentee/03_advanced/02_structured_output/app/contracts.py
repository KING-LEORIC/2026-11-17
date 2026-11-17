"""Day22 · 메시지와 출력 계약 | PPT 14~23 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
# JSON 직렬화 기능 제공
# - Python 객체를 JSON 문자열로 변환
import json
# 요청 생성 및 출력 형식 정의
# - WireAnswer : 응답 출력 스키마
# - OUTPUT_FORMAT : 공급자용 출력 형식 정의
# - checkpoint_request : 기본 요청 생성 함수
from coursekit.request import WireAnswer, OUTPUT_FORMAT, build_request as checkpoint_request
# 응답 데이터 접근 유틸리티
# - get : 안전한 필드 조회
# - output_text : 응답 본문 추출
from coursekit.response import get, output_text

"""
사용자 질문과 선택된 지식을 요청 메시지로 구성하고,
구조화 출력을 위한 Schema를 Responses API 요청 형식에 연결한다.

또한 응답 상태를 검증하여 예외 상황을 구분하고,
Wire Schema가 요구하는 출력 계약을 만족하는지 확인한다.
"""

def make_request(model, instructions, question, selected, *, structured=True):
    # TODO D22-02-A01: 질문과 선택 지식만 user input으로 직렬화하세요.
    # 입력·완료 기준: selected_ids가 아닌 선택된 지식의 id·title·content·category를 보냅니다. expected_behavior는 넣지 않습니다.
    # BEGIN D22-02-A01

    # 사용자 입력 데이터 구성
    # - 질문
    # - 선택된 지식 목록
    payload = {"question": question, "knowledge": selected}  # 이번 selected를 넣습니다.
    # JSON 문자열로 직렬화
    # - 한글이 유니코드로 변환되지 않도록 설정
    serialized = json.dumps(payload, ensure_ascii=False)  # json.dumps(..., ensure_ascii=False)
    # raise NotImplementedError("D22-02-A01: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-02-A01
    # TODO D22-02-A02: 공급자용 Schema를 요청의 text.format으로 연결하세요.
    # 입력·완료 기준: response_format이 아니라 Responses의 text.format입니다. Wire와 로컬 KnowledgeAnswer는 다릅니다.
    # BEGIN D22-02-A02

    # 기본 요청 템플릿 생성
    request = checkpoint_request(model, instructions, question, selected, structured=False)
    # 사용자 메시지 등록
    # - 직렬화된 질문 및 지식 전달
    request["input"] = [{"role":"user", "content":serialized}]  # role="user", content=serialized
    # 구조화 출력 형식 지정
    # - OUTPUT_FORMAT Schema 적용
    request["text"] = {"format" : OUTPUT_FORMAT}   # {"format": OUTPUT_FORMAT}
    return request
    # raise NotImplementedError("D22-02-A02: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-02-A02

def response_gate(response):
    # TODO D22-02-A03: 거절 콘텐츠와 미완료 상태를 먼저 구분하세요.
    # 입력·완료 기준: API status와 answer JSON의 status는 다릅니다. 거절을 형식 오류로 바꾸지 않습니다.
    # BEGIN D22-02-A03

    # 응답 메시지 검사
    # - 모델의 거절 응답 여부 확인
    for item in get(response, "output", []) or []:
        if get(item, "type") == "message":
            for part in get(item, "content", []) or []:
                if get(part,"type")=="refusal":
                    return None, "refused"  # refusal이면 None, "refused" 반환
    # API 처리 상태 확인
    # - completed 상태만 정상 처리
    if get(response, "status") != "completed":  # completed가 아니면 오류 반환
        return None,get(response,"status") or "response_error"
    # raise NotImplementedError("D22-02-A03: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-02-A03
    # TODO D22-02-A04: 완료 응답에서도 빈 본문을 검사한 뒤 원문을 반환하세요.
    # 입력·완료 기준: 원문을 수정해 유효한 JSON처럼 만들지 않습니다. 로컬 검증기는 다음 단계에서 실행됩니다.
    # BEGIN D22-02-A04

    # 응답 본문 추출
    raw = output_text(response)
    # 빈 응답 차단
    if not raw.strip():
        return None, "empty_output"
    return raw, None
    # 힌트: 공백을 제거한 결과가 비어 있으면 (None, "empty_output")
    # raise NotImplementedError("D22-02-A04: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-02-A04

def choose_cases():
    # TODO D22-02-A05: 정상 질문 D02와 정보 부족 질문 D03의 순서를 지정하세요.
    # 입력·완료 기준: 실제 호출 2개입니다. 부족 응답은 유효한 업무 결과일 수 있습니다.
    # BEGIN D22-02-A05

    # 실습 케이스 실행 순서
    # - D02 : 정상 응답 확인
    # - D03 : 정보 부족 응답 확인
    cases = ["D02", "D03"]  # D02는102, D03은101을 제공합니다.
    return cases
    # raise NotImplementedError("D22-02-A05: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-02-A05

def check_wire_schema():
    # TODO D22-02-A06: Wire Schema의 네 필드 필수·추가 필드 금지를 검사하세요.
    # 입력·완료 기준: 이 검사로 로컬 길이·출처·사실성 규칙까지 통과했다고 말하지 않습니다.
    # BEGIN D22-02-A06

    # Wire Schema 정의 조회
    schema = WireAnswer.model_json_schema()
    # 필수 필드 검증
    assert set(schema["required"])=={"status","answer","source_ids","missing_information"}
    # 정의되지 않은 필드 허용 금지
    assert schema["additionalProperties"] is False
    return True
    # raise NotImplementedError("D22-02-A06: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-02-A06

"""
질문과 선택된 지식을 JSON 형태로 직렬화하여 사용자 메시지로 전달하고,
OUTPUT_FORMAT을 이용한 구조화 출력 요청을 구성하도록 구현하였다.

또한 응답 거절 여부와 완료 상태를 검증하고,
빈 응답을 차단하도록 처리하였다.

마지막으로 WireAnswer Schema의 필수 필드 구성과
추가 필드 금지 규칙을 검증하여 출력 계약 준수 여부를 확인하도록 구현하였다.
"""

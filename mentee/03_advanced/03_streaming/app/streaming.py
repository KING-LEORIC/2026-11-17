"""Day22 · Streaming과 완료 판정 | PPT 24~31 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
# 응답 데이터 접근 유틸리티
# - get : 객체 속성을 안전하게 조회
from coursekit.response import get

"""
스트리밍 응답 이벤트를 수신하여 부분 출력과 최종 응답을 구분하고,
첫 출력 시간 및 전체 요청 시간을 측정한다.

또한 완료 이벤트 유무를 검증하여
스트리밍 처리 과정의 정상 동작 여부를 확인한다.
"""

def receive_event(state, event, clock, started):
    state.events_seen += 1
    kind = get(event,"type")
    if kind == "response.output_text.delta":
        # TODO D22-03-A01: 비어 있지 않은 첫 텍스트의 시간과 delta를 누적하세요.
        # 입력·완료 기준: clock은 단조 시계입니다. 빈 delta를 첫 표시로 세지 않습니다.
        # BEGIN D22-03-A01

        # 스트리밍 텍스트 조각 추출
        delta = get(event, "delta", "")
        # 프로토콜 오류 검사
        # - 문자열이 아닌 delta 차단
        if not isinstance(delta,str):
            state.error="stream_protocol_error"
            return
        # 첫 출력 시점 기록
        # - 빈 문자열은 제외
        if delta and state.first_text_ms is None:
            state.first_text_ms=(clock()-started)*1000
            # pass  # (clock() - started) * 1000
        # state.parts.append(...)로 누적. delta 개수는 Token 수가 아닙니다.

        # 수신된 텍스트 누적
        # - delta 개수는 토큰 수와 다름
        state.parts.append(delta)
        # raise NotImplementedError("D22-03-A01: TODO를 완성하고 이 raise를 제거하세요")
        # END D22-03-A01
    elif kind in {"response.completed","response.incomplete","response.failed"}:
        # TODO D22-03-A02: 최종 이벤트의 Response를 보관하세요.
        # 입력·완료 기준: 부분 문자열을 합쳤다고 completed를 직접 만들어서는 안 됩니다.
        # BEGIN D22-03-A02
        # 중복 terminal이면 오류, 아니면 state.final에 event.response 저장

        # 완료 이벤트 중복 여부 검사
        if state.final_response is not None:
            state.error="duplicate_terminal_event"
        # 최종 Response 저장
        state.final_response = get(event,"response")
        # final_response = get(event, "response")
        # raise NotImplementedError("D22-03-A02: TODO를 완성하고 이 raise를 제거하세요")
        # END D22-03-A02
    elif kind == "error":
        # 스트리밍 처리 중 오류 발생
        state.error="stream_error"

def streaming_choice():
    # TODO D22-03-A03: 실제 스트리밍을 요청하도록 선택값을 반환하세요.
    # 입력·완료 기준: 메시지 UI를 새로 만드는 실습이 아닙니다. 최종 상태·부분 파일·first_text_ms를 확인합니다.
    # BEGIN D22-03-A03

    # 스트리밍 모드 활성화
    use_stream = True  # True이면 Responses stream=True
    return use_stream
    # raise NotImplementedError("D22-03-A03: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-03-A03

def compare_runs():
    # TODO D22-03-A04: 동일 입력의 비스트리밍과 스트리밍 순서를 지정하세요.
    # 입력·완료 기준: --action compare에서만 2회 호출합니다. 기본 run은 스트리밍1회입니다.
    # BEGIN D22-03-A04

    # 실행 모드 비교
    # - False : 일반 응답
    # - True : 스트리밍 응답
    modes = [False, True]  # 두 경우만 비교하며 출력 문장 일치를 강요하지 않습니다.
    return modes
    # raise NotImplementedError("D22-03-A04: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-03-A04

def timing_view(result):
    # TODO D22-03-A05: 첫 표시 시간과 전체 요청 시간을 분리해 요약하세요.
    # 입력·완료 기준: 미표시인 None과 실제 관측0은 다릅니다. 시뮬레이션 시간을 실제 LLM 속도로 해석하지 않습니다.
    # BEGIN D22-03-A05

    # 성능 측정 결과 요약
    # - first_text_ms : 첫 출력까지 걸린 시간
    # - request_ms : 요청 처리 시간
    # - e2e_ms : 전체 처리 시간
    view = {"source_mode" : result["source_mode"], "first_text_ms" : result.get("first_text_ms"),
            "request_ms" : result.get("request_ms"), "e2e_ms" : result.get("e2e_ms")}  # 각 값은 result에서 읽고 None을0으로 바꾸지 않습니다.
    return view
    # raise NotImplementedError("D22-03-A05: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-03-A05

def check_no_terminal():
    # TODO D22-03-A06: 완료 이벤트가 없으면 최종 Response가 없는지 모의 검사하세요.
    # 입력·완료 기준: raw가 있다는 이유로 성공 처리하지 않는 분기 검사입니다.
    # BEGIN D22-03-A06
    
    # 스트리밍 상태 객체 제공
    # - 이벤트 처리 결과 저장
    # - 부분 응답 및 최종 응답 관리
    from coursekit.response import StreamState
    # 테스트용 객체 생성 유틸리티
    # - event 객체 모의 생성에 사용
    # - 속성 방식(event.type) 접근 지원
    from coursekit.fixtures import namespace
    # 스트리밍 상태 객체 생성
    state = StreamState()
    # delta 이벤트만 전달하고 final이 없는지 확인합니다.

    # delta 이벤트만 전달
    # - 완료 이벤트 없이 부분 출력만 존재하는 상황 검증
    receive_event(state,namespace({"type":"response.output_text.delta","delta":"partial"}),lambda:1.0,0.0)
    # 최종 응답이 생성되지 않아야 함
    assert state.final is None and state.parts==["partial"]
    return True
    # raise NotImplementedError("D22-03-A06: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-03-A06

"""
스트리밍 이벤트에서 출력 조각을 누적하고,
첫 응답 표시 시점을 측정하도록 구현하였다.

또한 완료 이벤트 수신 시 최종 Response를 저장하고,
비스트리밍과 스트리밍 실행 모드를 비교할 수 있도록 구성하였다.

마지막으로 완료 이벤트 없이 부분 출력만 존재하는 경우를 검증하여,
최종 응답 생성 여부를 올바르게 판정하도록 구현하였다.
"""
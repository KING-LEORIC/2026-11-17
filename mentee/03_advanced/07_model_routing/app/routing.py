"""Day22 · 명시적 모델 선택 | PPT 53~59 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
# coursekit 설정 모듈에서 모델 선택 기능 사용
# - checkpoint_choose : 지정된 모드에 맞는 모델을 반환하는 함수
from coursekit.config import choose_model as checkpoint_choose

# 실행 모드에 따른 모델 라우팅 함수
# - mode : 요청된 실행 모드 ("fast" 또는 "quality")
# - models : 사용 가능한 모델 설정 딕셔너리
def route(mode, models):
    # TODO D22-07-A01: fast·quality만허용하고실제모델과선택이유를반환하세요.
    # 입력·완료 기준: 알수없는모드를fast로조용히바꾸지않습니다. quality권한없으면not_run입니다.
    # BEGIN D22-07-A01

    # 허용된 실행 모드 집합 정의
    allowed = {"fast", "quality"}
    # model = None   # models.get(mode), 미설정은오류
    # reason = ""    # explicit_mode:<mode>
    # checkpoint_choose(mode, models)를이용할수있습니다.
    
    # mode가 허용된 모드 목록에 포함되지 않는 경우
    if mode not in allowed:
        # 지원하지 않는 실행 모드 에러 발생
        raise ValueError("지원하지 않는 실행 모드")
    # 허용된 모드인 경우 체크포인트 모델 선택 함수 호출 결과 반환
    return checkpoint_choose(mode, models)
    # raise NotImplementedError("D22-07-A01: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-07-A01

# 실행 결과 레코드를 뷰 형태로 가공하는 함수
# - result : 원본 실행 결과 딕셔너리
def record_view(result):
    # TODO D22-07-A02: 어떤모델이든동일한결과필드로비교하세요.
    # 입력·완료 기준: 고가모델이항상더좋다는결론을미리넣지않습니다.
    # BEGIN D22-07-A02
    
    # 비교에 사용할 표준 결과 필드 목록 정의
    fields = ["case_id", "source_mode", "model", "route_reason", "run_status",
              "answer_object", "evidence_ok", "usage", "request_ms", "estimated_usd"]
    # 딕셔너리 컴프리헨션을 이용해 지정된 필드만 추출하여 새 딕셔너리 생성
    row = {key: result.get(key) for key in fields}  # {key: result.get(key) for key in fields}
    # 가공된 결과 행 반환
    return row
    # raise NotImplementedError("D22-07-A02: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-07-A02

# 비교 모드 목록을 반환하는 함수
# - 명시적 비교 테스트를 위한 모드 리스트 구성
def comparison_modes():
    # TODO D22-07-A03: 명시적비교에서만fast·quality를한번씩선택하세요.
    # 입력·완료 기준: 기본run은한모델만호출합니다. compare는계정권한·예산확인후선택합니다.
    # BEGIN D22-07-A03

    # fast와 quality 모드가 각각 한 번씩 포함된 리스트 정의
    modes = ["fast", "quality"]  # fast와quality각한번, while fallback금지
    # 모드 목록 반환
    return modes
    # raise NotImplementedError("D22-07-A03: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-07-A03

# 알 수 없는 모드 요청 시 예외 발생 여부를 모의 검사하는 함수
# - 잘못된 모드 입력에 대한 방어 로직 검증
def reject_unknown_mode():
    # TODO D22-07-A04: 잘못된mode가호출전에오류인지모의검사하세요.
    # 입력·완료 기준: 인증오류를다른모델이나계정으로우회하지않습니다.
    # BEGIN D22-07-A04
    # route("unknown", models)는ValueError여야합니다. 실제전송하지않습니다.

    try:
        # 잘못된 모드로 route 함수 호출 시도
        route("unknown", {"fast": "example"})
    except ValueError:
        # ValueError 예외가 정상적으로 발생한 경우 검증 성공 처리
        return True
    # 예외가 발생하지 않은 경우 테스트 실패 처리
    raise AssertionError("잘못된 모드를 허용했습니다.")
    # raise NotImplementedError("D22-07-A04: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-07-A04

# 설정되지 않은 quality 모드 처리 검사 함수
# - quality 모드가 미설정 상태일 때 자동 대체되지 않는지 확인
def check_unconfigured_quality():
    # TODO D22-07-A05: quality가미설정이면다른모델로자동대체하지않는지확인하세요.
    # 입력·완료 기준: 선택정책검사는simulated이고두모델실제비교와구분합니다.
    # BEGIN D22-07-A05

    # coursekit 설정 모듈에서 설정 오류 예외 클래스 임포트
    from coursekit.config import SetupError
    # quality=None에대한예외를확인합니다.

    try:
        # quality가 None인 설정으로 route 함수 호출 시도
        route("quality", {"fast" : "example", "quality" : None})
    except SetupError:
        # SetupError 예외가 정상적으로 발생한 경우 검증 성공 처리
        return True
    # 예외가 발생하지 않은 경우 테스트 실패 처리
    raise AssertionError("quality 미설정을 통과했습니다.")
    # raise NotImplementedError("D22-07-A05: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-07-A05

# 근거 검증 뷰 결과를 확인하는 함수
# - 자동 검증 결과를 임의로 변경하지 않는지 검증
def check_evidence_view():
    # TODO D22-07-A06: 자동검증결과를사람의근거승인으로만들지않는지확인하세요.
    # 입력·완료 기준: 공통결과구조의None을임의True로바꾸지않습니다.
    # BEGIN D22-07-A06

    # run_status와 evidence_ok 상태를 포함한 딕셔너리로 record_view 호출
    row = record_view({"run_status" : "validated", "evidence_ok" : None})
    # evidence_ok 필드가 여전히 None으로 유지되는지 단언문으로 확인
    assert row["evidence_ok"] is None
    # 검증 통과 시 True 반환
    return True
    # raise NotImplementedError("D22-07-A06: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-07-A06


"""
Day22 과정의 명시적 모델 선택 및 라우팅 정책을 검증하도록 구현하였다.
route 함수를 통해 실행 모드를 엄격히 제어하며, 잘못된 모드나 미설정된 모델에 대해서는 적절한 예외 처리가 수행되도록 구성하였다.
또한 레코드 가공 및 비교 모드 검증 함수들을 포함하여 안정적인 모델 비교 실행 경로를 보장한다.
"""
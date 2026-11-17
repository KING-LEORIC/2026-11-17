"""Day22 · 오류와 제한 재시도 | PPT 32~38 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
# 기본 오류 분류 기능 제공
# - 공통 오류 유형 식별
# - 기본 재시도 여부 판단
from coursekit.errors import classify_error as checkpoint_classify
# 재시도 정책 객체 제공
# - 재시도 횟수 제한 관리
# - 전송 예산 관리
from coursekit.runner import RetryPolicy

"""
인증 오류와 속도 제한 오류를 구분하여 재시도 여부를 결정하고,
재시도 정책 및 대기 시간을 계산한다.

또한 재시도 횟수와 종료 조건을 검증하여
불필요한 재전송이 발생하지 않도록 확인한다.
"""

def classify(error):
    # TODO D22-04-A01: 401·403은 중단하고, 429의 quota와 일시적 제한을 구분하세요.
    # 입력·완료 기준: 알 수 없는429는 무조건 재시도하지 않습니다. 실제로 제한을 유발하는 호출은 금지합니다.
    # BEGIN D22-04-A01

    # 오류 상태 코드 및 상세 코드 조회
    status = error.status
    codes = {error.code, error.error_type}
    # 인증 오류
    # - API 키 문제
    # - 재시도로 해결되지 않음
    if status == 401:
        result = {"kind" : "auth_error", "retryable" : False}  # 기다려도 키는 바뀌지 않습니다.
        return result
    # 권한 오류
    # - 모델 접근 권한 없음
    # - 재시도로 해결되지 않음
    if error.status==403:
        result = {"kind" : "permission_error", "retryable" : False}
        return result
    # 할당량 초과
    # - 결제 또는 사용량 한도 도달
    # - 재시도 중단
    elif error.status==429 and codes & {"insufficient_quota", "billing_hard_limit_reached", "billing_not_active", "usage_limit_reached"}:
        result = {"kind":"quota_error","retryable":False}
        return result
    # 일시적 요청 제한
    # - 속도 제한으로 인한 오류
    # - 일정 시간 후 재시도 가능
    elif error.status==429 and codes & {"rate_limit_exceeded", "rate_limit_error", "requests","tokens"}:
        result = {"kind":"rate_limit","retryable":True}
        return result
        # result = {}  # quota이면중단, rate_limit_exceeded면제한 재시도
    # 그 외는 checkpoint_classify(error)를 이용합니다.

    # 정의되지 않은 오류는 기본 분류 사용
    return checkpoint_classify(error)
    # raise NotImplementedError("D22-04-A01: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-04-A01

def make_policy():
    # TODO D22-04-A02: 생성 최대2·생성별 전송최대2·전체 전송최대4를 설정하세요.
    # 입력·완료 기준: SDK max_retries=0은 제공 코드에 설정되어 있습니다. 무한 fallback을 추가하지 않습니다.
    # BEGIN D22-04-A02

    # 재시도 제한 정책 정의
    # - 생성 단계 최대 2회
    # - 단계별 전송 최대 2회
    # - 전체 전송 최대 4회
    limits = {"max_generations": 2, "max_sends_per_generation": 2, "max_sends_total": 4}
    # 재시도 정책 객체 생성 및 반환
    # - 전체 실행 예산 60초 적용
    return RetryPolicy(**limits, elapsed_budget_s=60.0)
    # RetryPolicy(**limits, elapsed_budget_s=60.0)
    # raise NotImplementedError("D22-04-A02: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-04-A02

def delay(attempt, retry_after_s, remaining_s, jitter=0.0):
    # TODO D22-04-A03: 헤더 최소 대기와 지수 대기 중 큰 값을 계산하세요.
    # 입력·완료 기준: 함수에 전달되는 헤더값은 이미 검증된 초 단위입니다.
    # BEGIN D22-04-A03

    # Retry-After 헤더 값 반영
    hinted = 0.0 if retry_after_s is None else retry_after_s
    # 대기 불가능한 상황 검사
    if hinted<0 or remaining_s<=0:
        return None
    # 실제 재시도 대기시간 계산
    # - Retry-After
    # - 지수 백오프
    # - 지터
    wait = max(hinted, min(8.0, 2 ** min(attempt - 1, 3))) + jitter  # max(최소 대기, 지수 대기) + jitter
    # raise NotImplementedError("D22-04-A03: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-04-A03
    # TODO D22-04-A04: 대기시간이 남은 작업 예산 이상이면 None으로 중단하세요.
    # 입력·완료 기준: 대기 후 실행기는 남은 예산과 횟수를 다시 검사합니다.
    # BEGIN D22-04-A04
    # None / wait 중 선택합니다. min(wait, remaining_s)로당기지 않습니다.

    # 남은 예산 내에서만 재시도 허용
    return None if wait >= remaining_s else wait
    # raise NotImplementedError("D22-04-A04: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-04-A04

def check_attempts(results):
    # TODO D22-04-A05: 각 시도의 번호가 누락되지 않고 총4이하인지 확인하세요.
    # 입력·완료 기준: 실패한 첫 시도도 목록에서 지우지 않습니다.
    # BEGIN D22-04-A05
    for result in results:
        attempts = result["attempts"]
        # 번호는1부터연속, 길이는4이하입니다.

        # 전송 횟수 상한 검증
        assert len(attempts) <= 4
        # 시도 번호 연속성 검증
        assert [a["send_attempt"] for a in attempts] == list(range(1, len(attempts) + 1))
    return True
        # pass
    # raise NotImplementedError("D22-04-A05: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-04-A05

def check_terminal(results):
    # TODO D22-04-A06: timeout·거절·할당량에서 전송이1번으로 끝났는지 확인하세요.
    # 입력·완료 기준: 실제 서버 완료 여부를 모르는 timeout은 자동 재전송하지 않습니다.
    # BEGIN D22-04-A06

    # 케이스별 결과 조회
    by_case = {r["case_id"] : r for r in results}
    # 즉시 종료 대상 검증
    # - timeout
    # - refused
    # - quota
    # - auth
    for name in ("timeout", "refused", "quota", "auth"):
        assert by_case[name]["simulated_send_count"] == 1
    return True
    # raise NotImplementedError("D22-04-A06: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-04-A06

def check_shared_budget(results):
    # TODO D22-04-A07: 통신2종과 형식수정이 공유한4회 기록의 generation 번호를 확인하세요.
    # 입력·완료 기준: 모의 전송4번을 실제 과금4회라고 표시하지 않습니다.
    # BEGIN D22-04-A07

    # 공유 예산 사용 사례 조회
    run = next(r for r in results if r["case_id"] == "shared_four")
    # generation 진행 순서 검증
    assert [a["generation_no"] for a in run["attempts"]] == [1, 1, 2, 2]
    # 공유 전송 예산 검증
    assert run["simulated_send_count"] == 4 and run["new_api_send_count"] == 0
    return True
    # raise NotImplementedError("D22-04-A07: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-04-A07

"""
401 인증 오류와 403 권한 오류는 즉시 중단하고,
429 오류는 할당량 초과와 일시적 속도 제한으로 구분하여 처리하도록 구현하였다.

또한 지수 백오프 기반 대기 시간을 계산하고,
재시도 정책의 횟수 제한 및 작업 예산을 검증하도록 구성하였다.

마지막으로 종료 조건과 공유 재시도 예산 사용 내역을 검사하여
재전송 정책이 올바르게 동작하는지 확인하도록 구현하였다.
"""
"""Day22 · AI 지식 답변 생성기 v2 | PPT 60~68 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
# coursekit 러너 모듈에서 재시도 정책 클래스 임포트
# - RetryPolicy : 생성 및 전송 횟수 제한, 시간 예산 설정
from coursekit.runner import RetryPolicy
# coursekit 지표 모듈에서 사용량 읽기 및 실행 요약 함수 임포트
# - checkpoint_usage : 실행 결과에서 사용량 정보를 추출하는 함수
# - summarize_runs : 전체 실행 결과 요약 함수
from coursekit.metrics import read_usage as checkpoint_usage, summarize_runs
# coursekit 레코드 모듈에서 테이블 행 변환 함수 임포트
# - table_rows : 실행 데이터를 테이블 행 형태로 변환
from coursekit.records import table_rows

# 프로젝트 테스트 케이스 목록을 정의하고 반환하는 함수
# - 최종 연동 확인 질문 H01, H02, H03을 순서대로 지정
def project_cases():
    # TODO D22-08-A01: 최종연동확인질문H01·H02·H03을같은순서로지정하세요.
    # 입력·완료 기준: 이미본질문이므로새holdout의일반화성능이라고부르지않습니다.
    # BEGIN D22-08-A01

    # 테스트 케이스 식별자 리스트 정의 (H01은 Streaming 포함)
    cases = ["H01", "H02", "H03"]  # H01→H02→H03. H01은Streaming입니다.
    # 정의된 케이스 리스트 반환
    return cases
    # raise NotImplementedError("D22-08-A01: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-08-A01

# 실행 결과 데이터로부터 테이블 행 데이터를 생성하는 함수
# - runs : 실행 결과 데이터 리스트
def project_rows(runs):
    # TODO D22-08-A02: 각실행의상태·사용량·시간을표행으로연결하세요.
    # 입력·완료 기준: 실패한행도버리지않습니다. 모든질문의예상답을실측답으로채우지않습니다.
    # BEGIN D22-08-A02
    
    # table_rows 함수를 이용해 각 실행의 상태, 사용량, 시간 등을 테이블 행으로 변환
    rows = table_rows(runs)  # table_rows(runs)는unknown과source구분에필요한필드를제공합니다.
    # 변환된 행 데이터 반환
    return rows
    # raise NotImplementedError("D22-08-A02: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-08-A02

# 실행 결과 전체를 요약하는 함수
# - runs : 실행 결과 데이터 리스트
def project_summary(runs):
    # TODO D22-08-A03: 실제·모의·캐시·미실행을분리하여요약하세요.
    # 입력·완료 기준: 소수관찰로P95·SLA·보편적모델우열을주장하지않습니다.
    # BEGIN D22-08-A03

    # summarize_runs 함수를 이용해 실제, 모의, 캐시, 미실행 상태별로 실행 결과 요약 생성
    summary = summarize_runs(runs)  # summarize_runs(runs)
    # 요약 정보 반환
    return summary
    # raise NotImplementedError("D22-08-A03: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-08-A03

# 프로젝트 실행 결과에 대한 자동 검사를 수행하는 함수
# - runs : 실행 결과 데이터 리스트
def check_project(runs):
    # TODO D22-08-A04: 자동검사후사람미평가None을유지하고전송상한을확인하세요.
    # 입력·완료 기준: 사람평가는tools/review.py의별도파일로남깁니다. 새API·DB·RAG는만들지않습니다.
    # BEGIN D22-08-A04

    # 각 실행 항목을 순회하며 검증 수행
    for run in runs:
        # 근거 승인 상태 추출 (사람 평가 전에는 None 유지)
        evidence = run.get("evidence_ok")  # 사람평가전None
        # API 전송 횟수 추출 (기본값 0)
        sends = run.get("new_api_send_count", 0)
        # None유지·전송4이하를assert합니다.
        # pass

        # evidence가 None인지 확인
        assert evidence is None
        # 전송 횟수가 4 이하인지 확인
        assert sends <= 4
    # 검증 통과 시 True 반환
    return True
    # raise NotImplementedError("D22-08-A04: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-08-A04

# 최초 시도와 마지막 시도의 상태를 비교하고 분리하여 보존하는 함수
# - runs : 실행 결과 데이터 리스트
def compare_first_and_last(runs):
    # TODO D22-08-A05: 최초시도와마지막시도의상태를분리하여보존하세요.
    # 입력·완료 기준: 첫실패를마지막성공으로덮어쓰지않습니다.
    # BEGIN D22-08-A05

    # 가공된 행 정보를 저장할 빈 리스트 초기화
    rows = []
    # 각 실행 결과를 순회
    for run in runs:
        # 시도 내역 리스트 추출
        attempts = run.get("attempts", [])
        # first_error·last_status·attempt_count를서로다른필드에보관합니다.
        # pass

        # 실행 ID, 첫 시도 에러, 마지막 실행 상태, 총 시도 횟수, 소스 모드를 딕셔너리로 묶어 추가
        rows.append({"run_id" : run["run_id"], "first_error" : attempts[0].get("error") or attempts[0].get("validation_error") if attempts else None,
                     "last_status" : run["run_status"], "attempt_count" : len(attempts), "source_mode" : run["source_mode"]})
    # 결과 행 리스트 반환
    return rows
    # raise NotImplementedError("D22-08-A05: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-08-A05

# 공유 예산 정책을 정의하고 반환하는 함수
# - 프로젝트 전반에서 사용할 재시도 및 전송 예산 설정
def shared_limits():
    # TODO D22-08-A06: 일일프로젝트에도교안과같은공유예산을반환하세요.
    # 입력·완료 기준: 실제전체20회장부는제공된SendLedger가관리하며다른교시도같은장부를사용합니다.
    # BEGIN D22-08-A06

    # 최대 생성 횟수, 생성당 최대 전송 횟수, 총 전송 횟수, 시간 예산을 포함한 RetryPolicy 객체 생성
    policy = RetryPolicy(max_generations = 2, max_sends_per_generation = 2, max_sends_total = 4, elapsed_budget_s = 60.0)  # RetryPolicy(...)
    # 정책 객체 반환
    return policy
    # raise NotImplementedError("D22-08-A06: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-08-A06

# 미수신 사용량(usage)에 대한 최종 검사 함수
# - 미확인 비용과 실제 0원인 캐시 히트를 구분하는지 검증
def missing_usage_check():
    # TODO D22-08-A07: 미수신usage를0으로바꾸지않는지최종검사하세요.
    # 입력·완료 기준: 최종표에서미확인비용과실제0원인캐시히트를구분합니다.
    # BEGIN D22-08-A07

    # coursekit 픽스처 모듈에서 응답 생성 함수 임포트
    from coursekit.fixtures import response_for
    # usage가 없는 테스트 응답 객체 생성
    response = response_for("H01", usage = False)
    # 미수신 사용량 정보가 None으로 올바르게 반환되는지 단언문으로 확인
    assert checkpoint_usage(response) is None
    # 검증 통과 시 True 반환
    return True
    # raise NotImplementedError("D22-08-A07: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-08-A07

"""
Day22 AI 지식 답변 생성기 v2 과정의 프로젝트 검증 및 메트릭 처리 모듈이다.
테스트 케이스 정의, 실행 결과 덤프 및 요약, 자동 검사 로직, 최초/마지막 시도 분리,
그리고 공유 예산 정책 설정을 구현하여 안정적인 AI 파이프라인 평가 환경을 제공한다.
"""
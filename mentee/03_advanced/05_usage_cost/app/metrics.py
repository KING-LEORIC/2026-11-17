"""Day22 · 사용량·시간·비용 | PPT 39~46 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
# Decimal 연산 지원
# - 비용 계산 시 부동소수점 오차 방지
from decimal import Decimal as D
# JSON 설정 파일 조회 기능 제공
# - 모델별 가격 정보 조회
from coursekit.io import read_json
# 응답 데이터 접근 유틸리티
# - 없는 필드 접근 시 예외 방지
from coursekit.response import get
# 공통 비용 계산기
# - 사용량 및 가격 정보 사전 검증
from coursekit.metrics import estimate_cost as checkpoint_cost

"""
응답 사용량 정보를 추출하고,
모델별 가격표를 이용하여 예상 비용을 계산한다.

또한 실행 기록을 비용 정보와 함께 저장하고,
전체 실행 비용 집계 결과를 검증한다.
"""

def usage_of(response):
    # TODO D22-05-A01: 사용량이 없으면 None, 있으면 입력·출력과부분 상세를 읽으세요.
    # 입력·완료 기준: 없는 값에 or0을 쓰지 않습니다. delta 개수를출력 Token 수로쓰지 않습니다.
    # BEGIN D22-05-A01

    # 사용량 정보 조회
    u = get(response, "usage")
    # 사용량 정보가 없으면 종료
    if u is None:
        return None
    # Token 사용량 구성
    # - 입력 Token
    # - 출력 Token
    # - 캐시 입력 Token
    # - 추론 Token
    # - 전체 Token
    values = {"input_tokens" : get(u,"input_tokens"), "output_tokens" : get(u,"output_tokens"),
              "cached_tokens" : get(get(u,"input_tokens_details"),"cached_tokens"),
              "reasoning_tokens" : get(get(u,"output_tokens_details"),"reasoning_tokens"), "total_tokens" : get(u,"total_tokens")}
    return values
    # u가없으면None. 상세는 get(get(u,"..._details"),"..._tokens")
    # raise NotImplementedError("D22-05-A01: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-05-A01

def calculate(usage, model, *, service_tier="default"):
    checked=checkpoint_cost(usage,model,service_tier=service_tier)
    # 사전 검증 실패 시 기존 결과 반환
    if checked["estimated_usd"] is None:
        return checked
    from coursekit.io import ROOT
    # 모델 가격 정보 조회
    price=read_json(ROOT/"config"/"prices.json")["models"][model]
    # TODO D22-05-A02: 캐시를제외한 입력·캐시입력·출력 비용을 Decimal로 계산하세요.
    # 입력·완료 기준: 가격은 USD/100만Token입니다. reasoning을출력에다시더하지 않습니다. unknown과0구분.
    # BEGIN D22-05-A02

    # Token 사용량 조회
    i = usage["input_tokens"]
    c = usage["cached_tokens"]
    o = usage["output_tokens"]
    # 실제 입력 Token 수
    # - 전체 입력에서 캐시 입력 제외
    uncached = i - c # 입력 전체 - 캐시 입력
    # 모델별 단가 조회
    # - 입력
    # - 캐시 입력
    # - 출력
    pi = D(price["input_per_million"])
    pc = D(price["cached_input_per_million"])
    po = D(price["output_per_million"])
    # 예상 비용 계산
    # - 가격 기준은 100만 Token당 USD
    # - reasoning token은 output에 포함됨
    amount = (uncached * pi + c * pc + o * po) / D(1000000)    # 각 token수×해당단가의 합 / D(1000000)
    # 반환은 dict(checked, estimated_usd=str(amount))

    return dict(checked, estimated_usd = str(amount))
    # raise NotImplementedError("D22-05-A02: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-05-A02

def make_row(result, attempt, cost):
    # TODO D22-05-A03: 시도번호·실행출처·시간·사용량·비용을 같은 행에 남기세요.
    # 입력·완료 기준: 이 도구는 기존 run.json을 읽습니다. 측정을 위해 필요없는유료재호출은하지 않습니다.
    # BEGIN D22-05-A03
    # row = {"run_id": result["run_id"], "source_mode": result["source_mode"]}

    # 실행 결과 요약 행 생성
    # - 실행 정보
    # - 응답 시간
    # - 사용량
    # - 비용 정보
    row = {
        "run_id": result["run_id"],
        "source_mode": result["source_mode"],
        "send_attempt": attempt["send_attempt"],
        "request_ms": attempt["request_ms"],
        "first_text_ms": attempt.get("first_text_ms"),
        "usage": attempt.get("usage"),
        **cost,
    }
    return row
    # attempt에서 send_attempt·request_ms·first_text_ms·usage를읽고 cost와합칩니다.
    # raise NotImplementedError("D22-05-A03: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-05-A03

def unknown_checks():
    # TODO D22-05-A04: usage 없음과 모델 단가 미등록에서 비용이None인지 검사하세요.
    # 입력·완료 기준: 부족한사용량은0원으로확정하지 않습니다.
    # BEGIN D22-05-A04
    # calculate(None, 알려진모델)와 calculate(usage, "unknown")을 검사합니다.

    # 설정 파일의 등록 모델 조회
    # - 비용 계산 가능 모델 사용
    # - usage 누락 상황만 검증
    from coursekit.config import load_settings
    model = load_settings("simulated").models["fast"]
    # 사용량 정보 없음 검증
    assert calculate(None, model)["estimated_usd"] is None
    # 단가 정보 없음 검증
    assert calculate({"input_tokens": 1, "cached_tokens": 0, "output_tokens": 1}, "unknown")["estimated_usd"] is None
    return True
    # raise NotImplementedError("D22-05-A04: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-05-A04

def summarize(attempts):
    # TODO D22-05-A05: 전체비용미확인을보존하는 합산함수를 연결하세요.
    # 입력·완료 기준: known_estimated_usd와total_estimated_usd의 차이를설명합니다.
    # BEGIN D22-05-A05

    # 비용 집계 함수 연결
    # - 확인된 비용 합산
    # - 미확인 비용 개수 집계
    from coursekit.metrics import sum_cost
    result = sum_cost(attempts)
    return result
    # raise NotImplementedError("D22-05-A05: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-05-A05

def check_unknown_total():
    # TODO D22-05-A06: 첫 실패비용이unknown이면 마지막성공만으로총비용을확정하지마세요.
    # 입력·완료 기준: 원래캐시생성비용을캐시hit마다새로합산하지않습니다.
    # BEGIN D22-05-A06

    # 테스트용 비용 집계 데이터
    attempts = [{"source_mode":"api_live", "estimated_usd" : None},
                {"source_mode":"api_live", "estimated_usd" : "0.00138"}]
    # 직접작성한계산샘플입니다. 실제호출기록이아닙니다.

    report = summarize(attempts)
    # 확인 가능한 비용만 합산
    assert report["known_estimated_usd"] == "0.00138"
    # 미확인 비용이 존재하면 전체 비용 확정 불가
    assert report["total_estimated_usd"] is None
    # 미확인 비용 건수 확인
    assert report["unknown_cost_attempts"] == 1
    return True
    # raise NotImplementedError("D22-05-A06: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-05-A06

"""
응답 사용량 정보에서 입력·출력·캐시·추론 Token 수를 추출하고,
모델별 단가를 이용하여 예상 비용을 계산하도록 구현하였다.

또한 실행 결과와 비용 정보를 하나의 기록으로 저장하고,
비용 집계 결과를 통해 확인 가능한 비용과 미확인 비용을 구분하도록 구성하였다.

마지막으로 사용량 정보 누락 및 단가 정보 부재 상황을 검증하여,
비용을 임의로 0으로 계산하지 않도록 처리하였다.
"""
"""Day22 · 승인 응답 캐시 | PPT 47~52 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
# 객체 깊은 복사 기능 제공
# - 원본 데이터 변경 방지
from copy import deepcopy
# 해시 생성 기능 제공
# - 캐시 키 생성
from coursekit.io import digest
# 기본 요청 생성 함수
# - 캐시 키 비교용 요청 생성
from coursekit.request import build_request as checkpoint_request
# 승인 캐시 조회 기능
# - 만료 여부 확인
# - 승인 여부 확인
# - scope 검증 수행
from coursekit.cache import read_cache as checkpoint_cache

"""
요청 내용과 실행 조건을 기반으로 캐시 키를 생성하고,
승인된 캐시 응답 재사용 여부를 판단한다.

또한 문맥, 모델, 권한 범위 및 검증 버전에 따른
캐시 무효화 동작을 검증한다.
"""

def key_of(request, scope, validator_version="day21-v1"):
    # TODO D22-06-A01: 질문뿐 아니라 모델·전체요청·Schema·검증버전·scope로 캐시키를 만드세요.
    # 입력·완료 기준: API키는포함하지않습니다. 전체본문이키에들어가야같은ID의내용변경도감지합니다.
    # BEGIN D22-06-A01

    # 캐시 키 생성 기준 데이터
    # - 실행 범위
    # - 모델 정보
    # - 전체 요청 본문
    # - 출력 형식
    # - 검증 버전
    basis = {"scope" : scope, "model" : request["model"], "request" : request,
             "format" : request.get("text", {}).get("format"), "validator_version" : validator_version}
    # 요청 내용을 해시로 변환
    key = digest(basis)  # digest(basis): 정렬된JSON의SHA-256
    return key
    # raise NotImplementedError("D22-06-A01: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-06-A01

def approved_cache(cache, key, now, provided_ids, *, expected_source, scope):
    # TODO D22-06-A02: 현재문맥·실행출처·scope와함께 제공된 안전한캐시검사를 호출하세요.
    # 입력·완료 기준: 만료·미승인·현재출처불일치는미스입니다. 승인하려면tools/review.py로사람이기록합니다.
    # BEGIN D22-06-A02

    # 승인된 캐시 조회
    # - 만료 검사
    # - 출처 검사
    # - scope 검사
    cached = checkpoint_cache(cache, key, now, provided_ids, expected_source = expected_source, scope = scope)  # checkpoint_cache(..., expected_source=expected_source, scope=scope)
    return cached
    # None은미스입니다. 새답변을가짜로만들지않습니다.
    # raise NotImplementedError("D22-06-A02: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-06-A02

def compare_context_keys():
    # TODO D22-06-A03: 같은ID의본문변경이캐시키를바꾸는지확인하세요.
    # 입력·완료 기준: 이키비교는전송0회의모의검사입니다. 실제재사용은먼저생성·사람승인후reuse명령으로확인합니다.
    # BEGIN D22-06-A03

    # 테스트용 입력 데이터 조회
    from coursekit.io import input_parts
    # 테스트용 모델 조회
    from coursekit.config import load_settings
    case, selected, instructions = input_parts("H01")
    model = load_settings("simulated").models["fast"]
    # 원본 요청 생성
    first = checkpoint_request(model, instructions, case["question"], selected)
    # 선택 지식 복사
    # - 원본 데이터 수정 방지
    changed = deepcopy(selected)  # 원본JSON파일은바꾸지않습니다.
    # changed[0]["content"]수정 → 두번째request → key비교

    # 지식 내용 변경
    # - 동일 ID라도 본문 변경 시 캐시 무효화
    changed[0]["content"]+=" 실행 환경도 함께 적습니다."
    # 변경된 요청 생성
    second=checkpoint_request(model,instructions, case["question"], changed)
    # 캐시 키 변경 확인
    assert key_of(first, "classroom-demo") != key_of(second, "classroom-demo")
    return {"changed_context_miss" : True, "source_mode" : "simulated", "new_api_send_count" : 0}
    # raise NotImplementedError("D22-06-A03: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-06-A03

def model_key_check():
    # TODO D22-06-A04: 모델선택만바뀌어도다른키가되는지확인하세요.
    # 입력·완료 기준: 스트리밍여부는출력전달방식이며요청내생성설정은같게유지합니다.
    # BEGIN D22-06-A04
    # 동일질문·문맥으로fast/quality요청을만들어key를비교합니다. 전송하지않습니다.

    # 실습 입력 데이터 조회
    # - 질문 및 선택 지식 로드
    from coursekit.io import input_parts
    # 실행 설정 조회
    # - 모델 정보 로드
    from coursekit.config import load_settings
    # H01 실습 데이터 로드
    # - case : 질문 정보
    # - rows : 선택 지식 목록
    # - prompt : 시스템 지시문
    case, rows, prompt = input_parts("H01")
    # 시뮬레이션 설정의 fast 모델 조회
    # - 실제 전송 없이 키 비교에 사용
    models = load_settings("simulated").models
    # 모델별 요청 생성
    a = checkpoint_request(models["fast"], prompt, case["question"], rows)
    b = checkpoint_request(models["quality"], prompt, case["question"], rows)
    # 모델 변경 시 캐시 키 변경 확인
    assert key_of(a, "classroom-demo") != key_of(b, "classroom-demo")
    return True
    # raise NotImplementedError("D22-06-A04: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-06-A04

def ttl_check():
    # TODO D22-06-A05: 만료시간에같거나지난캐시가재사용되지않는지검사하세요.
    # 입력·완료 기준: TTL을읽을때마다연장하지않습니다.
    # BEGIN D22-06-A05

    # 만료된 캐시 데이터 구성
    fake = {"k": {"expires_at":10.0, "human_approved":True}}
    # now=10.0이면None입니다.
    
    # 만료 시각 도달 시 캐시 미사용
    assert approved_cache(fake, "k", 10.0, {103}, expected_source = "simulated", scope = "classroom-demo") is None
    return True
    # raise NotImplementedError("D22-06-A05: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-06-A05

def scope_and_version_check():
    # TODO D22-06-A06: 권한범위와검증버전의변경이키를바꾸는지검사하세요.
    # 입력·완료 기준: scope 문자열은실제인증시스템대체물이아닙니다. 학습용권한경계입니다.
    # BEGIN D22-06-A06
    # 동일request에서scope와validator_version을하나씩바꾸어비교합니다.

    # 실습 입력 데이터 조회
    # - 질문
    # - 선택 지식
    # - 시스템 지시문
    from coursekit.io import input_parts
    # 실행 환경 설정 조회
    # - 사용할 모델 정보 제공
    from coursekit.config import load_settings
    # H01 실습 데이터 로드
    # - case : 질문 정보
    # - rows : 선택 지식 목록
    # - prompt : 시스템 지시문
    case, rows, prompt = input_parts("H01")
    # 캐시 키 비교용 요청 생성
    # - fast 모델 사용
    # - 실제 API 전송은 수행하지 않음
    req = checkpoint_request(load_settings("simulated").models["fast"], prompt, case["question"], rows)
    # scope 변경 시 캐시 키 변경 확인
    assert key_of(req, "group-a") != key_of(req, "group-b")
    # 검증 버전 변경 시 캐시 키 변경 확인
    assert key_of(req, "group-a", "v1") != key_of(req, "group-a", "v2")
    return True
    # raise NotImplementedError("D22-06-A06: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-06-A06

def check_cache_accounting(result):
    # TODO D22-06-A07: 캐시히트는새전송0·현재사용량0·원래실행ID를남기는지확인하세요.
    # 입력·완료 기준: 캐시데이터의원출처api_live/simulated를함께보존합니다.
    # BEGIN D22-06-A07

    # 캐시 재사용 결과 검증
    if result["source_mode"] == "app_cache":
        # 캐시 재사용 시 비용 검증
        # - 신규 API 호출 없음
        # - 추가 비용 없음
        assert result["new_api_send_count"] == 0 and result["estimated_usd"] == "0"
        # 캐시 재사용 시 실행 정보 검증
        # - 입력 Token 사용 없음
        # - 원본 실행 ID 유지
        assert result["usage"]["input_tokens"] == 0 and result.get("origin_run_id")  # 새비용·전송·origin을검사합니다.
    return True
    # raise NotImplementedError("D22-06-A07: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-06-A07

"""
전체 요청 내용과 실행 조건을 기반으로 캐시 키를 생성하고,
승인된 캐시 응답만 재사용하도록 구현하였다.

또한 문맥 내용, 모델, 권한 범위 및 검증 버전이 변경될 경우
새로운 캐시 키가 생성되는지 검증하도록 구성하였다.

마지막으로 캐시 재사용 시 추가 전송 및 비용이 발생하지 않고,
원본 실행 정보가 유지되는지 확인하도록 구현하였다.
"""

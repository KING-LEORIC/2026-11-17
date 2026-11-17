"""Day22 · 첫 실제 응답 | PPT 6~13 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
# 파일 및 디렉터리 경로 객체 제공
# - 운영체제 독립적인 경로 처리 지원
from pathlib import Path
# coursekit 실행 지원 함수
# - parse_args : 실행 인자 해석
# - execute_case : 실습 케이스 실행
# - emit : 실행 결과 출력
from coursekit.support import parse_args, execute_case, emit
# JSON 파일 저장 함수
# - Python 객체를 JSON 형식으로 출력
from coursekit.io import write_json

# 클라이언트 기능 모음
# - make_first_request : 첫 요청 데이터 생성
# - create_response : 응답 데이터 생성
# - make_view : 화면 표시용 데이터 생성
# - setting_cases : 설정 예시 데이터 반환
# - check_safe_view : 출력 데이터 안전성 검증
from .client import make_first_request, create_response, make_view, setting_cases, check_safe_view
# 현재 프로젝트 기준 루트 디렉터리
# - __file__ : 현재 파일 경로
# - resolve() : 절대 경로 변환
# - parents[1] : 상위 2단계 디렉터리 선택
HERE=Path(__file__).resolve().parents[1]

"""
실습용 FIRST 케이스를 실행하기 위한 메인 진입점 구현

요청 생성 함수와 응답 생성 함수를 연결하여 실행 흐름을 구성하고,
실행 결과를 JSON 파일로 저장한 뒤 안전성 검증까지 수행한다.
"""

def main():
    # 실행 환경 정보 생성
    # - HERE : 프로젝트 기준 경로
    # 반환값
    # - args : 실행 옵션 객체
    args=parse_args(HERE)
    # FIRST 케이스 실행
    # 인자 설명
    # - args : 실행 환경 정보
    # - "FIRST" : 실행할 케이스 이름
    # - request_builder : 요청 생성 함수
    # - hooks : 실행 과정에서 사용할 사용자 함수 등록
    # hooks 상세
    # - create : 응답 생성 시 create_response 호출
    # 반환값
    # - result : 실행 결과 데이터
    result=execute_case(args,"FIRST",request_builder=make_first_request,hooks={"create":create_response})
    # 실행 결과 출력
    # 인자
    # - args : 출력 설정 정보
    # - result : 출력 대상 데이터
    emit(args,result)
    # 사용자 확인용 View 생성
    # 인자
    # - result : 실행 결과 데이터
    # 반환값
    # - view : 화면 표시용 데이터
    view=make_view(result)
    # 연결 상태 결과 저장
    # 저장 파일
    # - connection_view.json
    write_json(args.output_dir/"connection_view.json",view)
    # 설정 예시 저장
    # 저장 파일
    # - settings_cases.json
    write_json(args.output_dir/"settings_cases.json",setting_cases())
    # 출력 데이터 안전성 검증
    # - 민감정보 노출 여부 확인
    # - 허용된 형식 검증
    check_safe_view(view)

"""
첫 요청 데이터를 생성하여 FIRST 케이스를 실행하고,
실행 결과를 화면 표시용 데이터로 변환하여 JSON 파일로 저장하도록 구현하였다.

또한 설정 예시 데이터를 함께 저장하고,
최종 출력 결과에 대한 안전성 검증을 수행하여 응답 데이터의 무결성과 보안성을 확인하였다.
"""
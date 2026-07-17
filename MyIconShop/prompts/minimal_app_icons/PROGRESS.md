# PROGRESS.md — 아이콘팩 제작 진행 로그

## 세트 전체 진행 상태

| 단계 | 상태 | 비고 |
|---|---|---|
| 이미지 생성 (15종) | 완료 | 아래 표 참고. 전체 성공 |
| 배경 제거 (`etsy_listing/minimal_app_icons/icons/`) | 완료 | 15개 전체를 `remove_background_new.py`(솔리드 방식: 2배 슈퍼샘플링+실루엣 3종 다수결+색확장 디프린지)로 일괄 재처리 (2026-07-12). 구 버전의 잠재 불량(guitar/chat 흰 얼룩, flower 뱃지 누락, calc 뱃지 상단 잘림) 모두 해결 |
| 썸네일 (`etsy_listing/minimal_app_icons/thumbnail/`) | 완료 | `thumbnail.png` (2000×2000, 3×3 격자) |
| `README.txt` 라이선스/문의 항목 | 미완료 | 플레이스홀더 상태 (License/Usage, Support 항목 미기입) |
| ZIP 패키징 | 미완료 | `minimal-app-icons-v1.zip` 아직 생성 안 됨 |
| Etsy 등록 정보 확정 (제목·가격·태그) | 미완료 | `etsy_listing/minimal_app_icons/LISTING.md` 표 참고, 값 미정 |
| Etsy 실제 등록 | 미완료 | - |

세부 체크리스트는 `etsy_listing/minimal_app_icons/LISTING.md`에서 관리한다.

## 아이콘별 생성 로그

상태 값: 대기 / 진행중 / 성공 / 실패

| 아이콘 이름 | 참고 이미지 (target/) | 상태 | 최종 프롬프트 파일 | 비고 |
|---|---|---|---|---|
| heart (하트) | ../../target/Minimal App Icons.png (4행1열) | 성공 | ./heart_123050.md | 스타일 기준 프롬프트로 확정. 다른 아이콘은 이 프롬프트의 "3D clay render of a [오브젝트] icon, ..." 구조를 재사용 |
| phone (전화) | ../../target/Minimal App Icons.png (1행2열) | 성공 | ./phone_123459.md | - |
| chat (채팅) | ../../target/Minimal App Icons.png (1행3열) | 성공 | ./chat_125031.md | v1은 꼬리 2개로 실패, "single tail" 문구 추가해 재생성 성공 |
| camera (카메라) | ../../target/Minimal App Icons.png (1행4열) | 성공 | ./camera_130818.md | v1은 렌즈가 작아 실패, "oversized large lens" 문구 추가해 재생성 성공 |
| rocket (로켓) | ../../target/Minimal App Icons.png (2행1열) | 성공 | ./rocket_131359.md | - |
| weather (구름+해) | ../../target/Minimal App Icons.png (2행2열) | 성공 | ./weather_131835.md | - |
| clock (시계) | ../../target/Minimal App Icons.png (2행3열) | 성공 | ./clock_132218.md | - |
| photos (꽃) | ../../target/Minimal App Icons.png (2행4열) | 성공 | ./flower_132551.md | - |
| calculator (계산기) | ../../target/Minimal App Icons.png (3행1열) | 성공 | ./calc_132952.md | - |
| lightbulb (전구) | ../../target/Minimal App Icons.png (3행2열) | 성공 | ./bulb_135033.md | 5차 시도 끝에 확정. 필라멘트 모양·크기·위치 모두 만족 |
| bird (새) | ../../target/Minimal App Icons.png (3행3열) | 성공 | ./bird_135459.md | - |
| music (음악) | ../../target/Minimal App Icons.png (3행4열) | 성공 | ./music_140419.md | - |
| compass (나침반) | ../../target/Minimal App Icons.png (4행2열) | 성공 | ./compass_141019.md | v1은 문자 오배치+고리 장식 실패, 문구 보강해 재생성 성공 |
| gear (설정) | ../../target/Minimal App Icons.png (4행3열) | 성공 | ./gear_141311.md | - |
| guitar (기타) | ../../target/Minimal App Icons.png (4행4열) | 성공 | ./guitar_141625.md | - |

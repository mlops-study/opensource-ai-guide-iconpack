#!/usr/bin/env python3
"""
배경 투명화 스크립트 v2 (Python 3.11+, numpy/scipy 기반)

기존 v1의 개선판. 기존 색상 임계값 방식(--outer-only)이
픽셀을 "지운다/남긴다" 둘 중 하나로만 처리해서 생기던 두 가지 품질 문제를 해결한다.

  문제 1) 계단(jagged) 경계 — 알파가 0 또는 255뿐이라 안티에일리어싱이 사라짐
  문제 2) 흰 테두리(halo) — 경계 픽셀에 섞여 있던 배경 흰색이 그대로 남음

─────────────────────────────────────────────────────────────
 이 스크립트는 무엇을 하나요? (처음 사용하는 분을 위한 안내)
─────────────────────────────────────────────────────────────
  이미지 파일(PNG, JPG 등)에서 배경을 지워, 배경이 투명한 PNG 파일로
  바꿔주는 프로그램이다. 예를 들어 흰 배경 위에 그려진 아이콘 이미지를
  넣으면, 흰 배경만 사라지고 아이콘만 남은 투명 PNG가 새로 만들어진다.
  원본 파일은 지워지거나 바뀌지 않고 그대로 남는다.

  ▶ 준비물
    1) Python 3.11 이상 (터미널에서 `python3 --version`으로 확인 가능.
       설치되어 있지 않다면 python.org에서 최신 버전을 내려받는다)
    2) 인터넷 연결 — 처음 실행할 때 필요한 라이브러리(numpy, scipy,
       Pillow, 경우에 따라 rembg)를 스크립트가 자동으로 설치한다.
       한 번 설치된 뒤에는 인터넷 없이도 계속 사용할 수 있다.

  ▶ 실행 방법 (macOS 터미널 / Windows 명령 프롬프트 공통)
    1) 터미널(또는 명령 프롬프트)을 열고, 이 스크립트가 있는 폴더로 이동한다.
         cd 스크립트가_저장된_폴더_경로
    2) 배경을 지우고 싶은 이미지 파일명을 붙여 실행한다.
         python3 remove_background.py 내이미지.png
    3) 실행이 끝나면 같은 폴더에 `내이미지_nobg.png` 파일이 새로 생긴다.
    4) 새로 생긴 파일을 이미지 뷰어로 열어 배경이 잘 지워졌는지 확인한다.
       (투명한 부분은 보통 회색·흰색 체크무늬로 표시된다)

  ▶ 자주 겪는 문제
    - "python3: command not found"(또는 "'python3'은 내부 명령이
      아닙니다") → Python이 설치되어 있지 않거나 PATH에 등록되지 않은
      것이다. python.org에서 설치한 뒤 터미널을 새로 열어 다시 시도한다.
    - "이 스크립트는 Python 3.11 이상이 필요합니다" → 설치된 Python
      버전이 낮다는 뜻. 최신 버전을 설치한 뒤 다시 실행한다.
    - 실행 중 낯선 오류 메시지가 뜨며 멈춤 → 오류 메시지 전체를 그대로
      복사해 검색하거나, 메시지와 함께 도움을 요청한다.
    - 결과 이미지에 배경이 일부 남아 있음 → 아래 "동작 방식 4가지" 중
      상황에 맞는 방식(--soft, --ai 등)을 시도해본다.

  옵션 없이 그냥 실행하면 아래 "1) 솔리드 방식"이 기본으로 적용된다.
  옵션은 결과가 마음에 들지 않을 때만 선택적으로 사용하면 된다 —
  자세한 목록은 아래 "옵션" 섹션, 실행 예시는 "실행 예시" 섹션 참고.

─────────────────────────────────────────────────────────────
 동작 방식 4가지 (고급 — 결과를 다르게 만들고 싶을 때 참고)
─────────────────────────────────────────────────────────────
  1) 솔리드 방식 (기본값, --solid로 명시도 가능)  ★ 신규, 아이콘팩 권장
     - 기본 2배 슈퍼샘플링: 확대(LANCZOS) → 처리 → 프리멀티플라이드 알파 축소.
       경계 안티에일리어싱이 원본 크기 처리보다 한층 매끄러워진다
     - rembg 실루엣 3종(주모델 원본 / 주모델 대비증폭 / 보조모델 원본)의
       다수결 합의로 전경 결정 → 모델 하나가 크림·파스텔 뱃지를 놓치거나
       그림자를 잘못 포함해도 나머지가 보정한다. 1표뿐인 영역은 두꺼운
       덩어리(놓친 뱃지)만 채택하고 얇은 것(그림자 줄무늬)은 버린다.
       색은 원본에서 가져오므로 결과 색감은 변하지 않는다
     - 실루엣 내부는 완전 불투명으로 강제, 경계 ±band 픽셀은 마스크 블러로
       균일한 안티에일리어싱 생성
     - 색 확장 디프린지: 경계 픽셀의 RGB를 가장 가까운 내부 픽셀 색으로 치환
       → 배경 흰색 성분이 완전히 사라져 어두운 배경에서도 프린지 없음
     - rembg가 파스텔 뱃지 내부에 남기는 반투명 얼룩과, 색상 임계값 방식이
       배경 쪽 옅은 광택·그림자에 남기는 흰 얼룩을 모두 해결한다

  2) 소프트 방식 (--soft)  ★ 신규, rembg 설치 없이 동작
     - 외곽 플러드필로 배경 영역을 찾는 것은 기존과 동일 (내부 흰 영역 보존)
     - 경계 대역(band)의 픽셀에는 색 거리 비율로 연속 알파(0~255)를 부여해
       원본의 안티에일리어싱을 복원하고, 디프린지로 흰 테두리를 제거한다
     - 단, 배경 쪽에 옅은 광택·그림자 그라데이션이 넓게 깔린 이미지는
       얼룩이 남을 수 있다 → 그 경우 솔리드 방식 사용

  3) AI 방식 (--ai)
     - rembg 딥러닝 모델 출력을 그대로 저장. 사진·복잡한 배경에 적합
     - 파스텔 뱃지 내부에 반투명 얼룩이 생길 수 있음 → 그 경우 솔리드 방식 사용

  4) 하드 방식 (--hard)
     - 기존 --outer-only와 동일한 이진 처리 (비교·디버깅용으로만 유지)

─────────────────────────────────────────────────────────────
 옵션
─────────────────────────────────────────────────────────────
  --solid           솔리드 방식 (기본값. 플래그 없이 실행해도 동일)
  --soft            소프트 방식 (색상 임계값 기반, rembg 불필요)
  --ai              AI(rembg) 원본 출력 방식
  --hard            기존 이진 플러드필 방식 (비교용)
  --color R,G,B     배경색 직접 지정 (기본: 가장자리 1px 테두리의 중앙값 자동 감지)
                    --soft/--hard에서만 사용
  --tolerance N     배경 판정 색상 허용 오차, L1 거리 (기본: 15)
                    배경이 단색이 아니면 20~40으로 높여볼 것. --soft/--hard에서만 사용
  --band N          경계 소프트 처리 대역 폭(픽셀, 기본: 2). --solid/--soft에서 사용
  --min-size N      이 크기(픽셀 수) 미만의 고립된 전경 조각은 노이즈로 제거
                    (기본: 32, 0이면 끔). --solid/--soft/--hard에서 사용
  --model 이름      rembg 주 모델 (기본: isnet-general-use). --solid/--ai에서 사용
                    솔리드 방식은 보조 모델(u2net)을 자동으로 함께 사용한다
  --supersample N   처리 배율 (기본: 2). 확대→처리→축소로 경계 품질 향상.
                    1이면 원본 크기 그대로 처리. --solid에서만 사용
  --enhance N       실루엣 추출용 대비 증폭 배율 (기본: 3.0, 1이면 끔).
                    옅은 크림색 뱃지를 모델이 놓치지 않게 함. --solid에서만 사용
  --output 경로     출력 파일 경로 (기본: 원본파일명_nobg.png). 입력 1개일 때만
  --output-dir 경로 출력 디렉토리 — 파일명은 입력과 동일. 여러 입력 일괄 처리용
                    (입력을 여러 개 주면 모델은 한 번만 로드된다)

─────────────────────────────────────────────────────────────
 실행 예시
─────────────────────────────────────────────────────────────
  [가장 기본, 옵션 없이 실행] 같은 폴더에 "파일명_nobg.png"로 저장됨
  $ python3 remove_background.py 내이미지.png

  [솔리드 방식 + 저장 경로 직접 지정] 흰 배경 아이콘 — 매끄러운 경계 + 얼룩·흰 테두리 없음
  $ python3 remove_background.py MyIconShop/images/minimal_app_icons/guitar.png \
      --output MyIconShop/etsy_listing/minimal_app_icons/icons/guitar.png

  [소프트 방식] rembg 설치 없이 색상 기반으로 처리
  $ python3 remove_background.py logo.png --soft

  [AI 방식] 사진·복잡한 배경
  $ python3 remove_background.py photo.jpg --ai

  [배경색 수동 지정 + 넓은 허용 오차] (소프트 방식)
  $ python3 remove_background.py banner.png --soft --color "240,240,240" --tolerance 30
"""

import sys
import subprocess
import argparse
from pathlib import Path

if sys.version_info < (3, 11):
    v = sys.version_info
    print(f"[오류] 이 스크립트는 Python 3.11 이상이 필요합니다 (현재: {v.major}.{v.minor}).", file=sys.stderr)
    print("최신 Python을 설치한 뒤 'python3 --version'으로 버전을 확인하세요.", file=sys.stderr)
    sys.exit(1)

from typing import TypeAlias

RGB: TypeAlias = tuple[int, int, int]


def ensure_packages(packages: list[str]) -> None:
    for pkg in packages:
        mod = {"Pillow": "PIL"}.get(pkg, pkg.replace("-", "_"))
        try:
            __import__(mod)
        except ImportError:
            print(f"[설치 중] {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])


def _detect_bg_color(rgb, np) -> "tuple":
    """가장자리 1px 테두리 픽셀의 중앙값으로 배경색을 감지 (모서리 4점 평균보다 노이즈에 강함)."""
    border = np.concatenate([
        rgb[0, :], rgb[-1, :], rgb[1:-1, 0], rgb[1:-1, -1]
    ])
    color = np.median(border, axis=0)
    print(f"  배경색 자동 감지: RGB({int(color[0])}, {int(color[1])}, {int(color[2])})")
    return color


def remove_bg_soft(
    input_path: Path,
    output_path: Path,
    bg_color: RGB | None,
    tolerance: int,
    band: int,
    min_size: int = 32,
    hard: bool = False,
) -> None:
    """외곽 플러드필 + 경계 연속 알파 + 디프린지. hard=True면 기존 이진 방식."""
    ensure_packages(["numpy", "scipy", "Pillow"])
    import numpy as np
    from PIL import Image
    from scipy import ndimage

    label = "하드(이진)" if hard else "소프트"
    print(f"[{label} 방식] 배경 제거 중: {input_path.name}")

    img = Image.open(input_path).convert("RGBA")
    arr = np.asarray(img, dtype=np.float32)
    rgb, orig_alpha = arr[..., :3], arr[..., 3]

    bg = (np.array(bg_color, dtype=np.float32) if bg_color is not None
          else _detect_bg_color(rgb, np))

    # 배경색과의 L1 색 거리
    dist = np.abs(rgb - bg).sum(axis=2)

    # 1) 배경 후보(색 거리 ≤ tolerance) 중 이미지 가장자리와 연결된 영역만 배경으로 확정
    #    → 아이콘 내부의 흰 영역은 가장자리와 연결되지 않으므로 보존된다
    core = dist <= tolerance
    labels, _ = ndimage.label(core)
    edge_labels = np.unique(np.concatenate([
        labels[0, :], labels[-1, :], labels[:, 0], labels[:, -1]
    ]))
    edge_labels = edge_labels[edge_labels != 0]
    bg_mask = np.isin(labels, edge_labels)

    # 1-2) 미세 얼룩 제거: 배경 판정 후 남은 전경 조각 중 min_size 미만의
    #      고립된 조각은 노이즈(원본의 희미한 얼룩)로 보고 함께 투명화한다
    if min_size > 0:
        fg_labels, n_fg = ndimage.label(~bg_mask)
        if n_fg > 0:
            sizes = np.bincount(fg_labels.ravel())
            tiny_ids = np.where(sizes < min_size)[0]
            tiny_ids = tiny_ids[tiny_ids != 0]  # 라벨 0은 배경이므로 제외
            tiny = np.isin(fg_labels, tiny_ids)
            n_specks = int(tiny.sum())
            if n_specks:
                print(f"  미세 얼룩 제거: {n_specks:,} 픽셀")
            bg_mask |= tiny

    if hard:
        alpha = np.where(bg_mask, 0.0, 1.0)
    else:
        # 2) 경계 대역: 배경에 인접한 band 픽셀 폭의 전경 쪽 픽셀들.
        #    이 대역의 픽셀은 원본에서 배경색과 전경색이 섞인 안티에일리어싱 픽셀이므로
        #    "섞인 비율"을 알파로 복원한다.
        dilated = ndimage.binary_dilation(bg_mask, iterations=band)
        band_mask = dilated & ~bg_mask

        # 픽셀별 전경 기준색 거리(ref): 대역 밖 확실한 전경의 색 거리를 주변에서 가져온다.
        # 뱃지가 크림색(배경과 비슷)이면 ref가 작아지고, 진한 색이면 커져서
        # 어느 쪽이든 알파 = dist/ref 비율이 실제 혼합 비율에 가깝게 나온다.
        conf_dist = np.where(dilated, 0.0, dist)
        ref = ndimage.maximum_filter(conf_dist, size=2 * band + 3)
        ref = np.maximum(ref, 2.0 * tolerance)  # 주변에 확실한 전경이 없을 때의 하한

        t0 = 0.25 * tolerance  # 이 거리 이하는 완전 배경으로 간주
        grad = np.clip((dist - t0) / np.maximum(ref - t0, 1e-6), 0.0, 1.0)

        alpha = np.where(bg_mask, 0.0, np.where(band_mask, grad, 1.0))

        # 3) 디프린지: 반투명 픽셀 C = a*F + (1-a)*B 에서 전경색 F를 역산해
        #    배경 흰색 성분을 제거한다 (남겨두면 어두운 배경 위에서 흰 테두리로 보임)
        semi = band_mask & (alpha > 0.01) & (alpha < 1.0)
        a3 = np.maximum(alpha[..., None], 0.05)
        fg_est = np.clip(bg + (rgb - bg) / a3, 0.0, 255.0)
        rgb = np.where(semi[..., None], fg_est, rgb)

    out = np.dstack([rgb, np.minimum(orig_alpha, alpha * 255.0)])
    Image.fromarray(out.round().astype(np.uint8), "RGBA").save(output_path)

    n_bg = int(bg_mask.sum())
    n_semi = int(((alpha > 0.0) & (alpha < 1.0)).sum())
    print(f"  투명화된 픽셀: {n_bg:,} / 반투명 경계 픽셀: {n_semi:,}")
    print(f"[완료] 저장됨: {output_path}")


_sessions: dict = {}


def _get_session(model: str):
    """rembg 모델 세션 캐시 — 여러 파일 일괄 처리 시 모델을 한 번만 로드한다."""
    from rembg import new_session

    if model not in _sessions:
        _sessions[model] = new_session(model)
    return _sessions[model]


def remove_bg_ai(input_path: Path, output_path: Path, model: str) -> None:
    """rembg AI 모델로 배경 제거 (사진·복잡한 배경에 적합)."""
    ensure_packages(["rembg", "Pillow"])
    from rembg import remove

    print(f"[AI 방식] 배경 제거 중: {input_path.name} (모델: {model})")
    result = remove(input_path.read_bytes(), session=_get_session(model))
    output_path.write_bytes(result)
    print(f"[완료] 저장됨: {output_path}")


def remove_bg_solid(
    input_path: Path,
    output_path: Path,
    model: str,
    band: int,
    min_size: int,
    supersample: int = 2,
    enhance: float = 3.0,
) -> None:
    """하이브리드: rembg 실루엣 3종의 다수결 합의로 전경을 정하고, 내부는 완전 불투명으로 강제.

    - rembg는 배경/전경 '영역' 판정은 대체로 정확하지만, 모델·입력에 따라
      배경과 색이 거의 같은 크림/파스텔 뱃지를 통째로 또는 부분적으로 놓친다.
      (isnet이 놓치는 이미지를 u2net이 잡기도 하고, 그 반대도 있다.
       대비 증폭 입력이 잡기도 하고 오히려 놓치게 만들기도 한다.)
    - 그래서 실루엣을 3종 — ① model 원본 입력, ② model 대비 증폭 입력,
      ③ 보조 모델 원본 입력 — 으로 뽑아 다수결(2표 이상)을 기본 채택하고,
      1표뿐인 영역은 "두꺼운 덩어리"(놓친 뱃지 조각)만 추가 채택한다.
      얇은 1표 영역(그림자 줄무늬·경계 흔들림)은 버려진다.
    - 실루엣은 원본 해상도에서 추출한다 (업스케일 입력은 옅은 경계가 흐려져
      오판이 늘어난다). 픽셀 가공만 supersample 해상도에서 수행.
    - 내부 불투명 강제 + 경계 band픽셀 마스크 블러 알파 + 색 확장 디프린지로
      반투명 얼룩과 흰 테두리 문제를 해결한다.
    - supersample>1 이면 확대 해상도로 가공한 뒤 프리멀티플라이드 알파로
      원래 크기로 축소한다 → 경계 안티에일리어싱이 더 매끄러워진다.
    """
    ensure_packages(["rembg", "numpy", "scipy", "Pillow"])
    import numpy as np
    from PIL import Image
    from io import BytesIO
    from rembg import remove
    from scipy import ndimage

    aux_model = "u2net" if model != "u2net" else "isnet-general-use"
    print(f"[솔리드 방식] 배경 제거 중: {input_path.name} "
          f"(모델: {model}+{aux_model}, 슈퍼샘플링: x{supersample}, 대비 증폭: x{enhance})")

    orig = Image.open(input_path).convert("RGBA")
    w, h = orig.size

    # 0) 슈퍼샘플링: 확대 해상도로 가공하면 경계 알파의 계조가 세밀해지고,
    #    마지막 축소 단계에서 평균화되며 윤곽이 한층 매끄러워진다
    work = orig
    if supersample > 1:
        work = orig.resize((w * supersample, h * supersample), Image.LANCZOS)
        band *= supersample
        min_size *= supersample * supersample

    arr = np.asarray(work, dtype=np.float32)
    rgb, orig_alpha = arr[..., :3], arr[..., 3]

    def _clean(mask):
        """내부 구멍 메우기 + min_size 미만 고립 조각 제거"""
        mask = ndimage.binary_fill_holes(mask)
        if min_size > 0:
            labels, n = ndimage.label(mask)
            if n > 1:
                sizes = np.bincount(labels.ravel())
                tiny = np.where(sizes < min_size)[0]
                tiny = tiny[tiny != 0]
                mask &= ~np.isin(labels, tiny)
        return mask

    def _silhouette(img_rgb, model_name):
        """원본 해상도에서 실루엣 추출 → 작업 해상도 마스크로 업스케일"""
        buf = BytesIO()
        img_rgb.save(buf, "PNG")
        result = remove(buf.getvalue(), session=_get_session(model_name))
        a = np.asarray(Image.open(BytesIO(result)).convert("RGBA"), dtype=np.float32)[..., 3]
        if supersample > 1:
            a = np.asarray(Image.fromarray(a).resize(
                (w * supersample, h * supersample), Image.BILINEAR), dtype=np.float32)
        return _clean(a > 127.0)

    # 1) 실루엣 3종: model 원본 / model 대비 증폭 / 보조 모델 원본
    orig_rgb = orig.convert("RGB")
    src = np.asarray(orig_rgb, dtype=np.float32)
    enhanced = np.clip(255.0 - enhance * (255.0 - src), 0.0, 255.0).astype(np.uint8)
    masks = [
        _silhouette(orig_rgb, model),
        _silhouette(Image.fromarray(enhanced), model),
        _silhouette(orig_rgb, aux_model),
    ]

    # 2) 다수결 합의: 2표 이상은 확정 채택. 1표 영역은 확정 영역에서 떨어진
    #    "두꺼운 덩어리"(모델 하나만 잡아낸 옅은 뱃지 조각)만 추가하고,
    #    얇은 것(그림자 줄무늬·경계 흔들림)은 버린다
    votes = np.zeros(masks[0].shape, dtype=np.uint8)
    for m in masks:
        votes += m
    agree = votes >= 2
    union = votes >= 1
    fg = union.copy()
    cand = union & ~ndimage.binary_dilation(agree, iterations=4 * max(supersample, 1))
    cand_labels, n_cand = ndimage.label(cand)
    if n_cand:
        thick_core = ndimage.distance_transform_edt(cand) > 12 * max(supersample, 1)
        keep_ids = np.unique(cand_labels[thick_core])
        keep_ids = keep_ids[keep_ids != 0]
        thin = cand & ~np.isin(cand_labels, keep_ids)
        fg &= ~thin
    fg = _clean(fg)

    # 3) 내부는 완전 불투명(255), 실루엣 경계 ±band 픽셀은 마스크 가우시안 블러로
    #    균일한 안티에일리어싱을 만든다
    inner = ndimage.binary_erosion(fg, iterations=band)
    edge_zone = ndimage.binary_dilation(fg, iterations=band) & ~inner
    blur = ndimage.gaussian_filter(fg.astype(np.float32), sigma=1.0 * max(supersample, 1))
    alpha = np.where(inner, 1.0, np.where(edge_zone, blur, 0.0))

    # 4) 색 확장 디프린지: 경계 대역 픽셀의 RGB를 가장 가까운 내부(확실 전경)
    #    픽셀 색으로 치환한다. 경계 픽셀에 섞여 있던 배경 흰색이 완전히 사라져
    #    어두운 배경에 합성해도 밝은 프린지가 생기지 않는다.
    _, (iy, ix) = ndimage.distance_transform_edt(~inner, return_indices=True)
    rgb = np.where(edge_zone[..., None], rgb[iy, ix], rgb)

    out = np.dstack([rgb, np.minimum(orig_alpha, alpha * 255.0)])
    result_img = Image.fromarray(out.round().astype(np.uint8), "RGBA")

    # 5) 원래 크기로 축소 (프리멀티플라이드 알파 — 일반 RGBA 축소는 투명 픽셀의
    #    색이 경계에 번져 헤일로가 생기므로 알파를 곱한 상태로 축소 후 되돌린다)
    if supersample > 1:
        result_img = _downscale_premultiplied(result_img, (w, h), np)

    result_img.save(output_path)

    a_final = np.asarray(result_img, dtype=np.float32)[..., 3]
    n_semi = int(((a_final > 0.0) & (a_final < 255.0)).sum())
    print(f"  전경 픽셀: {int((a_final > 0).sum()):,} / 반투명 경계 픽셀: {n_semi:,}")
    print(f"[완료] 저장됨: {output_path}")


def _downscale_premultiplied(img, size: tuple[int, int], np):
    """RGBA 이미지를 프리멀티플라이드 알파로 축소해 경계 헤일로를 방지한다."""
    from PIL import Image

    arr = np.asarray(img, dtype=np.float32)
    a = arr[..., 3:] / 255.0
    premultiplied = arr[..., :3] * a
    channels = [
        np.asarray(Image.fromarray(premultiplied[..., i]).resize(size, Image.LANCZOS))
        for i in range(3)
    ]
    alpha = np.clip(np.asarray(Image.fromarray(a[..., 0] * 255.0).resize(size, Image.LANCZOS)), 0.0, 255.0)
    safe = np.maximum(alpha / 255.0, 1e-4)[..., None]
    rgb = np.clip(np.stack(channels, axis=-1) / safe, 0.0, 255.0)
    out = np.dstack([rgb, alpha])
    return Image.fromarray(out.round().astype(np.uint8), "RGBA")


def parse_color(value: str) -> RGB:
    parts = [int(v.strip()) for v in value.split(",")]
    if len(parts) < 3:  # noqa: PLR2004
        raise argparse.ArgumentTypeError("색상은 'R,G,B' 형식으로 입력하세요 (예: 255,255,255)")
    return (parts[0], parts[1], parts[2])


def main() -> None:
    parser = argparse.ArgumentParser(description="이미지 배경 투명화 v2 (솔리드/소프트 경계 + 디프린지)")
    parser.add_argument("input", nargs="+",
                        help="입력 이미지 파일 경로 (여러 개 지정 가능 — 모델은 한 번만 로드됨)")
    parser.add_argument("--solid", action="store_true",
                        help="솔리드 방식: AI 실루엣 + 내부 불투명 강제 + 경계 디프린지 (기본값)")
    parser.add_argument("--soft", action="store_true",
                        help="소프트 방식: 플러드필 + 경계 연속 알파 + 디프린지 (rembg 불필요)")
    parser.add_argument("--ai", action="store_true",
                        help="AI(rembg) 원본 출력 방식")
    parser.add_argument("--hard", action="store_true",
                        help="기존 이진 플러드필 방식 (비교·디버깅용)")
    parser.add_argument("--color", type=parse_color, default=None,
                        help="배경색 지정 (예: '255,255,255'). 미지정 시 자동 감지. --ai에서는 무시됨")
    parser.add_argument("--tolerance", type=int, default=15,
                        help="배경 판정 L1 색상 허용 오차 (기본: 15). --ai에서는 무시됨")
    parser.add_argument("--band", type=int, default=2,
                        help="경계 소프트 처리 대역 폭(픽셀, 기본: 2). --soft에서만 사용")
    parser.add_argument("--min-size", type=int, default=32,
                        help="이 크기(픽셀 수) 미만의 고립된 전경 조각은 노이즈로 보고 제거 (기본: 32, 0이면 끔)")
    parser.add_argument("--model", default="isnet-general-use",
                        help="rembg 모델 이름 (기본: isnet-general-use). --solid/--ai에서 사용")
    parser.add_argument("--supersample", type=int, default=2,
                        help="처리 배율 (기본: 2). 확대→처리→축소로 경계가 더 매끄러워짐. "
                             "1이면 원본 크기 그대로 처리. --solid에서만 사용")
    parser.add_argument("--enhance", type=float, default=3.0,
                        help="실루엣 추출용 대비 증폭 배율 (기본: 3.0). 배경과 색이 비슷한 "
                             "옅은 뱃지의 누락을 방지. 1이면 증폭 없음. --solid에서만 사용")
    parser.add_argument("--output", default=None,
                        help="출력 파일 경로 (기본: 원본파일명_nobg.png). 입력이 1개일 때만 사용")
    parser.add_argument("--output-dir", default=None,
                        help="출력 디렉토리 (파일명은 입력과 동일하게 저장). 여러 입력 처리 시 사용")
    args = parser.parse_args()

    if sum([args.solid, args.soft, args.ai, args.hard]) > 1:
        print("[오류] --solid / --soft / --ai / --hard 는 하나만 선택하세요.", file=sys.stderr)
        sys.exit(1)
    if args.output and len(args.input) > 1:
        print("[오류] 입력이 여러 개일 때는 --output 대신 --output-dir 을 사용하세요.", file=sys.stderr)
        sys.exit(1)

    for raw in args.input:
        input_path = Path(raw)
        if not input_path.exists():
            print(f"[오류] 파일을 찾을 수 없습니다: {input_path}", file=sys.stderr)
            sys.exit(1)

        if args.output:
            output_path = Path(args.output)
        elif args.output_dir:
            out_dir = Path(args.output_dir)
            out_dir.mkdir(parents=True, exist_ok=True)
            output_path = out_dir / input_path.name
        else:
            output_path = input_path.with_name(input_path.stem + "_nobg.png")

        if args.ai:
            remove_bg_ai(input_path, output_path, args.model)
        elif args.soft or args.hard:
            remove_bg_soft(input_path, output_path, args.color,
                           args.tolerance, args.band, args.min_size, hard=args.hard)
        else:
            remove_bg_solid(input_path, output_path, args.model, args.band,
                            args.min_size, args.supersample, args.enhance)


if __name__ == "__main__":
    main()

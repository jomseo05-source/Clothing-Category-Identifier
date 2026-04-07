# ---------------------------------------------------------
# Step 1: Build Stage (최적화 - 빌드 도구와 패키지 설치)
# ---------------------------------------------------------
FROM python:3.10-slim AS builder

# 빌드 캐시 최적화를 위한 설정
WORKDIR /build

# 패키지 설치 전 requirements.txt만 먼저 복사 (Layer Caching)
COPY requirements.txt .

# 전역 설치가 아닌 사용자 로컬 경로에 설치하여 최종 이미지로 전달 준비
RUN pip install --no-cache-dir --user -r requirements.txt

# ---------------------------------------------------------
# Step 2: Runtime Stage (최종 실행용 경량 이미지)
# ---------------------------------------------------------
FROM python:3.10-slim

# 보안: Non-root 사용자 생성 및 실행 권한 부여
RUN useradd -m -u 1000 appuser
WORKDIR /home/appuser/app

# 환경 변수 설정
ENV PATH="/home/appuser/.local/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

# 빌드 스테이지에서 설치된 라이브러리만 복사 (최종 이미지 용량 감소)
COPY --from=builder /root/.local /home/appuser/.local
COPY . .

# 소유권 변경 (보안을 위한 non-root 설정)
RUN chown -R appuser:appuser /home/appuser/app

# 포트 개방
EXPOSE 8000

# 사용자로 전환
USER appuser

# FastAPI 서버 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

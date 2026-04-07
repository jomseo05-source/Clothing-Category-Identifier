from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import time

# 내부 모듈
from app.ml.classifier import classifier
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.get("/")
async def root():
    return {"message": "의류 카테고리 식별 API 서버가 동작 중입니다.", "docs": "/docs"}

@app.post(f"{settings.API_V1_STR}/predict")
async def predict_clothing(file: UploadFile = File(...)):
    # 1. 파일 검증 (이미지 포맷 확인)
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일을 업로드해 주세요.")

    try:
        # 2. 이미지 읽기
        start_time = time.time()
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # 3. 모델 추론
        result = classifier.predict(image)
        
        # 4. 분석 소요 시간 추가
        process_time = time.time() - start_time
        result["process_time"] = f"{process_time:.4f}s"
        
        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"추론 중 내부 오류가 발생했습니다: {str(e)}"}
        )

# 서버 실행을 위한 엔트리 포인트 (개발 시에만 사용)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

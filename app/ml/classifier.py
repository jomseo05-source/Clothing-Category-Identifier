import torch
import torchvision.transforms as transforms
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights
from PIL import Image
import numpy as np

class ClothingClassifier:
    def __init__(self):
        # 경량 모델인 MobileNetV2 로드
        self.weights = MobileNet_V2_Weights.DEFAULT
        self.model = mobilenet_v2(weights=self.weights)
        self.model.eval()
        self.categories = self.weights.meta["categories"]
        
        # 전처리 파이프라인
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def predict(self, image: Image.Image):
        # 1. 이미지 전처리
        img_t = self.transform(image)
        batch_t = torch.unsqueeze(img_t, 0)

        # 2. 모델 추론
        with torch.no_grad():
            out = self.model(batch_t)
        
        # 3. 결과 해석 (Top 1)
        _, index = torch.max(out, 1)
        label = self.categories[index.item()]
        
        # 4. 의류 카테고리 (상의/하의) 및 스타일 매핑
        category = "Unknown"
        style = "Casual" # 기본값

        # ImageNet 클래스 기반 매핑 (의류 관련 클래스만 필터링)
        top_keywords = ["t-shirt", "jersey", "cardigan", "suit", "jacket", "coat", "shirt", "sweater", "vest"]
        bottom_keywords = ["jean", "pants", "short", "skirt", "trouser"]

        if any(k in label.lower() for k in top_keywords):
            category = "상의 (Top)"
        elif any(k in label.lower() for k in bottom_keywords):
            category = "하의 (Bottom)"
        else:
            # 의류가 아닐 경우의 처리 로직 (데모를 위해 확장 가능)
            category = f"기타 의류 ({label})"

        # 간단한 스타일 분석 로직 (색상 기반)
        style = self._analyze_style(image)

        return {
            "prediction": label,
            "category": category,
            "style": style
        }

    def _analyze_style(self, image: Image.Image):
        # 이미지를 작게 줄여서 주요 색상 추출
        img = image.resize((50, 50))
        img_arr = np.array(img)
        avg_color = img_arr.mean(axis=(0, 1))

        # 매우 단순화된 스타일 매핑 예시
        # R, G, B 평균값을 기반으로 색 감지
        if avg_color.max() < 100:
            return "Chic/Dark"
        elif avg_color[0] > 180 and avg_color[1] > 180 and avg_color[2] > 180:
            return "Minimal/Bright"
        elif avg_color[0] > 150 and avg_color[1] < 100:
            return "Vivid/Point"
        else:
            return "Casual"

# 싱글톤 인스턴스 생성
classifier = ClothingClassifier()

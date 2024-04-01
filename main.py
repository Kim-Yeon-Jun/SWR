import requests
import easyocr
from fastapi import FastAPI, HTTPException

app = FastAPI()

async def extract_text_from_image(image_url: str):
    try:
        # 이미지 다운로드
        response = requests.get(image_url)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
        
        # EasyOCR을 초기화하고 이미지에서 텍스트 추출
        reader = easyocr.Reader(['ko'])  # 영어 텍스트 추출을 위해 'en' 지정, 다른 언어도 가능
        results = reader.readtext(response.content)
        
        # 추출된 텍스트 정보를 JSON 형식으로 반환
        extracted_text = [{"text": result[1], "confidence": result[2]} for result in results]
        
        return {"image_url": image_url, "extracted_text": extracted_text}
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

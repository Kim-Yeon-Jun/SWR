import requests
import easyocr
from fastapi import FastAPI, HTTPException

app = FastAPI()

# # 이미지 URL을 받아서 텍스트를 추출하여 JSON 형식으로 반환하는 엔드포인트
# @app.get("/detect/")
# async def extract_text_from_image(image_url: str):
#     try:
#         # 이미지 다운로드
#         response = requests.get(image_url)
#         response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
        
#         # EasyOCR을 초기화하고 이미지에서 텍스트 추출
#         reader = easyocr.Reader(['ko'])  
#         results = reader.readtext(response.content)
        
#         # 추출된 텍스트 정보를 JSON 형식으로 반환
#         extracted_text = [{"text": result[1], "confidence": result[2]} for result in results]
#         print(result for result in results)
#         return {"image_url": image_url, "extracted_text": extracted_text}
    
#     except requests.exceptions.RequestException as e:
#         raise HTTPException(status_code=400, detail=str(e))
@app.get("/")
def hello_world():
    print("hello_wordld")
    
    return None
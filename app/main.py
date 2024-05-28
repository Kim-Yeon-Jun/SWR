import requests
import re
import easyocr
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR/"templates"))
@app.post("/detect/")
async def extract_text_from_image(file: UploadFile = File(...)):
    try:
        # 이미지 파일 읽기
        contents = await file.read()
        
        # EasyOCR을 초기화하고 이미지에서 텍스트 추출
        reader = easyocr.Reader(['ko'])
        results = reader.readtext(contents)
        
        # 추출된 텍스트를 한 줄로 합치기
        text = ' '.join([result[1] for result in results])
        text = text.split(' ', 1)[1]
        print(text)

        # 이름 추출
        name_pattern = re.compile(r"[가-힣]{2,4}")  # 글자 수가 2에서 4인 한글 패턴
        name_match = name_pattern.search(text)
        name = name_match.group() if name_match else None

        # 주민등록번호 추출
        rrn_pattern = re.compile(r"\d{6}-\d{7}")  # 숫자-숫자 형식 패턴
        rrn_match = rrn_pattern.search(text)
        rrn = rrn_match.group() if rrn_match else None

        birth = rrn.split('-')[0]
        gender_check = rrn.split('-')[1][0]
        print(gender_check)
        if gender_check == "1" or gender_check=="3":
            gender = "male" #male
        elif gender_check == "2" or gender_check =="4":
            gender = "female" #female
        else :
            gender = "gender check failed"
        # JSON 형식으로 반환
        result = {"name": name, "birth" : birth, "gender" : gender}
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
# 루트 엔드포인트 - 파일 업로드 폼 표시
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    context = {"request": request, "title": "데이터 수집가"}
    return templates.TemplateResponse("index.html", context=context)
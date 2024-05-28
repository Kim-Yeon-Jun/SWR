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
async def preprocess_image(contents):
    reader = easyocr.Reader(['ko'])
    results = reader.readtext(contents)
    return results

@app.post("/detect/")
async def extract_text_from_image(file: UploadFile = File(...)):
    try:
        # 이미지 파일 읽기
        contents = await file.read()
        
        # EasyOCR을 초기화하고 이미지에서 텍스트 추출
        results = await preprocess_image(contents)

        # 추출된 텍스트를 한 줄로 합치기
        text = ' '.join([result[1] for result in results])
        print(f"1 : {text}")
        text = text.split(' ', 1)[1]
        print(f"2 : {text}")
        text = text.replace(" ","")
        print(f"3 : {text}")

        # 이름 추출
        name_pattern = re.compile(r"[가-힣]{2,4}")  # 글자 수가 2에서 4인 한글 패턴
        name_match = name_pattern.search(text)
        name = name_match.group() if name_match else "name check failed"

        # 주민등록번호 추출
        rrn_pattern = re.compile(r"\d{6}-\d{7}")  # 숫자-숫자 형식 패턴
        rrn_match = rrn_pattern.search(text)
        rrn = rrn_match.group() if rrn_match else "rrn check failed"

        birth = rrn.split('-')[0]
        gender_check = rrn.split('-')[1][0]
        print(gender_check)
        
        if gender_check == "1" or gender_check=="3":
            gender = "male" #male
        elif gender_check == "2" or gender_check =="4":
            gender = "female" #female
        else :
            gender = "gender check failed"
        
        if gender_check == "1" or gender_check == "2":
            print("gender_check 1900")
            year = 1900
        elif gender_check == "3" or gender_check == "4":
            print("gender_check 2000")
            year = 2000
        
        print(f"gender_check = {gender_check}")
        tmp = int(birth[0:2])
        year += tmp
        print(f"tmp : {tmp}, year = {year}")
        month = birth[2:4]
        day = birth[4:6]
        birth = f"{year}-{month}-{day}"
        print(type(name),type(birth),type(gender))
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
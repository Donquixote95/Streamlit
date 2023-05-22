import streamlit as st
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import psycopg2
import httpx

# FastAPI와 PostgreSQL 연결
app = FastAPI()
# PostgreSQL 연결 설정
connection_info = "host=147.47.200.145 dbname=teamdb12 user=team12 password=494196 port=34543"
conn = psycopg2.connect(connection_info)

# 경마 정보 조회
@app.get("/horses")
def get_horses():
    try:
        print("Hello World")
        # 데이터베이스 쿼리 실행
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM public."2013" LIMIT 10')
        rows = cursor.fetchall()
        cursor.close()

        # 경마 정보를 JSON 형식으로 변환하여 반환
        horses = []
        for row in rows:
            horse = {
                "날짜": row[0],
                "경기번호": row[1],
                "순위": row[2],
                "말id": row[3],
                "기수id": row[4],
                "조교사id": row[5]
            }
            horses.append(horse)

        return horses
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="147.47.200.145", port=34543) # FastAPI 백엔드 설정 필요


# FastAPI 백엔드 URL 설정
backend_url = "http://localhost:8000"

# 경마 정보 조회 함수
def get_horses():
    try:
        response = httpx.get(f"{backend_url}/horses")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch horse information")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")    

# 페이지 제목 설정
st.set_page_config(page_title="경마 AI", page_icon="🏇")

# 경마 설명
st.title("경마 정보 AI")
st.write("경마는 말들이 주어진 경주장에서 경주하는 스포츠입니다.")

# 경주 목록 표시
races = st.selectbox("경주 선택", ["경주 1", "경주 2", "경주 3"])

# 경주 세부 정보 표시
if races == "경주 1":
  st.write("경주 1은 오늘 오후 3시에 시작합니다.")
  st.write("총 10마리의 말이 참가합니다.")
  st.write("궁금한 말을 선택해주세요!")

elif races == "경주 2":
  st.write("경주 2는 오늘 오후 4시에 시작합니다.")
  st.write("총 10마리의 말이 참가합니다.")
  st.write("궁금한 말을 선택해주세요!")

elif races == "경주 3":
  st.write("경주 3은 오늘 오후 5시에 시작합니다.")
  st.write("총 6마리의 말이 참가합니다.")
  st.write("궁금한 말을 선택해주세요!")

# 베팅 양식 표시
if races != "":
  st.form("마권을 어느 정도 구입하셨나요?")
  amount = st.number_input("숫자 입력")
  horse = st.selectbox("말 선택", ["말 1", "말 2", "말 3", "말 4", "말 5", "말 6", "말 7", "말 8", "말 9", "말 10"])
  st.button("결과 확인")

#   if st.form_submit_button():
#     st.write("결과입니다!")
#     st.write("Good Luck!")    

# 경마 정보 입력
st.header("이번 주 출전정보")
horse_id = st.text_input("검색하고 싶은 것을 입력하세요")

def main():
    # 경마 정보 조회
    horses = get_horses()

    # 경마 정보 출력
    if horses:
        st.header("경마 정보")
        for horse in horses:
            st.write(horse)

# Streamlit 애플리케이션 실행
if __name__ == '__main__':
    main()
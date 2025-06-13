import streamlit as st
import requests
import os

st.title("`.fz` 파일 시각화 도구")

# 다운로드 URL
url = "https://raw.githubusercontent.com/bgkim89/finalproject/main/0613.fz"
local_filename = "0613.fz"

# 파일 다운로드
if not os.path.exists(local_filename):
    st.write("파일을 다운로드 중입니다...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_filename, "wb") as f:
            f.write(response.content)
        st.success("파일 다운로드 완료!")
    else:
        st.error("파일 다운로드 실패")

# 파일 읽기 시도
try:
    with open(local_filename, "rb") as f:
        content = f.read()

    # 시각화를 위해 처음 몇 바이트만 표시
    st.subheader("파일 내용 (바이너리 500바이트까지 보기):")
    st.code(content[:500])

    # 텍스트 디코딩 시도
    try:
        decoded = content.decode('utf-8')
        st.subheader("UTF-8 텍스트로 디코딩한 결과:")
        st.text(decoded[:1000])
    except UnicodeDecodeError:
        st.warning("텍스트로 디코딩할 수 없는 바이너리 파일입니다.")

except Exception as e:
    st.error(f"파일을 여는 중 오류 발생: {e}")

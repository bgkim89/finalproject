import streamlit as st
import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np
import gzip
import io
import requests

st.title("GitHub에서 FITS (.fz) 파일 시각화")

# GitHub Raw URL (고정)
url = "https://raw.githubusercontent.com/bgkim89/finalproject/main/0613.fz"

try:
    st.info(f"FITS 파일을 다음 URL에서 불러옵니다:\n{url}")

    # GitHub에서 .fz 파일 다운로드
    response = requests.get(url)
    response.raise_for_status()

    # .fz (gzip) 압축 해제
    with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
        decompressed_data = f.read()

    # FITS 데이터 읽기
    with fits.open(io.BytesIO(decompressed_data)) as hdul:
        st.write("📄 FITS 헤더 정보:")
        st.text(hdul.info())

        data = hdul[0].data

        if data is not None:
            st.write(f"데이터 shape: {data.shape}")

            # 이미지 시각화
            fig, ax = plt.subplots()
            ax.imshow(data, cmap="gray", origin="lower", aspect="auto")
            ax.set_title("FITS 이미지 (0613.fz)")
            st.pyplot(fig)
        else:
            st.warning("FITS 파일에 이미지 데이터가 없습니다.")

except Exception as e:
    st.error(f"오류 발생: {e}")

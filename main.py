import streamlit as st
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import io
import requests

st.title("GitHub에서 .fz (Tile-compressed FITS) 파일 불러오기 및 시각화")

# GitHub Raw URL (.fz 파일)
url = "https://raw.githubusercontent.com/bgkim89/finalproject/main/0613.fz"

try:
    st.info(f"다음 경로에서 파일을 불러옵니다:\n{url}")

    # GitHub에서 파일 다운로드
    response = requests.get(url)
    response.raise_for_status()

    # .fz 파일을 astropy로 직접 열기
    with fits.open(io.BytesIO(response.content)) as hdul:
        st.write("📄 FITS 헤더 정보:")
        st.text(hdul.info())

        data = hdul[0].data

        if data is not None:
            st.write(f"데이터 shape: {data.shape}")
            fig, ax = plt.subplots()
            ax.imshow(data, cmap='gray', origin='lower', aspect='auto')
            ax.set_title('FITS 이미지 (tile-compressed .fz)')
            st.pyplot(fig)
        else:
            st.warning("FITS 파일에 이미지 데이터가 없습니다.")

except Exception as e:
    st.error(f"오류 발생: {e}")

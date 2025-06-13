import streamlit as st
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import gzip
import io
import os

st.title("내부 경로에서 FITS (.fz) 파일 불러와 시각화")

# 상대 경로 지정
file_path = "https://github.com/bgkim89/finalproject/blob/main/k21i_100108_031209_ori.fits.fz"

# 파일 존재 여부 확인
if not os.path.exists(file_path):
    st.error(f"파일이 존재하지 않습니다: {file_path}")
else:
    try:
        # 파일 열기 및 gzip 해제
        with gzip.open(file_path, 'rb') as f:
            decompressed_data = f.read()

        # 메모리에서 FITS 열기
        with fits.open(io.BytesIO(decompressed_data)) as hdul:
            st.write("FITS 헤더 정보:")
            st.text(hdul.info())

            data = hdul[0].data

            if data is not None:
                st.write(f"데이터 shape: {data.shape}")
                fig, ax = plt.subplots()
                ax.imshow(data, cmap='gray', origin='lower', aspect='auto')
                ax.set_title("FITS 이미지")
                st.pyplot(fig)
            else:
                st.warning("FITS 파일에 이미지 데이터가 없습니다.")

    except Exception as e:
        st.error(f"파일 처리 중 오류 발생: {e}")

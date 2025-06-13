import streamlit as st
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import gzip
import io

st.title("FITS 파일 시각화 도구")

# 업로드
uploaded_file = st.file_uploader("FITS (.fits.fz) 파일을 업로드하세요", type=["fits", "fz"])

if uploaded_file is not None:
    # .fz 압축 해제
    with gzip.open(uploaded_file, 'rb') as f:
        decompressed_data = f.read()

    # 메모리 파일 객체로 변환
    with fits.open(io.BytesIO(decompressed_data)) as hdul:
        st.write("헤더 정보:", hdul.info())

        # 첫 번째 HDU의 데이터 추출
        data = hdul[0].data

        if data is not None:
            st.write("데이터 shape:", data.shape)

            # 시각화
            fig, ax = plt.subplots()
            ax.imshow(data, cmap='gray', origin='lower', aspect='auto')
            ax.set_title('FITS 이미지')
            st.pyplot(fig)
        else:
            st.warning("이 FITS 파일에는 이미지 데이터가 포함되어 있지 않습니다.")


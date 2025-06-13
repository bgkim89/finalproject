import streamlit as st
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import gzip
import io
import requests

st.title("GitHub에서 FITS (.fz) 파일 불러오기 및 시각화")

# GitHub Raw URL (수동 지정하거나 아래에 직접 하드코딩 가능)
RAW_URL = "https://raw.githubusercontent.com/your-username/your-repo/main/your-file.fits.fz"

try:
    st.info(f"다음 경로에서 파일을 불러옵니다:\n{RAW_URL}")
    
    # GitHub에서 파일 다운로드
    response = requests.get(RAW_URL)
    response.raise_for_status()

    # gzip 압축 해제
    with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
        decompressed_data = f.read()

    # FITS 파일 열기
    with fits.open(io.BytesIO(decompressed_data)) as hdul:
        st.write("FITS 헤더 정보:")
        st.text(hdul.info())

        # 첫 번째 데이터 HDU 시각화
        data = hdul[0].data
        if data is not None:
            st.write(f"데이터 shape: {data.shape}")
            fig, ax = plt.subplots()
            ax.imshow(data, cmap='gray', origin='lower', aspect='auto')
            ax.set_title('FITS 이미지')
            st.pyplot(fig)
        else:
            st.warning("FITS 파일에 이미지 데이터가 없습니다.")

except Exception as e:
    st.error(f"오류 발생: {e}")

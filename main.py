import streamlit as st
import random
import time
import threading
from datetime import datetime

# 데이터 로딩 함수 (랜덤으로 숫자를 증가시킴)
def update_count():
    while not st.session_state.stop:
        st.session_state.count = random.randint(0, 100)  # 랜덤한 숫자로 카운트 업데이트
        time.sleep(1)  # 1초마다 데이터 갱신

# Streamlit 앱
st.title('Real-time Data Display')

# 초기 상태 설정
if 'start' not in st.session_state:
    st.session_state.start = False
if 'stop' not in st.session_state:
    st.session_state.stop = False
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# 시작 버튼 클릭 시
if st.button('시작'):
    st.session_state.start = True
    st.session_state.stop = False
    countdown_placeholder = st.empty() # 카운트다운 표시를 위한 빈 영역

    ## 3초 카운트다운
    for i in range(3, 0, -1):
        countdown_placeholder.write(f"{i}초")
        time.sleep(1)
    # 카운트다운 완료 후 빈 영역 제거
    countdown_placeholder.empty()

    # 카운트다운 완료 후 데이터 업데이트 시작
    st.session_state.count = random.randint(0, 100)  # 초기 랜덤 값 설정
    st.session_state.start_time = datetime.now()

    # 데이터 업데이트 스레드 시작
    if 'update_thread' not in st.session_state or not st.session_state.update_thread.is_alive():
        st.session_state.update_thread = threading.Thread(target=update_count)
        st.session_state.update_thread.start()

# 종료 버튼 클릭 시
if st.button('종료'):
    st.session_state.stop = True
    st.session_state.start = False
    if 'update_thread' in st.session_state:
        st.session_state.update_thread.join()

    end_time = datetime.now()
    elapsed_time = (end_time - st.session_state.start_time).total_seconds()

    # 최종 결과 표시
    st.write(f"최종 갯수: {st.session_state.count}")
    st.write(f"경과 시간: {elapsed_time:.2f} 초")

# 실시간 데이터 표시
if st.session_state.start and not st.session_state.stop:
    st.write(f"현재 갯수: {st.session_state.count}")
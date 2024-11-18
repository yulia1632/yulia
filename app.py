import streamlit as st
import pandas as pd
import time


st.title("전기차 충전소 모아보기")
st.image('image.jpg')
data = pd.read_csv("members.csv")
data["PW"] = data["PW"].astype(str)

# 로그인 폼
with st.form("login_form"):
    ID = st.text_input("ID", placeholder="아이디를 입력하세요")
    PW = st.text_input("Password", type="password", placeholder="비밀번호를 입력하세요")
    submit_button = st.form_submit_button("로그인")

# 비회원 버튼
guest_button = st.button("비회원으로 계속하기")

if submit_button:
    if not ID or not PW:
        st.warning("ID와 비밀번호를 모두 입력해주세요.")
    else:
        # 사용자 확인
        user = data[(data["ID"] == ID) & (data["PW"] == str(PW))]
        
        if not user.empty:
            st.success(f"{ID}님 환영합니다!")
            st.session_state["ID"] = ID
            
            # 로그인 진행 시 로딩 표시
            progress_text = "로그인 중입니다."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            time.sleep(1)
            my_bar.empty()
            
            # 페이지 이동
            st.switch_page("pages/ev_charging.py")
        else:
            st.error("아이디 또는 비밀번호가 일치하지 않습니다.")

elif guest_button:
    st.session_state["ID"] = "Guest"
    st.success("비회원으로 접속합니다.")
    
    # 비회원도 동일한 페이지로 이동
    st.switch_page("pages/ev_charging.py")

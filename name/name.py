import streamlit as st
import pandas as pd
import os

# 이름 목록을 저장할 파일 경로 설정
NAME_LIST_FILE = 'name_list.txt'

# 파일에서 이름 목록 불러오기
def load_names():
    if os.path.exists(NAME_LIST_FILE):
        with open(NAME_LIST_FILE, 'r', encoding='utf-8') as file:
            names = file.read().splitlines()
            return names
    return []

# 이름 목록을 파일에 저장하기
def save_names(names):
    with open(NAME_LIST_FILE, 'w', encoding='utf-8') as file:
        file.write('\n'.join(names))

# Streamlit 애플리케이션 설정
st.title('2025학년도 대학수학능력시험 기도 명단')

# 파일에서 이름 목록 불러와서 세션 상태에 저장
if 'name_list' not in st.session_state:
    st.session_state['name_list'] = load_names()

# 탭 설정
tabs = st.tabs(['이름 입력', '명단 확인', '엑셀 파일 업로드'])

# 이름 입력 탭
with tabs[0]:
    st.header('이름 입력')
    name = st.text_input('이름을 입력하세요:', '')

    # 이름 추가 버튼
    if st.button('추가') and name:
        if name not in st.session_state['name_list']:
            st.session_state['name_list'].append(name)
            save_names(st.session_state['name_list'])  # 파일에 저장
            st.success(f'{name} 학생이 기도 명단에 추가되었습니다.')
        else:
            st.warning(f'{name} 학생은 이미 명단에 있습니다.')

# 엑셀 파일 업로드 탭
with tabs[2]:
    st.header('엑셀 파일 업로드')
    uploaded_file = st.file_uploader('엑셀 파일을 업로드하세요 (.xlsx 형식)', type=['xlsx'])

    if uploaded_file is not None:
        # 엑셀 파일을 데이터프레임으로 읽기
        df = pd.read_excel(uploaded_file)

        # 엑셀 파일에서 이름 열 가져오기
        if '이름' in df.columns:
            new_names = df['이름'].dropna().tolist()  # '이름' 열의 값들을 리스트로 변환
            added_count = 0
            for new_name in new_names:
                if new_name not in st.session_state['name_list']:
                    st.session_state['name_list'].append(new_name)
                    added_count += 1
            st.session_state['name_list'] = list(set(st.session_state['name_list']))  # 중복 제거
            save_names(st.session_state['name_list'])  # 파일에 저장
            st.success(f'엑셀 파일에서 {added_count}개의 새로운 이름이 추가되었습니다.')
        else:
            st.error('엑셀 파일에 "이름" 열이 없습니다.')

# 명단 확인 탭
with tabs[1]:
    st.header('명단 확인')
    if st.session_state['name_list']:
        st.write('입력된 이름 목록:')
        # 이름 목록을 한 번만 스크롤로 표시
        st.markdown(
            f"""
            <div style='height: 600px; overflow: hidden; position: relative;'>
                <div style='display: flex; flex-direction: column; position: absolute; animation: scrollAnimation 30s linear infinite;'>
                    <div>{', '.join(st.session_state['name_list'])}</div>
                </div>
            </div>
            <style>
                @keyframes scrollAnimation {{
                    0% {{ transform: translateY(0); }}
                    100% {{ transform: translateY(-100%); }}
                }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.write('아직 입력된 이름이 없습니다.')

import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="사랑의교회 고3부 수능기도", page_icon="data:image/png;base64,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", layout="wide")

# 이름 목록을 저장할 파일 경로 설정
NAME_LIST_FILE = 'name_list.txt'

# 파일에서 이름 목록 불러오기
def load_names():
    if os.path.exists(NAME_LIST_FILE):
        with open(NAME_LIST_FILE, 'r', encoding='utf-8') as file:
            names = file.read().splitlines()
            return sorted(names)  # 불러올 때 정렬
    return []

# 이름 목록을 파일에 저장하기
def save_names(names):
    with open(NAME_LIST_FILE, 'w', encoding='utf-8') as file:
        file.write('\n'.join(sorted(names)))  # 저장할 때 정렬

# 파일에서 이름 목록 불러와서 세션 상태에 저장
if 'name_list' not in st.session_state:
    st.session_state['name_list'] = load_names()

# 사이드바에 페이지 선택 메뉴 추가
page = st.sidebar.radio("페이지 선택", ["이름 입력", "2025 수험생 명단 확인", "엑셀 파일 업로드"])

# 이름 입력 페이지
if page == "이름 입력":
    st.title('2025학년도 수능 기도 명단 입력')
    name = st.text_input('이름을 입력하세요:', '')

    # 이름 추가 버튼
    if st.button('추가') and name:
        if name not in st.session_state['name_list']:
            st.session_state['name_list'].append(name)
            st.session_state['name_list'].sort()
            save_names(st.session_state['name_list'])
            st.success(f'{name} 학생이 기도 명단에 추가되었습니다.')
        else:
            st.warning(f'{name} 학생은 이미 명단에 있습니다.')

# 2025 수험생 명단 확인 페이지
elif page == "2025 수험생 명단 확인":
    st.title('2025학년도 수험생 기도 명단')

    # 모바일에서 화면에 맞추도록 CSS 추가
    st.markdown(
        """
        <style>
        .main {
            padding-left: 0rem !important;
            padding-right: 0rem !important;
        }
        .scrollable-table {
            width: 100%;
            overflow-x: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            table-layout: auto; /* 모바일 화면에 맞게 열 크기 자동 조정 */
        }
        td {
            padding: 10px;
            font-size: 18px;
            text-align: center;
            word-wrap: break-word;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.session_state['name_list']:
        # 이름 목록을 10개씩 묶어 테이블 형식으로 구성
        rows = [st.session_state['name_list'][i:i+10] for i in range(0, len(st.session_state['name_list']), 10)]
        name_table_html = "<table>"
        for row in rows:
            name_table_html += "<tr>" + "".join([f"<td><b>{name}</b></td>" for name in row]) + "</tr>"
        name_table_html += "</table>"

        # 무한 스크롤 애니메이션 설정
        st.markdown(
            f"""
            <div class='scrollable-table' style='height: 800px;'>
                <div style='position: relative; animation: scrollAnimation 90s linear infinite;'>
                    {name_table_html}
                    {name_table_html} <!-- 무한 스크롤 -->
                </div>
            </div>
            <style>
                @keyframes scrollAnimation {{
                    0% {{ transform: translateY(0); }}
                    100% {{ transform: translateY(-50%); }}
                }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.write('아직 입력된 이름이 없습니다.')


# 엑셀 파일 업로드 페이지
elif page == "엑셀 파일 업로드":
    st.title('엑셀 파일 기도 명단 업데이트')
    uploaded_file = st.file_uploader('엑셀 파일을 업로드하세요 (.xlsx 형식)', type=['xlsx'])

    if uploaded_file is not None:
        # 엑셀 파일을 데이터프레임으로 읽기
        df = pd.read_excel(uploaded_file)

        # 엑셀 파일에서 이름 열 가져오기
        if '이름' in df.columns:
            new_names = df['이름'].dropna().tolist()
            added_count = 0
            for new_name in new_names:
                if new_name not in st.session_state['name_list']:
                    st.session_state['name_list'].append(new_name)
                    added_count += 1
            st.session_state['name_list'] = sorted(list(set(st.session_state['name_list'])))
            save_names(st.session_state['name_list'])
            st.success(f'엑셀 파일에서 {added_count}개의 새로운 이름이 추가되었습니다.')
        else:
            st.error('엑셀 파일에 "이름" 열이 없습니다.')

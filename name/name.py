import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="사랑의교회 고3부 수능기도", page_icon="https://url.kr/mjf2lq", layout="wide")

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
page = st.sidebar.radio("페이지 선택", ["이름 입력", "2025 수험생 명단 확인", "엑셀 파일 업로드", "이름 삭제"])

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

    # 사이드바에 기도 명단 인원 수를 작은 글씨로 표시
    st.sidebar.metric("기도 명단 인원", len(st.session_state['name_list']))

    # CSS로 우측 상단에 작은 크기로 기도 명단 인원 표시
    st.markdown(
    f"""
    <style>
    .left-info {{
        font-size: 20px;
        color: gray;
        text-align: right;
        position: absolute;
        top: 0px;
        right: 0;
        margin-right: 0px;
        margin-bottom: 0px;
    }}
    </style>
    <div class="left-info">기도 명단 인원: {len(st.session_state['name_list'])}명</div>
    """,
    unsafe_allow_html=True
    )

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
            table-layout: auto;
        }
        td {
            padding: 20px;
            font-size: 40px;
            text-align: center;
            word-wrap: break-word;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.session_state['name_list']:
        # 이름 목록을 10개씩 묶어 테이블 형식으로 구성
        rows = [st.session_state['name_list'][i:i+6] for i in range(0, len(st.session_state['name_list']), 6)]
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

# 이름 삭제 페이지
elif page == "이름 삭제":
    st.title('이름 삭제')
    if st.session_state['name_list']:
        delete_name = st.selectbox("삭제할 이름을 선택하세요:", st.session_state['name_list'])
        if st.button('삭제'):
            if delete_name in st.session_state['name_list']:
                st.session_state['name_list'].remove(delete_name)
                save_names(st.session_state['name_list'])
                st.success(f'{delete_name} 학생이 명단에서 삭제되었습니다.')
    else:
        st.write("현재 기도 명단에 이름이 없습니다.")

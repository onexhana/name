import streamlit as st

st.title("엑셀페이지")
st.write("여기에 캘린더 관련 내용을 작성하세요.")


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

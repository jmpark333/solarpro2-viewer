import streamlit as st
import os
import json
import datetime

# 2025-07-11-07:39:06: 실행 경로 문제 해결 - 항상 deploy_viewer 폴더 기준으로 파일 접근 (by Cascade)

CHAT_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="solar-pro2 Chat Viewer", page_icon="☀️", layout="wide")  # (2025-07-11-07:45:42) 가로폭 wide 옵션 추가 by Cascade
st.title("☀️ solar-pro2 채팅 기록 뷰어")

# 채팅 파일 리스트
def list_chat_history_files():
    files = [f for f in os.listdir(CHAT_DIR) if f.startswith('chat_history_') and f.endswith('.json')]
    files.sort(reverse=True)
    return files

def get_chat_title(file):
    try:
        with open(os.path.join(CHAT_DIR, file), 'r', encoding='utf-8') as f:
            history = json.load(f)
        for chat in history:
            if chat.get('role') == 'user' and chat.get('content'):
                content = chat['content'].strip().replace('\n', ' ')
                return content[:30] + ('...' if len(content) > 30 else '')
        return '(대화 없음)'
    except Exception:
        return '(불러오기 오류)'

def extract_date_from_filename(filename):
    try:
        return filename.replace('chat_history_', '').replace('.json', '')
    except:
        return ''

sidebar_files = list_chat_history_files()

# 사이드바: 날짜별 그룹핑 + 제목 리스트
selected_file = st.sidebar.radio(
    '채팅 기록 목록',
    sidebar_files,
    format_func=lambda x: f"{extract_date_from_filename(x)} | {get_chat_title(x)}" if x else '',
    index=0 if sidebar_files else None
)

# 본문: 선택된 채팅 전체 내용 출력
if selected_file:
    st.markdown(f"### 🗂️ {extract_date_from_filename(selected_file)} | {get_chat_title(selected_file)}")
    with open(os.path.join(CHAT_DIR, selected_file), 'r', encoding='utf-8') as f:
        history = json.load(f)
    import re
    latex_pattern = re.compile(r'(\\boxed|\\\(|\\\[|\$)')
    for chat in history:
        if chat['role'] == 'assistant':
            speaker_html = "<img src='https://em-content.zobj.net/source/twitter/376/robot_1f916.png' width='22' style='vertical-align:middle; margin-right:5px;'> <span style='font-size:1.2em; font-weight:bold;'>solar-pro2:</span>"  # 2025-07-11-08:14:03 이미지 아이콘으로 변경 by Cascade
        else:
            speaker_html = "<img src='https://em-content.zobj.net/source/twitter/376/person-raising-hand_1f64b.png' width='22' style='vertical-align:middle; margin-right:5px;'> <span style='font-size:1.2em; font-weight:bold;'>사용자:</span>"
        content = chat['content']
        # (2025-07-10-23:45:59) 최종답변(assistant 메시지 중 '최종 답변' 또는 '최종답변' 포함)은 음영 없이 출력
        if chat['role'] == 'assistant' and (('최종 답변' in content) or ('최종답변' in content)):
            st.markdown(
                f"{speaker_html}  {content}",
                unsafe_allow_html=True
            )
        elif chat['role'] == 'assistant':
            st.markdown(
                f"<div style='background-color:#f3f6fa; border-radius:8px; padding:0.7em 1em; margin-bottom:0.7em;'>{speaker_html}<br><span style='font-size:1.0em'>{content}</span></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(f"{speaker_html} <span style='font-size:1.0em'>{content}</span>", unsafe_allow_html=True)

else:
    st.info('저장된 채팅 기록이 없습니다.')

st.caption('2025-07-11-07:39:06 solar-pro2 대화 뷰어 (실행 경로 고정, 읽기 전용) by Cascade')

# (2025-07-11-07:39:06) 주요 변경: 실행 경로 고정, 입력/저장/삭제/모델 API 완전 제거, 읽기 전용 뷰어 구현
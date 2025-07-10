import streamlit as st
import os
import json
import datetime

# 2025-07-10-23:18:33: 대화 기록 뷰어(읽기 전용) 앱 생성 (by Cascade)

st.set_page_config(page_title="solar-pro2 Chat Viewer", page_icon="☀️")
st.title("☀️ solar-pro2 채팅 기록 뷰어")

# 채팅 파일 리스트

def list_chat_history_files():
    files = [f for f in os.listdir('.') if f.startswith('chat_history_') and f.endswith('.json')]
    files.sort(reverse=True)
    return files

def get_chat_title(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
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
last_date = None
selected_file = st.sidebar.radio(
    '채팅 기록 목록',
    sidebar_files,
    format_func=lambda x: f"{extract_date_from_filename(x)} | {get_chat_title(x)}" if x else '',
    index=0 if sidebar_files else None
)

# 본문: 선택된 채팅 전체 내용 출력
if selected_file:
    st.markdown(f"### 🗂️ {extract_date_from_filename(selected_file)} | {get_chat_title(selected_file)}")
    with open(selected_file, 'r', encoding='utf-8') as f:
        history = json.load(f)
    import re
    latex_pattern = re.compile(r'(\\boxed|\\\(|\\\[|\$)')
    for chat in history:
        speaker = "🙋 사용자:" if chat['role'] == 'user' else "🤖 solar-pro2:"
        content = chat['content']
        # (2025-07-10-23:45:59) 최종답변(assistant 메시지 중 '최종 답변' 또는 '최종답변' 포함)은 음영 없이 출력
        if chat['role'] == 'assistant' and (('최종 답변' in content) or ('최종답변' in content)):
            st.markdown(
                f"<span style='font-size:1.4em; font-weight:bold;'>🤖 solar-pro2:</span>  {content}",
                unsafe_allow_html=True
            )
        elif chat['role'] == 'assistant':
            st.markdown(
                f"<div style='background-color:#f3f6fa; border-radius:8px; padding:0.7em 1em; margin-bottom:0.7em;'><span style='font-size:1.4em; font-weight:bold;'>{speaker}</span><br><span style='font-size:1.15em'>{content}</span></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(f"<span style='font-size:1.4em; font-weight:bold;'>{speaker}</span> <span style='font-size:1.15em'>{content}</span>", unsafe_allow_html=True)
else:
    st.info('저장된 채팅 기록이 없습니다.')

st.caption('2025-07-10-23:18:33 solar-pro2 대화 뷰어 (읽기 전용) by Cascade')

# (2025-07-10-23:18:33) 주요 변경: 입력/저장/삭제/모델 API 완전 제거, 읽기 전용 뷰어 구현

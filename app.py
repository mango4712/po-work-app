import streamlit as st
import pandas as pd
from datetime import date, timedelta
import random
import base64
import os

# ==========================================
# 1. 페이지 설정 및 반응형 귀여운 CSS 디자인
# ==========================================
st.set_page_config(page_title="po-work (포워크)", page_icon="🥔", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    .stApp { background-color: #F0EACA; }
    .block-container { max-width: 480px !important; padding-top: 2rem !important; padding-bottom: 3rem !important; }
    
    .app-title { font-family: 'Jua', sans-serif; text-align: center; font-size: clamp(55px, 15vw, 85px); color: #2e7d32; margin-bottom: 0; line-height: 1.2; text-shadow: 2px 2px 0px #AEF0B7; }
    .app-subtitle { text-align: center; font-family: 'Jua', sans-serif; font-size: 20px; color: #555; margin-top: 5px; margin-bottom: 25px; }
    input, select { font-size: 16px !important; }
    
    .banner-text { font-family: 'Jua', sans-serif; border: 3px dashed #2e7d32; background-color: #ffffff; padding: 12px; border-radius: 15px; color: #2e7d32; font-size: 20px; text-align: center; margin-bottom: 15px; word-break: keep-all; }
    .card-box { border: none; border-radius: 15px; padding: 15px; margin-bottom: 15px; background-color: #ffffff; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); }
    .img-placeholder { border-radius: 10px; height: 90px; display: flex; align-items: center; justify-content: center; font-weight: bold; background-color: #AEF0B7; color: #2e7d32; }
    .info-text { font-size: 14px; line-height: 1.6; margin-bottom: 0; }
    .shuttle-text { font-size: 13px; font-weight: bold; margin-top: 12px; border-top: 2px dashed #eee; padding-top: 10px; color: #555; }
    .red-text { color: #D32F2F; font-weight: bold; text-align: center; font-size: 18px; margin: 15px 0; line-height: 1.5; }
    .blue-notice { color: #1976D2; font-size: 15px; text-align: center; margin-top: 10px; font-weight: bold; }
    .ticket-box { background-color: #fff; border: 2px solid #2e7d32; border-radius: 15px; padding: 20px; margin-top: 20px; border-left: 15px solid #2e7d32; box-shadow: 0px 4px 6px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# ⭐️ 핵심 변경: 모든 접속자가 공유하는 '공용 메모장 (서버 DB 역할)'
# ==========================================
@st.cache_resource
def get_shared_jobs():
    return [
        {"id": 1, "village": "춘천시 신북읍", "job_type": "감자 수확", "work_date": date.today() + timedelta(days=2), "wage": "100,000", "req_people": 4, "current_apply": 2, "photo_b64": None, "temp": "38.5°C", "weather": "☀️ 맑음 (최고 22도)"},
        {"id": 2, "village": "홍천군 서면", "job_type": "옥수수 수확", "work_date": date.today() + timedelta(days=3), "wage": "90,000", "req_people": 2, "current_apply": 2, "photo_b64": None, "temp": "36.5°C", "weather": "☁️ 흐림 (최고 18도)"},
        {"id": 3, "village": "춘천시 동면", "job_type": "비료 운반", "work_date": date.today() + timedelta(days=4), "wage": "120,000", "req_people": 3, "current_apply": 1, "photo_b64": None, "temp": "40.2°C", "weather": "⛅ 구름 조금 (최고 20도)"},
        {"id": 4, "village": "화천군 하남면", "job_type": "잡초 제거", "work_date": date.today() + timedelta(days=5), "wage": "85,000", "req_people": 5, "current_apply": 0, "photo_b64": None, "temp": "37.0°C", "weather": "☀️ 맑음 (최고 25도)"},
        {"id": 5, "village": "양구군 남면", "job_type": "김장 배추", "work_date": date.today() + timedelta(days=6), "wage": "110,000", "req_people": 6, "current_apply": 2, "photo_b64": None, "temp": "39.1°C", "weather": "☀️ 맑음 (최고 15도)"},
    ]

# 모든 유저가 이 SHARED_JOBS 리스트를 똑같이 바라보고 수정하게 됩니다.
SHARED_JOBS = get_shared_jobs()

if 'page' not in st.session_state: st.session_state['page'] = 'home'
if 'selected_job_id' not in st.session_state: st.session_state['selected_job_id'] = None
if 'current_page' not in st.session_state: st.session_state['current_page'] = 1 
if 'filter_type' not in st.session_state: st.session_state['filter_type'] = "전체보기" 
if 'banner_msg' not in st.session_state:
    st.session_state['banner_msg'] = random.choice(["오늘 단기알바 어때요? 🥔", "공강 시간에 쏠쏠하게 벌어가세요! 💸", "주말 농촌 꿀알바 어때요? 🚌"])

def navigate_to(page_name): st.session_state['page'] = page_name

# ==========================================
# 2. 첫 화면 (Home)
# ==========================================
if st.session_state['page'] == 'home':
    st.markdown("<style>div.stButton > button { font-family: 'Jua', sans-serif; height: 80px; font-size: 28px; border: none; border-radius: 20px; margin-bottom: 15px; background-color: white; box-shadow: 0px 4px 6px rgba(0,0,0,0.1); color: #333; transition: all 0.2s ease-in-out; } div.stButton > button:hover { background-color: #AEF0B7; color: #2e7d32; transform: translateY(-2px); }</style>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        try:
            st.image("potato.png", use_container_width=True)
        except:
            st.markdown("<div style='font-size: 100px; text-align: center;'>🥔</div>", unsafe_allow_html=True)

    st.markdown("<h1 class='app-title' style='margin-top: -10px;'>po-work</h1>", unsafe_allow_html=True)
    st.markdown("<p class='app-subtitle'>단기 알바를 모집하고 신청해 보세요!</p>", unsafe_allow_html=True)
    
    if st.button("주 민 🏡", use_container_width=True):
        navigate_to('resident_login')
        st.rerun()
    if st.button("대 학 생 🎓", use_container_width=True):
        navigate_to('student_login')
        st.rerun()

# ==========================================
# 3. 로그인 화면 (주민 / 대학생)
# ==========================================
elif st.session_state['page'] == 'resident_login':
    st.markdown("<style>div.stButton > button { font-family: 'Jua', sans-serif; border-radius: 12px; font-size: 18px; }</style>", unsafe_allow_html=True)
    st.markdown("<p style='font-family: \"Jua\", sans-serif; font-size: 20px; color: #2e7d32; margin-bottom: -15px;'>po-work</p>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-family: \"Jua\", sans-serif; margin-top: 0;'>주민 로그인 🏡</h1>", unsafe_allow_html=True)
    
    with st.form("resident_login_form"):
        st.write("안전한 일손 매칭을 위해 마을 인증을 진행합니다.")
        st.text_input("성함", placeholder="예: 홍길동")
        st.text_input("휴대전화 번호", placeholder="예: 010-1234-5678")
        st.text_input("거주 마을 / 지역", placeholder="예: 춘천시 신북읍")
        
        if st.form_submit_button("인증하고 시작하기", use_container_width=True):
            navigate_to('resident')
            st.rerun()
            
    if st.button("⬅️ 처음 화면으로", use_container_width=True):
        navigate_to('home')
        st.rerun()

elif st.session_state['page'] == 'student_login':
    st.markdown("<style>div.stButton > button { font-family: 'Jua', sans-serif; border-radius: 12px; font-size: 18px; }</style>", unsafe_allow_html=True)
    st.markdown("<p style='font-family: \"Jua\", sans-serif; font-size: 20px; color: #2e7d32; margin-bottom: -15px;'>po-work</p>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-family: \"Jua\", sans-serif; margin-top: 0;'>대학생 로그인 🎓</h1>", unsafe_allow_html=True)
    
    with st.form("student_login_form"):
        st.write("안전한 매칭을 위해 대학교 학생 인증을 진행합니다.")
        st.text_input("이름", placeholder="예: 홍길동") 
        st.text_input("학교명", placeholder="예: 강원대학교")
        st.text_input("학번", placeholder="예: 202600000")
        st.text_input("휴대전화 번호", placeholder="예: 010-1234-5678")
        
        if st.form_submit_button("학교 인증하고 시작하기", use_container_width=True):
            navigate_to('student_list')
            st.rerun()
            
    if st.button("⬅️ 처음 화면으로", use_container_width=True):
        navigate_to('home')
        st.rerun()

# ==========================================
# 4. 마을 주민 화면
# ==========================================
elif st.session_state['page'] == 'resident':
    st.markdown("<style>div.stButton > button { font-family: 'Jua', sans-serif; border-radius: 12px; font-size: 18px; }</style>", unsafe_allow_html=True)
    st.markdown("<p style='font-family: \"Jua\", sans-serif; font-size: 20px; color: #2e7d32; margin-bottom: -15px;'>po-work</p>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-family: \"Jua\", sans-serif; margin-top: 0;'>마을 주민 홈 🏡</h1>", unsafe_allow_html=True)
    
    st.write("📝 **일손 요청서 작성**")
    name_contact = st.text_input("접수 마을회관 / 연락처")
    work_date = st.date_input("날짜")
    location = st.text_input("상세 장소")
    
    job_options = ["감자 수확", "옥수수 수확", "김장 배추", "비료 운반", "잡초 제거", "기타 (직접입력)"]
    selected_job = st.selectbox("하는 일 분류", job_options)
    
    job_desc = selected_job
    if selected_job == "기타 (직접입력)": 
        job_desc = st.text_input("하는 일 (직접 적어주세요)")
        
    req_people = st.number_input("필요한 인원", min_value=1, value=1)
    wage = st.text_input("일당 (예: 100,000)")
    uploaded_photo = st.file_uploader("밭이나 작물 사진 첨부 (선택)", type=["png", "jpg", "jpeg"])
    
    col_blank, col_submit = st.columns([2.5, 1.2])
    with col_submit:
        if st.button("완 료", use_container_width=True):
            photo_b64_str = base64.b64encode(uploaded_photo.getvalue()).decode("utf-8") if uploaded_photo else None
            new_job = {
                "id": len(SHARED_JOBS) + 1,
                "village": location, "job_type": job_desc, "work_date": work_date,
                "wage": wage, "req_people": req_people, "current_apply": 0,
                "photo_b64": photo_b64_str,
                "temp": "36.5°C", "weather": "날씨 정보 대기중" 
            }
            # 공용 게시판(SHARED_JOBS)에 새 알바 정보를 추가!
            SHARED_JOBS.append(new_job)
            navigate_to('resident_success')
            st.rerun()

    col_back, col_blank2 = st.columns([1.5, 2.5])
    with col_back:
        if st.button("⬅️ 로그아웃", use_container_width=True):
            navigate_to('home')
            st.rerun()

elif st.session_state['page'] == 'resident_success':
    st.markdown("<style>div.stButton > button { font-family: 'Jua', sans-serif; border-radius: 12px; font-size: 20px; height: 60px; background-color: #ffffff; }</style>", unsafe_allow_html=True)
    st.write("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 class='app-title'>po-work</h1>", unsafe_allow_html=True)
    st.write("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-family: \"Jua\", sans-serif; text-align: center; word-break: keep-all; line-height: 1.5;'>일손 요청 게시글이<br>업로드 되었습니다 ✨</h3>", unsafe_allow_html=True)
    st.write("<br><br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.5, 2, 0.5])
    with col2:
        if st.button("주민 홈으로", use_container_width=True):
            navigate_to('resident')
            st.rerun()

# ==========================================
# 5. 대학생 화면 - 리스트 
# ==========================================
elif st.session_state['page'] == 'student_list':
    st.markdown("<style>div.stButton > button { font-family: 'Jua', sans-serif; border-radius: 10px; }</style>", unsafe_allow_html=True)
    
    col_logo, col_logout = st.columns([3, 1])
    with col_logo:
        st.markdown("<p style='font-family: \"Jua\", sans-serif; font-size: 20px; color: #2e7d32; margin-bottom: -15px;'>po-work</p>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-family: \"Jua\", sans-serif; margin-top: 0;'>대 학 생 🎓</h1>", unsafe_allow_html=True)
    with col_logout:
        st.write("<br>", unsafe_allow_html=True)
        if st.button("로그아웃"):
            navigate_to('home')
            st.rerun()
            
    st.markdown(f"<div class='banner-text'>{st.session_state['banner_msg']}</div>", unsafe_allow_html=True)
    
    unique_job_types = list(set([job['job_type'] for job in SHARED_JOBS]))
    filter_options = ["전체보기"] + sorted(unique_job_types)
    selected_filter = st.selectbox("🔍 어떤 종류의 알바를 찾으시나요?", filter_options, index=filter_options.index(st.session_state['filter_type']) if st.session_state['filter_type'] in filter_options else 0)
    
    if selected_filter != st.session_state['filter_type']:
        st.session_state['filter_type'] = selected_filter
        st.session_state['current_page'] = 1
        st.rerun()
        
    filtered_jobs = SHARED_JOBS if st.session_state['filter_type'] == "전체보기" else [j for j in SHARED_JOBS if j['job_type'] == st.session_state['filter_type']]
    
    items_per_page = 3
    reversed_jobs = list(reversed(filtered_jobs)) 
    total_pages = max(1, (len(reversed_jobs) - 1) // items_per_page + 1)
    
    if st.session_state['current_page'] > total_pages: st.session_state['current_page'] = 1
    paginated_jobs = reversed_jobs[(st.session_state['current_page'] - 1) * items_per_page : (st.session_state['current_page']) * items_per_page]
    
    if len(paginated_jobs) == 0:
        st.info("해당 업무의 알바 공고가 없습니다.")
    else:
        for job in paginated_jobs:
            st.markdown("<div class='card-box'>", unsafe_allow_html=True)
            col_img, col_info, col_btn = st.columns([1.2, 2.5, 1])
            
            with col_img:
                if job.get('photo_b64'):
                    img_html = f"<img src='data:image/jpeg;base64,{job['photo_b64']}' style='width: 100%; height: 90px; object-fit: cover; border-radius: 10px; border: 1px solid #ccc;'/>"
                    st.markdown(img_html, unsafe_allow_html=True)
                else:
                    st.markdown("<div class='img-placeholder'>사진</div>", unsafe_allow_html=True)
                    
            with col_info:
                st.markdown(f"""
                <p class='info-text'>
                    {job['village']} <span style='font-size:12px; color:#E65100; font-weight:bold;'>🌡️{job.get('temp', '36.5°C')}</span><br>
                    {job['work_date']}<br>
                    (하는일) {job['job_type']}<br>
                    <b>일당 : {job['wage']} 원</b>
                </p>
                """, unsafe_allow_html=True)
                
            with col_btn:
                if job['current_apply'] >= job['req_people']:
                    st.button("마 감", key=f"list_btn_{job['id']}", disabled=True, use_container_width=True)
                else:
                    if st.button("신 청", key=f"list_btn_{job['id']}", use_container_width=True):
                        st.session_state['selected_job_id'] = job['id']
                        navigate_to('student_detail')
                        st.rerun()
            
            st.markdown(f"<div class='shuttle-text'>🚌 셔틀노선 : 강원대 후문 ➔ {job['village'].split()[0]}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    col_blank1, col_prev, col_page, col_next, col_blank2 = st.columns([1, 1, 1.2, 1, 1])
    with col_prev:
        if st.button("◀", disabled=(st.session_state['current_page'] <= 1), use_container_width=True):
            st.session_state['current_page'] -= 1; st.rerun()
    with col_page:
        st.markdown(f"<div style='font-family: \"Jua\", sans-serif; text-align: center; margin-top: 10px; font-size: 18px; color: #555;'>{st.session_state['current_page']} / {total_pages}</div>", unsafe_allow_html=True)
    with col_next:
        if st.button("▶", disabled=(st.session_state['current_page'] >= total_pages), use_container_width=True):
            st.session_state['current_page'] += 1; st.rerun()

# ==========================================
# 6. 대학생 화면 - 상세페이지
# ==========================================
elif st.session_state['page'] == 'student_detail':
    job = next((j for j in SHARED_JOBS if j['id'] == st.session_state['selected_job_id']), None)
    
    st.markdown("<p style='font-family: \"Jua\", sans-serif; font-size: 20px; color: #2e7d32; margin-bottom: -15px;'>po-work</p>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-family: \"Jua\", sans-serif; margin-top: 0;'>대 학 생 🎓</h1>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background-color: white; padding: 20px; border-radius: 15px; margin-top: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.05);'>
        <div style='font-size: 20px; margin-bottom: 15px;'>
            <b>(하는일) {job['job_type']}</b><br>
            일당 : <span style='color:#2e7d32; font-weight:bold;'>{job['wage']} 원</span>
        </div>
        <div style='font-size: 15px; line-height: 1.8; color: #444; border-bottom: 1px dashed #ddd; padding-bottom: 15px; margin-bottom: 15px;'>
            📍 장소 : {job['village']} <span style='color:#E65100; font-weight:bold;'>(농가 감자온도: {job.get('temp', '36.5°C')})</span><br>
            ⏰ 일시 : {job['work_date']} 09:00~18:00<br>
            🌤️ <b>당일 날씨 예보 : {job.get('weather', '알 수 없음')}</b>
        </div>
        <div style='font-size: 14px; font-weight:bold; color: #555;'>
            🚌 셔틀노선 : 강원대 후문 ➔ 구봉산 ➔ {job['village'].split()[0]}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<div class='red-text' style='font-family: \"Jua\", sans-serif; font-size: 22px;'>모집인원 : {job['req_people']}<br>신청인원 : {job['current_apply']}</div>", unsafe_allow_html=True)
    
    st.markdown("<style>#apply_btn > button { font-family: 'Jua', sans-serif; height: 65px; font-size: 24px; border: none; background-color: #2e7d32; color: white; border-radius: 15px; box-shadow: 0px 4px 6px rgba(46,125,50,0.3); }</style>", unsafe_allow_html=True)
    st.markdown("<div id='apply_btn'>", unsafe_allow_html=True)
    if st.button("신 청 하 기", use_container_width=True):
        navigate_to('student_apply_form')
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='blue-notice'>* 신청후 취소가 어렵습니다</div>", unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    col_back, col_blank = st.columns([1.5, 3])
    with col_back:
        if st.button("⬅️ 뒤로가기", use_container_width=True):
            navigate_to('student_list')
            st.rerun()

# ==========================================
# 7. 대학생 화면 - 신청 정보 입력 폼
# ==========================================
elif st.session_state['page'] == 'student_apply_form':
    job = next((j for j in SHARED_JOBS if j['id'] == st.session_state['selected_job_id']), None)
    
    st.markdown("<style>div.stButton > button { font-family: 'Jua', sans-serif; border-radius: 12px; font-size: 18px; }</style>", unsafe_allow_html=True)
    st.markdown("<p style='font-family: \"Jua\", sans-serif; font-size: 20px; color: #2e7d32; margin-bottom: -15px;'>po-work</p>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-family: \"Jua\", sans-serif; margin-top: 0;'>대 학 생 🎓</h1>", unsafe_allow_html=True)
    
    st.info(f"선택한 알바: {job['village']} - {job['job_type']}")
    
    remaining_spots = job['req_people'] - job['current_apply']
    
    with st.form("student_apply_info_form"):
        st.write("📝 **알바 추가 확인 정보**")
        
        companion_options = ["혼자 갈래요 🙋‍♀️"]
        if remaining_spots >= 2: companion_options.append("친구 1명 같이 가요 👯‍♀️ (+1명)")
        if remaining_spots >= 3: companion_options.append("친구 2명 같이 가요 👨‍👩‍👧 (+2명)")
        
        companion = st.selectbox("친구와 동반 신청하시겠어요?", companion_options)
        
        col_blank, col_submit = st.columns([1.5, 2.5])
        with col_submit:
            if st.form_submit_button("최종 신청 완료하기", use_container_width=True):
                apply_count = 1
                if "1명" in companion: apply_count = 2
                elif "2명" in companion: apply_count = 3
                
                # 공용 게시판(SHARED_JOBS)에 신청 인원 반영!
                job['current_apply'] += apply_count
                st.session_state['last_apply_count'] = apply_count
                navigate_to('student_success')
                st.rerun()
                
    col_back, col_blank2 = st.columns([1.5, 2.5])
    with col_back:
        if st.button("⬅️ 뒤로가기", use_container_width=True):
            navigate_to('student_detail')
            st.rerun()

# ==========================================
# 8. 대학생 화면 - 신청 완료 (탑승권)
# ==========================================
elif st.session_state['page'] == 'student_success':
    job = next((j for j in SHARED_JOBS if j['id'] == st.session_state['selected_job_id']), None)
    apply_count = st.session_state.get('last_apply_count', 1)
    
    st.markdown("<style>div.stButton > button { font-family: 'Jua', sans-serif; border-radius: 12px; font-size: 20px; height: 60px; background-color: #ffffff; }</style>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    st.markdown("<h1 class='app-title'>po-work</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-family: \"Jua\", sans-serif; text-align: center; color: #2e7d32;'>일손 신청 완료 🎉</h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='ticket-box'>
        <h4 style='margin-top:0; color:#2e7d32; border-bottom: 2px dashed #ccc; padding-bottom: 10px;'>🚌 po-work 셔틀 탑승권</h4>
        <p style='font-size: 15px; line-height: 1.8; margin-bottom: 0;'>
            <b>목적지 :</b> {job['village']} ({job['job_type']})<br>
            <b>날 짜 :</b> {job['work_date']}<br>
            <b>탑승장 :</b> 강원대학교 후문 버스정류장<br>
            <b>탑승인원 :</b> 총 {apply_count}명
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    
    st.markdown("<style>#board_btn > button { background-color: #E65100; color: white; border: none; box-shadow: 0px 4px 6px rgba(230,81,0,0.3); }</style>", unsafe_allow_html=True)
    st.markdown("<div id='board_btn'>", unsafe_allow_html=True)
    if st.button("📍 셔틀 탑승 완료! (이장님께 알림 보내기)", use_container_width=True):
        st.toast(f"✅ {job['village']} 이장님께 '{apply_count}명 셔틀 탑승 완료' 알림이 전송되었습니다!", icon="🚌")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.5, 2, 0.5])
    with col2:
        if st.button("대학생 홈으로", use_container_width=True):
            st.session_state['banner_msg'] = random.choice(["오늘 단기알바 어때요? 🥔", "공강 시간에 쏠쏠하게 벌어가세요! 💸", "주말 농촌 꿀알바 어때요? 🚌"])
            navigate_to('student_list')
            st.rerun()

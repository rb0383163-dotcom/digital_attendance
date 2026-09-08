import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date
import io

# Page Config
st.set_page_config(
    page_title="Digital Attendance",
    page_icon="📊",
    layout="wide"
)

# Credentials
USERNAME = "admin"
PASSWORD = "1234"
SUBJECTS = ["PATHWAY", "CY LAB"]

DATA_FOLDER = Path("data")
DATA_FOLDER.mkdir(exist_ok=True)
STUDENT_FILE = DATA_FOLDER / "students.csv"
ATTENDANCE_FILE = DATA_FOLDER / "attendance.csv"

STUDENT_DATA = [
    ("174CY24001", "A KUSUMITHA"), ("174CY24003", "AFTHAB"), ("174CY24004", "AKASH B"),
    ("174CY24005", "ALTAF H"), ("174CY24007", "B M MAHESH"), ("174CY24008", "B SAIFULLA"),
    ("174CY24009", "BHARATH SAJJAN S"), ("174CY24012", "G S ABHISHEK"), ("174CY2413", "GIRISH G M"),
    ("174CY24015", "H B HARSHAVARDHANA"), ("174CY24016", "H HANEEF"), ("174CY24018", "HOOLESH N"),
    ("174CY24020", "K BHUMIKA"), ("174CY24021", "K M RAJA"), ("174CY24022", "K N SANJAYA"),
    ("174CY24023", "KODERA KOTRESHA"), ("174CY24025", "LAVANYA"), ("174CY2027", "M PAVANA KUMARA"),
    ("174CY24028", "M PREMA"), ("174CY24029", "M SIDDIQ"), ("174CY24030", "M TAKIB"),
    ("174CY24031", "MANJUNATHA B T"), ("174CY24033", "MOHAMMAD RUMAN J"), ("174CY24034", "MOHAMMED RAFIQ"),
    ("174CY24036", "N M KEERTHI"), ("174CY24037", "N SRINIVASA"), ("174CY24038", "PARAMESHA S H"),
    ("174CY24040", "RAMESHA L"), ("174CY24041", "RIYAZ SAB K"), ("174CY24042", "ROSHNI"),
    ("174CY24043", "RUSHIKETHAN P S"), ("174CY24044", "SAHARA BEGAM"), ("174CY24045", "SAMARTHA G"),
    ("174CY24048", "SUMA A"), ("174CY24049", "SWAPNA G"), ("174CY24051", "VINAY K"),
    ("174CY24052", "VISHWARADHYA B M"), ("174CY25401", "RAVIKUMARA S M"), ("174CY25701", "DHANUNJAYA J"),
    ("174CY25703", "PALLAVI H C"), ("174CY25705", "YOGESHA P"),
]

def create_student_file():
    pd.DataFrame(STUDENT_DATA, columns=["Reg No", "Name"]).to_csv(STUDENT_FILE, index=False)

def create_attendance_file():
    if not ATTENDANCE_FILE.exists():
        pd.DataFrame(columns=["Date", "Reg No", "Name", "Subject", "Status"]).to_csv(ATTENDANCE_FILE, index=False)

def load_students(): return pd.read_csv(STUDENT_FILE)
def load_attendance():
    try: return pd.read_csv(ATTENDANCE_FILE)
    except: return pd.DataFrame(columns=["Date", "Reg No", "Name", "Subject", "Status"])
def save_attendance(df): df.to_csv(ATTENDANCE_FILE, index=False)

st.markdown("""
<style>
.main-title {font-size:28px; font-weight:800; color:#2563eb;}
.student-card {background:white; border:1px solid #e2e8f0; border-radius:12px; padding:10px; margin-bottom:8px;}
@media (max-width: 768px) {.block-container{padding:0.8rem;} .stButton button{min-height:48px;}}
</style>
""", unsafe_allow_html=True)

create_student_file()
create_attendance_file()
if "logged_in" not in st.session_state: st.session_state.logged_in = False

def login_page():
    st.markdown('<div class="main-title">Digital Attendance</div><p>Cumulative Attendance System</p>', unsafe_allow_html=True)
    _, c, _ = st.columns([1,2,1])
    with c:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("LOGIN", type="primary", use_container_width=True):
            if u == USERNAME and p == PASSWORD:
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("Invalid login")

def main_app():
    students = load_students()
    attendance = load_attendance()
    
    with st.sidebar:
        st.title("Attendance")
        page = st.radio("Menu", ["Dashboard", "Mark Attendance", "Student Details", "Reports", "Download"])
        if st.button("LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    if page == "Dashboard":
        st.markdown('<div class="main-title">Dashboard</div>', unsafe_allow_html=True)
        total = len(attendance)
        present = len(attendance[attendance["Status"]=="Present"])
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Students", len(students)); c2.metric("Total Records", total)
        c3.metric("Present", present); c4.metric("Percentage", f"{(present/total*100 if total else 0):.1f}%")
        
        if not attendance.empty:
            rows = []
            for _, s in students.iterrows():
                rec = attendance[attendance["Reg No"]==s["Reg No"]]
                tot = len(rec); pres = len(rec[rec["Status"]=="Present"])
                perc = (pres/tot*100 if tot else 0)
                rows.append({"Reg No": s["Reg No"], "Name": s["Name"], "Total": tot, "Present": pres, "Absent": tot-pres, "Percentage": round(perc,1)})
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    elif page == "Mark Attendance":
        st.markdown('<div class="main-title">Mark Attendance</div>', unsafe_allow_html=True)
        col1,col2 = st.columns(2)
        with col1: subject = st.selectbox("Subject", SUBJECTS)
        with col2: selected_date = st.date_input("Date", value=date.today())
        search = st.text_input("Search Student")

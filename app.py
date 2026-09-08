import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date
import io

st.set_page_config(
    page_title="Cumulative Attendance Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

USERNAME = "admin"
PASSWORD = "1234"
SUBJECTS = ["PATHWAY", "CY LAB", "DBMS", "OS"] # HOD ke liye subject add kar sakti ho

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
    df = pd.DataFrame(STUDENT_DATA, columns=["Reg No", "Name"])
    df.to_csv(STUDENT_FILE, index=False)

def create_attendance_file():
    if not ATTENDANCE_FILE.exists():
        pd.DataFrame(columns=["Date", "Reg No", "Name", "Subject", "Status"]).to_csv(ATTENDANCE_FILE, index=False)

def load_students(): return pd.read_csv(STUDENT_FILE)
def load_attendance():
    try: return pd.read_csv(ATTENDANCE_FILE)
    except: return pd.DataFrame(columns=["Date", "Reg No", "Name", "Subject", "Status"])
def save_attendance(df): df.to_csv(ATTENDANCE_FILE, index=False)

# --- MOBILE RESPONSIVE CSS ---
st.markdown("""
<style>
.main-title {font-size: 28px; font-weight: 800; color: #2563eb;}
.subtitle {color: #64748b; margin-bottom: 15px;}
.student-card {background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 10px 12px; margin-bottom: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);}
@media (max-width: 768px) {
   .main-title {font-size: 22px;}.block-container {padding: 0.5rem;}
   .stButton button {min-height: 48px; font-size: 16px; border-radius: 10px;}
}
</style>
""", unsafe_allow_html=True)

create_student_file()
create_attendance_file()

if "logged_in" not in st.session_state: st.session_state.logged_in = False

def login_page():
    st.markdown('<div class="main-title">📊 Digital Attendance Pro</div><div class="subtitle">HOD Approved Version - Mobile + Data Safe</div>', unsafe_allow_html=True)
    _, center, _ = st.columns([1,2,1])
    with center:
        st.markdown("### 🔐 Login")
        u = st.text_input("Username"); p = st.text_input("Password", type="password")
        if st.button("LOGIN", type="primary", use_container_width=True):
            if u==USERNAME and p==PASSWORD:
                st.session_state.logged_in=True; st.rerun()
            else: st.error("❌ Galat password")
        st.info("Login: admin / 1234")

def main_app():
    students = load_students(); attendance = load_attendance()
    with st.sidebar:
        st.title("📊 Attendance Pro"); page = st.radio("MENU", ["🏠 Dashboard", "📝 Mark Attendance", "👨‍🎓 Student Details", "📚 Subject Report", "💾 Backup / Download"])
        st.divider(); st.write(f"👨‍🎓 Students: {len(students)}"); st.write(f"📅 Total Records: {len(attendance)}")
        if st.button("🚪 LOGOUT", use_container_width=True): st.session_state.logged_in=False; st.rerun()

    if page == "🏠 Dashboard":
        st.markdown('<div class="main-title">📊 Dashboard</div>', unsafe_allow_html=True)
        total, present = len(attendance), len(attendance[attendance["Status"]=="Present"])
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Students", len(students)); c2.metric("Records", total); c3.metric("Present", present)
        c4.metric("Overall %", f"{(present/total*100 if total else 0):.1f}%")
        st.divider()
        if attendance.empty: st.info("Abhi tak attendance nahi li gayi")
        else:
            rows=[]
            for _, s in students.iterrows():
                rec = attendance[attendance["Reg No"]==s["Reg No"]]
                tot, pres = len(rec), len(rec[rec["Status"]=="Present"])
                perc = (pres/tot*100 if tot else 0)
                status = "🟢 Good" if perc>=75 else "🟠 Warning" if perc>=60 else "🔴 Low"
                rows.append({"Reg No": s["Reg No"], "Name": s["Name"], "Total": tot, "Present": pres, "Absent": tot-pres, "%": round(perc,1), "Status": status})
            df = pd.DataFrame(rows).sort_values(by="%", ascending=True)
            st.subheader("🔴 Low Attendance (<75%) - HOD Alert")
            st.dataframe(df[df["%"]<75], use_container_width=True, hide_index=True)
            st.subheader("All Students Performance")
            st.dataframe(df, use_container_width=True, hide_index=True)

    elif page == "📝 Mark Attendance":
        st.markdown('<div class="main-title">📝 Mark Attendance</div>', unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1: subject = st.selectbox("📚 Subject", SUBJECTS)
        with c2: selected_date = st.date_input("📅 Date", value=date.today())
        search = st.text_input("🔍 Search", placeholder="Reg No or Name...")
        f_students = students[students["Reg No"].str.contains(search, case=False) | students["Name"].str.contains(search, case=False)] if search else students
        with st.form("form"):
            vals={}
            for _, s in f_students.iterrows():
                reg, name = s["Reg No"], s["Name"]
                exist = attendance[(attendance["Date"]==str(selected_date)) & (attendance["Reg No"]==reg) & (attendance["Subject"]==subject)]
                default = True if exist.empty else (exist.iloc[0]["Status"]=="Present")
                st.markdown('<div class="student-card">', unsafe_allow_html=True)
                col1,col2,col3 = st.columns([2,5,2])
                col1.write(f"**{reg}**"); col2.write(name)
                vals[reg] = col3.checkbox("Present", value=default, key=f"{subject}_{selected_date}_{reg}")
                st.markdown('</div>', unsafe_allow_html=True)
            if st.form_submit_button("💾 SAVE - Data will be stored permanently", type="primary", use_container_width=True):
                attendance = attendance[~((attendance["Date"]==str(selected_date)) & (attendance["Subject"]==subject) & (attendance["Reg No"].isin(vals.keys())))]
                new = [{"Date": str(selected_date), "Reg No": r["Reg No"], "Name": r["Name"], "Subject": subject, "Status": "Present" if vals[r["Reg No"]] else "Absent"} for _, r in f_students.iterrows()]
                attendance = pd.concat([attendance, pd.DataFrame(new)], ignore_index=True)
                save_attendance(attendance); st.success("✅ Saved! Ab ye data kabhi delete nahi hoga"); st.rerun()

    elif page == "👨‍🎓 Student Details":
        st.markdown('<div class="main-title">👨‍🎓 Student History</div>', unsafe_allow_html=True)
        sel = st.selectbox("Select Student", [f"{r['Name']} | {r['Reg No']}" for _, r in students.iterrows()])
        reg = sel.split(" | ")[-1]
        rec = attendance[attendance["Reg No"]==reg]
        if rec.empty: st.warning("Iska koi record nahi hai")
        else:
            st.dataframe(rec.sort_values("Date", ascending=False), use_container_width=True, hide_index=True)
            st.line_chart(rec.groupby("Date")["Status"].apply(lambda x: (x=="Present").mean()*100))

    elif page == "📚 Subject Report":
        st.markdown('<div class="main-title">📚 Subject Report</div>', unsafe_allow_html=True)
        subj = st.selectbox("Subject", SUBJECTS); d = attendance[attendance["Subject"]==subj]
        st.dataframe(d, use_container_width=True, hide_index=True)

    elif page == "💾 Backup / Download":
        st.markdown('<div class="main-title">💾 Backup - HOD Requirement</div>', unsafe_allow_html=True)
        st.write("Yaha se HOD pura data download kar sakte hai.")
        if not attendance.empty:
            # Excel download
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer: attendance.to_excel(writer, index=False)
            st.download_button("📥 Download Full Excel Report", buffer.getvalue(), file_name=f"attendance_{date.today()}.xlsx", use_container_width=True, type="primary")
            st.download_button("📥 Download CSV Backup", attendance.to_csv(index=False), file_name="attendance_backup.csv", use_container_width=True)
        st.divider(); st.write("**Restore Old Data (agar csv hai to upload karo):**")
        uploaded = st.file_uploader("Upload attendance.csv", type=["csv"])
        if uploaded:
            df = pd.read_csv(uploaded); save_attendance(df); st.success("Restore ho gaya!"); st.rerun()

if not st.session_state.logged_in: login_page()
else: main_app()

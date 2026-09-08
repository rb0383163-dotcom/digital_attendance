import streamlit as st
import pandas as pd
from datetime import date, datetime
from supabase import create_client

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Digital Attendance",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# LOGIN
# =========================================================

USERNAME = "admin"
PASSWORD = "1234"

SUBJECTS = ["PATHWAY", "CY LAB"]

# =========================================================
# STUDENT DATA
# =========================================================

STUDENT_DATA = [
    ("174CY24001", "A KUSUMITHA"),
    ("174CY24003", "AFTHAB"),
    ("174CY24004", "AKASH B"),
    ("174CY24005", "ALTAF H"),
    ("174CY24007", "B M MAHESH"),
    ("174CY24008", "B SAIFULLA"),
    ("174CY24009", "BHARATH SAJJAN S"),
    ("174CY24012", "G S ABHISHEK"),
    ("174CY24013", "GIRISH G M"),
    ("174CY24015", "H B HARSHAVARDHANA"),
    ("174CY24016", "H HANEEF"),
    ("174CY24018", "HOOLESH N"),
    ("174CY24020", "K BHUMIKA"),
    ("174CY24021", "K M RAJA"),
    ("174CY24022", "K N SANJAYA"),
    ("174CY24023", "KODERA KOTRESHA"),
    ("174CY24025", "LAVANYA"),
    ("174CY24027", "M PAVANA KUMARA"),
    ("174CY24028", "M PREMA"),
    ("174CY24029", "M SIDDIQ"),
    ("174CY24030", "M TAKIB"),
    ("174CY24031", "MANJUNATHA B T"),
    ("174CY24033", "MOHAMMAD RUMAN J"),
    ("174CY24034", "MOHAMMED RAFIQ"),
    ("174CY24036", "N M KEERTHI"),
    ("174CY24037", "N SRINIVASA"),
    ("174CY24038", "PARAMESHA S H"),
    ("174CY24040", "RAMESHA L"),
    ("174CY24041", "RIYAZ SAB K"),
    ("174CY24042", "ROSHNI"),
    ("174CY24043", "RUSHIKETHAN P S"),
    ("174CY24044", "SAHARA BEGAM"),
    ("174CY24045", "SAMARTHA G"),
    ("174CY24048", "SUMA A"),
    ("174CY24049", "SWAPNA G"),
    ("174CY24051", "VINAY K"),
    ("174CY24052", "VISHWARADHYA B M"),
    ("174CY25401", "RAVIKUMARA S M"),
    ("174CY25701", "DHANUNJAYA J"),
    ("174CY25703", "PALLAVI H C"),
    ("174CY25705", "YOGESHA P"),
]

students = pd.DataFrame(
    STUDENT_DATA,
    columns=["Reg No", "Name"]
)

# =========================================================
# SUPABASE CONNECTION
# =========================================================

@st.cache_resource
def get_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = get_supabase()
except Exception:
    st.error("Supabase connection failed. Please check Streamlit Secrets.")
    st.stop()

# =========================================================
# DATABASE FUNCTIONS
# =========================================================

def load_attendance():
    try:
        response = (
            supabase
            .table("Attendance")
            .select("*")
            .order("attendance date", desc=True)
            .execute()
        )

        data = response.data

        if not data:
            return pd.DataFrame(
                columns=[
                    "id",
                    "student name",
                    "student id",
                    "attendance date",
                    "status",
                    "created at"
                ]
            )

        return pd.DataFrame(data)

    except Exception as e:
        st.error(f"Unable to load attendance: {e}")
        return pd.DataFrame()


def save_attendance(records):
    try:
        response = (
            supabase
            .table("Attendance")
            .insert(records)
            .execute()
        )

        return True

    except Exception as e:
        st.error(f"Unable to save attendance: {e}")
        return False


def delete_existing_attendance(attendance_date, student_ids):
    try:
        for student_id in student_ids:
            (
                supabase
                .table("Attendance")
                .delete()
                .eq("attendance date", str(attendance_date))
                .eq("student id", student_id)
                .execute()
            )

        return True

    except Exception as e:
        st.error(f"Unable to update attendance: {e}")
        return False


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>
    .main-title {
        font-size: 30px;
        font-weight: 800;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 0.8rem;
        }

        .stButton button {
            min-height: 45px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SESSION
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    st.markdown(
        '<div class="main-title">📊 Digital Attendance</div>',
        unsafe_allow_html=True
    )

    st.write("Student Attendance Management System")

    _, center, _ = st.columns([1, 2, 1])

    with center:

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "LOGIN",
            type="primary",
            use_container_width=True
        ):

            if username == USERNAME and password == PASSWORD:

                st.session_state.logged_in = True
                st.rerun()

            else:

                st.error("Invalid username or password.")


# =========================================================
# MAIN APPLICATION
# =========================================================

def main_app():

    attendance = load_attendance()

    # -----------------------------------------------------
    # SIDEBAR
    # -----------------------------------------------------

    with st.sidebar:

        st.title("📊 Attendance")

        page = st.radio(
            "Menu",
            [
                "🏠 Dashboard",
                "📝 Mark Attendance",
                "👨‍🎓 Student Details",
                "📅 Attendance History",
                "📚 Reports",
                "⬇️ Download"
            ]
        )

        st.divider()

        if st.button(
            "LOGOUT",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.rerun()

    # =====================================================
    # DASHBOARD
    # =====================================================

    if page == "🏠 Dashboard":

        st.markdown(
            '<div class="main-title">🏠 Dashboard</div>',
            unsafe_allow_html=True
        )

        st.write(
            f"Today's Date: **{date.today().strftime('%d-%m-%Y')}**"
        )

        total_students = len(students)

        total_records = len(attendance)

        if not attendance.empty:
            present_count = len(
                attendance[
                    attendance["status"].astype(str).str.lower()
                    == "present"
                ]
            )
        else:
            present_count = 0

        percentage = (
            present_count / total_records * 100
            if total_records
            else 0
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Students",
            total_students
        )

        c2.metric(
            "Total Records",
            total_records
        )

        c3.metric(
            "Present",
            present_count
        )

        c4.metric(
            "Percentage",
            f"{percentage:.1f}%"
        )

        if not attendance.empty:

            st.subheader("Student Attendance Summary")

            rows = []

            for _, student in students.iterrows():

                student_id = student["Reg No"]

                student_name = student["Name"]

                records = attendance[
                    attendance["student id"].astype(str)
                    == str(student_id)
                ]

                total = len(records)

                present = len(
                    records[
                        records["status"].astype(str).str.lower()
                        == "present"
                    ]
                )

                absent = total - present

                percent = (
                    present / total * 100
                    if total
                    else 0
                )

                rows.append(
                    {
                        "Reg No": student_id,
                        "Name": student_name,
                        "Total": total,
                        "Present": present,
                        "Absent": absent,
                        "Percentage": round(percent, 1)
                    }
                )

            summary = pd.DataFrame(rows)

            st.dataframe(
                summary,
                use_container_width=True,
                hide_index=True
            )

    # =====================================================
    # MARK ATTENDANCE
    # =====================================================

    elif page == "📝 Mark Attendance":

        st.markdown(
            '<div class="main-title">📝 Mark Attendance</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            subject = st.selectbox(
                "Subject",
                SUBJECTS
            )

        with col2:

            selected_date = st.date_input(
                "Attendance Date",
                value=date.today()
            )

        search = st.text_input(
            "🔍 Search Student"
        )

        display_students = students.copy()

        if search:

            search_lower = search.lower()

            display_students = display_students[
                display_students["Reg No"].str.lower().str.contains(
                    search_lower
                )
                |
                display_students["Name"].str.lower().str.contains(
                    search_lower
                )
            ]

        st.write(
            f"**Students: {len(display_students)}**"
        )

        attendance_status = {}

        for _, student in display_students.iterrows():

            student_id = student["Reg No"]

            student_name = student["Name"]

            col1, col2, col3 = st.columns([2, 4, 2])

            with col1:
                st.write(student_id)

            with col2:
                st.write(student_name)

            with col3:

                status = st.selectbox(
                    "Status",
                    ["Present", "Absent"],
                    key=f"{student_id}_{selected_date}_{subject}"
                )

                attendance_status[student_id] = status

        if st.button(
            "💾 SAVE ATTENDANCE",
            type="primary",
            use_container_width=True
        ):

            if not attendance_status:

                st.warning("No students found.")

            else:

                student_ids = list(
                    attendance_status.keys()
                )

                # Remove old attendance for the selected date
                # and selected students before saving again.
                if delete_existing_attendance(
                    selected_date,
                    student_ids
                ):

                    records = []

                    current_time = datetime.now().isoformat()

                    for _, student in display_students.iterrows():

                        student_id = student["Reg No"]

                        student_name = student["Name"]

                        status = attendance_status[
                            student_id
                        ]

                        records.append(
                            {
                                "student name": student_name,
                                "student id": student_id,
                                "attendance date": str(selected_date),
                                "status": status,
                                "created at": current_time
                            }
                        )

                    if save_attendance(records):

                        st.success(
                            f"Attendance saved successfully for "
                            f"{selected_date.strftime('%d-%m-%Y')}!"
                        )

                        st.rerun()

    # =====================================================
    # STUDENT DETAILS
    # =====================================================

    elif page == "👨‍🎓 Student Details":

        st.markdown(
            '<div class="main-title">👨‍🎓 Student Details</div>',
            unsafe_allow_html=True
        )

        selected_student = st.selectbox(
            "Select Student",
            students["Reg No"] + " - " + students["Name"]
        )

        selected_reg_no = selected_student.split(" - ")[0]

        student_records = attendance[
            attendance["student id"].astype(str)
            == str(selected_reg_no)
        ]

        student_name = students[
            students["Reg No"] == selected_reg_no
        ]["Name"].iloc[0]

        st.subheader(student_name)

        st.write(
            f"Registration Number: **{selected_reg_no}**"
        )

        total = len(student_records)

        present = len(
            student_records[
                student_records["status"].astype(str).str.lower()
                == "present"
            ]
        )

        absent = total - present

        percentage = (
            present / total * 100
            if total
            else 0
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total", total)

        c2.metric("Present", present)

        c3.metric("Absent", absent)

        c4.metric(
            "Percentage",
            f"{percentage:.1f}%"
        )

        if not student_records.empty:

            st.subheader("Attendance History")

            display = student_records.copy()

            display = display.rename(
                columns={
                    "student name": "Student Name",
                    "student id": "Student ID",
                    "attendance date": "Attendance Date",
                    "status": "Status",
                    "created at": "Created At"
                }
            )

            st.dataframe(
                display,
                use_container_width=True,
                hide_index=True
            )

            csv = display.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "⬇️ Download Student History",
                csv,
                f"{selected_reg_no}_attendance.csv",
                "text/csv",
                use_container_width=True
            )

        else:

            st.info(
                "No attendance records found for this student."
            )

    # =====================================================
    # ATTENDANCE HISTORY
    # =====================================================

    elif page == "📅 Attendance History":

        st.markdown(
            '<div class="main-title">📅 Attendance History</div>',
            unsafe_allow_html=True
        )

        if attendance.empty:

            st.info(
                "No attendance history available yet."
            )

        else:

            dates = sorted(
                attendance["attendance date"]
                .dropna()
                .astype(str)
                .unique(),
                reverse=True
            )

            selected_history_date = st.selectbox(
                "Select Date",
                dates
            )

            history = attendance[
                attendance["attendance date"].astype(str)
                == selected_history_date
            ].copy()

            st.write(
                f"Attendance Date: "
                f"**{pd.to_datetime(selected_history_date).strftime('%d-%m-%Y')}**"
            )

            st.dataframe(
                history,
                use_container_width=True,
                hide_index=True
            )

            csv = history.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "⬇️ Download This Date",
                csv,
                f"attendance_{selected_history_date}.csv",
                "text/csv",
                use_container_width=True
            )

    # =====================================================
    # REPORTS
    # =====================================================

    elif page == "📚 Reports":

        st.markdown(
            '<div class="main-title">📚 Reports</div>',
            unsafe_allow_html=True
        )

        if attendance.empty:

            st.info("No attendance records available.")

        else:

            subject = st.selectbox(
                "Select Subject",
                SUBJECTS
            )

            st.info(
                "Note: Your current Supabase Attendance table "
                "does not contain a Subject column. "
                "This report therefore shows overall attendance."
            )

            rows = []

            for _, student in students.iterrows():

                student_id = student["Reg No"]

                records = attendance[
                    attendance["student id"].astype(str)
                    == str(student_id)
                ]

                total = len(records)

                present = len(
                    records[
                        records["status"].astype(str).str.lower()
                        == "present"
                    ]
                )

                absent = total - present

                percentage = (
                    present / total * 100
                    if total
                    else 0
                )

                rows.append(
                    {
                        "Reg No": student_id,
                        "Name": student["Name"],
                        "Total": total,
                        "Present": present,
                        "Absent": absent,
                        "Percentage": round(
                            percentage,
                            1
                        )
                    }
                )

            report = pd.DataFrame(rows)

            st.dataframe(
                report,
                use_container_width=True,
                hide_index=True
            )

            csv = report.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "⬇️ Download Report",
                csv,
                "attendance_report.csv",
                "text/csv",
                use_container_width=True
            )

    # =====================================================
    # DOWNLOAD
    # =====================================================

    elif page == "⬇️ Download":

        st.markdown(
            '<div class="main-title">⬇️ Download Data</div>',
            unsafe_allow_html=True
        )

        if attendance.empty:

            st.info(
                "No attendance data available to download."
            )

        else:

            st.write(
                f"Total attendance records: **{len(attendance)}**"
            )

            csv = attendance.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
      

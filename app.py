import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Cumulative Attendance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# SETTINGS
# =========================================================

USERNAME = "admin"
PASSWORD = "1234"

SUBJECTS = [
    "PATHWAY",
    "CY LAB"
]

DATA_FOLDER = Path("data")
DATA_FOLDER.mkdir(exist_ok=True)

STUDENT_FILE = DATA_FOLDER / "students.csv"
ATTENDANCE_FILE = DATA_FOLDER / "attendance.csv"


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
    ("174CY2413", "GIRISH G M"),
    ("174CY24015", "H B HARSHAVARDHANA"),
    ("174CY24016", "H HANEEF"),
    ("174CY24018", "HOOLESH N"),
    ("174CY24020", "K BHUMIKA"),
    ("174CY24021", "K M RAJA"),
    ("174CY24022", "K N SANJAYA"),
    ("174CY24023", "KODERA KOTRESHA"),
    ("174CY24025", "LAVANYA"),
    ("174CY2027", "M PAVANA KUMARA"),
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


# =========================================================
# CREATE STUDENT CSV
# =========================================================

def create_student_file():

    df = pd.DataFrame(
        STUDENT_DATA,
        columns=["Reg No", "Name"]
    )

    # Always keep the latest student list
    df.to_csv(
        STUDENT_FILE,
        index=False
    )


# =========================================================
# CREATE ATTENDANCE FILE
# =========================================================

def create_attendance_file():

    if not ATTENDANCE_FILE.exists():

        df = pd.DataFrame(
            columns=[
                "Date",
                "Reg No",
                "Name",
                "Subject",
                "Status"
            ]
        )

        df.to_csv(
            ATTENDANCE_FILE,
            index=False
        )


# =========================================================
# LOAD FUNCTIONS
# =========================================================

def load_students():

    return pd.read_csv(STUDENT_FILE)


def load_attendance():

    df = pd.read_csv(ATTENDANCE_FILE)

    if df.empty:
        return pd.DataFrame(
            columns=[
                "Date",
                "Reg No",
                "Name",
                "Subject",
                "Status"
            ]
        )

    return df


# =========================================================
# SAVE ATTENDANCE
# =========================================================

def save_attendance(df):

    df.to_csv(
        ATTENDANCE_FILE,
        index=False
    )


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #2563eb;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #64748b;
        font-size: 16px;
        margin-bottom: 20px;
    }

    .student-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 8px;
    }

    .success-text {
        color: #16a34a;
        font-weight: 700;
    }

    .warning-text {
        color: #ea580c;
        font-weight: 700;
    }

    .danger-text {
        color: #dc2626;
        font-weight: 700;
    }

    @media (max-width: 768px) {

        .main-title {
            font-size: 25px;
        }

        .block-container {
            padding: 1rem 0.6rem;
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
# INITIALIZE FILES
# =========================================================

create_student_file()
create_attendance_file()


# =========================================================
# LOGIN
# =========================================================

def login_page():

    st.markdown(
        '<div class="main-title">📊 Digital Attendance</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Cumulative Attendance Management System'
        '</div>',
        unsafe_allow_html=True
    )

    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        st.markdown("### 🔐 Login")

        username = st.text_input(
            "Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )

        login_button = st.button(
            "LOGIN",
            type="primary",
            use_container_width=True
        )

        if login_button:

            if (
                username == USERNAME
                and password == PASSWORD
            ):

                st.session_state.logged_in = True
                st.rerun()

            else:

                st.error(
                    "❌ Invalid username or password"
                )

        st.info(
            "Demo Login: admin / 1234"
        )


# =========================================================
# ATTENDANCE PERCENTAGE
# =========================================================

def get_percentage(records):

    if len(records) == 0:
        return 0

    present = len(
        records[
            records["Status"] == "Present"
        ]
    )

    return (
        present / len(records)
    ) * 100


# =========================================================
# PERFORMANCE COLOR
# =========================================================

def performance_status(percent):

    if percent >= 75:
        return "🟢 Good"

    elif percent >= 60:
        return "🟠 Warning"

    else:
        return "🔴 Low"


# =========================================================
# MAIN APPLICATION
# =========================================================

def main_app():

    students = load_students()
    attendance = load_attendance()

    # =====================================================
    # SIDEBAR
    # =====================================================

    with st.sidebar:

        st.title("📊 Attendance")

        st.caption(
            "Digital Attendance System"
        )

        st.divider()

        page = st.radio(
            "MENU",
            [
                "🏠 Dashboard",
                "📝 Mark Attendance",
                "👨‍🎓 Student Details",
                "📚 Subject Report"
            ]
        )

        st.divider()

        st.write(
            f"👨‍🎓 **Students:** {len(students)}"
        )

        st.write(
            f"📚 **Subjects:** {len(SUBJECTS)}"
        )

        st.divider()

        if st.button(
            "🚪 LOGOUT",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.rerun()


    # =====================================================
    # DASHBOARD
    # =====================================================

    if page == "🏠 Dashboard":

        st.markdown(
            '<div class="main-title">'
            '📊 Cumulative Attendance'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="subtitle">'
            'Overall attendance and performance'
            '</div>',
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # SUMMARY
        # -------------------------------------------------

        total_students = len(students)

        total_classes = len(attendance)

        total_present = len(
            attendance[
                attendance["Status"] == "Present"
            ]
        )

        total_absent = len(
            attendance[
                attendance["Status"] == "Absent"
            ]
        )

        overall_percentage = (
            total_present
            / total_classes
            * 100
            if total_classes > 0
            else 0
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "👨‍🎓 Students",
            total_students
        )

        c2.metric(
            "📅 Records",
            total_classes
        )

        c3.metric(
            "✅ Present",
            total_present
        )

        c4.metric(
            "📈 Attendance",
            f"{overall_percentage:.1f}%"
        )

        st.divider()

        # -------------------------------------------------
        # PERFORMANCE
        # -------------------------------------------------

        st.subheader(
            "📈 Attendance Performance"
        )

        if attendance.empty:

            st.info(
                "No attendance records available."
            )

        else:

            performance_rows = []

            for _, student in students.iterrows():

                reg = student["Reg No"]
                name = student["Name"]

                records = attendance[
                    attendance["Reg No"] == reg
                ]

                total = len(records)

                present = len(
                    records[
                        records["Status"] == "Present"
                    ]
                )

                absent = total - present

                percentage = (
                    present / total * 100
                    if total > 0
                    else 0
                )

                performance_rows.append({
                    "Reg No": reg,
                    "Name": name,
                    "Total Classes": total,
                    "Present": present,
                    "Absent": absent,
                    "Attendance %": round(
                        percentage,
                        2
                    ),
                    "Performance":
                        performance_status(
                            percentage
                        )
                })

            performance_df = pd.DataFrame(
                performance_rows
            )

            st.dataframe(
                performance_df,
                use_container_width=True,
                hide_index=True
            )


    # =====================================================
    # MARK ATTENDANCE
    # =====================================================

    elif page == "📝 Mark Attendance":

        st.markdown(
            '<div class="main-title">'
            '📝 Mark Attendance'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="subtitle">'
            'Select subject and date, then mark students'
            '</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            subject = st.selectbox(
                "📚 Select Subject",
                SUBJECTS
            )

        with col2:

            selected_date = st.date_input(
                "📅 Attendance Date",
                value=date.today()
            )

        st.divider()

        search = st.text_input(
            "🔍 Search Student",
            placeholder="Search by Reg No or Name..."
        )

        filtered_students = students.copy()

        if search:

            filtered_students = students[
                students["Reg No"]
                .astype(str)
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                students["Name"]
                .astype(str)
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        st.write(
            f"👥 Students: **{len(filtered_students)}**"
        )

        if filtered_students.empty:

            st.warning(
                "No student found."
            )

        else:

            # =================================================
            # FORM
            # =================================================

            with st.form(
                "attendance_form"
            ):

                attendance_values = {}

                for index, student in filtered_students.iterrows():

                    reg = student["Reg No"]
                    name = student["Name"]

                    existing = attendance[
                        (
                            attendance["Date"]
                            == str(selected_date)
                        )
                        &
                        (
                            attendance["Reg No"]
                            == reg
                        )
                        &
                        (
                            attendance["Subject"]
                            == subject
                        )
                    ]

                    default_present = True

                    if not existing.empty:

                        default_present = (
                            existing.iloc[0]["Status"]
                            == "Present"
                        )

                    st.markdown(
                        '<div class="student-card">',
                        unsafe_allow_html=True
                    )

                    c1, c2, c3 = st.columns(
                        [2, 5, 3]
                    )

                    with c1:

                        st.write(
                            f"**{reg}**"
                        )

                    with c2:

                        st.write(
                            f"**{name}**"
                        )

                    with c3:

                        # Checkbox
                        attendance_values[reg] = st.checkbox(
                            "Present",
                            value=default_present,
                            key=(
                                f"attendance_"
                                f"{subject}_"
                                f"{selected_date}_"
                                f"{reg}"
                            )
                        )

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )

                st.divider()

                save_button = st.form_submit_button(
                    "💾 SAVE ATTENDANCE",
                    type="primary",
                    use_container_width=True
                )

                if save_button:

                    # Remove old records for
                    # this date + subject + selected students

                    attendance = attendance[
                        ~(
                            (
                                attendance["Date"]
                                == str(selected_date)
                            )
                            &
                            (
                                attendance["Subject"]
                                == subject
                            )
                            &
                            (
                                attendance["Reg No"].isin(
                                    list(
                                        attendance_values.keys()
                                    )
                                )
                            )
                        )
                    ]

                    new_records = []

                    for _, student in filtered_students.iterrows():

                        reg = student["Reg No"]
                        name = student["Name"]

                        status = (
                            "Present"
                            if attendance_values[reg]
                            else "Absent"
                        )

                        new_records.append({
                            "Date":
                                str(selected_date),
                            "Reg No":
                                reg,
                            "Name":
                                name,
                            "Subject":
                                subject,
                            "Status":
                                status
                        })

                    new_df = pd.DataFrame(
                        new_records
                    )

                    attendance = pd.concat(
                        [
                            attendance,
                            new_df
                        ],
                        ignore_index=True
                    )

                    save_attendance(
                        attendance
                    )

                    st.success(
                        "✅ Attendance saved successfully!"
                    )

                    st.rerun()


    # =====================================================
    # STUDENT DETAILS
    # =====================================================

    elif page == "👨‍🎓 Student Details":

        st.markdown(
            '<div class="main-title">'
            '👨‍🎓 Student Details'
            '</div>',
            unsafe_allow_html=True
        )

        search = st.text_input(
            "🔍 Search Student",
            placeholder="Type name or Reg No..."
        )

        filtered = students.copy()

        if search:

            filtered = students[
                students["Reg No"]
                .astype(str)
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                students["Name"]
                .astype(str)
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        if filtered.empty:

            st.warning(
                "No student found."
            )

        else:

            # Student name selection

            student_names = [
                f"{row['Name']} | {row['Reg No']}"
                for _, row in filtered.iterrows()
            ]

            selected_student = st.selectbox(
                "👆 Tap / Select Student",
                student_names
            )

            selected_reg = (
                selected_student
                .split(" | ")[-1]
            )

            student = students[
                students["Reg No"] == selected_reg
            ].iloc[0]

            st.divider()

            st.markdown(
                f"## 👤 {student['Name']}"
            )

            st.write(
                f"**Registration Number:** "
                f"{student['Reg No']}"
            )

            student_records = attendance[
                attendance["Reg No"]
                == selected_reg
            ]

            # -------------------------------------------------
            # NO DATA
            # -------------------------------------------------

            if student_records.empty:

                st.info(
                    "📭 No attendance data available "
                    "for this student."
                )

            else:

                total = len(student_records)

                present = len(
                    student_records[
                        student_records["Status"]
                        == "Present"
                    ]
                )

                absent = total - present

                percentage = (
                    present / total * 100
                    if total > 0
                    else 0
                )

                c1, c2, c3, c4 = st.columns(4)

                c1.metric(
                    "📅 Total Classes",
                    total
                )

                c2.metric(
                    "✅ Present",
                    present
                )

                c3.metric(
                    "❌ Absent",
                    absent
                )

                c4.metric(
                    "📈 Attendance",
                    f"{percentage:.1f}%"
                )

                st.divider()

                # -------------------------------------------------
                # SUBJECT WISE
                # -------------------------------------------------

                st.subheader(
                    "📚 Subject-wise Attendance"
                )

                subject_rows = []

                for sub in SUBJECTS:

                    records = student_records[
                        student_records["Subject"]
                        == sub
                    ]

                    total_sub = len(records)

                    present_sub = len(
                        records[
                            records["Status"]
                            == "Present"
                        ]
                    )

                    absent_sub = (
                        total_sub - present_sub
                    )

                    percent_sub = (
                        present_sub
                        / total_sub
                        * 100
                        if total_sub > 0
                        else 0
                    )

                    subject_rows.append({
                        "Subject":
                            sub,
                        "Total Classes":
                            total_sub,
                        "Present":
                            present_sub,
                        "Absent":
                            absent_sub,
                        "Attendance %":
                            round(
                                percent_sub,
                                2
                            ),
                        "Performance":
                            performance_status(
                                percent_sub
                            )
                    })

                subject_df = pd.DataFrame(
                    subject_rows
                )

                st.dataframe(
                    subject_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.divider()

                # -------------------------------------------------
                # COMPLETE HISTORY
                # -------------------------------------------------

                st.subheader(
                    "📅 Complete Attendance History"
                )

                history = student_records[
                    [
                        "Date",
                        "Subject",
                        "Status"
                    ]
                ].sort_values(
                    "Date",
                    ascending=False
                )

                st.dataframe(
                    history,
                    use_container_width=True,
                    hide_index=True
                )


    # =====================================================
    # SUBJECT REPORT
    # =====================================================

    elif page == "📚 Subject Report":

        st.markdown(
            '<div class="main-title">'
            '📚 Subject Attendance Report'
            '</div>',
            unsafe_allow_html=True
        )

        selected_subject = st.selectbox(
            "Select Subject",
            SUBJECTS
        )

        subject_records = attendance[
            attendance["Subject"]
            == selected_subject
        ]

        if subject_records.empty:

            st.info(
                f"No attendance records for "
                f"{selected_subject}."
            )

        else:

            rows = []

            for _, student in students.iterrows():

                reg = student["Reg No"]
                name = student["Name"]

                records = subject_records[
                    subject_records["Reg No"]
                    == reg
                ]

                total = len(records)

                present = len(
                    records[
                        records["Status"]
                        == "Present"
                    ]
                )

                absent = total - present

                percentage = (
                    present / total * 100
                    if total > 0
                    else 0
                )

                rows.append({
                    "Reg No":
                        reg,
                    "Name":
                        name,
                    "Total":
                        total,
                    "Present":
                        present,
                    "Absent":
                        absent,
                    "Attendance %":
                        round(
                            percentage,
                            2
                        ),
                    "Performance":
                        performance_status(
                            percentage
                        )
                })

            report = pd.DataFrame(rows)

            st.dataframe(
                report,
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            st.subheader(
                f"📊 {selected_subject} Statistics"
            )

            total_records = len(
                subject_records
            )

            total_present = len(
                subject_records[
                    subject_records["Status"]
                    == "Present"
                ]
            )

            total_absent = (
                total_records
                - total_present
            )

            percentage = (
                total_present
                / total_records
                * 100
                if total_records > 0
                else 0
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Total Records",
                total_records
            )

            c2.metric(
                "Present",
                total_present
            )

            c3.metric(
                "Attendance",
                f"{percentage:.1f}%"
            )


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


# =========================================================
# START
# =========================================================

if st.session_state.logged_in:

    main_app()

else:

    login_page()

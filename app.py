import sqlite3
from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Employee Management System", page_icon="👥", layout="wide")

DB = "employees.db"
DEPARTMENTS = ["HR", "IT", "Finance", "Sales", "Marketing", "Operations"]
STATUSES = ["Active", "On Leave", "Resigned"]

st.markdown(
    """
<style>
.block-container {padding-top: 2rem;}
div[data-testid="stMetric"] {
    background: rgba(120,130,160,0.12);
    border: 1px solid rgba(120,130,160,0.25);
    border-radius: 14px; padding: 14px 18px;
}
.title {font-size: 2rem; font-weight: 700; margin-bottom: 0;}
.sub {opacity: .7; margin-bottom: 1.2rem;}
</style>
""",
    unsafe_allow_html=True,
)


# ---------- Database ----------
def get_conn():
    c = sqlite3.connect(DB)
    c.execute(
        """CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, email TEXT, phone TEXT,
        department TEXT, designation TEXT, salary REAL,
        joining_date TEXT, status TEXT DEFAULT 'Active')"""
    )
    return c


def load():
    c = get_conn()
    df = pd.read_sql("SELECT * FROM employees", c)
    c.close()
    return df


def run(query, params=()):
    c = get_conn()
    c.execute(query, params)
    c.commit()
    c.close()


# ---------- Sidebar ----------
st.sidebar.title("👥 EMS")
page = st.sidebar.radio(
    "Menu", ["📊 Dashboard", "➕ Add Employee", "🗂️ Manage Employees", "⬇️ Export"]
)
st.sidebar.caption("Employee Management System • Streamlit")

df = load()

# ---------- Dashboard ----------
if page == "📊 Dashboard":
    st.markdown('<p class="title">📊 Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub">Company ka overview ek nazar mein</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Employees", len(df))
    c2.metric("Active", int((df["status"] == "Active").sum()) if len(df) else 0)
    c3.metric("Avg Salary", f"₹{df['salary'].mean():,.0f}" if len(df) else "₹0")
    c4.metric("Departments", df["department"].nunique() if len(df) else 0)

    if df.empty:
        st.info("Abhi koi employee nahi hai. 'Add Employee' se shuru karein.")
    else:
        left, right = st.columns(2)
        with left:
            st.subheader("Department-wise Employees")
            d = df["department"].value_counts().reset_index()
            d.columns = ["department", "count"]
            st.plotly_chart(px.pie(d, names="department", values="count", hole=0.45), use_container_width=True)
        with right:
            st.subheader("Avg Salary by Department")
            s = df.groupby("department", as_index=False)["salary"].mean()
            st.plotly_chart(px.bar(s, x="department", y="salary", color="department"), use_container_width=True)

        st.subheader("Recently Added")
        st.dataframe(df.sort_values("id", ascending=False).head(5), use_container_width=True, hide_index=True)

# ---------- Add ----------
elif page == "➕ Add Employee":
    st.markdown('<p class="title">➕ Add Employee</p>', unsafe_allow_html=True)
    with st.form("add_form", clear_on_submit=True):
        a, b = st.columns(2)
        name = a.text_input("Full Name *")
        email = b.text_input("Email")
        phone = a.text_input("Phone")
        dept = b.selectbox("Department", DEPARTMENTS)
        desig = a.text_input("Designation")
        salary = b.number_input("Salary (₹)", min_value=0.0, step=1000.0)
        joined = a.date_input("Joining Date", value=date.today())
        status = b.selectbox("Status", STATUSES)
        if st.form_submit_button("Save Employee", type="primary"):
            if not name.strip():
                st.error("Name zaroori hai.")
            else:
                run(
                    "INSERT INTO employees(name,email,phone,department,designation,salary,joining_date,status) VALUES(?,?,?,?,?,?,?,?)",
                    (name.strip(), email, phone, dept, desig, salary, str(joined), status),
                )
                st.success(f"{name} add ho gaya ✅")

# ---------- Manage ----------
elif page == "🗂️ Manage Employees":
    st.markdown('<p class="title">🗂️ Manage Employees</p>', unsafe_allow_html=True)
    f1, f2 = st.columns([2, 1])
    q = f1.text_input("🔍 Search (name / email / designation)")
    dept_f = f2.selectbox("Department", ["All"] + DEPARTMENTS)

    view = df.copy()
    if q:
        mask = view[["name", "email", "designation"]].fillna("").apply(
            lambda col: col.str.contains(q, case=False)
        ).any(axis=1)
        view = view[mask]
    if dept_f != "All":
        view = view[view["department"] == dept_f]
    st.dataframe(view, use_container_width=True, hide_index=True)

    if not df.empty:
        st.divider()
        st.subheader("Edit / Delete")
        options = {f"{r.id} - {r.name}": r.id for r in df.itertuples()}
        pick = st.selectbox("Employee chunein", list(options))
        emp = df[df["id"] == options[pick]].iloc[0]

        with st.form("edit_form"):
            a, b = st.columns(2)
            name = a.text_input("Name", emp["name"])
            email = b.text_input("Email", emp["email"] or "")
            phone = a.text_input("Phone", emp["phone"] or "")
            dept = b.selectbox("Department", DEPARTMENTS, index=DEPARTMENTS.index(emp["department"]) if emp["department"] in DEPARTMENTS else 0)
            desig = a.text_input("Designation", emp["designation"] or "")
            salary = b.number_input("Salary (₹)", min_value=0.0, step=1000.0, value=float(emp["salary"] or 0))
            status = a.selectbox("Status", STATUSES, index=STATUSES.index(emp["status"]) if emp["status"] in STATUSES else 0)
            u, d = st.columns(2)
            if u.form_submit_button("Update", type="primary"):
                run(
                    "UPDATE employees SET name=?,email=?,phone=?,department=?,designation=?,salary=?,status=? WHERE id=?",
                    (name, email, phone, dept, desig, salary, status, int(emp["id"])),
                )
                st.success("Updated ✅")
                st.rerun()
            if d.form_submit_button("Delete"):
                run("DELETE FROM employees WHERE id=?", (int(emp["id"]),))
                st.warning("Deleted 🗑️")
                st.rerun()

# ---------- Export ----------
else:
    st.markdown('<p class="title">⬇️ Export</p>', unsafe_allow_html=True)
    st.download_button(
        "Download CSV",
        df.to_csv(index=False).encode("utf-8"),
        "employees.csv",
        "text/csv",
        type="primary",
    )
    st.dataframe(df, use_container_width=True, hide_index=True)

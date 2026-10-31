# 👥 Employee Management System

A simple, modern and easy-to-use **Employee Management System** built with **Python** and **Streamlit**. It helps organizations manage employee records, track departments and salaries, and view useful insights through an interactive dashboard.

🔗 **Live Demo:** [Open the App](https://employee-manangement-system-mohsqodtgeo9hxbzfyh8ad.streamlit.app/)

---

## 📌 About the Project

Managing employee data in registers or scattered spreadsheets is slow and error-prone. This project provides a single web-based place to **add, view, search, update, delete and export** employee information, with a clean interface that anyone can use without technical knowledge.

## ✨ Features

- 📊 **Dashboard** – Total employees, active employees, average salary and number of departments at a glance
- 📈 **Interactive Charts** – Department-wise employee distribution (pie chart) and average salary by department (bar chart)
- ➕ **Add Employee** – Easy form to register a new employee (name, email, phone, department, designation, salary, joining date, status)
- 🗂️ **Manage Employees** – View all records in a table
- 🔍 **Search & Filter** – Search by name, email or designation and filter by department
- ✏️ **Edit / Update** – Modify any employee's details
- 🗑️ **Delete** – Remove an employee record
- ⬇️ **Export** – Download all employee data as a CSV file
- 🌗 **Light / Dark mode friendly** UI

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3 | Core programming language |
| Streamlit | Web interface / GUI |
| SQLite | Lightweight database |
| Pandas | Data handling |
| Plotly | Interactive charts |
| GitHub | Version control |
| Streamlit Community Cloud | Hosting |

## 📁 Project Structure

```
employee-management-system/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .gitignore          # Files ignored by Git
├── README.md           # Project documentation
└── employees.db        # SQLite database (auto-created on first run)
```

## 🗄️ Database Schema

**Table: `employees`**

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto increment) |
| name | TEXT | Full name of the employee |
| email | TEXT | Email address |
| phone | TEXT | Phone number |
| department | TEXT | HR, IT, Finance, Sales, Marketing, Operations |
| designation | TEXT | Job title / position |
| salary | REAL | Salary in ₹ |
| joining_date | TEXT | Date of joining |
| status | TEXT | Active, On Leave or Resigned |

## 🚀 How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

4. Open `http://localhost:8501` in your browser.

## ☁️ Deployment (Streamlit Community Cloud)

1. Upload the project to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **Create app**, select your repository and set the main file to `app.py`.
4. Click **Deploy**.

> ⚠️ **Note:** On Streamlit Community Cloud, the SQLite file may reset when the app restarts. For permanent storage, connect an external database such as Supabase, PostgreSQL or Google Sheets.

## 🔮 Future Scope

- 🔐 Login system (Admin / HR roles)
- 🗓️ Attendance tracking
- 🏖️ Leave management
- 💰 Payroll and salary slip generation
- 📧 Email notifications
- ☁️ Cloud database integration
- 📤 Bulk import from Excel / CSV

## 👨‍💻 Developers

This project was created by:

- **Tanveer**
- **Abhay**

## 🤝 Contributing

Suggestions and improvements are welcome. Fork the repository, make your changes and open a pull request.

## 📄 License

This project is created for educational purposes. You are free to use and modify it.

---

⭐ If you like this project, don't forget to give it a star on GitHub!

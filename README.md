# School Finance Management System

A comprehensive desktop application for managing school finance operations including student records, fee payments, expenses, and teacher loans.

## 🎯 Features

- **Student Management**: Register and manage student information
- **Payment Tracking**: Record and track student fee payments
- **Expense Management**: Record school expenses with descriptions
- **Loan Management**: Manage teacher loans and repayments
- **PDF Receipts**: Automatically generate payment receipts
- **Excel Export**: Export student data to Excel format
- **Dashboard**: Real-time summary of financial metrics
- **Multi-tab Interface**: Easy navigation between modules

## ✅ Requirements

- Python 3.7+
- Windows OS (for EXE distribution)
- ~50MB disk space

## 🚀 Quick Start

### Running from Source

1. **Clone the repository:**
```bash
git clone https://github.com/geoffreymiyoge-lgtm/school-finance-system.git
cd school-finance-system
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python app.py
```

### Building a Standalone EXE

```bash
python build_exe.py
```

Your executable will be in: `dist/SchoolFinanceSystem.exe`

## 🔐 Default Credentials

| Field | Value |
|-------|-------|
| Username | admin |
| Password | admin123 |

⚠️ **Important**: Change these credentials in the database after first login!

## ⚙️ Configuration

Edit `config.py` to customize:

```python
SCHOOL_NAME = "Itierio Elck Primary Boarding School"
DEFAULT_FEE = 1500  # Default fee amount in KSh
DATABASE = "database/school.db"
```

## 📁 Project Structure

```
school-finance-system/
├── app.py                 # Main entry point
├── config.py             # Configuration settings
├── database.py           # Database initialization
├── dashboard.py          # Main dashboard UI
├── login.py             # Login authentication
├── students.py          # Student management module
├── payments.py          # Fee payment tracking
├── expenses.py          # Expense management
├── loans.py             # Teacher loans management
├── receipts.py          # PDF receipt generation
├── exports.py           # Excel export functionality
├── build_exe.py         # PyInstaller build script
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🗄️ Database Schema

### users
```sql
username TEXT PRIMARY KEY
password TEXT
```

### students
```sql
admission_no TEXT PRIMARY KEY
name TEXT
grade TEXT
stream TEXT
parent TEXT
phone TEXT
expected REAL
paid REAL
```

### payments
```sql
id INTEGER PRIMARY KEY
admission_no TEXT
date TEXT
amount REAL
```

### expenses
```sql
id INTEGER PRIMARY KEY
date TEXT
description TEXT
amount REAL
```

### loans
```sql
id INTEGER PRIMARY KEY
teacher TEXT
date TEXT
given REAL
repaid REAL
```

## 📊 Dashboard Metrics

The dashboard displays real-time information:

- **Students**: Total number of registered students
- **Collected**: Total fees collected
- **Expenses**: Total school expenses
- **Loans Given**: Total loans given to teachers
- **Outstanding Loans**: Remaining loan balance
- **Fee Balance**: Outstanding student fees
- **Cash Balance**: Net cash position

## 📋 Usage Guide

### Students Tab
1. Fill in student details (Admission No, Name, Grade, etc.)
2. Click **Add Student** to register
3. Search for students using the search field
4. Select a student to update or delete

### Payments Tab
1. Enter student admission number
2. Click **Search Student** to verify details
3. Enter payment amount
4. Click **Record Payment**
5. PDF receipt is automatically generated

### Expenses Tab
1. Enter expense description
2. Enter amount
3. Click **Add Expense**
4. Delete expenses using the **Delete Selected** button

### Loans Tab
1. Enter teacher name and loan amount
2. Click **Give Loan** to record
3. To record repayment:
   - Select the loan
   - Enter repayment amount
   - Click **Record Repayment**

## 🔧 Troubleshooting

### "Module not found" Error
```bash
pip install -r requirements.txt
```

### Database Error
Delete the `database` folder and restart to create a fresh database.

### PyInstaller Not Found
```bash
pip install PyInstaller==6.1.0
```

### EXE Build Failed
Ensure you're running the build script from the project root directory.

## 📝 Generated Folders

The application automatically creates:
- `database/` - SQLite database location
- `receipts/` - PDF receipt storage
- `exports/` - Excel export files
- `dist/` - Compiled EXE (after build)
- `build/` - Build artifacts (after build)

## 🛡️ Security Notes

- Default credentials should be changed immediately
- Database passwords are stored in plain text (for this version)
- Consider implementing proper encryption in production
- Regular database backups are recommended

## 📦 Dependencies

- **PyInstaller** - EXE compilation
- **reportlab** - PDF generation
- **openpyxl** - Excel file handling
- **tkinter** - GUI framework (built-in)
- **sqlite3** - Database (built-in)

## 🎓 Learning Resources

This application demonstrates:
- Tkinter GUI development
- SQLite database operations
- File I/O (PDF and Excel)
- Application packaging with PyInstaller
- Multi-tab interface design
- Data validation and error handling

## 📄 License

Open source - feel free to modify and distribute

## 👤 Author

**Geoffrey Miyoge** (@geoffreymiyoge-lgtm)

## 🤝 Contributing

Found a bug or want to contribute? Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📧 Support

For issues, questions, or suggestions, please create an issue on GitHub.

---

**Last Updated**: June 2026
**Status**: ✅ Ready to Use

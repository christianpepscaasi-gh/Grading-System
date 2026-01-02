# 🎓 Grade Prediction System — PSU Campus Edition
**Grade Prediction System** is a machine-learning powered desktop application designed to assist faculty and students of **Pangasinan State University (PSU)** in evaluating academic performance using an 80/20 weighted grading model and **RandomForestRegressor AI**.
This project is a capstone requirement under the **BSIT Department**, developed for deployment in **Campus Computer Laboratories (Lab 3 & Lab 4)** and intended for future integration into the **PSU campus server system**.

---

## 🚀 Purpose & Vision

- Provide an intelligent, fast, and **data-driven grade evaluation tool**
- Support instructors in predicting **final weighted grades**
- Reduce manual computation errors
- Prepare the system for **future campus-wide deployment**
- Build a reusable academic performance model for PSU infrastructure

---

## 💡 Key Features

- Upload `.CSV` or `.Excel` student records
- Auto-fill missing grade/skill fields as `0` (ignored by model)
- Predict **Final Weighted Grade** instantly
- View results in an organized scrollable table
- Export predictions to Excel/CSV
- Runs as a **standalone EXE (Windows Desktop App)**

---

## 🧠 Grading Interpretation Scale

| Score | Meaning |
|------:|--------|
| 1     | Excellent / Highest Performance |
| 3     | Average / Passing |
| 5     | Failed |
| Blank | Treated as `0` (ignored by model) |

---

## 📁 Project Structure

GradePredictionSystem/
├── app.py
├── model/
│ └── grade_model.pkl
├── dist/
│ └── app.exe
└── README.md

yaml

---

## 🛠 Requirements for Source Execution

- Python `3.9.x`
- Dependencies:
- pandas
- numpy
- joblib
- scikit-learn
- openpyxl
- tkinter (built-in)

---

Install all dependencies:

pip install -r requirements.txt
▶ Running the Application
💻 Run from Executable (For faculty, students, and lab use)
Open: dist/app.exe

Click Upload CSV / Excel

View predicted weighted grades

Click Save Predictions to export results

---

🧪 Run from Source (For professor code review)

python app.py
🌐 Future Deployment Plan
This system is planned for installation in:

PSU Computer Laboratories 3 & 4

Campus internal server for institutional use

---

👨‍🏫 Academic Supervisor
Project Adviser / Professor:
🧑 Sir Virgilio Aquino
📌 Pangasinan State University, Lingayen Campus
📚 Instructor: VIRGILIO AQUINO

Project Given & Reviewed by:
👔 Sir Virgilio Aquino
🧪 Deployment Target: Lab 3 & Lab 4 Campus Labs

✍ Developer
Christian Peps Caasi
📍 Anda, Pangasinan
🎣 Hobbies: Fishing & Drawing
💻 Department: BSIT — PSU

📌 Notes
The model is trained using RandomForestRegressor via Joblib
Missing values are auto-converted to 0 for prediction compatibility
First execution may take a few seconds due to AI model initialization

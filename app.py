import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import joblib
import os
import sys

# ======================================================
# Paths & Model (EXE-safe)
# ======================================================
if getattr(sys, 'frozen', False):
    # Running as EXE
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "grade_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load model:\n{e}")
    sys.exit(1)

# ======================================================
# Feature Columns
# ======================================================
GRADE_COLS = [
    'CC101','CC102','GE5','GE6','GE7','CC103','CO101','GE1','GE2','GE3',
    'MS101','GEE3','CC104','GE4','GEE1','GEE4','HCI101','OOP101','CC105',
    'HCI102','MT101','NET101','SAD101','WD101','GE9','IM102','CC106','MD101',
    'MS102','NET102','OS101','SP101','WS101','GEEL2','CAP101','ELEC1','ELEC2',
    'IAS101','IPT101','TECH101','GE8','IC1'
]

SKILL_COLS = [f"skill{i}" for i in range(1, 16)]
ALL_FEATURES = GRADE_COLS + SKILL_COLS

# ======================================================
# App Window
# ======================================================
root = tk.Tk()
root.title("Grade Prediction System")
root.geometry("1200x650")
root.configure(bg="#e9f5e1")

# ======================================================
# Instructions
# ======================================================
instructions = tk.Label(
    root,
    text=(
        "Instructions:\n"
        "1 = Highest / Excellent\n"
        "3 = Average / Passing\n"
        "5 = Failed\n"
        "Leave blank for 0 (ignored by model)"
    ),
    font=("Courier New", 10, "bold"),
    bg="#e9f5e1",
    justify="left"
)
instructions.pack(pady=5)

# ======================================================
# Styles
# ======================================================
style = ttk.Style()
style.theme_use("default")
style.configure(
    "Treeview",
    background="#f7fbf4",
    foreground="black",
    rowheight=25,
    fieldbackground="#f7fbf4",
    font=("Courier New", 10)
)
style.configure(
    "Treeview.Heading",
    background="#cfe2cf",
    foreground="black",
    font=("Courier New", 10, "bold")
)

# ======================================================
# Table (Treeview)
# ======================================================
COLUMNS = ["#"] + ALL_FEATURES + ["PredictedGrade"]

tree = ttk.Treeview(root, columns=COLUMNS, show="headings")
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

for col in COLUMNS:
    tree.heading(col, text=col)
    tree.column(col, width=90, anchor="center")
tree.column("#", width=40)

# Scrollbars
scroll_y = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
scroll_x = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

# ======================================================
# Functions
# ======================================================
def load_file():
    file_path = filedialog.askopenfilename(
        title="Select Grade File",
        filetypes=[
            ("Excel files", "*.xlsx *.xls"),
            ("CSV files", "*.csv"),
            ("All files", "*.*")
        ]
    )
    if not file_path:
        return

    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path, engine="openpyxl")

        df.columns = df.columns.astype(str).str.strip()

        # Fill missing grades/skills with 0
        for col in ALL_FEATURES:
            if col not in df.columns:
                df[col] = 0
            else:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        df = df[ALL_FEATURES]

        predictions = model.predict(df)
        display_table(df, predictions)

    except Exception as err:
        messagebox.showerror("Error", str(err))


def display_table(df, predictions):
    tree.delete(*tree.get_children())
    for idx, row in df.iterrows():
        pred_val = predictions[idx]
        # Safe rounding for numeric predictions
        if isinstance(pred_val, (float, int)):
            pred_val = round(pred_val, 4)
        tree.insert("", "end", values=[idx + 1] + list(row.values) + [pred_val])


def save_predictions():
    if not tree.get_children():
        messagebox.showwarning("No Data", "No predictions to save.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[
            ("Excel files", "*.xlsx"),
            ("CSV files", "*.csv")
        ]
    )
    if not file_path:
        return

    rows = []
    for item in tree.get_children():
        values = tree.item(item)["values"]
        rows.append(values[1:])  # remove row index

    df = pd.DataFrame(rows, columns=ALL_FEATURES + ["PredictedGrade"])

    try:
        if file_path.endswith(".csv"):
            df.to_csv(file_path, index=False)
        else:
            df.to_excel(file_path, index=False)

        messagebox.showinfo("Success", "Predictions saved successfully!")

    except Exception as err:
        messagebox.showerror("Save Error", str(err))

# ======================================================
# Buttons
# ======================================================
btn_frame = tk.Frame(root, bg="#e9f5e1")
btn_frame.pack(pady=10)

upload_btn = tk.Button(
    btn_frame,
    text="Upload CSV / Excel",
    command=load_file,
    bg="#6aa84f",
    fg="white",
    font=("Courier New", 11, "bold"),
    padx=20,
    pady=8
)

save_btn = tk.Button(
    btn_frame,
    text="Save Predictions",
    command=save_predictions,
    bg="#38761d",
    fg="white",
    font=("Courier New", 11, "bold"),
    padx=20,
    pady=8
)

upload_btn.pack(side=tk.LEFT, padx=10)
save_btn.pack(side=tk.LEFT, padx=10)

# ======================================================
# Run App
# ======================================================
root.mainloop()

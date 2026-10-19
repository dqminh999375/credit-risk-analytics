Dưới đây là một file **`README.md`** cực kỳ chuyên nghiệp, được viết theo chuẩn của các dự án Data/Data Science trên GitHub. Nó không chỉ giúp giảng viên (nhà tuyển dụng) hiểu bạn đã làm gì, mà còn thể hiện bạn là người có tư duy hệ thống (System Thinking) và biết cách viết tài liệu (Documentation).

Bạn hãy copy toàn bộ nội dung trong khung dưới đây, dán vào file `README.md` ở thư mục gốc của dự án, lưu lại (Ctrl+S), rồi push lên GitHub nhé.

---

```markdown
# Credit Risk Portfolio Analytics Pipeline

## 📌 Project Overview
This project is an end-to-end data pipeline and analytics solution for a consumer-finance loan portfolio. Using the **Home Credit Default Risk** dataset (Kaggle, 2018) as a structural analogue, the pipeline extracts raw data, transforms it into a relational model, and loads it into a PostgreSQL database. Finally, it generates actionable business insights and visualizations through SQL Analytics and Python.

The goal is to answer a critical business question: **"Where is our credit risk concentrated today (by default rate and financial exposure), and which underwriting rules should change before the next quarterly review?"**

## 🏗️ Pipeline Architecture
The project follows a strict **Extract-Transform-Load (ETL)** pattern, ensuring data integrity and reproducibility. The actual repository structure is as follows:

```text
├── data/
│   ├── raw/                 # Raw CSV files from Kaggle (gitignored)
│   └── processed/           # Cleaned CSV files ready for database (gitignored)
├── notebooks/
│   ├── 01_dataset_profiling.ipynb
│   ├── 02_notebooks.ipynb
│   ├── 03_insight_visualization.ipynb
│   ├── 04_ML.ipynb
│   └── 05_python_dashboard.ipynb
├── sql/
│   ├── 01_create_schema.sql
│   ├── 02_create_tables.sql
│   ├── 03_data_quality_check.sql
│   ├── 04_risk_analysis.sql
│   └── 05_sensitivity_checks.sql
├── src/                     # Python ETL scripts
├── dashboard/               # Exported static visualisations (PNG)
├── .env                     # (gitignored) Database credentials
├── .gitignore
├── README.md
└── requirements.txt         # Python dependencies (Rename your requirement.txt to this)

## ⚙️ 1. ETL Process (Python & PostgreSQL)
- **Extract:** Loads `application_train.csv`, `bureau.csv`, and `previous_application.csv`.
- **Transform:** 
  - Handled the `DAYS_EMPLOYED = 365243` anomaly (approx. 1,000 years) by flagging it and setting it to `NaN`.
  - Aggregated 1.7M bureau records and 1.6M previous applications to the customer level (one row per `SK_ID_CURR`).
  - Engineered features such as `age`, `employment_years`, `credit_income_ratio`, and `credit_income_band`.
- **Validate:** Checked for duplicate primary keys, invalid target values, and negative incomes.
- **Load:** Pushed the clean data into PostgreSQL. The database's **Foreign Key constraints successfully blocked 90,120 orphan records**, ensuring referential integrity.

## 📊 2. Business Intelligence & Analytics (SQL & Python)
The analysis is built on two benchmarks: the overall portfolio default rate (**8.07%**) and the even-share of defaulted exposure. 

### Key Findings:
1. **The Q4 Trap:** The highest credit-to-income quartile (Q4) has a *below-average* default rate (7.37%), but it contributes **37.2% of total defaulted exposure** because their average loan sizes are 4x larger than Q1. (Risk rate ≠ Risk concentration).
2. **The External Score King:** `EXT_SOURCE_2` is the strongest predictor. The "Very Low" band defaults at **17.52%**, which is 6.6x riskier than the "High" band (2.64%).
3. **Danger Zones:** Applicants with 3+ prior overdue credits default at a massive **57.63%**, and those refused in 50%+ of previous applications default at 14.17%.

### Dashboard Generation:
Instead of a drag-and-drop tool (like Power BI), the dashboard is generated programmatically using **Python (Matplotlib/Seaborn)** for 100% reproducibility. 
- `Page1_Portfolio_Overview.png`: Overall KPIs and default rates by age.
- `Page2_The_Risk_Trap.png`: The dual-axis chart comparing default rate vs. defaulted exposure.
- `Page3_Danger_Zones.png`: Early warning signals (External scores, overdue history, refusal matrices).

## 🚀 3. How to Run the Project
### Prerequisites
- Python 3.9+
- PostgreSQL installed and running on port `5432`.

### Step-by-Step Execution:
1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/credit-risk-analytics-pipeline.git
   cd credit-risk-analytics-pipeline
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Setup environment variables:** Create a `.env` file in the root directory:
   ```text
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=credit_risk_analytics
   DB_USER=postgres
   DB_PASSWORD=123456789
   ```
4. **Download raw data:** Download the 3 CSV files from Kaggle and place them in `data/raw/`.
5. **Run the ETL pipeline:**
   ```bash
   python src/main.py
   ```
6. **Setup the Database:** Run the SQL scripts in order (`01_create_schema.sql`, `02_create_tables.sql`, etc.) using a PostgreSQL client (e.g., pgAdmin or VS Code).
7. **Load data into PostgreSQL:**
   ```bash
   python src/load.py
   ```
8. **Generate the Dashboard:**
   Open `notebooks/05_python_dashboard.ipynb` and run all cells. The PNG charts will be saved in the `dashboard/` folder.

## 👤 Author
* Đàm Quang Minh - Lâm Nguyễn Thanh Hoài 
- Course: EMM4010 — Specialized Topic 1 (Applied Mathematics in Economics, Management and Finance)
- Student ID: K234131608 -K234131596
- Instructor: Lê Thị Thanh An

---
*This project is part of the D4 Midterm Case-Study Report.*
```

---


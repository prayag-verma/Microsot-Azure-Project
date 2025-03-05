# 🚀 Azure Incremental Load Realtime Project

## 📌 Overview
This project demonstrates how to implement **incremental data loading** in **Azure Data Factory (ADF)**. It provides a step-by-step guide on setting up an **ETL pipeline** that transfers only new or modified records from a **transactional database** to an **analytical database** in real-time.

## 🏗️ Architecture
- **Source**: Azure SQL Database (Transactional DB)
- **Target**: Azure SQL Database (Analytical DB)
- **ETL Tool**: Azure Data Factory (ADF)
- **Incremental Strategy**: Using `MAX(order_date)` to fetch only new records

## 🔧 Steps to Implement

### STEP1️⃣: Login to Azure SQL Database
- Sign in to **Azure Portal**
- Navigate to **SQL Database** and open an existing or create a new one
- Click on **Query Editor (preview)** and login with credentials

### STEP2️⃣: Create Source Tables
- Create three tables: `customers`, `products`, and `orders` using SQL queries

### STEP3️⃣: Create Target Tables
- Create three dimension tables: `customers_dim`, `products_dim`, and `orders_dim`

### STEP4️⃣: Insert Sample Data (Source & Target)
- Insert sample data into `customers`, `products`, and `orders`
- Verify using `SELECT` statements
- Repeat the process for `customers_dim`, `products_dim`, and `orders_dim`

### STEP5️⃣: Set Up Azure Data Factory (ADF)
- Navigate to **Azure Data Factory** in the Azure Portal
- Create a new **Data Factory instance** (if not already created)
- Click on **Launch Studio**

### STEP6️⃣: Create Linked Services
- Go to **Manage** → **Linked Services**
- Click **+ New** → Select `Azure SQL Database`
- Configure connection settings and save

### STEP7️⃣: Create Datasets
- Go to **Author** → **Datasets**
- Create datasets for `order_dim` and `order` tables

### STEP8️⃣: Create Pipeline & Lookup Activity
- Create a new **pipeline**: `Incremental-load-pl`
- Add **Lookup Activity** to fetch the latest `order_date` from `order_dim`

### STEP9️⃣: Add Copy Data Activity
- Drag **Copy Data Activity** and connect it to Lookup Activity
- Set **source dataset**: `order_tbl_ds`
- Apply filter: Copy only `order_date > max(order_date)` from Lookup

### STEP🔟: Configure & Run Pipeline
- Configure dynamic content for **incremental load**
- Enable **First Row Only** in Lookup (to fetch a single max `order_date` value)
- **Trigger pipeline execution** and validate data loading

### STEP1️⃣1️⃣: Schedule Automated Runs
- Go to **Manage** → **Triggers** → **Create New Trigger**
- Define execution schedule (daily, hourly, etc.)
- Monitor pipeline execution via **Monitor** tab

## 🎯 Expected Outcome
- The pipeline successfully loads **only new records** into `order_dim`
- Data is transferred **incrementally**, avoiding duplicate processing
- The process is **automated** using triggers for scheduled execution

---

## 🙌 Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:
1. **Fork** the repository.
2. **Create** a new branch for your feature or bugfix.
3. **Commit** your changes.
4. **Submit** a pull request.

---

## 📧 Contact

👤 **Prayag Verma**  
👥 **The University of Texas at Dallas**  

🔗 **LinkedIn:**  → [linkedin.com/in/prayagv](https://www.linkedin.com/in/prayagv/)  
🔗 **Portfolio:**  → [profile.aimtocode.com](https://profile.aimtocode.com/)  

💬 Feel free to **raise an issue** or **contribute via pull requests**!  

## 📄 License

This repository is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code as per the license terms.

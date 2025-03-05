# 📊 **Multi-Cloud Data Integration with Azure Data Factory**

## 🚀 **Overview**

In this project, we integrate data from multiple cloud platforms (AWS and Azure) into **Snowflake** using **Azure Data Factory (ADF)**. We extract "customers" data from **AWS S3** and "orders" data from **Azure Blob Storage**, orchestrate the ETL process via ADF, and load everything into Snowflake for business analysis.

---

## 🏗️ **Architecture Overview**
```plaintext
1. AWS S3 (Customers Data)  →  Azure Data Factory  →  Snowflake Warehouse

2. Azure Blob Storage (Orders Data) →  Azure Data Factory  →  Snowflake Warehouse
```

---

## 📝 **Prerequisites**
To follow along, ensure you have:

✅ **AWS S3 Bucket** (For customer data - `customers.csv`)
   - Bucket Name: `customers-data-s3-bucket`
   - File Name: `customers.csv`

✅ **Azure Blob Storage** (For order data - `orders.csv`)
   - Container Name: `orders`
   - File Name: `orders.csv`

✅ **Snowflake Account**
   - Create tables: `customers` and `orders`

✅ **Azure Data Factory (ADF)**
   - ADF Trigger (For scheduling and orchestration)

---

## 🛠️ **Step-by-Step Implementation**

### 🔹 **Step 1: Create AWS S3 Bucket and Upload File**
1. Go to **AWS Dashboard** → **S3** → Click `Create bucket`.
2. Enter a unique name, e.g., `customers-data-s3-bucket`, and enable "Block all public access".
3. Click `Create Bucket`.
4. Upload the `customers.csv` file into the bucket.

### 🔹 **Step 2: Set Up IAM User for ADF Access to S3**
1. Go to **AWS IAM Console** → Create a new user (`adf-s3-access-user`).
2. Attach policy `AmazonS3ReadOnlyAccess`.
3. Generate **Access Key ID** and **Secret Access Key**.

### 🔹 **Step 3: Create Azure Blob Storage and Upload File**
1. Create a **Storage Account** (`awsazstorageac`).
2. Create a **Container** named `orders`.
3. Upload `orders.csv` into the `orders` container.

### 🔹 **Step 4: Set Up Snowflake (Data Warehouse)**
1. **Create Database:**
   ```sql
   CREATE DATABASE SALES_DB;
   ```
2. **Create Schema:**
   ```sql
   CREATE SCHEMA SALES_DB.SALES_SCHEMA;
   ```
3. **Create Tables:**
   ```sql
   CREATE TABLE SALES_DB.SALES_SCHEMA.CUSTOMERS (
   CUSTOMER_ID NUMBER(38, 0) NOT NULL PRIMARY KEY,
    FIRST_NAME VARCHAR(16777216),
    LAST_NAME VARCHAR(16777216),
    EMAIL VARCHAR(16777216),
    PHONE VARCHAR(16777216),
    ADDRESS VARCHAR(16777216)
   );
   
   CREATE TABLE SALES_DB.SALES_SCHEMA.ORDERS (
    ORDER_ID NUMBER(38, 0) NOT NULL PRIMARY KEY,
    CUSTOMER_ID NUMBER(38, 0),
    ORDER_DATE DATE,
    TOTAL_AMOUNT FLOAT,
    ORD_QTY NUMBER(5, 0)
   );
   
   ```

---

## 🔗 **Step 5: Configure Linked Services in ADF**
### 5a: Create Linked Service for AWS S3
- Go to **Azure Data Factory Studio** → **Manage** → **Linked Services** → `+ New`
- Select **Amazon S3**, enter `Access Key ID`, `Secret Access Key`, `Bucket Name`, and `Region`.
- Click `Test Connection`, then `Create`.

### 5b: Create Linked Service for Azure Blob Storage
- Go to **Azure Data Factory Studio** → **Manage** → **Linked Services** → `+ New`
- Select **Azure Blob Storage** → Enter **Storage Account Name** and **Access Key**.
- Click `Test Connection`, then `Create`.

### 5c: Create Linked Service for Snowflake
- Select **Snowflake** → Enter **Account, Database, Schema, Warehouse, Authentication Type**.
- Click `Test Connection`, then `Create`.

---

## 📂 **Step 6: Create Datasets in ADF**
### 6a: Create Dataset for AWS S3 Customers Data
- **Azure Data Factory Studio** → **Author** → **Datasets** → `+ New`
- Search **Amazon S3**, select **Delimited Text**, enter path to `customers.csv`.

### 6b: Create Dataset for Azure Blob Orders Data
- Repeat the same steps as **6a**, but select **Azure Blob Storage** and use `orders.csv`.

### 6c: Create Dataset for Snowflake Customers Table
- Select **Snowflake Linked Service**, enter **Customers Table** name.

### 6d: Create Dataset for Snowflake Orders Table
- Select **Snowflake Linked Service**, enter **Orders Table** name.

---

## 🔀 **Step 7: Create the ADF Pipeline**
1. **Go to Azure Data Factory Studio** → **Author** → **Pipelines** → `+ New Pipeline`.
2. **Add Copy Data Activity for Customers Data:**
   - **Source**: Select `Customers_S3`
   - **Sink**: Select `Customers_Snowflake`
3. **Add Copy Data Activity for Orders Data:**
   - **Source**: Select `Orders_Blob`
   - **Sink**: Select `Orders_Snowflake`
4. **Enable Staging:** Use an Azure Blob Storage container (`staging`).
5. Click `Publish All` to save changes.

---

## ⏳ **Step 8: Create ADF Trigger**
1. **ADF Studio** → **Author** → Select **Pipeline** → Click **Add Trigger**.
2. Configure schedule as needed.
3. Click `Publish & Test`.

---

## ✅ **Step 9: Validate Data in Snowflake**
```sql
SELECT * FROM SALES_DB.SALES_SCHEMA.CUSTOMERS;
SELECT * FROM SALES_DB.SALES_SCHEMA.ORDERS;
```

---

## 📢 **Conclusion**
This project showcases how to integrate data across multiple cloud platforms using **Azure Data Factory**, moving customer and order data from **AWS S3 & Azure Blob Storage** into **Snowflake**. The end result is a **unified, cloud-agnostic data pipeline** that enables seamless data ingestion and business analytics.

---

## 🔗 **Connect with Me**
👤 **Prayag Verma**  
🔗 **LinkedIn:** [linkedin.com/in/prayagv](https://www.linkedin.com/in/prayagv/)  
🔗 **GitHub:** [github.com/prayag-verma](https://github.com/prayag-verma)  
🔗 **Portfolio:**  → [profile.aimtocode.com](https://profile.aimtocode.com/)

---

## 📄 **License**
This repository is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code as per the license terms.

🚀 Feel free to raise an issue or contribute via pull requests!  

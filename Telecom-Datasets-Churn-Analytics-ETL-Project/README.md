# 📊 **Telecom Churn ETL Pipeline Using Azure Cloud Services**

## 🚀 **Overview**
This project demonstrates a fully automated ETL pipeline using Azure Data Factory, Databricks, and Azure SQL Database to process and analyze T-Mobile customer churn data. The solution is designed to be scalable, secure, and efficient, leveraging Azure's cloud capabilities.

---

## 🚀 Getting Started

To get started, most out of these projects:

**Clone the Repository:**
   ```bash
   git clone https://github.com/prayag-verma/Microsot-Azure-Project/tree/main/Telecom-Datasets-Churn-Analytics-ETL-Project
   cd Microsot-Azure-Project/tree/main/Telecom-Datasets-Churn-Analytics-ETL-Project
   ```

### 🤝 **Contributors**  

👤 **Prayag Verma**  
👥 **Data Engineer**  

🔗 **LinkedIn:**  → [linkedin.com/in/prayagv](https://www.linkedin.com/in/prayagv/)  
🔗 **Portfolio:**  → [profile.aimtocode.com](https://profile.aimtocode.com/)

---

## 🗂️ **Container Structure**
```plaintext
telecodatasa
├── raw
│   └── t-mobile
│       └── 2024
│           └── 02
│               └── 14
│                   └── Telecom_churn_customer_sample_data.xlsx
├── staging
│   └── t-mobile
└── curated
    └── t-mobile
```

---

## 🏗️ **Resource Group Creation**
- **Resource Group**: `Tmobile-teleco-rg`
- **Project**: `T Mobile`
- **Environment**: Development

```sh
az group create --name Tmobile-teleco-rg --location eastus
```

---

## 📦 **Azure Data Lake Storage Gen2 Setup**

### 🔹 **Basics**
- **Storage Account Name**: `telecodatasa`
- **Location**: East US
- **Primary Service**: Azure Data Lake Storage Gen2
- **Performance**: Standard
- **Replication**: Locally-redundant storage (LRS)
- **Access Tier**: Hot

### 🔹 **Container Creation**
- `raw`
- `staging`
- `curated`

```sh
az storage container create --name raw --account-name telecodatasa
az storage container create --name staging --account-name telecodatasa
az storage container create --name curated --account-name telecodatasa
```

---

## 🔗 **Linked Services Setup**
### 1. **ADLS Gen2**
- **Name**: `ls_telecodatasa`
- **Type**: Azure Data Lake Storage Gen2
- **Authentication**: Service Principal
- **URL**: `https://telecodatasa.dfs.core.windows.net`

### 2. **Azure SQL Database**
- **Name**: `ls_tmobile_sqldb`
- **Server**: `t-mobile-sql-server.database.windows.net`
- **Database**: `t-mobile-sql-db`
- **Authentication**: SQL Authentication
- **User**: `sql-server-dmin`
- **Password**: `Secret@Key#2025!`

### 3. **Databricks**
- **Name**: `ls_teleco_dbricks`
- **Domain**: `https://adb-2011499564703575.15.azuredatabricks.net`
- **Authentication**: Access Token
- **Cluster**: `etl-cluster`

### 4. **Customer Info Databricks**
- **Name**: `ls_telecom_customer_info_databricks`
- **Type**: Databricks
- **Purpose**: For extended customer info transformations
 
---

## 🗄️ **Create Tables**

### 📌 **telecom_analytics Table**
```sql
SET ANSI_NULLS ON;
GO
SET QUOTED_IDENTIFIER ON;
GO
CREATE TABLE [dbo].[telecom_analytics](
	[CustomerID] [varchar](50) NOT NULL,
	[Gender] [varchar](10) NULL,
	[SeniorCitizen] [bit] NULL,
	[Partner] [varchar](5) NULL,
	[Dependents] [varchar](5) NULL,
	[Tenure] [int] NULL,
	[PhoneService] [varchar](5) NULL,
	[MultipleLines] [varchar](20) NULL,
	[InternetService] [varchar](20) NULL,
	[OnlineSecurity] [varchar](20) NULL,
	[OnlineBackup] [varchar](20) NULL,
	[DeviceProtection] [varchar](20) NULL,
	[TechSupport] [varchar](20) NULL,
	[StreamingTV] [varchar](20) NULL,
	[StreamingMovies] [varchar](20) NULL,
	[Contract] [varchar](20) NULL,
	[PaperlessBilling] [varchar](5) NULL,
	[PaymentMethod] [varchar](30) NULL,
	[MonthlyCharges] [decimal](10, 2) NULL,
	[TotalCharges] [decimal](10, 2) NULL,
	[Churn] [varchar](5) NULL,
	[LoadDate] [datetime] NULL
) ON [PRIMARY];
GO
ALTER TABLE [dbo].[telecom_analytics] ADD CONSTRAINT [PK_telecom_analytics] PRIMARY KEY CLUSTERED ([CustomerID] ASC);
GO
CREATE NONCLUSTERED INDEX [IX_telecom_analytics_churn] ON [dbo].[telecom_analytics]([Churn] ASC);
GO
ALTER TABLE [dbo].[telecom_analytics] ADD DEFAULT (getdate()) FOR [LoadDate];
GO
```
---

### 📌 **telecom_customer_info Table**
```sql
SET ANSI_NULLS ON;
GO
SET QUOTED_IDENTIFIER ON;
GO
CREATE TABLE [dbo].[telecom_customer_info](
	[CustomerID] [varchar](50) NOT NULL,
	[Count] [int] NULL,
	[Country] [varchar](100) NULL,
	[State] [varchar](100) NULL,
	[City] [varchar](100) NULL,
	[ZipCode] [varchar](20) NULL,
	[LatLong] [varchar](100) NULL,
	[Latitude] [decimal](10, 6) NULL,
	[Longitude] [decimal](10, 6) NULL,
	[ChurnValue] [int] NULL,
	[ChurnScore] [decimal](5, 2) NULL,
	[CLTV] [decimal](10, 2) NULL,
	[ChurnReason] [varchar](255) NULL,
	[LoadDate] [datetime] NULL
) ON [PRIMARY];
GO
ALTER TABLE [dbo].[telecom_customer_info] ADD CONSTRAINT [PK_telecom_customer_extended] PRIMARY KEY CLUSTERED ([CustomerID] ASC);
GO
CREATE NONCLUSTERED INDEX [IX_customer_extended_churn] ON [dbo].[telecom_customer_info]([ChurnScore] ASC, [ChurnValue] ASC);
GO
CREATE NONCLUSTERED INDEX [IX_customer_extended_location] ON [dbo].[telecom_customer_info]([Country] ASC, [State] ASC, [City] ASC);
GO
ALTER TABLE [dbo].[telecom_customer_info] ADD DEFAULT (getdate()) FOR [LoadDate];
GO
ALTER TABLE [dbo].[telecom_customer_info] ADD CONSTRAINT [FK_customer_extended] FOREIGN KEY([CustomerID]) REFERENCES [dbo].[telecom_analytics]([CustomerID]);
GO
```

---

## 📊 **Datasets Configuration**
### 1. **Source Dataset (Raw Input)**
- **Name**: `ds_source_excel`
- **Type**: Excel (ADLS Gen2)
- **Path**: `raw/t-mobile/2024/02/14/Telecom_churn_customer_sample_data.xlsx`

### 2. **Staging Dataset (Cleansed)**
- **Name**: `ds_staging_parquet`
- **Type**: Parquet (ADLS Gen2)
- **Path**: `staging/t-mobile/cleansed_data.parquet`

### 3. **Curated Dataset (Transformed Parquet)**
- **Name**: `ds_transformed_parquet_curated_to_sqlDB`
- **Type**: Parquet (ADLS Gen2)
- **Path**: `curated/t-mobile/transformed_data.parquet`

### 4. **Customer Info Curated Dataset**
- **Name**: `ds_transformed_parquet_curated_to_customer_info_sqlDB`
- **Type**: Parquet (ADLS Gen2)
- **Path**: `curated/t-mobile/telecom_customer_info.parquet`

### 5. **SQL DB Target Table**
- **Name**: `ds_curated_sql`
- **Type**: Azure SQL Table
- **Table**: `dbo.telecom_analytics`

### 6. **Customer Info SQL Table**
- **Name**: `ds_telecom_customer_info_table_sql`
- **Type**: Azure SQL Table
- **Table**: `dbo.telecom_customer_info`

---

## 📋 **Pipeline and Activities Setup**
### 1. **Main Pipeline**
- **Name**: `pl_tmobile_churn_main`

### 2. **Activities**
#### A. **Copy Source to Staging**
- **Activity**: `copy_source_to_staging`
- **Source**: `ds_source_excel`
- **Sink**: `ds_staging_parquet`

#### B. **Databricks Transformation**
- **Activity**: `transform_staging_to_curated`
- **Type**: Databricks Notebook
- **Notebook Path**: `/Users/transform_staging_to_curated`

#### C. **Copy Curated to SQL**
- **Activity**: `copy_curated_to_sql`
- **Source**: `ds_transformed_parquet_curated_to_sqlDB`
- **Sink**: `ds_curated_sql`

#### D. **Another Databricks Transformation**
- **Activity**: `transform_customer_info_staging_to_curated`
- **Type**: Databricks Notebook
- **Path**: `/Users/telecom_customer_info_table`

#### E. **Copy Customer Info to SQL**
- **Activity**: `copy_curated_to_customer_info_sql`
- **Source**: `ds_transformed_parquet_curated_to_customer_info_sqlDB`
- **Sink**: `ds_telecom_customer_info_table_sql`

---

## 📓 **Databricks Notebooks**
### 1. `transform_staging_to_curated`
- Reads staging parquet, applies transformations, and writes to  `curated/t-mobile/transformed_data.parquet` for telecom analytics, check check databricks notebook `Databricks/transform_staging_to_curated.py)`

### 2. `telecom_customer_info_table`
- Extends data transformations and writes to `curated/t-mobile/telecom_customer_info.parquet` for Customer Info, check databricks notebook `Databricks/telecom_customer_info_table.py)`

---

## 🚦 **Running the Pipeline**
1. Upload Excel file to `/raw/telecom/2024/02/14/Telecom_churn_customer_sample_data.xlsx`
2. Trigger `pl_tmobile_churn_main` pipeline in Azure Data Factory.
3. Monitor execution and logs.

---

## ✅ **Output**
- Transformed data loaded into Azure SQL tables:
  - `dbo.telecom_analytics`
  - `dbo.telecom_customer_info`

---

## 📢 **Feedback**
Open issues or suggestions are welcome!

💬 Feel free to raise an issue or contribute via pull requests!  

Contributions are welcome! If you have additional exercises, improvements, or suggestions, please fork the repository and submit a pull request.

## 📄 License

This project is licensed under the MIT License.
=======
Feel free to explore, learn, and contribute!

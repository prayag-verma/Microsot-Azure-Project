# COMMAND ----------
from pyspark.sql.functions import current_timestamp, col
import json

# COMMAND ----------
# Configuration and Helper Functions
def get_configs():
    return {
        "storage_account": "telecodatasa",
        "oauth_configs": {
            "fs.azure.account.auth.type": "OAuth",
            "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
            "fs.azure.account.oauth2.client.id": "1c48d69e-4eca-4b6b-95ee-04d03ae1afae",
            "fs.azure.account.oauth2.client.secret": "YOUR_AZURE_SECRET_HERE",
            "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/84c31ca0-ac3b-4eae-ad11-519d80233e6f/oauth2/token"
        },
        "mount_points": {
            "staging": "/mnt/staging",
            "curated": "/mnt/curated"
        }
    }

def check_mount(mount_point):
    """Check if a mount point exists"""
    try:
        return any(mount.mountPoint == mount_point for mount in dbutils.fs.mounts())
    except Exception as e:
        print(f"Error checking mount {mount_point}: {str(e)}")
        return False

def safe_unmount(mount_point):
    """Safely unmount if exists"""
    try:
        if check_mount(mount_point):
            dbutils.fs.unmount(mount_point)
            print(f"Successfully unmounted {mount_point}")
    except Exception as e:
        print(f"Error unmounting {mount_point}: {str(e)}")

def mount_storage(container, mount_point):
    """Mount storage with proper error handling"""
    configs = get_configs()
    try:
        if not check_mount(mount_point):
            dbutils.fs.mount(
                source = f"abfss://{container}@{configs['storage_account']}.dfs.core.windows.net/t-mobile",
                mount_point = mount_point,
                extra_configs = configs['oauth_configs']
            )
            print(f"Successfully mounted {container} at {mount_point}")
        else:
            print(f"Mount point {mount_point} already exists")
    except Exception as e:
        print(f"Error mounting {container}: {str(e)}")
        raise e

# COMMAND ----------
# Main Transformation Code
try:
    configs = get_configs()
    
    # Setup mounts
    mount_storage("staging", configs["mount_points"]["staging"])
    mount_storage("curated", configs["mount_points"]["curated"])
    
    # Read staging data
    print("Reading parquet file...")
    df = spark.read.parquet(f"{configs['mount_points']['staging']}/cleansed_data.parquet")
    print(f"Read {df.count()} rows")

    # Select and rename columns to match SQL schema
    df_transformed = df.select(
        col("CustomerID"),
        col("Gender"),
        col("Senior_Citizen").alias("SeniorCitizen"),
        col("Partner"),
        col("Dependents"),
        col("Tenure_Months").alias("Tenure"),
        col("Phone_Service").alias("PhoneService"),
        col("Multiple_Lines").alias("MultipleLines"),
        col("Internet_Service").alias("InternetService"),
        col("Online_Security").alias("OnlineSecurity"),
        col("Online_Backup").alias("OnlineBackup"),
        col("Device_Protection").alias("DeviceProtection"),
        col("Tech_Support").alias("TechSupport"),
        col("Streaming_TV").alias("StreamingTV"),
        col("Streaming_Movies").alias("StreamingMovies"),
        col("Contract"),
        col("Paperless_Billing").alias("PaperlessBilling"),
        col("Payment_Method").alias("PaymentMethod"),
        col("Monthly_Charges").alias("MonthlyCharges"),
        col("Total_Charges").alias("TotalCharges"),
        col("Churn_Label").alias("Churn")
    )

    # Cast columns and add LoadDate
    df_transformed = df_transformed \
        .withColumn("SeniorCitizen", col("SeniorCitizen").cast("boolean")) \
        .withColumn("Tenure", col("Tenure").cast("integer")) \
        .withColumn("MonthlyCharges", col("MonthlyCharges").cast("decimal(10,2)")) \
        .withColumn("TotalCharges", col("TotalCharges").cast("decimal(10,2)")) \
        .withColumn("LoadDate", current_timestamp())

    print("Transformations applied successfully")

    # Write to curated
    print("Writing to curated...")
    df_transformed.write.mode("overwrite").parquet(f"{configs['mount_points']['curated']}/transformed_data.parquet")
    print("Write complete")

except Exception as e:
    print(f"Error occurred: {str(e)}")
    raise e

finally:
    # Cleanup
    for mount_point in configs["mount_points"].values():
        safe_unmount(mount_point)
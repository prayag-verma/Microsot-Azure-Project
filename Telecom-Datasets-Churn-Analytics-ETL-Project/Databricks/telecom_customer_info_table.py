# COMMAND ----------
# Setup Code
from pyspark.sql.functions import current_timestamp, col
import json

# Global configurations
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

def mount_storage(container, mount_point, configs):
    """Mount storage with proper error handling"""
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

def setup_mounts():
    """Setup all required mounts"""
    configs = get_configs()
    for container, mount_point in [("staging", configs["mount_points"]["staging"]), 
                                 ("curated", configs["mount_points"]["curated"])]:
        mount_storage(container, mount_point, configs)
    return configs

def cleanup_mounts(configs):
    """Cleanup all mounts"""
    for mount_point in configs["mount_points"].values():
        safe_unmount(mount_point)

# COMMAND ----------
# MAGIC %md
# MAGIC ## Extended Data Transformation

# COMMAND ----------
try:
    # Setup mounts and get configs
    configs = setup_mounts()

    # Check if the file exists before reading
    staging_path = f"{configs['mount_points']['staging']}/cleansed_data.parquet"
    if not dbutils.fs.ls(staging_path):
        raise FileNotFoundError(f"Path does not exist: {staging_path}")
    
    # Read staging data
    print("Reading parquet file...")
    df = spark.read.parquet(f"{configs['mount_points']['staging']}/cleansed_data.parquet")
    print(f"Read {df.count()} rows")

    # Select and rename columns for extended table
    telecom_customer_info_table = df.select(
        col("CustomerID"),
        col("Count").cast("integer"),
        col("Country"),
        col("State"),
        col("City"),
        col("Zip_Code").alias("ZipCode"),
        col("Lat_Long").alias("LatLong"),
        col("Latitude").cast("decimal(10,6)"),
        col("Longitude").cast("decimal(10,6)"),
        col("Churn_Value").alias("ChurnValue").cast("integer"),
        col("Churn_Score").alias("ChurnScore").cast("decimal(5,2)"),
        col("CLTV").cast("decimal(10,2)"),
        col("Churn_Reason").alias("ChurnReason")
    )

    # Add LoadDate
    telecom_customer_info_table = telecom_customer_info_table.withColumn("LoadDate", current_timestamp())

    print("Transformations applied successfully")

    # Write to curated
    print("Writing to curated...")
    telecom_customer_info_table.write.mode("overwrite").parquet(f"{configs['mount_points']['curated']}/telecom_customer_info.parquet")
    print("Write complete")

except Exception as e:
    print(f"Error occurred: {str(e)}")
    raise e

finally:
    # Cleanup
    try:
        cleanup_mounts(configs)
    except:
        pass  # Ignore cleanup errors
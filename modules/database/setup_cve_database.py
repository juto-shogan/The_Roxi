import os
import json
import psycopg2 # PostgreSQL adapter

# Database setup
def initialize_database(db_name, db_user, db_password, db_host, db_port):
    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        cursor = connection.cursor()

        # Set search path to public schema
        cursor.execute("SET search_path TO public;")

        # Create tables if they don't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cve_data (
            cve_id TEXT PRIMARY KEY,
            description TEXT,
            problem_type TEXT,
            published_date TEXT,
            updated_date TEXT,
            state TEXT
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS affected_products (
            id SERIAL PRIMARY KEY,
            cve_id TEXT REFERENCES cve_data (cve_id),
            product_name TEXT,
            vendor_name TEXT,
            version TEXT
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cve_references (
            id SERIAL PRIMARY KEY,
            cve_id TEXT REFERENCES cve_data (cve_id),
            reference_name TEXT,
            reference_url TEXT
        )
        """)
        connection.commit()
        print("Database tables initialized successfully.")
        return connection
    except Exception as e:
        print(f"Error connecting to or initializing database: {e}")
        return None

# Process a single CVE JSON file
def process_cve_file(file_path, cursor, connection):
    try:
        with open(file_path, "r", encoding="utf-8") as file: # Specify encoding for broader compatibility
            cve_data = json.load(file)

        # Extract data
        cve_id = cve_data.get("cveMetadata", {}).get("cveId", "N/A")
        
        # Ensure description and problem_type are extracted safely
        description = "N/A"
        if cve_data.get("containers", {}).get("cna", {}).get("descriptions"):
            description = cve_data["containers"]["cna"]["descriptions"][0].get("value", "N/A")

        problem_type = "N/A"
        if cve_data.get("containers", {}).get("cna", {}).get("problemTypes"):
            if cve_data["containers"]["cna"]["problemTypes"][0].get("descriptions"):
                problem_type = cve_data["containers"]["cna"]["problemTypes"][0]["descriptions"][0].get("description", "N/A")

        published_date = cve_data.get("cveMetadata", {}).get("datePublished", "N/A")
        updated_date = cve_data.get("cveMetadata", {}).get("dateUpdated", "N/A")
        state = cve_data.get("cveMetadata", {}).get("state", "N/A")
        
        # Insert main CVE data
        # ON CONFLICT DO NOTHING is equivalent to INSERT OR IGNORE
        cursor.execute("""
        INSERT INTO cve_data (cve_id, description, problem_type, published_date, updated_date, state)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (cve_id) DO NOTHING
        """, (cve_id, description, problem_type, published_date, updated_date, state))

        # Insert affected products
        affected = cve_data.get("containers", {}).get("cna", {}).get("affected", [])
        for product in affected:
            product_name = product.get("product", "N/A")
            vendor_name = product.get("vendor", "N/A")
            version = product.get("versions", [{}])[0].get("version", "N/A")
            
            cursor.execute("""
            INSERT INTO affected_products (cve_id, product_name, vendor_name, version)
            VALUES (%s, %s, %s, %s)
            """, (cve_id, product_name, vendor_name, version))
        
        # Insert references
        references = cve_data.get("containers", {}).get("cna", {}).get("references", [])
        for reference in references:
            reference_name = reference.get("name", "N/A")
            reference_url = reference.get("url", "N/A")
            
            cursor.execute("""
            INSERT INTO cve_references (cve_id, reference_name, reference_url)
            VALUES (%s, %s, %s)
            """, (cve_id, reference_name, reference_url))

    except Exception as e:
        connection.rollback() # Rollback changes if an error occurs
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"Error processing {file_path}: {e}\n")
        print(f"Error processing {file_path}: {e}. Rolled back transaction for this file.")

# Process all CVE JSON files in a folder
def process_folder(folder_path, connection):
    cursor = connection.cursor()
    file_count = 0

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".json"):  # Only process JSON files
                file_path = os.path.join(root, file)
                process_cve_file(file_path, cursor, connection) # Pass connection to rollback
                file_count += 1
                
                # Commit and log progress every 1000 files
                if file_count % 1000 == 0:
                    connection.commit()
                    print(f"Processed {file_count} files...")

    connection.commit()
    print(f"Finished processing {file_count} files.")

# Entry point for the script
if __name__ == "__main__":
    folder_path = r"c:\Users\somto\Downloads\cvelist-main\cves"  # Replace with the folder containing CVE JSON files
    
    # --- PostgreSQL Connection Details ---
    # !! IMPORTANT: Replace with your actual PostgreSQL database credentials !!
    db_name = "roxi_cve_database"
    db_user = "your_username" 
    db_password = "your_password"
    db_host = "localhost" # Or your PostgreSQL server IP/hostname
    db_port = "5432" # Default PostgreSQL port
    # ------------------------------------

    # Initialize database
    connection = initialize_database(db_name, db_user, db_password, db_host, db_port)

    if connection:
        # Process CVE files in the folder
        process_folder(folder_path, connection)

        # Close the database connection
        connection.close()
        print("CVE processing complete.")
    else:
        print("Database connection failed. Exiting.")
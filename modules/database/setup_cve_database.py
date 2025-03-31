import os
import json
import sqlite3

# Database setup
def initialize_database(db_file):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cve_id TEXT,
        product_name TEXT,
        vendor_name TEXT,
        version TEXT,
        FOREIGN KEY (cve_id) REFERENCES cve_data (cve_id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cve_references (  -- Renamed to avoid SQLite keyword conflict
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cve_id TEXT,
        reference_name TEXT,
        reference_url TEXT,
        FOREIGN KEY (cve_id) REFERENCES cve_data (cve_id)
    )
    """)
    connection.commit()
    return connection

# Process a single CVE JSON file
def process_cve_file(file_path, cursor):
    try:
        with open(file_path, "r") as file:
            cve_data = json.load(file)

        # Extract data
        cve_id = cve_data.get("cveMetadata", {}).get("cveId", "N/A")
        description = cve_data.get("containers", {}).get("cna", {}).get("descriptions", [{}])[0].get("value", "N/A")
        problem_type = cve_data.get("containers", {}).get("cna", {}).get("problemTypes", [{}])[0].get("descriptions", [{}])[0].get("description", "N/A")
        published_date = cve_data.get("cveMetadata", {}).get("datePublished", "N/A")
        updated_date = cve_data.get("cveMetadata", {}).get("dateUpdated", "N/A")
        state = cve_data.get("cveMetadata", {}).get("state", "N/A")
        
        # Insert main CVE data
        cursor.execute("""
        INSERT OR IGNORE INTO cve_data (cve_id, description, problem_type, published_date, updated_date, state)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (cve_id, description, problem_type, published_date, updated_date, state))

        # Insert affected products
        affected = cve_data.get("containers", {}).get("cna", {}).get("affected", [])
        for product in affected:
            product_name = product.get("product", "N/A")
            vendor_name = product.get("vendor", "N/A")
            version = product.get("versions", [{}])[0].get("version", "N/A")
            
            cursor.execute("""
            INSERT INTO affected_products (cve_id, product_name, vendor_name, version)
            VALUES (?, ?, ?, ?)
            """, (cve_id, product_name, vendor_name, version))
        
        # Insert references
        references = cve_data.get("containers", {}).get("cna", {}).get("references", [])
        for reference in references:
            reference_name = reference.get("name", "N/A")
            reference_url = reference.get("url", "N/A")
            
            cursor.execute("""
            INSERT INTO cve_references (cve_id, reference_name, reference_url)
            VALUES (?, ?, ?)
            """, (cve_id, reference_name, reference_url))

    except Exception as e:
        # Log errors for later review
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"Error processing {file_path}: {e}\n")

# Process all CVE JSON files in a folder
def process_folder(folder_path, connection):
    cursor = connection.cursor()
    file_count = 0

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".json"):  # Only process JSON files
                file_path = os.path.join(root, file)
                process_cve_file(file_path, cursor)
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
    db_file = "roxi_cve_database.db"  # Replace with your desired database file name

    # Initialize database
    connection = initialize_database(db_file)

    # Process CVE files in the folder
    process_folder(folder_path, connection)

    # Close the database connection
    connection.close()
    print("CVE processing complete.")

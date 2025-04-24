import json
import psycopg2
import os # Optional: for using environment variables for credentials

def test_postgres_queries(jsonl_file_path, db_params):
    """
    Reads SQL queries from a JSONL file, executes them against a PostgreSQL DB,
    and reports success/failure counts.

    Args:
        jsonl_file_path (str): Path to the input JSONL file containing queries.
        db_params (dict): Dictionary with PostgreSQL connection parameters
                          (host, database, user, password, port - optional).
    """
    successful_queries = 0
    failed_queries = 0
    none_queries = 0
    total_queries = 0

    print(f"Starting query testing from file: {jsonl_file_path}")

    try:
        with open(jsonl_file_path, 'r') as f:
            conn = psycopg2.connect(**db_params)
            cur = conn.cursor()

            for i, line in enumerate(f):
                total_queries += 1
                query_info = None
                sql_query = None
                

                try:
                    # Parse the JSON line
                    query_info = json.loads(line.strip())
                    sql_query = query_info.get('sql')

                    if not sql_query:
                        print(f"Line {i+1}: Skipping - 'sql' field missing or empty.")
                        failed_queries += 1
                        continue

                    # --- Database Connection ---
                    # Establish connection for each query to ensure isolation,
                    # though connecting once outside the loop might be more efficient
                    # for many queries if transactional integrity isn't paramount for testing.
                  

                    # --- Execute Query ---
                    # Wrap in EXPLAIN to check syntax without modifying data or
                    # running potentially very long queries.
                    # Remove "EXPLAIN" if you want to fully execute them.
                    # Add "LIMIT 1" to SELECT queries to avoid fetching large results
                    # during testing, unless the query already has LIMIT/OFFSET.
                    test_sql = sql_query.strip()
                    if test_sql.upper().startswith("SELECT") and "LIMIT" not in test_sql.upper() and "OFFSET" not in test_sql.upper():
                       # Add LIMIT 1 to SELECTs if they don't have one already
                       if test_sql.endswith(';'):
                           test_sql = test_sql[:-1] + " LIMIT 1;"
                       else:
                           test_sql = test_sql + " LIMIT 1"

                    # Optionally use EXPLAIN for syntax check without full execution
                    # test_sql = f"EXPLAIN {test_sql}"

                    # print(f"Line {i+1}: Testing query: {test_sql[:100]}...") # Optional: print query start
                    cur.execute(test_sql)

                    # Optional: Fetch one result for SELECTs to ensure execution path works
                    if test_sql.upper().startswith("SELECT"):
                        result = cur.fetchone()
                        if result is None or len(result) == 0:
                            none_queries += 1
                            print(f"Line {i+1}: No result")
                        else:
                            print(f"Line {i+1}: First result: {result}")
                    # conn.commit() # Commit changes if any (for INSERT, UPDATE, DELETE)
                                  # Or rollback if you only want to test syntax: conn.rollback()
                    successful_queries += 1
                    # print(f"Line {i+1}: Success.") # Optional: print success

                except json.JSONDecodeError as e:
                    print(f"Line {i+1}: Failed to parse JSON - {e}")
                    failed_queries += 1
                except psycopg2.Error as e:
                    print(f"Line {i+1}: Query failed - Error: {e}")
                    print(f"Failed SQL: {sql_query}")
                    failed_queries += 1
                    if conn:
                        conn.rollback() # Rollback any transaction started by the failed query
                except Exception as e:
                    print(f"Line {i+1}: An unexpected error occurred - {e}")
                    print(f"Query context: {query_info}")
                    failed_queries += 1
                    if conn:
                        conn.rollback()
                # finally:
                #     # --- Cleanup ---
                #     if cur:
                #         cur.close()
                #     if conn:
                #         conn.close()

    except FileNotFoundError:
        print(f"Error: Input file not found at {jsonl_file_path}")
        return
    except Exception as e:
        print(f"An error occurred reading the file or during setup: {e}")
        return

    # --- Print Summary ---
    print("\n--- Query Testing Summary ---")
    print(f"Total queries processed: {total_queries}")
    print(f"Successfully executed: {successful_queries}")
    print(f"Queries with no result: {none_queries}")
    print(f"Failed queries:        {failed_queries}")
    print("---------------------------")

# --- Configuration ---
# !! Replace with your actual database details or use environment variables !!
db_connection_params = {
    'host': '10.40.137.49',          # e.g., 'localhost' or IP address
    'database': 'tmf',
    'user': 'mitobi',
    'password': 'mitobi',
    # 'port': '5432' # Optional, defaults to 5432 if not specified
}

# Path to your generated JSONL file
jsonl_file_path = 'data/generated_sql_dataset_500.jsonl'

# --- Run the Test ---
if __name__ == "__main__":
    # Basic check if placeholders are still present
    if 'your_host' in db_connection_params.values() or \
       'your_db_name' in db_connection_params.values() or \
       'your_user' in db_connection_params.values() or \
       'your_password' in db_connection_params.values() or \
       'path/to/your/output.jsonl' == jsonl_file_path:
       print("ERROR: Please update database connection details and the JSONL file path in the script before running.")
    else:
        test_postgres_queries(jsonl_file_path, db_connection_params)
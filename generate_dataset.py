import google.generativeai as genai
import json
import os
import time
import sys

# --- Configuration ---
INPUT_DDL_FILE = "data/schema/rawdata-ddl.sql"
OUTPUT_JSONL_FILE = "generated_sql_dataset.jsonl"
TARGET_NUM_EXAMPLES = 500  # Target number of examples to generate
EXAMPLES_PER_BATCH = 25     # How many examples to request per API call (adjust based on performance/rate limits)
MAX_RETRIES = 5           # Max retries per batch on failure
RETRY_DELAY_SECONDS = 15  # Time to wait before retrying
GEMINI_MODEL_NAME = 'gemini-2.5-flash-preview-04-17' # Or another suitable Gemini model available via API
# --- End Configuration ---

def load_ddl(filepath):
    """Loads the DDL content from the specified file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"ERROR: Input DDL file not found at '{filepath}'")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to read DDL file '{filepath}': {e}")
        sys.exit(1)

def clean_response_text(text):
    """Removes markdown code block formatting from the API response."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[len("```json"):].strip()
    if text.endswith("```"):
        text = text[:-len("```")].strip()
    return text

def generate_dataset():
    """Generates the dataset using the Gemini API."""
    # Configure API Key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("ERROR: GOOGLE_API_KEY environment variable not set.")
        sys.exit(1)
    genai.configure(api_key=api_key)

    # Load Schema
    schema_ddl = load_ddl(INPUT_DDL_FILE)
    print(f"Loaded DDL schema from '{INPUT_DDL_FILE}'.")

    # Initialize Gemini Model
    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        print(f"Initialized Gemini model: {GEMINI_MODEL_NAME}")
    except Exception as e:
        print(f"ERROR: Failed to initialize Gemini model: {e}")
        sys.exit(1)

    # Generation Loop
    generated_count = 0
    # Clear or create the output file
    with open(OUTPUT_JSONL_FILE, "w", encoding="utf-8") as f:
        pass # Just to clear the file if it exists

    print(f"Starting dataset generation. Target: {TARGET_NUM_EXAMPLES} examples.")

    while generated_count < TARGET_NUM_EXAMPLES:
        print("-" * 20)
        print(f"Examples generated so far: {generated_count} / {TARGET_NUM_EXAMPLES}")
        num_needed = TARGET_NUM_EXAMPLES - generated_count
        num_to_request_now = min(EXAMPLES_PER_BATCH, num_needed)

        # --- Construct the Prompt ---
        # This is the core part, instructing the model clearly
        prompt_text = f"""
You are an expert PostgreSQL data generation assistant.
Your task is to generate {num_to_request_now} diverse and realistic English examples for a text-to-SQL dataset based on the provided PostgreSQL schema.

**Provided PostgreSQL Schema:**
```sql
{schema_ddl}
```

Instructions for each example:

1.Create an English Question (sql_prompt): Formulate a clear, natural language question that a user might ask about the data described by the schema. Vary the questions from simple lookups to more complex queries involving joins, aggregations, filtering, sorting, etc.
2.Generate PostgreSQL Query (sql): Write the correct PostgreSQL query that accurately answers the sql_prompt.
  - Use ONLY tables and columns defined in the provided schema.
  - Ensure correct PostgreSQL syntax.
  - Generate queries of varying complexity (e.g., using SELECT, WHERE, JOIN, GROUP BY, HAVING, ORDER BY, LIMIT, OFFSET, WITH clauses, subqueries).
3. Generate SQL Context (sql_context): This is crucial. Provide the necessary SQL context to execute the generated sql query on a temporary database. This context MUST include:
  - The CREATE TABLE statements only for the tables explicitly referenced in the generated sql query. Copy these directly from the provided schema above.
  - 1 or 2 realistic INSERT INTO ... VALUES ...; statements only for those referenced tables. The inserted data should be minimal but relevant, allowing the sql query to potentially produce a meaningful (even if empty) result when executed.

Output Format:

Return the generated examples as a valid JSON list. Each element in the list MUST be a JSON object with exactly these three keys: "sql_prompt", "sql", "sql_context".

Example JSON Object Structure:
JSON

{{
  "sql_prompt": "Show the names and email addresses of all customers living in London, ordered by name.",
  "sql": "SELECT name, email FROM customers WHERE city = 'London' ORDER BY name;",
  "sql_context": "CREATE TABLE customers (customer_id SERIAL PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), city VARCHAR(50));\\nINSERT INTO customers (name, email, city) VALUES ('Alice Smith', 'alice@example.com', 'London');\\nINSERT INTO customers (name, email, city) VALUES ('Bob Johnson', 'bob.j@sample.org', 'London');"
}}

(Note: The sql_context should contain actual CREATE/INSERT statements relevant to the specific sql query.)

Do NOT include the json ... markdown formatting in your final response. Output only the raw JSON list.

Generate {num_to_request_now} examples now.
"""
        
        retries = 0
        success = False
        while retries < MAX_RETRIES and not success:
            try:
                print(f"Requesting batch of {num_to_request_now} examples (Attempt {retries + 1}/{MAX_RETRIES})...")
                response = model.generate_content(prompt_text)

                # Clean and parse the response
                response_text = clean_response_text(response.text)
                batch_data = json.loads(response_text) # Expecting a list

                # Basic validation of the received batch structure
                validated_batch = []
                if isinstance(batch_data, list):
                    for item in batch_data:
                        if isinstance(item, dict) and "sql_prompt" in item and "sql" in item and "sql_context" in item:
                            validated_batch.append(item)
                        else:
                            print(f"WARN: Skipping invalid item in batch: {item}")
                else:
                    print(f"WARN: API response was not a JSON list: {type(batch_data)}")
                    raise ValueError("API response format incorrect (expected list)")


                if validated_batch:
                    print(f"INFO: Successfully received and parsed {len(validated_batch)} examples.")
                    # Append valid examples to the JSONL file
                    with open(OUTPUT_JSONL_FILE, "a", encoding="utf-8") as f:
                        for example in validated_batch:
                            f.write(json.dumps(example, ensure_ascii=False) + "\n")

                    generated_count += len(validated_batch)
                    success = True # Exit retry loop

                else:
                    print("WARN: Received empty or invalid batch from API.")
                    # No point retrying if the API returned something, but it was empty/invalid
                    # Consider stopping or just trying the next batch iteration. Let's retry.
                    retries += 1
                    print(f"Waiting {RETRY_DELAY_SECONDS} seconds before retrying...")
                    time.sleep(RETRY_DELAY_SECONDS)


            except json.JSONDecodeError as e:
                print(f"ERROR: Failed to decode JSON response (Attempt {retries + 1}/{MAX_RETRIES}). Error: {e}")
                try:
                    print("--- API Response Text ---")
                    print(response.text)
                    print("-------------------------")
                except NameError: # response might not be defined if generate_content failed early
                    print("(No response text available)")
                retries += 1
                print(f"Waiting {RETRY_DELAY_SECONDS} seconds before retrying...")
                time.sleep(RETRY_DELAY_SECONDS)
            except Exception as e:
                # Catch other potential errors (API connection, rate limits handled by library?, etc.)
                print(f"ERROR: API call or processing failed (Attempt {retries + 1}/{MAX_RETRIES}). Error: {e}")
                retries += 1
                print(f"Waiting {RETRY_DELAY_SECONDS} seconds before retrying...")
                time.sleep(RETRY_DELAY_SECONDS)

        if not success:
            print(f"ERROR: Failed to generate batch after {MAX_RETRIES} attempts. Stopping.")
            break # Exit main generation loop

    # --- Completion ---
    print("-" * 20)
    if generated_count >= TARGET_NUM_EXAMPLES:
        print(f"Successfully generated {generated_count} examples.")
    else:
        print(f"Generation stopped early. Generated {generated_count} out of {TARGET_NUM_EXAMPLES} examples.")
    print(f"Dataset saved to '{OUTPUT_JSONL_FILE}'")

if __name__ == "__main__":
    generate_dataset()
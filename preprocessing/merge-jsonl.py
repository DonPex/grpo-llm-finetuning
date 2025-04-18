import json
import sys

def create_enriched_jsonl(sql_file_path, questions_file_path, output_file_path):
    """
    Reads SQL queries and corresponding questions, enriches the SQL JSON objects
    with the questions, and writes the results to a .jsonl file.

    Args:
        sql_file_path (str): Path to the file containing JSON objects with SQL queries (one per line).
        questions_file_path (str): Path to the file containing corresponding questions (one per line).
        output_file_path (str): Path to the output .jsonl file.
    """
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as sql_file, \
             open(questions_file_path, 'r', encoding='utf-8') as questions_file, \
             open(output_file_path, 'w', encoding='utf-8') as outfile:

            sql_lines = sql_file.readlines()
            question_lines = questions_file.readlines()

            if len(sql_lines) != len(question_lines):
                print(f"Error: Number of lines in '{sql_file_path}' ({len(sql_lines)}) "
                      f"does not match the number of lines in '{questions_file_path}' ({len(question_lines)}).",
                      file=sys.stderr)
                return

            for i, sql_line in enumerate(sql_lines):
                try:
                    # Strip whitespace and parse the JSON from generated-sql.txt
                    sql_data = json.loads(sql_line.strip())

                    # Get the corresponding question, stripping newline characters
                    question = question_lines[i].strip()

                    # Create the new enriched dictionary
                    enriched_data = {"sql_prompt": question}
                    enriched_data.update(sql_data) # Add the original sql and sql_context fields

                    # Write the enriched data as a JSON line to the output file
                    json.dump(enriched_data, outfile)
                    outfile.write('\n')

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON on line {i+1} of {sql_file_path}: {e}", file=sys.stderr)
                    # Optionally skip the line or handle the error differently
                    continue
                except IndexError:
                    # This should not happen if lengths match, but good practice to include
                    print(f"Error: Reached end of questions file prematurely at line {i+1}.", file=sys.stderr)
                    break

            print(f"Successfully created enriched file: {output_file_path}")

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

# --- Script Execution ---
# Replace with the actual file paths if running this script directly
sql_input_filename = 'data/generated-sql-with-inserts.jsonl'
questions_input_filename = 'data/questions-simple.txt'
output_filename = 'full-dataset.jsonl'

# Create the enriched file
create_enriched_jsonl(sql_input_filename, questions_input_filename, output_filename)
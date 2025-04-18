import json

def extract_sql_context(file_path):
  """
  Extracts the 'sql_context' values from a file containing JSON objects per line.

  Args:
    file_path: The path to the input text file.

  Returns:
    A list containing all the 'sql_context' values found in the file.
    Returns an empty list if the file is not found or cannot be processed.
  """
  sql_context_list = []
  try:
    # Use the filename provided by the user
    with open(file_path, 'r', encoding='utf-8') as f:
      for line_num, line in enumerate(f, 1):
        try:
          # Trim whitespace and check if the line is not empty
          line = line.strip()
          if line:
            data = json.loads(line)
            # Check if 'sql_context' key exists and its value is not empty/None
            if data.get('sql_context'):
              sql_context_list.append(data['sql_context'])
        except json.JSONDecodeError as e:
          # Error handling: Skip invalid JSON lines silently as requested.
          # Uncomment the print statement below for debugging invalid lines.
          print(f"DEBUG: Skipping invalid JSON on line {line_num}. Error: {e}. Line content: '{line[:100]}...'")
          pass # Continue to the next line
        except Exception as e:
          # Error handling: Skip other errors silently.
          # Uncomment the print statement below for debugging other processing errors.
          print(f"DEBUG: An error occurred processing line {line_num}: {line[:100]}... Error: {e}")
          pass # Continue to the next line
  except FileNotFoundError:
    # Error handling: File not found.
    # Uncomment the print statement below for debugging.
    # print(f"DEBUG: Error - File not found at {file_path}")
    return [] # Return empty list as processing cannot continue
  except Exception as e:
    # Error handling: Other file reading errors.
    # Uncomment the print statement below for debugging.
    # print(f"DEBUG: An error occurred reading the file: {e}")
    return [] # Return empty list

  return sql_context_list

# Specify the path to the text file uploaded by the user
# The execution environment should map this filename to the uploaded file content.
file_path = 'data/generated-sql.jsonl'

# Extract the values
sql_contexts = extract_sql_context(file_path)

# Print only the extracted 'sql_context' values, each separated by a blank line.
if sql_contexts:
  # Join all contexts with two newlines (one after the context, one for the blank line)
  print("\n\n".join(sql_contexts))


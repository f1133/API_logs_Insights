import re
from collections import defaultdict
from datetime import datetime, timedelta
import pandas as pd
from tabulate import tabulate

def extract_log_info(log_line):
    log_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}).+ "(GET|POST|PUT|DELETE) (\S+) HTTP/\d\.\d" (\d+) (\d+)'
    match = re.search(log_pattern, log_line)
    if match:
        timestamp, http_method, endpoint, status_code, response_size = match.groups()
        return timestamp, http_method, endpoint, int(status_code), int(response_size)
    else:
        return None

def process_log_file(file_path):
    log_entries = []
    with open(file_path, 'r') as log_file:
        for line in log_file:
            log_entry = extract_log_info(line)
            if log_entry:
                log_entries.append(log_entry)
    return log_entries

def save_table_to_file(table_data, file_name):
    with open(file_name, 'w') as file:
        file.write(table_data)

def get_status_message(status_code):
    status_messages = {
        "200": "OK",
        "201": "Created",
        "204": "No Content",
        "400": "Bad Request",
        "401": "Unauthorized",
        "403": "Forbidden",
        "404": "Not Found",
        "500": "Server Error",
        "503": "Service Unavailable",
    }
    return status_messages.get(str(status_code), "Unknown")

def main():
    log_file_path = "api-prod-out.log" 
    log_entries = process_log_file(log_file_path)

    # Create a DataFrame from the log entries
    df = pd.DataFrame(log_entries, columns=['Timestamp', 'HTTP Method', 'Endpoint', 'Status Code', 'Response Size'])

    # Insight 1: Which endpoint is called how many times
    endpoint_counts = df['Endpoint'].value_counts().reset_index()
    endpoint_counts.columns = ['Endpoint', 'count']

    # Insight 2: How many API calls were being made on a per-minute basis
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Timestamp'] = df['Timestamp'].apply(lambda t: t.replace(second=0, microsecond=0))
    api_calls_per_minute = df['Timestamp'].value_counts().reset_index()
    api_calls_per_minute.columns = ['Timestamp', 'count']

    # Insight 3: How many API calls are there in total for each HTTP status code
    status_code_counts = df['Status Code'].value_counts().reset_index()
    status_code_counts.columns = ['statusCode', 'count']
    status_code_counts['statusCode'] = status_code_counts['statusCode'].astype(str)
    status_code_counts['statusMessage'] = status_code_counts['statusCode'].apply(get_status_message)
    status_code_counts_table = tabulate(status_code_counts[['statusMessage', 'statusCode', 'count']], headers='keys', tablefmt='pipe', showindex=False)
    
    # Save the tables to files
    save_table_to_file(tabulate(endpoint_counts, headers='keys', tablefmt='grid', showindex=False), "endpoint_counts.txt")
    save_table_to_file(tabulate(api_calls_per_minute, headers='keys', tablefmt='grid', showindex=False), "api_calls_per_minute.txt")
    save_table_to_file(status_code_counts_table, "status_code_counts.txt")

    # Print the results
    print("Which endpoint is called how many times:")
    print(tabulate(endpoint_counts, headers='keys', tablefmt='grid', showindex=False))

    print("\nHow many API calls were being made on a per-minute basis:")
    print(tabulate(api_calls_per_minute, headers='keys', tablefmt='grid', showindex=False))

    print("\nCount of API hits for each endpoint:")
    print(status_code_counts_table)

if __name__ == "__main__":
    main()

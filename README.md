

# Log Analysis with Python

This Python script is designed to perform log analysis on a log file containing API access data. It extracts relevant information from the log file, processes it, and presents insightful statistics in the form of tables.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python (https://www.python.org/downloads/)

### Installation

1. Clone the repository to your local machine.

```bash
git clone https://github.com/f1133/unomok.git
```

2. Navigate to the project directory.

```bash
cd your-repository
```

3. Install the required dependencies.

```bash
pip install pandas tabulate
```

### Usage

1. Place your log file (`api-prod-out.log`) in the same directory as the script.

2. Run the script.

```bash
python log_analysis.py
```

3. The script will process the log file and display insightful statistics about API access.

4. Tables will also be saved to files: `endpoint_counts.txt`, `api_calls_per_minute.txt`, and `status_code_counts.txt`.

## Insights

1. **Which endpoint is called how many times:** This section shows the count of API calls for each unique endpoint.

2. **How many API calls were being made on a per-minute basis:** This section shows the number of API calls made per minute.

3. **Count of API hits for each HTTP status code:** This section displays the total number of API calls for each HTTP status code along with the corresponding status message.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


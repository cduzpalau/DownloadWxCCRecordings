import requests
import argparse
import json
import os
import yaml

# Function to read task IDs from a text file
def read_task_ids(file_path):
    try:
        with open(file_path, 'r') as file:
            task_ids = [line.strip() for line in file if line.strip()]
        if len(task_ids) > 10:
            raise ValueError("Input file contains more than 10 task IDs. Please limit the file to 10 task IDs.")
        return task_ids
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

# Function to write URLs to a text file
def write_urls(file_path, urls):
    try:
        with open(file_path, 'w') as file:
            for url in urls:
                file.write(url + '\n')
        print(f"URLs saved to: {file_path}")
    except Exception as e:
        print(f"Error writing to file: {file_path} - {e}")

# Function to load configuration from a YAML file
def load_config(config_file):
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        print(f"Error: Config file not found: {config_file}")
        exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing config file: {e}")
        exit(1)

# Function to fetch capture URLs using the Webex Contact Center API
def fetch_capture_urls(task_ids, include_segments, org_id, url_expiration, base_url, api_key, developer_mode):
    urls = []
    file_data = []
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    endpoint = f"{base_url}/v1/captures/query"

    payload = {
        "query": {
            "orgId": org_id,
            "urlExpiration": url_expiration,
            "taskIds": task_ids,
            "includeSegments": include_segments
        }
    }

    if developer_mode:
        print(f"[DEBUG] Sending POST request to {endpoint} with payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(endpoint, headers=headers, json=payload)

        if developer_mode:
            print(f"[DEBUG] Response status code: {response.status_code}")
            print(f"[DEBUG] Response body: {response.text}")

        response.raise_for_status()

        captures = response.json()
        for task in captures.get('data', []):
            task_id = task.get('taskId')
            for recording in task.get('recording', []):
                file_path = recording.get('attributes', {}).get('filePath')
                file_name = recording.get('attributes', {}).get('fileName')
                if file_path and file_name:
                    urls.append(file_path)
                    file_data.append((task_id, file_name, file_path))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching captures: {e}")

    return urls, file_data

# Function to download files
def download_files(file_data, output_directory, developer_mode):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for task_id, file_name, file_path in file_data:
        output_file = os.path.join(output_directory, f"{task_id}_{file_name}")
        if developer_mode:
            print(f"[DEBUG] Downloading file from {file_path} to {output_file}")
        try:
            response = requests.get(file_path, stream=True)
            response.raise_for_status()
            with open(output_file, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Downloaded: {output_file}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file {file_name} for task {task_id}: {e}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Download Webex Contact Center capture URLs.")
    parser.add_argument("input_file", help="Path to the input file containing task IDs.")
    parser.add_argument("output_file", help="Path to the output file for saving capture URLs.")
    parser.add_argument("--config", default="config.yml", help="Path to the configuration YAML file (default: config.yml).")
    parser.add_argument("--include-segments", action="store_true", help="Include segments in the capture URLs.")
    parser.add_argument("--url-expiration", type=int, default=10, help="URL expiration time in minutes (default: 10).")
    parser.add_argument("--download", action="store_true", help="Download files directly from the parsed URLs.")
    parser.add_argument("--output-directory", default="downloads", help="Directory to save downloaded files (default: downloads).")
    parser.add_argument("--developer-mode", action="store_true", help="Enable developer mode for verbose logging.")

    args = parser.parse_args()

    config = load_config(args.config)

    org_id = config.get('org-id')
    base_url = config.get('base-url')
    api_key = config.get('api-key')

    if not all([org_id, base_url, api_key]):
        print("Error: Missing required configuration parameters in config.yml")
        exit(1)

    task_ids = read_task_ids(args.input_file)
    urls, file_data = fetch_capture_urls(task_ids, args.include_segments, org_id, args.url_expiration, base_url, api_key, args.developer_mode)

    if args.download:
        download_files(file_data, args.output_directory, args.developer_mode)
    else:
        if urls:
            write_urls(args.output_file, urls)
        else:
            print("No capture URLs found.")

if __name__ == "__main__":
    main()

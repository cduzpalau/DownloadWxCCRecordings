# Webex Contact Center Recording Downloader

This Python script allows you to interact with the Webex Contact Center API to:

1. Fetch URLs for task captures.
2. Optionally download the capture files (also called voice recordings) directly, renaming them for better organization.

## Features
- Fetch capture URLs for up to 10 task IDs in a single request using [list captures API call](https://developer.webex-cx.com/documentation/captures/v1/list-captures)
- Parse and save capture URLs into a text file for use with tools like `wget`.
- Download captures directly, renaming them as `<taskId>_<fileName>.wav`.
- Supports YAML configuration for API keys and settings.
- Developer mode for detailed debugging logs.

## Prerequisites
- Python 3.7+
- Required Python libraries:
  - `requests`
  - `pyyaml`

Install dependencies using:
```bash
pip install requests pyyaml
```

## Usage

### Input File
Prepare a text file (e.g., `input.txt`) with up to 10 task IDs, each on a new line, you can use Analyser to fetch the session IDs from the voice calls you need to download the recordings from:
```
task-id-1
task-id-2
...
```

### Configuration File
Create a `config.yml` file with the following format:
```yaml
# Configuration for Webex Contact Center API
org-id: "<your-org-id>"
base-url: "<webex-api-base-url>"
api-key: "<your-api-key>"
```
Replace the placeholders with your actual values.

### Command-Line Arguments
Run the script with:
```bash
python script.py <input_file> <output_file> [options]
```

#### Required Arguments:
- `<input_file>`: Path to the input file containing task IDs.
- `<output_file>`: Path to save the list of capture URLs.

#### Optional Arguments:
- `--config`: Path to the YAML configuration file (default: `config.yml`).
- `--include-segments`: Include segmented captures in the results.
- `--url-expiration`: URL expiration time in minutes (default: 10).
- `--download`: Download the capture files directly.
- `--output-directory`: Directory to save downloaded files (default: `downloads`).
- `--developer-mode`: Enable detailed logging for debugging.

### Examples

#### Fetch and Save URLs
```bash
python script.py input.txt output.txt
```

#### Fetch and Download Captures
```bash
python script.py input.txt output.txt --download
```

#### Enable Developer Mode
```bash
python script.py input.txt output.txt --developer-mode
```

## Output
- **URL Mode:** A text file containing capture URLs, one per line.
- **Download Mode:** Files saved to the specified directory, renamed as `<taskId>_<fileName>.wav`.

## Error Handling
- The script enforces a limit of 10 task IDs. Exceeding this limit will raise an error.
- Missing or invalid configuration parameters in `config.yml` will cause the script to exit with an error message.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
Contributions are welcome! Feel free to fork this repository and submit pull requests.

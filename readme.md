Here is a Python script to download Webex Contact Center captures using the API. The script takes a text file with task IDs as input and produces a text file containing the URLs of the captures. The --include-segments command-line option allows you to control whether the includeSegments boolean is set.

Instructions to Use the Script
	1.	Install Required Libraries:
Ensure requests is installed. You can install it with:

pip install requests

2.	Prepare the Input File:
Create a text file with task IDs, each on a separate line.

3.	Run the Script:
Use the following command to run the script:

python webex_capture_downloader.py input.txt output.txt --base-url <API_BASE_URL> --api-key <API_KEY> [--include-segments]

Replace <API_BASE_URL> with the Webex Contact Center API base URL, <API_KEY> with your API key, and include the --include-segments flag if desired.

4.	Output:
The script generates an output file (output.txt in the example) containing the capture URLs, which can be used with wget:

wget -i output.txt
# WhatsApp Direct Message Link Updater for Google Contacts CSV

This script processes your exported Google Contacts CSV file by converting phone numbers into a WhatsApp direct message link. The link is written to the **"Website 1 - Value"** field based on the phone number present in the **"Phone 1 - Value"** column.

## Features

- **Phone Number Normalization:**  
  Cleans and standardizes various phone number formats by:
  - Removing non-digit characters.
  - Handling multiple numbers separated by ` ::: ` (using the first one).
  - Removing country codes or extra digits when necessary.
  
- **WhatsApp Link Generation:**  
  Creates a WhatsApp DM link in the format:  
  `https://wa.me/91<normalized_phone_number>`

- **In-Place CSV Update:**  
  Searches for CSV files in the current directory, processes them, and updates the file with the new WhatsApp DM links in the **"Website 1 - Value"** column.

- **Verbose Logging:**  
  Provides detailed logging output for troubleshooting and tracking the processing steps.

## Requirements

- **Python Version:** 3.6 or later (tested with Python 3.11)
- **Dependencies:**  
  - [pandas](https://pandas.pydata.org/)  
    Install via pip:  
    ```bash
    pip install pandas
    ```

## Setup & Usage

1. **Export Your Google Contacts:**  
   Export your Google Contacts as a CSV file. Ensure the CSV includes the following columns:
   - **"Phone 1 - Value"**: Contains the phone numbers.
   - **"Website 1 - Value"**: Will be updated with the WhatsApp DM link.

2. **Place Files in the Same Directory:**  
   Save the exported CSV file and the script (e.g., `run.py`) in the same directory.

3. **Run the Script:**  
   Open a terminal or command prompt in that directory and run:
   ```bash
   python run.py
   ```
   The script will search for CSV files, process each file, and update the CSV with WhatsApp DM links.

4. **Check Logging Output:**  
   The script provides verbose logging to the console. Review the logs for details on processing steps, warnings, or any errors encountered.

## Troubleshooting

- **Missing Columns:**  
  If the script reports missing columns, verify your CSV file contains **"Phone 1 - Value"** and **"Website 1 - Value"**.

- **Unexpected Phone Formats:**  
  If you see warnings related to phone number lengths, ensure your phone numbers follow a format that the script can process. The script defaults to taking the last 10 digits if the format is not as expected.

## Customization

Feel free to modify the script to handle additional phone number formats or to change the logging verbosity as needed.

## License

This project is free to use and modify. No warranty is provided.

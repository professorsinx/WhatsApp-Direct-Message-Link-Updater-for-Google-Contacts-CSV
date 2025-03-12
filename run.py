#!/usr/bin/env python3
import os
import glob
import re
import logging
import pandas as pd

# Configure logging for detailed output.
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def clean_phone_number(raw_phone):
    """
    Clean and normalize the phone number.

    Handles multiple inconsistencies:
     - If the string contains multiple phone numbers separated by " ::: ", use the first one.
     - Remove all non-digit characters.
     - If the cleaned number starts with '91' and has 12 digits, remove the country code.
     - If it starts with a '0' and is 11 digits long, drop the leading 0.
     - If the number is longer than 10 digits, take the last 10 digits.
     
    Returns a tuple (normalized_number, note) where:
     - normalized_number: The 10-digit phone number (or empty string if it cannot be normalized).
     - note: A string note in case of unexpected format.
    """
    note = ""
    if pd.isna(raw_phone) or not isinstance(raw_phone, str) or raw_phone.strip() == "":
        note = "Empty phone value"
        return "", note

    logging.debug(f"Raw phone value: {raw_phone}")

    # If multiple numbers are present, split by " ::: " and choose the first one.
    if " ::: " in raw_phone:
        parts = raw_phone.split(" ::: ")
        raw_phone = parts[0].strip()
        logging.debug(f"Multiple numbers found. Using first number: {raw_phone}")

    # Remove all non-digit characters.
    digits = re.sub(r'\D', '', raw_phone)
    logging.debug(f"Digits extracted: {digits}")

    # If the number has 12 digits and starts with '91', remove the country code.
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
        logging.debug("Removed leading '91' from a 12-digit number.")
    # If the number has 11 digits and starts with '0', remove the leading '0'.
    elif len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]
        logging.debug("Removed leading '0' from an 11-digit number.")
    # If the number is longer than 10 digits, assume the last 10 digits are the local number.
    elif len(digits) > 10:
        logging.warning(f"Unexpected digit length ({len(digits)}) for number {digits}. Taking last 10 digits.")
        digits = digits[-10:]

    # Log a warning if the normalized number is not exactly 10 digits.
    if len(digits) != 10:
        note = f"Unexpected normalized length: {len(digits)} digits."
        logging.warning(f"After cleaning, phone number {raw_phone} resulted in {digits} ({note})")
    else:
        logging.info(f"Normalized phone number: {digits}")

    return digits, note

def process_csv_file(csv_file):
    """
    Reads the CSV file, normalizes phone numbers, updates the existing "Website 1 - Value"
    field with the WhatsApp direct message link, and writes back to the same file.
    """
    logging.info(f"Processing file: {csv_file}")

    try:
        # Read CSV file using pandas.
        df = pd.read_csv(csv_file, dtype=str, encoding='utf-8', keep_default_na=False)
    except Exception as e:
        logging.error(f"Error reading {csv_file}: {e}")
        return

    # Define the column names.
    phone_column = "Phone 1 - Value"
    website_column = "Website 1 - Value"

    # Check if the required columns exist.
    if phone_column not in df.columns:
        logging.error(f"Column '{phone_column}' not found in {csv_file}. Skipping this file.")
        return

    if website_column not in df.columns:
        logging.error(f"Column '{website_column}' not found in {csv_file}. Skipping this file.")
        return

    # Update the Website 1 - Value field with the WhatsApp DM link.
    updated_websites = []
    # Using items() instead of iteritems() for compatibility with newer pandas versions.
    for index, raw_phone in df[phone_column].items():
        normalized_phone, note = clean_phone_number(raw_phone)
        if normalized_phone:
            whatsapp_link = f"https://wa.me/91{normalized_phone}"
        else:
            whatsapp_link = ""  # Leave empty if normalization fails.
        updated_websites.append(whatsapp_link)
        logging.debug(f"Row {index}: Raw: {raw_phone} | Normalized: {normalized_phone} | Link: {whatsapp_link} | Note: {note}")

    # Replace the existing "Website 1 - Value" column with the updated WhatsApp links.
    df[website_column] = updated_websites

    # Write the updated DataFrame back to the same CSV file.
    try:
        df.to_csv(csv_file, index=False, encoding='utf-8')
        logging.info(f"File '{csv_file}' updated successfully with WhatsApp DM links in '{website_column}'.")
    except Exception as e:
        logging.error(f"Error writing to {csv_file}: {e}")

def main():
    # Search for CSV files in the current directory.
    csv_files = glob.glob("*.csv")
    if not csv_files:
        logging.info("No CSV files found in the current directory.")
        return

    logging.info(f"Found CSV files: {csv_files}")

    # Process each CSV file found.
    for csv_file in csv_files:
        process_csv_file(csv_file)

if __name__ == "__main__":
    main()

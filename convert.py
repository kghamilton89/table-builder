import pandas as pd
from datetime import datetime
import sys
import os
import glob

def find_first_input_csv(exclude_filename):
    csv_files = [f for f in glob.glob("*.csv") if f != exclude_filename]
    if not csv_files:
        raise FileNotFoundError("No input CSV files found in the current directory.")
    return csv_files[0]

def main():
    if len(sys.argv) != 3:
        print("Usage: python convert.py <customer_name> <output_filename_without_extension>")
        sys.exit(1)

    customer = sys.argv[1]
    output_filename = sys.argv[2] + ".csv"

    try:
        # Find the first input CSV (excluding the output file)
        input_file = find_first_input_csv(output_filename)
        print(f"Found input file: {input_file}")

        # Read the input CSV
        df = pd.read_csv(input_file)

        # Create Unix timestamp column called 'time'
        df['time'] = df['Date (dd/MM/yyyy HH:mm:ss)'].apply(
            lambda x: int(datetime.strptime(x, "%d/%m/%Y %H:%M:%S").timestamp())
        )

        # Drop the original date column
        df = df.drop(columns=['Date (dd/MM/yyyy HH:mm:ss)'])

        # Melt to long format
        melted = pd.melt(
            df,
            id_vars=['time', 'Type'],
            var_name='ASN',
            value_name='Value'
        )

        # Add Customer column
        melted['Customer'] = customer

        # Reorder columns
        melted = melted[['time', 'Type', 'Customer', 'ASN', 'Value']]

        # Append to output file if it exists, or create it
        if os.path.exists(output_filename):
            melted.to_csv(output_filename, mode='a', index=False, header=False)
            print(f"Appended to {output_filename}")
        else:
            melted.to_csv(output_filename, index=False)
            print(f"Created new file: {output_filename}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

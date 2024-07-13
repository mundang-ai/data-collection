import csv
import re
import sys

def clean_text(text):
    # Remove numbers at the beginning of the string
    cleaned = re.sub(r'^\d+\s*', '', text)
    # Remove any remaining digits
    cleaned = re.sub(r'\d', '', cleaned)
    return cleaned.strip()

def clean_csv(input_file, output_file):
    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
             open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            
            for row in reader:
                if len(row) >= 6:
                    # Clean columns 4, 5, and 6 (indices 3, 4, and 5)
                    for i in range(3, 6):
                        row[i] = clean_text(row[i])
                writer.writerow(row)
        
        print(f"Cleaned data has been written to {output_file}")
    except FileNotFoundError:
        print(f"Error: The input file '{input_file}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to write to '{output_file}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <input_file_path> <output_file_path>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    clean_csv(input_file, output_file)

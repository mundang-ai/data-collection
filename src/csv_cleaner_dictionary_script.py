import csv
import re
import sys

def clean_text(text):
    # Remove numbers at the beginning of the string
    cleaned = re.sub(r'^\d+\s*', '', text)
    
    # Function to replace numbers not in brackets
    def replace_non_bracketed(match):
        if match.group(1) is not None:  # If there's a bracket, don't replace
            return match.group(0)
        return ''  # Otherwise, remove the number
    
    # Remove any remaining digits, except those in brackets
    cleaned = re.sub(r'\[(\d+)\]|\d', replace_non_bracketed, cleaned)
    
    return cleaned.strip()

def clean_csv(input_file, output_file):
    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
             open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            
            for row in reader:
                # Clean all columns in the row
                cleaned_row = [clean_text(cell) for cell in row]
                writer.writerow(cleaned_row)
        
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

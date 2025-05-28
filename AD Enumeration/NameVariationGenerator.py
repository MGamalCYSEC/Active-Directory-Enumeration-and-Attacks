import os

def generate_name_variations(input_file, output_file):
    try:
        # Read input file
        with open(input_file, 'r') as file:
            names = file.readlines()

        # Open output file for writing
        with open(output_file, 'w') as file:
            for name in names:
                name = name.strip()
                if not name:
                    continue

                parts = name.split()

                if len(parts) != 2:
                    file.write(f"Invalid name format: {name}\n")
                    continue

                first_name, last_name = parts

                # Full Name Variations
                file.write(f"{first_name}{last_name}\n")
                file.write(f"{first_name}.{last_name}\n")
                file.write(f"{last_name}.{first_name}\n")
                file.write(f"{first_name}_{last_name}\n")
                file.write(f"{last_name}_{first_name}\n")
                file.write(f"{first_name}-{last_name}\n")
                file.write(f"{last_name}-{first_name}\n")

                # Initials and Name Combinations
                file.write(f"{first_name[0]}{last_name}\n")
                file.write(f"{last_name}.{first_name[0]}\n")
                file.write(f"{first_name[0]}.{last_name}\n")
                file.write(f"{first_name}.{last_name[0]}\n")
                file.write(f"{last_name[0]}.{first_name}\n")
                file.write(f"{first_name[0]}.{last_name[0]}\n")

                # First Name Only
                file.write(f"{first_name}\n")

                # Last Name Only
                file.write(f"{last_name}\n")

                # Reverse Order Formats
                file.write(f"{last_name}{first_name[0]}\n")
                file.write(f"{first_name}{last_name[0]}\n")
                file.write(f"{last_name}.{first_name}\n")

        print(f"Name variations have been written to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

def print_help():
    help_text = """
Usage: python script_name.py <input_file> <output_file>

This script generates variations of names provided in an input file and writes them to an output file.

Arguments:
  <input_file>   Path to the input file containing names (one name per line, in 'First Last' format).
  <output_file>  Path to the output file where name variations will be saved.

Example:
  python script_name.py names.txt variations.txt
    """
    print(help_text)

# Usage example
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print_help()
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

        if os.path.exists(input_file):
            generate_name_variations(input_file, output_file)
        else:
            print(f"Input file '{input_file}' does not exist.")

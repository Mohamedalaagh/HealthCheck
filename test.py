import json

# Input and output file paths
input_file = 'disease.txt'
output_file = 'disease.json'

# List to store disease data
diseases = []

# Read the disease.txt file
with open(input_file, 'r') as file:
    for line in file:
        # Split the line into components
        parts = line.strip().split('|')
        
        # Ensure the line has the correct number of parts
        if len(parts) == 5:
            # Create a dictionary for the disease
            disease = {
                "name": parts[0],
                "type": parts[1],
                "danger_percentage": f"{parts[2]}%",  # Add % to danger_percentage
                "best_practices": parts[3].split(','),  # Convert best practices to a list
                "link": parts[4]
            }
            
            # Add the disease to the list
            diseases.append(disease)

# Write the data to a JSON file
with open(output_file, 'w') as file:
    json.dump(diseases, file, indent=4)

print(f"Data has been successfully converted to {output_file}.")
import json

input_file = 'disease.txt'
output_file = 'disease.json'

diseases = []

with open(input_file, 'r') as file:
    for line in file:
        parts = line.strip().split('|')
        if len(parts) == 5:
            disease = {
                "name": parts[0],
                "type": parts[1],
                "danger_percentage": f"{parts[2]}%",
                "best_practices": parts[3].split(','),
                "link": parts[4]
            }
            diseases.append(disease)

with open(output_file, 'w') as file:
    json.dump(diseases, file, indent=4)

print(f"Data has been successfully converted to {output_file}.")

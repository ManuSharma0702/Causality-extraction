import pandas as pd
import json
import re
# Read the text file
with open("test.txt", "r", encoding='UTF-8') as file:
    lines = file.readlines()

# Parse each line as JSON and store data
data = []
for line in lines:
    # Remove trailing newline and parse the line as JSON
    entry = json.loads(line.strip())
    extracted_double_angle_brackets = re.findall(r'<<\s*(.*?)\s*>>', entry['text'])
    extracted_double_square_brackets = re.findall(r'\[\[\s*(.*?)\s*]]', entry['text'])
  
    entry["entities"] = [extracted_double_angle_brackets[0], extracted_double_square_brackets[0]]
    data.append({"text": entry["text"], "label": entry["label"], "entities": entry['entities']})

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("test.csv", index=False)
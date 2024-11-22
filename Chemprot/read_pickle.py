import pandas as pd

# Load the dataset
df = pd.read_csv("test.csv", names=["text", "label", "entities"])

# Get the initial length of the dataset
initial_length = len(df)

# Group by 'text' and 'entities' and combine labels
grouped = df.groupby(["text", "entities"])

# Identify and print duplicate entries (those with multiple labels for the same 'text' and 'entities')
duplicates = grouped.filter(lambda x: len(x) > 1)

print("\n=== Duplicate Entries (before combining) ===")
print(duplicates)

# Combine labels for duplicate rows
combined_df = (
    grouped["label"]
    .apply(lambda x: list(set(x)))  # Combine labels into a unique list
    .reset_index()
)

combined_df["label"] = combined_df["label"].apply(lambda x: ", ".join(x))

# Save the processed dataset to a new CSV file
combined_df.to_csv("test_combined.csv", index=False)

# Get the final length of the dataset
final_length = len(combined_df)

# Print the results
print(f"\nInitial number of rows: {initial_length}")
print(f"Final number of rows: {final_length}")

print("\n=== Combined Dataset (after merging duplicates) ===")


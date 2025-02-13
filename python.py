import pandas as pd

# Specify the path to your CSV file
csv_file_path = 'c:/Users/saina/OneDrive/Desktop/Electricity_Demand-and_Price_ForecastingInfosys_Internship_Oct2025/final_dataset.csv'

# Read the CSV file into a DataFrame
data = pd.read_csv(csv_file_path)

# Display the first few rows of the DataFrame
print(data.head())

# Display the first 10 rows
print(data.head(10))

# Display specific columns
print(data[['date', 'demand', 'RRP']].head())

# Display all columns without truncation
pd.set_option('display.max_columns', None)
print(data.head())

# Display the shape of the DataFrame
print(data.shape)

# 1. Handling Missing Values
# Drop rows with any missing values
df_cleaned = data.dropna()

# Alternatively, fill missing values with a specific value (e.g., 0 or mean of the column)
# df_cleaned = data.fillna(0)
# df_cleaned = data.fillna(data.mean())

# 2. Removing Duplicates
df_cleaned = df_cleaned.drop_duplicates()

# 3. Converting Data Types
# Convert a column to a specific data type (e.g., 'date' column to datetime)
df_cleaned['date'] = pd.to_datetime(df_cleaned['date'], format='%d-%m-%Y', dayfirst=True)

# 4. Handling Outliers
# Select only numeric columns for quantile calculation
numeric_cols = df_cleaned.select_dtypes(include=['number']).columns

# Remove outliers using the IQR method
Q1 = df_cleaned[numeric_cols].quantile(0.25)
Q3 = df_cleaned[numeric_cols].quantile(0.75)
IQR = Q3 - Q1
df_cleaned = df_cleaned[~((df_cleaned[numeric_cols] < (Q1 - 1.5 * IQR)) | (df_cleaned[numeric_cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

# 5. Renaming Columns
# Rename columns to more meaningful names
df_cleaned = df_cleaned.rename(columns={'old_name': 'new_name'})

# 6. Standardizing Text Data
if 'text_column' in df_cleaned.columns:
    # Convert text data to lowercase
    df_cleaned['text_column'] = df_cleaned['text_column'].str.lower()

    # Remove leading/trailing whitespace
    df_cleaned['text_column'] = df_cleaned['text_column'].str.strip()
else:
    print("Column 'text_column' does not exist in the DataFrame.")

# 7. Encoding Categorical Variables
if 'categorical_column' in df_cleaned.columns:
    # Convert categorical variables to dummy/indicator variables
    df_cleaned = pd.get_dummies(df_cleaned, columns=['categorical_column'])
else:
    print("Column 'categorical_column' does not exist in the DataFrame.")

# Display the cleaned DataFrame
print("Cleaned DataFrame:")
print(df_cleaned.head())

# Save the cleaned DataFrame to a new CSV file
df_cleaned.to_csv('cleaned_data.csv', index=False)
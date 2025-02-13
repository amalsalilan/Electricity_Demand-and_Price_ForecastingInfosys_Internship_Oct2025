import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Specify the path to your CSV file
csv_file_path = 'c:/Users/saina/OneDrive/Desktop/Electricity_Demand-and_Price_ForecastingInfosys_Internship_Oct2025/final_dataset.csv'

# Specify the data types for the columns
dtype = {
    'date': str,
    'demand': float,
    'RRP': float,
    'demand_pos_RRP': float,
    'RRP_positive': float,
    'demand_neg_RRP': float,
    'RRP_negative': float,
    'frac_at_neg_RRP': float,
    'min_temperature': float,
    'max_temperature': float,
    'solar_exposure': float,
    'rainfall': float,
    'school_day': str,
    'holiday': str
}

# Read the CSV file into a DataFrame
data = pd.read_csv(csv_file_path, dtype=dtype, low_memory=False)

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

# Resample the data to monthly frequency and calculate the mean for numeric columns only
df_monthly = df_cleaned.resample('M', on='date').mean(numeric_only=True)

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

# Display summary statistics of the cleaned DataFrame
print(df_cleaned.describe())

# Save the cleaned DataFrame to a new CSV file
df_cleaned.to_csv('cleaned_data.csv', index=False)

# Histogram of a numeric column
df_cleaned['demand'].hist()
plt.title('Histogram of Demand')
plt.xlabel('Demand')
plt.ylabel('Frequency')
plt.show()

# Boxplot of a numeric column
sns.boxplot(x=df_cleaned['demand'])
plt.title('Boxplot of Demand')
plt.xlabel('Demand')
plt.show()

# Scatter plot between two numeric columns
plt.scatter(df_cleaned['demand'], df_cleaned['RRP'])
plt.title('Scatter Plot of Demand vs RRP')
plt.xlabel('Demand')
plt.ylabel('RRP')
plt.show()

# Line plot of monthly demand over time with month names on x-axis
plt.figure(figsize=(14, 8))
plt.plot(df_monthly.index, df_monthly['demand'], linestyle='-', color='blue', alpha=0.7, label='Monthly Mean Demand')
plt.plot(df_monthly.index, df_monthly['demand'].rolling(window=12).mean(), color='red', linewidth=2, label='12-Month Rolling Mean')
plt.title('Monthly Demand Over Time')
plt.xlabel('Year-Month')
plt.ylabel('Demand')
plt.xticks(df_monthly.index, df_monthly.index.strftime('%b %Y'), rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Line plot of monthly RRP over time with month names on x-axis
plt.figure(figsize=(14, 8))
plt.plot(df_monthly.index, df_monthly['RRP'], linestyle='-', color='green', alpha=0.7, label='Monthly Mean RRP')
plt.plot(df_monthly.index, df_monthly['RRP'].rolling(window=12).mean(), color='orange', linewidth=2, label='12-Month Rolling Mean RRP')
plt.title('Monthly RRP Over Time')
plt.xlabel('Year-Month')
plt.ylabel('RRP')
plt.xticks(df_monthly.index, df_monthly.index.strftime('%b %Y'), rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

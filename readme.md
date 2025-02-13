# Electricity Demand and Price Forecasting

This project aims to analyze and forecast electricity demand and price using historical data. The project includes data cleaning, visualization, and analysis steps.

## Project Structure

## Files

- [`cleaned_data.csv`](cleaned_data.csv): Cleaned dataset after preprocessing.
- [`final_dataset.csv`](final_dataset.csv): Original dataset containing historical electricity demand and price data.
- [`figures`](figures): Directory containing generated plots and visualizations.
- [`python.py`](python.py): Main script for data processing, analysis, and visualization.
- [`LICENSE`](LICENSE): License file for the project.

## Installation

1. Clone the repository:

```sh
git clone https://github.com/yourusername/electricity-demand-forecasting.git
cd electricity-demand-forecasting

Create a virtual environment and activate it:

Install the required dependencies:

Usage

Data Cleaning: The script reads the final_dataset.csv file, handles missing values, removes duplicates, converts data types, handles outliers, renames columns, standardizes text data, and encodes categorical variables.

Data Visualization: The script generates various plots to visualize the data, including histograms, box plots, scatter plots, and line plots.

Example Plots

Histogram of Demand: Visualizes the frequency distribution of electricity demand.

Boxplot of Demand: Shows the distribution and outliers of electricity demand.

Scatter Plot of Demand vs RRP: Displays the relationship between electricity demand and RRP.

Monthly Demand Over Time: Line plot showing the monthly mean demand and 12-month rolling mean.

Monthly RRP Over Time: Line plot showing the monthly mean RRP and 12-month rolling mean.

Running the Script
To run the script, execute the following command in your terminal:

Dependencies

pandas
matplotlib
seaborn
Install the required dependencies using pip:

License
This project is licensed under the MIT License. See the LICENSE file for details.
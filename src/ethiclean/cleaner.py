import pandas as pd


class DataCleaner:
    """A class to clean and standardize messy CSV data."""

    def clean_csv(self, file_path):
        """
        Clean a CSV file by standardizing column headers and removing blank rows.
        
        This method performs the following operations:
        1. Reads the CSV file into a DataFrame
        2. Converts all column headers to lowercase
        3. Replaces spaces in column names with underscores
        4. Removes any rows that are completely blank (all NaN values)
        
        Args:
            file_path (str): Path to the CSV file to be cleaned.
            
        Returns:
            pd.DataFrame: A cleaned DataFrame with standardized column names and no blank rows.
        """
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)
        
        # Standardize column headers: convert to lowercase and replace spaces with underscores
        # This ensures consistent column naming conventions across the dataset
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Remove rows that are completely blank (all NaN values)
        # This cleans up formatting issues or incomplete entries in the dataset
        df = df.dropna(how='all')
        
        return df


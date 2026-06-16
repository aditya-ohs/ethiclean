import pandas as pd
import warnings


class BiasDetector:
    """A class to detect potential bias in categorical columns of a DataFrame."""

    def detect_class_imbalance(self, df, column_name):
        """
        Analyze the distribution of unique values in a column and detect class imbalance.
        
        This method performs the following operations:
        1. Validates that the column exists in the DataFrame
        2. Calculates the count and percentage of each unique value
        3. Identifies if any single group dominates the dataset (>80%)
        4. Issues a warning if significant imbalance is detected
        
        Args:
            df (pd.DataFrame): The DataFrame containing the column to analyze.
            column_name (str): The name of the column to check for bias.
            
        Returns:
            dict: A dictionary containing:
                - 'distributions': dict of each unique value and its percentage
                - 'imbalance_detected': bool indicating if any group exceeds 80%
                - 'dominant_group': str or None, the group exceeding 80% (if any)
                - 'dominant_percentage': float or None, the percentage of the dominant group
                - 'total_records': int, the total number of records analyzed
        """
        # Validate that the specified column exists in the DataFrame
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in DataFrame.")
        
        # Get the total count of non-null values in the column
        total_records = df[column_name].notna().sum()
        
        if total_records == 0:
            raise ValueError(f"Column '{column_name}' contains no non-null values.")
        
        # Calculate the frequency of each unique value
        value_counts = df[column_name].value_counts()
        
        # Calculate the percentage distribution for each unique value
        # This shows the proportion of the dataset each group represents
        distributions = (value_counts / total_records * 100).round(2).to_dict()
        
        # Identify if any single group exceeds 80% of the dataset
        # This threshold indicates potential bias or class imbalance
        imbalance_detected = False
        dominant_group = None
        dominant_percentage = None
        
        for group, percentage in distributions.items():
            if percentage > 80:
                imbalance_detected = True
                dominant_group = group
                dominant_percentage = percentage
                # Issue a warning about the detected imbalance
                warnings.warn(
                    f"Potential bias detected in column '{column_name}': "
                    f"Group '{group}' represents {percentage}% of the dataset.",
                    UserWarning
                )
                break
        
        # Return results as a structured dictionary
        return {
            'distributions': distributions,
            'imbalance_detected': imbalance_detected,
            'dominant_group': dominant_group,
            'dominant_percentage': dominant_percentage,
            'total_records': total_records
        }
        

import pandas as pd
from ethiclean.cleaner import DataCleaner
from ethiclean.bias import BiasDetector


class ReportGenerator:
    """A class to generate formatted health reports from cleaned data and bias analysis."""

    def generate_report(self, original_df, cleaned_df, bias_results):
        """
        Generate and print a formatted dataset health report to the terminal.
        
        This method creates a visually organized report showing:
        1. Report title and timestamp information
        2. Data cleaning statistics (rows removed, rows retained)
        3. Column header standardization summary
        4. Bias analysis results and warnings
        
        Args:
            original_df (pd.DataFrame): The original DataFrame before cleaning.
            cleaned_df (pd.DataFrame): The cleaned DataFrame after processing.
            bias_results (dict): Dictionary output from BiasDetector.detect_class_imbalance().
        """
        # Calculate cleaning statistics
        original_rows = len(original_df)
        cleaned_rows = len(cleaned_df)
        rows_removed = original_rows - cleaned_rows
        
        # Print the report header
        print("\n" + "=" * 70)
        print(" " * 15 + "DATASET HEALTH REPORT")
        print("=" * 70 + "\n")
        
        # Print data cleaning summary
        print("📊 DATA CLEANING SUMMARY")
        print("-" * 70)
        print(f"  Original rows:        {original_rows:,}")
        print(f"  Cleaned rows:         {cleaned_rows:,}")
        print(f"  Rows removed:         {rows_removed:,}")
        print(f"  Removal rate:         {(rows_removed / original_rows * 100):.2f}%")
        print()
        
        # Print column standardization information
        print("🔧 COLUMN STANDARDIZATION")
        print("-" * 70)
        print(f"  Total columns:        {len(cleaned_df.columns)}")
        print(f"  Standardized columns:")
        for col in cleaned_df.columns:
            print(f"    • {col}")
        print()
        
        # Print bias analysis results
        print("⚠️  BIAS ANALYSIS RESULTS")
        print("-" * 70)
        
        if bias_results['imbalance_detected']:
            # Print warning if imbalance is detected
            print(f"  ⛔ IMBALANCE DETECTED!")
            print(f"  Dominant group:       {bias_results['dominant_group']}")
            print(f"  Dominance level:      {bias_results['dominant_percentage']}%")
            print(f"  Status:               REQUIRES ATTENTION")
        else:
            # Print all clear message if no imbalance
            print("  ✅ No significant imbalance detected")
            print(f"  Status:               ALL CLEAR")
        
        print()
        print("  Distribution Breakdown:")
        for group, percentage in sorted(
            bias_results['distributions'].items(),
            key=lambda x: x[1],
            reverse=True
        ):
            # Create a simple bar chart representation
            bar_length = int(percentage / 5)
            bar = "█" * bar_length
            print(f"    {group:20} {percentage:6.2f}%  {bar}")
        print()
        print("=" * 70 + "\n")

    def generate_report_from_csv(self, csv_file_path, column_to_analyze):
        """
        Convenience method that performs cleaning and bias detection in one call.
        
        This method orchestrates the full workflow:
        1. Load the original CSV
        2. Clean the data using DataCleaner
        3. Detect bias using BiasDetector
        4. Generate and display the report
        
        Args:
            csv_file_path (str): Path to the CSV file to process.
            column_to_analyze (str): Name of the column to check for bias.
        """
        # Load the original DataFrame before any processing
        original_df = pd.read_csv(csv_file_path)
        
        # Clean the data using DataCleaner
        cleaner = DataCleaner()
        cleaned_df = cleaner.clean_csv(csv_file_path)
        
        # Analyze bias in the specified column using BiasDetector
        detector = BiasDetector()
        bias_results = detector.detect_class_imbalance(cleaned_df, column_to_analyze)
        
        # Generate and display the formatted report
        self.generate_report(original_df, cleaned_df, bias_results)

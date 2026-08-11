import pandas as pd
from datasets import load_dataset
import os

def main():
    print("Fetching dataset from Hugging Face...")
    # snehaanbhawal/resume-dataset contains 'Resume' and 'Category'
    dataset = load_dataset("Sachinkelenjaguri/Resume_dataset", split="train")
    
    # Convert to pandas dataframe
    df = dataset.to_pandas()
    
    print(f"Dataset loaded. Shape: {df.shape}")
    print("Columns:", df.columns)
    
    # Let's map columns to 'Category' and 'Resume'
    if 'Resume_str' in df.columns and 'Category' in df.columns:
        df = df[['Category', 'Resume_str']]
        df = df.rename(columns={'Resume_str': 'Resume'})
    elif 'resume' in df.columns and 'category' in df.columns:
        df = df[['category', 'resume']]
        df = df.rename(columns={'category': 'Category', 'resume': 'Resume'})
    
    # Drop NAs
    df = df.dropna()
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    output_path = 'data/real_resumes.csv'
    df.to_csv(output_path, index=False)
    print(f"Saved cleaned dataset to {output_path}")

if __name__ == "__main__":
    main()

"""
EMAIL PRIORITY PREDICTION SYSTEM
Step 1: Data Preprocessing (Modified for Real-World Emails)
This script works with real emails collected from multiple sources
"""

import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
import re
import warnings
warnings.filterwarnings('ignore')

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


def load_data(filepath):
    """Load email data from CSV file"""
    print("Loading email data from:", filepath)
    data = pd.read_csv(filepath)
    print(f"Total emails loaded: {len(data)}")
    print(f"\nEmail Sources in Dataset:")
    print(data['source'].value_counts() if 'source' in data.columns else "No source info")
    print("\nFirst few rows:")
    print(data[['email_id', 'sender', 'subject', 'priority']].head())
    return data


def clean_text(text):
    """
    Clean and preprocess text data
    Remove special characters, URLs, and extra spaces
    """
    if pd.isna(text):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespaces
    text = ' '.join(text.split())
    
    return text


def remove_stopwords(text):
    """Remove common stopwords from text"""
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)


def preprocess_data(data):
    """
    Main preprocessing function
    Combines all cleaning operations
    """
    print("\n" + "="*70)
    print("PREPROCESSING REAL-WORLD EMAIL DATA")
    print("="*70)
    
    df = data.copy()
    
    # Check for missing values
    print("\nMissing values before cleaning:")
    print(df.isnull().sum())
    
    # Fill missing values with empty strings
    df['subject'] = df['subject'].fillna('')
    df['body'] = df['body'].fillna('')
    df['sender'] = df['sender'].fillna('unknown')
    
    if 'source' in df.columns:
        print(f"\nProcessing emails from {df['source'].nunique()} different sources:")
        for source in df['source'].unique():
            count = len(df[df['source'] == source])
            print(f"  • {source}: {count} emails")
    
    # Combine subject and body for text processing
    df['full_text'] = df['subject'] + ' ' + df['body']
    
    # Clean the text
    print("\n" + "-"*70)
    print("Cleaning text data...")
    df['cleaned_text'] = df['full_text'].apply(clean_text)
    
    print("Removing stopwords...")
    df['cleaned_text'] = df['cleaned_text'].apply(remove_stopwords)
    
    # Show statistics
    print("\n" + "-"*70)
    print("TEXT STATISTICS:")
    print(f"  Average subject length: {df['subject'].str.len().mean():.1f} characters")
    print(f"  Average body length: {df['body'].str.len().mean():.1f} characters")
    print(f"  Average cleaned text length: {df['cleaned_text'].str.len().mean():.1f} characters")
    
    # Priority distribution
    print("\n" + "-"*70)
    print("EMAIL PRIORITY DISTRIBUTION:")
    if 'priority' in df.columns:
        print(df['priority'].value_counts())
        print("\nPercentage Distribution:")
        print((df['priority'].value_counts(normalize=True) * 100).round(2))
    
    # Display sample cleaned data
    print("\n" + "-"*70)
    print("Sample of Cleaned Data:")
    for idx, row in df.head(3).iterrows():
        print(f"\nEmail #{row['email_id']} (from {row.get('source', 'Unknown')}):")
        print(f"  Original Subject: {row['subject'][:60]}")
        print(f"  Cleaned Text: {row['cleaned_text'][:80]}...")
        print(f"  Priority: {row.get('priority', 'Unknown')}")
    
    return df


def save_preprocessed_data(df, filepath):
    """Save preprocessed data to CSV file"""
    # Keep necessary columns
    cols_to_save = ['email_id', 'sender', 'subject', 'body', 'time_of_day', 
                    'recipient_count', 'cleaned_text', 'priority']
    
    # Add source if it exists
    if 'source' in df.columns:
        cols_to_save.insert(7, 'source')
    
    df_save = df[cols_to_save]
    df_save.to_csv(filepath, index=False)
    print(f"\n✓ Preprocessed data saved to: {filepath}")
    print(f"  Total samples: {len(df_save)}")


if __name__ == "__main__":
    import os
    
    print("="*70)
    print("EMAIL DATA PREPROCESSING SYSTEM")
    print("="*70)
    
    # Check which data file to use
    if os.path.exists('gmail_emails.csv'):
        data_file = 'gmail_emails.csv'
        print("\nUsing Gmail messages exported by 0a_gmail_collector.py")
    elif os.path.exists('real_world_emails.csv'):
        data_file = 'real_world_emails.csv'
        print("\nUsing REAL-WORLD email dataset collected from multiple sources")
    elif os.path.exists('sample_data.csv'):
        data_file = 'sample_data.csv'
        print("\nUsing SAMPLE email dataset (for demo purposes)")
    else:
        print("\n❌ ERROR: No email data file found!")
        print("Please run: python 0_email_collector.py")
        print("OR create sample_data.csv manually")
        exit(1)
    
    # Load data
    data = load_data(data_file)
    
    # Preprocess data
    preprocessed_data = preprocess_data(data)
    
    # Save preprocessed data
    save_preprocessed_data(preprocessed_data, 'preprocessed_emails.csv')
    
    print("\n" + "="*70)
    print("DATA PREPROCESSING COMPLETED SUCCESSFULLY!")
    print("="*70)
    print("\nNext step: Run feature engineering")
    print("Command: python 2_feature_engineering.py")
    print("\nNote: Make sure to update the input file name in")
    print("  2_feature_engineering.py if needed")

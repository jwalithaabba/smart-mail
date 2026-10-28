"""
EMAIL PRIORITY PREDICTION SYSTEM
Step 0b: Manual Email Input Interface
Add your own emails from Gmail or other sources manually
"""

import pandas as pd
import json
import os
from datetime import datetime


class EmailInputInterface:
    """Interactive interface for adding emails manually"""
    
    def __init__(self):
        self.emails = []
        self.priority_options = ['Critical', 'High', 'Medium', 'Low', 'Spam']
        self.time_options = ['morning', 'afternoon', 'evening']
        
        # Try to load existing emails
        if os.path.exists('real_world_emails.csv'):
            self.load_existing_emails()
    
    def load_existing_emails(self):
        """Load existing emails from CSV"""
        try:
            df = pd.read_csv('real_world_emails.csv')
            self.emails = df.to_dict('records')
            print(f"✓ Loaded {len(self.emails)} existing emails")
        except:
            self.emails = []
    
    def get_email_input(self):
        """Get email details from user input"""
        print("\n" + "="*70)
        print("ADD NEW EMAIL")
        print("="*70)
        
        email = {}
        
        # Email ID
        email['email_id'] = len(self.emails) + 1
        
        # Sender
        print("\n1. SENDER:")
        print("   Examples: boss@company.com, newsletter@amazon.com, friend@gmail.com")
        email['sender'] = input("   Enter sender email address: ").strip()
        
        if not email['sender']:
            print("❌ Sender email is required")
            return None
        
        # Subject
        print("\n2. SUBJECT:")
        email['subject'] = input("   Enter email subject: ").strip()
        
        if not email['subject']:
            print("❌ Subject is required")
            return None
        
        # Body
        print("\n3. BODY:")
        print("   Enter email body (press Enter twice to finish):")
        lines = []
        empty_count = 0
        while True:
            line = input("   ")
            if line == "":
                empty_count += 1
                if empty_count >= 2:
                    break
                lines.append(line)
            else:
                empty_count = 0
                lines.append(line)
        
        email['body'] = ' '.join(lines).strip()
        
        if not email['body']:
            print("❌ Body is required")
            return None
        
        # Time of day
        print("\n4. TIME OF DAY:")
        print("   Options: morning, afternoon, evening")
        while True:
            time = input("   Enter time of day: ").lower().strip()
            if time in self.time_options:
                email['time_of_day'] = time
                break
            else:
                print("   Invalid choice. Please enter: morning, afternoon, or evening")
        
        # Recipient count
        print("\n5. RECIPIENT COUNT:")
        print("   Enter number of recipients (1 = personal, 1000+ = broadcast)")
        while True:
            try:
                recipient_count = int(input("   Enter recipient count: "))
                if recipient_count > 0:
                    email['recipient_count'] = recipient_count
                    break
                else:
                    print("   Please enter a positive number")
            except ValueError:
                print("   Please enter a valid number")
        
        # Source
        print("\n6. EMAIL SOURCE:")
        print("   Examples: Gmail, Work, LinkedIn, Newsletter, E-commerce, Bank")
        email['source'] = input("   Enter email source/platform: ").strip()
        
        if not email['source']:
            email['source'] = 'Manual Input'
        
        # Priority
        print("\n7. PRIORITY LEVEL:")
        print("   Options:")
        for i, p in enumerate(self.priority_options, 1):
            print(f"     {i}. {p}")
        
        while True:
            try:
                choice = int(input("   Select priority (1-5): "))
                if 1 <= choice <= 5:
                    email['priority'] = self.priority_options[choice - 1]
                    break
                else:
                    print("   Please enter a number between 1 and 5")
            except ValueError:
                print("   Please enter a valid number")
        
        return email
    
    def display_email_summary(self, email):
        """Display summary of entered email"""
        print("\n" + "-"*70)
        print("EMAIL SUMMARY:")
        print("-"*70)
        print(f"ID:             {email['email_id']}")
        print(f"From:           {email['sender']}")
        print(f"Subject:        {email['subject'][:60]}...")
        print(f"Body Preview:   {email['body'][:80]}...")
        print(f"Time:           {email['time_of_day']}")
        print(f"Recipients:     {email['recipient_count']}")
        print(f"Source:         {email['source']}")
        print(f"Priority:       {email['priority']}")
        print("-"*70)
    
    def confirm_email(self):
        """Get user confirmation"""
        response = input("\nConfirm adding this email? (y/n): ").lower().strip()
        return response == 'y'
    
    def save_emails(self):
        """Save emails to CSV"""
        if not self.emails:
            print("No emails to save")
            return False
        
        df = pd.DataFrame(self.emails)
        
        # Reorder columns
        cols = ['email_id', 'sender', 'subject', 'body', 'time_of_day', 
                'recipient_count', 'source', 'priority']
        df = df[[c for c in cols if c in df.columns]]
        
        df.to_csv('real_world_emails.csv', index=False)
        print(f"\n✓ Saved {len(self.emails)} emails to: real_world_emails.csv")
        return True
    
    def display_all_emails(self):
        """Display all emails in dataset"""
        if not self.emails:
            print("No emails in dataset")
            return
        
        df = pd.DataFrame(self.emails)
        
        print("\n" + "="*70)
        print(f"ALL EMAILS ({len(df)} total)")
        print("="*70)
        
        for idx, row in df.iterrows():
            print(f"\n{idx+1}. Email ID: {row['email_id']}")
            print(f"   From: {row['sender']}")
            print(f"   Subject: {row['subject'][:60]}...")
            print(f"   Priority: {row['priority']:<10} | Source: {row['source']:<15} | Recipients: {row['recipient_count']}")
    
    def get_statistics(self):
        """Show statistics of collected emails"""
        if not self.emails:
            print("No emails to analyze")
            return
        
        df = pd.DataFrame(self.emails)
        
        print("\n" + "="*70)
        print("DATASET STATISTICS")
        print("="*70)
        
        print(f"\nTotal Emails: {len(df)}")
        
        print(f"\nPriority Distribution:")
        print(df['priority'].value_counts())
        
        print(f"\nSource Distribution:")
        print(df['source'].value_counts())
        
        print(f"\nTime Distribution:")
        print(df['time_of_day'].value_counts())
        
        print(f"\nRecipient Count Statistics:")
        print(f"  Min: {df['recipient_count'].min()}")
        print(f"  Max: {df['recipient_count'].max()}")
        print(f"  Mean: {df['recipient_count'].mean():.0f}")
        print(f"  Median: {df['recipient_count'].median():.0f}")
    
    def run_interactive_mode(self):
        """Run interactive email input mode"""
        print("\n" + "="*70)
        print("EMAIL PRIORITY PREDICTION SYSTEM")
        print("INTERACTIVE EMAIL INPUT")
        print("="*70)
        print("\nYou can add emails from Gmail, Outlook, or any other source manually.")
        print("Just copy-paste the email details.")
        
        while True:
            print("\n" + "="*70)
            print("MAIN MENU")
            print("="*70)
            print("1. Add new email")
            print("2. View all emails")
            print("3. Show statistics")
            print("4. Save and exit")
            print("5. Exit without saving")
            
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                email = self.get_email_input()
                if email:
                    self.display_email_summary(email)
                    if self.confirm_email():
                        self.emails.append(email)
                        print("✓ Email added successfully!")
                    else:
                        print("✗ Email not added")
            
            elif choice == '2':
                self.display_all_emails()
            
            elif choice == '3':
                self.get_statistics()
            
            elif choice == '4':
                if self.save_emails():
                    print("\n✓ All emails saved successfully!")
                    print("Next step: Run python 1_data_preprocessing_realemails.py")
                break
            
            elif choice == '5':
                response = input("Exit without saving? (y/n): ").lower().strip()
                if response == 'y':
                    break
            
            else:
                print("Invalid option. Please select 1-5")


def add_sample_emails_quickly():
    """Add pre-defined emails quickly for testing"""
    print("\n" + "="*70)
    print("ADDING SAMPLE EMAILS FOR QUICK TESTING")
    print("="*70)
    
    sample_emails = [
        {
            'email_id': 1,
            'sender': 'boss@company.com',
            'subject': 'URGENT: Budget Review Meeting Tomorrow',
            'body': 'Please prepare budget review materials for tomorrow morning meeting. This is critical for Q4 planning.',
            'time_of_day': 'morning',
            'recipient_count': 1,
            'source': 'Work - Gmail',
            'priority': 'Critical'
        },
        {
            'email_id': 2,
            'sender': 'deals@amazon.com',
            'subject': '50% OFF Today Only - Don\'t Miss Out!',
            'body': 'Buy now and save 50% on all electronics. Free shipping on orders over 25 dollars. Click here now!',
            'time_of_day': 'evening',
            'recipient_count': 5000000,
            'source': 'E-Commerce - Gmail',
            'priority': 'Spam'
        },
        {
            'email_id': 3,
            'sender': 'alerts@github.com',
            'subject': 'Security: Critical Vulnerability Found',
            'body': 'A critical vulnerability has been found in your dependencies. Update to version 2.0.1 immediately.',
            'time_of_day': 'morning',
            'recipient_count': 1000,
            'source': 'Developer - Email',
            'priority': 'Critical'
        },
    ]
    
    df = pd.DataFrame(sample_emails)
    df.to_csv('real_world_emails.csv', index=False)
    
    print(f"\n✓ Added {len(sample_emails)} sample emails")
    print("Saved to: real_world_emails.csv")
    print("\nYou can now add more emails or proceed to preprocessing")


if __name__ == "__main__":
    import sys
    
    print("\n" + "="*70)
    print("EMAIL INPUT SYSTEM - CHOOSE AN OPTION")
    print("="*70)
    print("\n1. Interactive Mode - Add emails one by one")
    print("2. Quick Test - Add sample emails and start testing")
    print("3. Exit")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == '1':
        interface = EmailInputInterface()
        interface.run_interactive_mode()
    
    elif choice == '2':
        add_sample_emails_quickly()
        print("\n✓ Ready to proceed!")
        print("Run: python 1_data_preprocessing_realemails.py")
    
    else:
        print("Exiting...")

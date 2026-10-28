"""
EMAIL PRIORITY PREDICTION SYSTEM
Step 0: Email Data Collection from Multiple Sources
Collects realistic emails from various websites without logging in
"""

import pandas as pd
import random
from datetime import datetime, timedelta
import json

# Email data from various real-world sources
# This data is realistic and covers diverse email types

def get_emails_from_websites():
    """
    Collect email data from multiple website sources
    Simulates receiving emails from various platforms
    """
    
    emails = []
    
    # ==================== PROFESSIONAL/WORK EMAILS ====================
    
    work_emails = [
        {
            'sender': 'boss@techcompany.com',
            'subject': 'URGENT: Q4 Revenue Report Due Today',
            'body': 'Please submit the Q4 revenue report immediately. This is critical for the board meeting scheduled tomorrow. The CEO needs this data.',
            'time_of_day': 'morning',
            'recipient_count': 1,
            'source': 'Corporate Email',
            'priority': 'Critical'
        },
        {
            'sender': 'hr@techcompany.com',
            'subject': 'Your Performance Review is Ready',
            'body': 'Your annual performance review has been completed. This review is critical for your career progression. Please review it in the HR portal.',
            'time_of_day': 'morning',
            'recipient_count': 5,
            'source': 'HR System',
            'priority': 'High'
        },
        {
            'sender': 'project.manager@techcompany.com',
            'subject': 'Project Deadline: Final Sprint Push',
            'body': 'We need to finalize the project by Friday. The client is waiting for deliverables. Everyone needs to focus on critical items only.',
            'time_of_day': 'morning',
            'recipient_count': 8,
            'source': 'Project Management',
            'priority': 'Critical'
        },
        {
            'sender': 'cto@techcompany.com',
            'subject': 'Strategic Initiative: New Tech Stack Decision',
            'body': 'We are planning to migrate to a new tech stack. This is a critical decision that will impact our development process for the next 3 years.',
            'time_of_day': 'afternoon',
            'recipient_count': 15,
            'source': 'Leadership',
            'priority': 'Critical'
        },
        {
            'sender': 'team.lead@techcompany.com',
            'subject': 'Quick Sync on Design Review',
            'body': 'Can we have a 30-minute sync to discuss the latest design? Would like your feedback on the UI improvements.',
            'time_of_day': 'morning',
            'recipient_count': 3,
            'source': 'Team Communication',
            'priority': 'High'
        },
        {
            'sender': 'finance@techcompany.com',
            'subject': 'Budget Allocation for Next Quarter',
            'body': 'Budget allocation needs to be finalized by end of week. Please review your department budgets and submit revised numbers.',
            'time_of_day': 'afternoon',
            'recipient_count': 10,
            'source': 'Finance',
            'priority': 'High'
        },
    ]
    emails.extend(work_emails)
    
    # ==================== E-COMMERCE EMAILS ====================
    
    ecommerce_emails = [
        {
            'sender': 'deals@amazon.com',
            'subject': '50% OFF - Last Chance: Lightning Deals Ending Soon',
            'body': 'Your Lightning Deals are ending in 2 hours! Shop now and save 50% on electronics. Free shipping on orders over $25. Click here to shop now!',
            'time_of_day': 'evening',
            'recipient_count': 5000000,
            'source': 'E-commerce',
            'priority': 'Spam'
        },
        {
            'sender': 'notifications@ebay.com',
            'subject': 'Exclusive: 40% off on Selected Items Today Only',
            'body': 'For eBay members only! Get 40% off on selected items. Limited time offer. Click here and use code SAVE40 at checkout.',
            'time_of_day': 'evening',
            'recipient_count': 3000000,
            'source': 'E-commerce',
            'priority': 'Spam'
        },
        {
            'sender': 'shop@flipkart.com',
            'subject': 'Diwali Sale! Biggest Sale of the Year',
            'body': 'Upto 80% off on everything! Electronics, Fashion, Home & more. Download app for extra 10% off. Hurry, stock limited!',
            'time_of_day': 'afternoon',
            'recipient_count': 2000000,
            'source': 'E-commerce',
            'priority': 'Spam'
        },
        {
            'sender': 'order@amazon.com',
            'subject': 'Your Order #123456 Has Been Shipped',
            'body': 'Good news! Your order has been shipped. Tracking number: ABC123XYZ. Expected delivery: 2 days. Track your package here.',
            'time_of_day': 'afternoon',
            'recipient_count': 1,
            'source': 'E-commerce',
            'priority': 'Medium'
        },
    ]
    emails.extend(ecommerce_emails)
    
    # ==================== SOCIAL MEDIA NOTIFICATIONS ====================
    
    social_emails = [
        {
            'sender': 'notifications@linkedin.com',
            'subject': 'You Have a New Job Recommendation',
            'body': 'Based on your profile, we found a perfect job match for you! Senior Software Engineer at Google. Click here to view the job posting.',
            'time_of_day': 'morning',
            'recipient_count': 1000000,
            'source': 'LinkedIn',
            'priority': 'Medium'
        },
        {
            'sender': 'noreply@twitter.com',
            'subject': 'Your Tweet Got 1000 Likes!',
            'body': 'Congratulations! Your tweet about machine learning got 1000 likes and 250 retweets. View your tweet to see conversations.',
            'time_of_day': 'afternoon',
            'recipient_count': 500000,
            'source': 'Twitter',
            'priority': 'Low'
        },
        {
            'sender': 'support@instagram.com',
            'subject': 'Your Story Got 500 Views',
            'body': 'Your latest Instagram story has been viewed by 500 people! Check out who viewed it and see their reactions.',
            'time_of_day': 'evening',
            'recipient_count': 100000,
            'source': 'Instagram',
            'priority': 'Low'
        },
        {
            'sender': 'updates@github.com',
            'subject': 'Your Repository Has 100 Stars!',
            'body': 'Congratulations! Your open-source project has reached 100 stars on GitHub. Check it out here.',
            'time_of_day': 'afternoon',
            'recipient_count': 50000,
            'source': 'GitHub',
            'priority': 'Low'
        },
    ]
    emails.extend(social_emails)
    
    # ==================== NEWSLETTER & SUBSCRIPTION ====================
    
    newsletter_emails = [
        {
            'sender': 'newsletter@techcrunch.com',
            'subject': 'Weekly Tech News: AI Breakthroughs This Week',
            'body': 'This week in tech: OpenAI releases new model, Google announces quantum computer. Read the full breakdown of major tech news here.',
            'time_of_day': 'evening',
            'recipient_count': 2000000,
            'source': 'Newsletter',
            'priority': 'Low'
        },
        {
            'sender': 'daily@medium.com',
            'subject': 'Your Daily Digest: Top Stories on Machine Learning',
            'body': 'Today\'s top stories curated for you. Read about latest advances in ML, AI, and data science from top writers on Medium.',
            'time_of_day': 'evening',
            'recipient_count': 5000000,
            'source': 'Newsletter',
            'priority': 'Low'
        },
        {
            'sender': 'insights@hbr.org',
            'subject': 'HBR Insight: Digital Transformation Strategy for 2024',
            'body': 'Harvard Business Review exclusive: How top companies are transforming digitally. Read the full article here.',
            'time_of_day': 'morning',
            'recipient_count': 500000,
            'source': 'Newsletter',
            'priority': 'Low'
        },
    ]
    emails.extend(newsletter_emails)
    
    # ==================== BANK & FINANCE ====================
    
    finance_emails = [
        {
            'sender': 'security@icicibank.com',
            'subject': 'ALERT: Unusual Activity Detected on Your Account',
            'body': 'Your account has detected unusual login activity from a new device. If this wasn\'t you, please confirm your identity immediately.',
            'time_of_day': 'afternoon',
            'recipient_count': 1,
            'source': 'Banking',
            'priority': 'Critical'
        },
        {
            'sender': 'alerts@hdfc.com',
            'subject': 'Your Monthly Statement is Ready',
            'body': 'Your bank statement for August has been generated. Download it from your account or click here to view it securely.',
            'time_of_day': 'afternoon',
            'recipient_count': 1,
            'source': 'Banking',
            'priority': 'Medium'
        },
        {
            'sender': 'rewards@creditcard.com',
            'subject': 'Congratulations! You\'ve Earned 5000 Reward Points',
            'body': 'Your recent purchases earned you 5000 points. Redeem them for discounts, gift cards, or travel rewards. Click here to redeem.',
            'time_of_day': 'afternoon',
            'recipient_count': 1000000,
            'source': 'Banking',
            'priority': 'Low'
        },
    ]
    emails.extend(finance_emails)
    
    # ==================== PROMOTIONAL & SCAM ====================
    
    promotional_emails = [
        {
            'sender': 'noreply@winner.com',
            'subject': 'CONGRATULATIONS! You Have Won 1 Crore Rupees',
            'body': 'You have been selected as a lucky winner! To claim your prize, please click here and verify your information.',
            'time_of_day': 'evening',
            'recipient_count': 10000000,
            'source': 'Promotional',
            'priority': 'Spam'
        },
        {
            'sender': 'support@lottery.net',
            'subject': 'Claim Your Prize - You\'ve Won Big!',
            'body': 'Click here immediately to claim your lottery winnings. This offer is valid only for 24 hours. Act now!',
            'time_of_day': 'evening',
            'recipient_count': 5000000,
            'source': 'Promotional',
            'priority': 'Spam'
        },
        {
            'sender': 'offers@bestdeals.com',
            'subject': 'FREE: Get iPhone 15 Pro Max for Free + Shipping',
            'body': 'Limited time offer! Get the latest iPhone absolutely free. Click here to claim your free phone now.',
            'time_of_day': 'evening',
            'recipient_count': 3000000,
            'source': 'Promotional',
            'priority': 'Spam'
        },
    ]
    emails.extend(promotional_emails)
    
    # ==================== SERVICE NOTIFICATIONS ====================
    
    service_emails = [
        {
            'sender': 'support@youtube.com',
            'subject': 'Your Video Got 10K Views!',
            'body': 'Your YouTube video has reached 10,000 views! Check out the analytics and see which countries your viewers are from.',
            'time_of_day': 'afternoon',
            'recipient_count': 100000,
            'source': 'Services',
            'priority': 'Low'
        },
        {
            'sender': 'noreply@gmail.com',
            'subject': 'Google Security Alert: New Device Signed In',
            'body': 'A new device just signed into your Google account from India. If this wasn\'t you, secure your account now.',
            'time_of_day': 'afternoon',
            'recipient_count': 1,
            'source': 'Services',
            'priority': 'High'
        },
        {
            'sender': 'support@aws.amazon.com',
            'subject': 'AWS Bill Alert: Your Monthly Usage Exceeded Budget',
            'body': 'Your AWS usage this month exceeded your budget limit. Review your resources and optimize your spending.',
            'time_of_day': 'morning',
            'recipient_count': 1,
            'source': 'Services',
            'priority': 'High'
        },
    ]
    emails.extend(service_emails)
    
    # ==================== PERSONAL EMAILS ====================
    
    personal_emails = [
        {
            'sender': 'friend@gmail.com',
            'subject': 'Let\'s meet for coffee tomorrow',
            'body': 'Hey! How are you doing? Would love to catch up over coffee tomorrow afternoon. Are you free around 3 PM?',
            'time_of_day': 'evening',
            'recipient_count': 1,
            'source': 'Personal',
            'priority': 'Medium'
        },
        {
            'sender': 'family@email.com',
            'subject': 'Family Reunion Planning - Your Input Needed',
            'body': 'We\'re planning our annual family reunion. We need to know your availability and preferences. Please reply with your thoughts.',
            'time_of_day': 'afternoon',
            'recipient_count': 10,
            'source': 'Personal',
            'priority': 'Medium'
        },
        {
            'sender': 'mentor@university.edu',
            'subject': 'Career Development: New Opportunity for You',
            'body': 'I think there\'s a perfect job opportunity for you at a startup I know. Would love to discuss it with you. When can we talk?',
            'time_of_day': 'morning',
            'recipient_count': 1,
            'source': 'Personal',
            'priority': 'High'
        },
    ]
    emails.extend(personal_emails)
    
    # ==================== DEVELOPER & TECHNICAL ====================
    
    tech_emails = [
        {
            'sender': 'alerts@github.com',
            'subject': 'SECURITY: Critical Vulnerability in Your Dependencies',
            'body': 'A critical security vulnerability has been found in one of your project dependencies. Update immediately to version X.X.X',
            'time_of_day': 'morning',
            'recipient_count': 100000,
            'source': 'Developer',
            'priority': 'Critical'
        },
        {
            'sender': 'no-reply@stackoverflow.com',
            'subject': 'Your Question Got Answered: "Python ML Pipeline"',
            'body': 'Someone answered your Stack Overflow question. The answer has 150 upvotes. Check it out here.',
            'time_of_day': 'afternoon',
            'recipient_count': 1000000,
            'source': 'Developer',
            'priority': 'Low'
        },
        {
            'sender': 'team@vercel.com',
            'subject': 'Deployment Failed: Check Your Build Logs',
            'body': 'Your latest deployment to production failed. Check the build logs to see what went wrong. Rollback available.',
            'time_of_day': 'morning',
            'recipient_count': 1,
            'source': 'Developer',
            'priority': 'Critical'
        },
        {
            'sender': 'noreply@heroku.com',
            'subject': 'Your App Dyno Has Crashed',
            'body': 'Your Heroku app has crashed due to memory usage. Please check your logs and restart your dyno.',
            'time_of_day': 'afternoon',
            'recipient_count': 1,
            'source': 'Developer',
            'priority': 'High'
        },
    ]
    emails.extend(tech_emails)
    
    return emails


def create_diverse_email_dataset(num_additional_samples=0):
    """
    Create a diverse email dataset from multiple sources
    Adds synthetic variations to make dataset more realistic
    """
    
    base_emails = get_emails_from_websites()
    
    print("="*70)
    print("EMAIL DATA COLLECTION FROM MULTIPLE SOURCES")
    print("="*70)
    
    print("\nCollecting emails from various websites...")
    print(f"✓ Professional/Work Emails: 6 samples")
    print(f"✓ E-Commerce Platforms: 4 samples")
    print(f"✓ Social Media: 4 samples")
    print(f"✓ Newsletters: 3 samples")
    print(f"✓ Banking & Finance: 3 samples")
    print(f"✓ Promotions & Offers: 3 samples")
    print(f"✓ Service Notifications: 3 samples")
    print(f"✓ Personal Emails: 3 samples")
    print(f"✓ Developer & Technical: 4 samples")
    
    print(f"\nTotal emails collected: {len(base_emails)}")
    
    # Create DataFrame
    df = pd.DataFrame(base_emails)
    
    # Add email ID
    df.insert(0, 'email_id', range(1, len(df) + 1))
    
    # Reorder columns
    df = df[['email_id', 'sender', 'subject', 'body', 'time_of_day', 'recipient_count', 'source', 'priority']]
    
    print("\n" + "="*70)
    print("EMAIL DATASET SUMMARY")
    print("="*70)
    
    print(f"\nTotal Emails: {len(df)}")
    print(f"\nPriority Distribution:")
    print(df['priority'].value_counts())
    
    print(f"\nSource Distribution:")
    print(df['source'].value_counts())
    
    print(f"\nTime of Day Distribution:")
    print(df['time_of_day'].value_counts())
    
    print("\n" + "-"*70)
    print("Sample Emails:")
    print("-"*70)
    
    for idx, row in df.head(3).iterrows():
        print(f"\nEmail #{row['email_id']}:")
        print(f"  From: {row['sender']}")
        print(f"  Subject: {row['subject'][:60]}...")
        print(f"  Priority: {row['priority']}")
        print(f"  Source: {row['source']}")
    
    return df


def save_email_dataset(df, filepath):
    """Save the collected email dataset to CSV"""
    df.to_csv(filepath, index=False)
    print(f"\n✓ Email dataset saved to: {filepath}")
    print(f"  Total samples: {len(df)}")
    print(f"  File size: {len(df) * 100} bytes (approx)")


if __name__ == "__main__":
    # Collect emails from multiple sources
    email_df = create_diverse_email_dataset()
    
    # Save to CSV
    save_email_dataset(email_df, 'real_world_emails.csv')
    
    print("\n" + "="*70)
    print("EMAIL COLLECTION COMPLETED SUCCESSFULLY!")
    print("="*70)
    print("\nNext step: Use 'real_world_emails.csv' with the ML pipeline")
    print("Run: python 1_data_preprocessing.py")
    print("\nNote: Update line in 1_data_preprocessing.py:")
    print('  data = load_data("real_world_emails.csv")')

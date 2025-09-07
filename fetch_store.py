from fetch.yt_fetch import fetch_youtube_workflows
from fetch.forum_fetch import fetch_forum_workflows
from fetch.google_fetch import fetch_google_trends_workflows
from crud import create_workflows
from database import SessionLocal
from llm import helper

yt_popular_workflows = [
    "n8n ClickUp Task Automation",
    "n8n Zendesk Ticket Automation",
    "n8n Freshdesk Ticket Automation",
    "n8n WordPress Automation",
    "n8n Google Ads Reporting Automation",
    "n8n Facebook Ads Automation",
    "n8n Instagram Posting Automation",
    "n8n TikTok Posting Automation",
    "n8n YouTube Upload Automation",
    "n8n Google Analytics Reporting",
    "n8n BigQuery Data Automation",
    "n8n SQL Database Sync",
    "n8n AI Content Generation Workflow",
    "n8n Document OCR & Data Extraction",
    "n8n Invoice Processing Workflow",
    "n8n WhatsApp Automation",
    "n8n Email Automation",
    "n8n Google Sheets Sync",
    "n8n Slack Notifications",
    "n8n Airtable Integration",
    "n8n Webhook Listener",
    "n8n CRM Automation",
    "n8n Trello Card Automation",
    "n8n Jira Issue Automation",
    "n8n Twitter Posting",
    "n8n LinkedIn Posting",
    "n8n GitHub Workflow Automation",
    "n8n Notion Database Updates",
    "n8n RSS Feed Monitoring",
    "n8n PDF Data Extraction",
    "n8n E-commerce Order Workflow",
    "n8n n8n automation examples",
    "n8n Google Drive File Automation",
    "n8n Dropbox File Sync",
    "n8n OneDrive File Automation",
    "n8n Calendar Event Automation (Google Calendar / Outlook)",
    "n8n Zoom Meeting Automation",
    "n8n Microsoft Teams Notifications",
    "n8n Telegram Bot Automation",
    "n8n Discord Bot Automation",
    "n8n Shopify Order Automation",
    "n8n WooCommerce Order Processing",
    "n8n Stripe Payment Automation",
    "n8n PayPal Transaction Automation",
    "n8n Salesforce CRM Integration",
    "n8n HubSpot CRM Automation",
    "n8n Asana Task Automation",
    "n8n Monday.com Task Updates",
]

n8n_forum_queries = [
    "help-me-build-my-workflow",
    "built-with-n8n",
]

google_trends_queries = [
    "n8n Salesforce CRM Integration",
    "n8n HubSpot CRM Automation",
    "n8n Asana Task Automation",
    "n8n Monday.com Task Updates",
    "n8n ClickUp Task Automation",
    "n8n Zendesk Ticket Automation",
    "n8n Freshdesk Ticket Automation",
    "n8n WordPress Automation",
    "n8n Google Ads Reporting Automation",
    "n8n Facebook Ads Automation",
    "n8n Instagram Posting Automation",
    "n8n TikTok Posting Automation",
    "n8n YouTube Upload Automation",
    "n8n Google Analytics Reporting",
    "n8n BigQuery Data Automation",
    "n8n SQL Database Sync",
    "n8n AI Content Generation Workflow",
    "n8n Document OCR & Data Extraction",
    "n8n Invoice Processing Workflow",
    "n8n WhatsApp Automation",
    "n8n Email Automation",
    "n8n Google Sheets Sync",
    "n8n Slack Notifications",
    "n8n Airtable Integration",
    "n8n Webhook Listener",
    "n8n CRM Automation",
    "n8n Trello Card Automation",
    "n8n Jira Issue Automation",
    "n8n Twitter Posting",
    "n8n LinkedIn Posting",
    "n8n GitHub Workflow Automation",
    "n8n Notion Database Updates",
    "n8n RSS Feed Monitoring",
    "n8n PDF Data Extraction",
    "n8n E-commerce Order Workflow",
    "n8n Google Drive File Automation",
    "n8n Dropbox File Sync",
    "n8n OneDrive File Automation",
    "n8n Calendar Event Automation (Google Calendar / Outlook)",
    "n8n Zoom Meeting Automation",
    "n8n Microsoft Teams Notifications",
    "n8n Telegram Bot Automation",
    "n8n Discord Bot Automation",
    "n8n Shopify Order Automation",
    "n8n WooCommerce Order Processing",
    "n8n Stripe Payment Automation",
    "n8n PayPal Transaction Automation",
]


def run_fetch_and_store():
    db = SessionLocal()
    try:
        # Fetch YouTube
        # for wf in yt_popular_workflows:
        #     data = fetch_youtube_workflows(query=wf, country="US")
        #     youtube_data = helper(data)
        #     print("==YT==\n")
        #     print(youtube_data)
        #     print("==YT==\n")
        #     create_workflows(db, youtube_data)
            
        #     data = fetch_youtube_workflows(query=wf, country="IN")
        #     youtube_data = helper(data)
        #     print("==YT==\n")
        #     print(youtube_data)
        #     print("==YT==\n")
        #     create_workflows(db, youtube_data)
 
        # # Fetch Forum
        # for wf in n8n_forum_queries:
        #     data = fetch_forum_workflows(category=wf, country="US")
        #     forum_data = helper(data)
        #     print("==FORUM==\n")
        #     print(forum_data)
        #     print("==FORUM==\n")
        #     create_workflows(db, forum_data)

        # Fetch Google
        for i in range(0,len(google_trends_queries), 5):
            google_data = fetch_google_trends_workflows(keyword_list = google_trends_queries[i : i+5], country="US")
            print("==GOOGLE==\n")
            print(google_data)
            print("==GOOGLE==\n")
            create_workflows(db, google_data)
            
            google_data = fetch_google_trends_workflows(keyword_list = google_trends_queries[i : i+5], country="IN")
            print("==GOOGLE==\n")
            print(google_data)
            print("==GOOGLE==\n")
            create_workflows(db, google_data)

        db.commit()
        print(" Data fetched and stored successfully")

    except Exception as e:
        db.rollback()
        print(f" Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_fetch_and_store()

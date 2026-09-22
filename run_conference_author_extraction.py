import asyncio
import os
import sys
from sciencedirect_author_scraper import ScienceDirectAuthorScraper, export_to_excel, logger

TOPICS_TO_SCRAPE = [
    # Track 1: AI & ML
    {"track": "Track 1: AI & ML", "topic": "Deep Learning Architectures and Applications"},
    {"track": "Track 1: AI & ML", "topic": "Explainable Trustworthy and Responsible AI"},
    
    # Track 2: IoT & CPS
    {"track": "Track 2: IoT & CPS", "topic": "IoT Security Privacy and Device Authentication"},
    {"track": "Track 2: IoT & CPS", "topic": "Edge and Fog Computing for IoT"},
    
    # Track 3: Robotics & Automation
    {"track": "Track 3: Robotics & Automation", "topic": "Autonomous Mobile Robots and Navigation"},
    {"track": "Track 3: Robotics & Automation", "topic": "Human-Robot Interaction and Collaboration"},
    
    # Track 4: Data Analytics
    {"track": "Track 4: Data Analytics", "topic": "Big Data Architectures and Scalable Processing"},
    {"track": "Track 4: Data Analytics", "topic": "Time-Series Analysis and Forecasting"},
    
    # Track 5: Blockchain
    {"track": "Track 5: Blockchain", "topic": "Blockchain Architectures and Consensus Mechanisms"},
    {"track": "Track 5: Blockchain", "topic": "Smart Contracts and Decentralized Applications"},
    
    # Track 6: Cybersecurity
    {"track": "Track 6: Cybersecurity", "topic": "Network Security Intrusion Detection and Prevention"},
    {"track": "Track 6: Cybersecurity", "topic": "Malware Analysis and Cyber Threat Intelligence"},
    
    # Track 7: Vision & Cloud
    {"track": "Track 7: Vision & Cloud", "topic": "Object Detection Recognition and Tracking"},
    {"track": "Track 7: Vision & Cloud", "topic": "Medical Image Analysis Diagnostics and Segmentation"},
]

OUTPUT_FILE = "Conference_Tracks_Foreign_Authors.xlsx"

async def run_extraction():
    logger.info("=================================================================")
    logger.info("STARTING MULTI-TRACK FOREIGN AUTHOR EXTRACTION ON SCIENCEDIRECT")
    logger.info("=================================================================")
    logger.info(f"Targeting {len(TOPICS_TO_SCRAPE)} topics across all 7 Conference Tracks...")
    logger.info(f"Output File: {OUTPUT_FILE}")

    async with ScienceDirectAuthorScraper(
        headless=False,
        delay_min=0.8,
        delay_max=1.8
    ) as scraper:
        records = await scraper.execute_topics(
            topic_queue=TOPICS_TO_SCRAPE,
            max_pages=1,
            max_articles_per_topic=3,
            output_path=OUTPUT_FILE
        )
        
        logger.info(f"\n=================================================================")
        logger.info(f"EXTRACTION COMPLETE: {len(records)} foreign authors extracted.")
        logger.info(f"Saved to: {OUTPUT_FILE}")
        logger.info("=================================================================")

if __name__ == '__main__':
    asyncio.run(run_extraction())

# Placement Tracker

A personal AI-powered placement tracking system that automatically monitors placement opportunities from Telegram and stores them in Notion.

---

## Flow

Telegram Placement Group

↓

Keyword Filtering

↓

AI Extraction (Gemini → DeepSeek → Qwen → Regex Fallback)

↓

Duplicate Detection

↓

Notion Database

---

## Idea & Implementation

College placement groups often contain a mix of internships, full-time opportunities, OA updates, interview schedules, results, webinars, hackathons, and other announcements.

The goal of this project is to automatically identify genuine placement opportunities, extract useful information, and maintain a centralized tracker without requiring manual data entry.

The system:

* Monitors a Telegram placement group in real time using Telethon.
* Filters irrelevant messages using custom rules.
* Extracts structured placement details using AI.
* Prevents duplicate entries.
* Stores opportunities in a Notion database for easy tracking and management.
* Supports both historical backfill and live monitoring.

### Tech Stack

* Python
* Telethon
* Gemini API
* OpenRouter API
* Notion API

---

## Output

### Notion Database

<img width="1522" height="632" alt="image" src="https://github.com/user-attachments/assets/91b158b1-2f1d-432d-be68-d8ecb2a9bb90" />


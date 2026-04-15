# 🛡️ GitHub Cyber Intelligence Finder

> Advanced OSINT tool for discovering cybersecurity professionals from GitHub follower networks using automated crawling and intelligence scoring.

---

## 🚀 Overview

GitHub Cyber Intelligence Finder is a Python-based OSINT (Open Source Intelligence) framework designed to analyze GitHub follower networks and identify cybersecurity-related professionals.

It scans public profiles, extracts meaningful data, and applies a weighted intelligence model to detect individuals working in:

- 🔐 Penetration Testing
- 🕵️ Bug Bounty Hunting
- 🧠 Reverse Engineering
- 🛡️ Threat Intelligence
- 🧨 Exploit Development
- ☁️ Cloud & Application Security

---

## ⚙️ Features

✔ Automated GitHub follower scraping  
✔ Multi-page crawling support  
✔ Profile bio + repository analysis  
✔ Weighted cybersecurity scoring system  
✔ Keyword intelligence engine  
✔ Profile ranking system  
✔ JSON structured output  
✔ Lightweight & fast execution  

---

## 🧠 Intelligence Engine

The tool uses a weighted detection system:

### 🔴 Strong Signals (High Confidence)
- Penetration tester
- Bug bounty hunter
- Red teamer
- Exploit developer
- Security researcher

### 🟡 Medium Signals
- CTF player
- OWASP contributor
- SQL injection
- XSS / CSRF
- Reverse engineering

### 🟢 Weak Signals
- Cybersecurity
- Security
- Hacking
- Exploit

---

## 📊 Scoring System

Each GitHub profile is analyzed and assigned a score:


Strong keyword = +5 to +6 points
Medium keyword = +3 to +4 points
Weak keyword = +1 to +2 points


Profiles exceeding threshold are classified as:

> ✅ Cybersecurity Relevant Profile

---

## 🧬 Workflow


Input Username
↓
Fetch Followers
↓
Extract Profile Data
↓
Analyze Bio + Repos
↓
Apply Scoring Engine
↓
Generate Intelligence Report


🛠️ Installation
  $ git clone https://github.com/ifyouknowyou/GitIntel.git
  $ cd GitIntel
  $ pip install -r requirements.txt

▶️ Usage
$ python3 github_cyber_finder.py

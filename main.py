import time
import json
import re
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

OUTPUT_FILE = "results.json"

MAX_PAGES = 10
MAX_PROFILES = 150
DELAY = 1.2


KEYWORDS = {
    "strong": {
        "penetration tester": 6,
        "pentester": 6,
        "security researcher": 6,
        "bug bounty": 6,
        "red team": 6,
        "exploit developer": 6,
        "vulnerability researcher": 6,
        "offensive security": 6,
        "appsec engineer": 5,
        "security engineer": 5,
        "threat intelligence": 5,
        "osint": 5,
        "reverse engineer": 5,
        "malware analyst": 5,
        "devsecops": 5,
        "cve": 5
    },

    "medium": {
        "ctf": 4,
        "owasp": 4,
        "xss": 4,
        "sql injection": 4,
        "csrf": 4,
        "rce": 4,
        "privilege escalation": 4,
        "reverse engineering": 4,
        "malware": 3,
        "phishing": 3,
        "ddos": 3,
        "zero day": 4,
        "backdoor": 3,
        "botnet": 3
    },

    "weak": {
        "security": 1,
        "cybersecurity": 1,
        "network security": 1,
        "exploit": 2,
        "hacking": 2,
        "shellcode": 2,
        "reverse shell": 2,
        "lateral movement": 2,
        "persistence": 2
    }
}


def log(msg):
    print(f"[+] {msg}")



def get_html(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        return r.text
    except Exception as e:
        log(f"Error fetching {url}: {e}")
        return ""


def extract_followers(username):
    profiles = set()

    log("Extracting followers...")

    for page in range(1, MAX_PAGES + 1):

        url = f"https://github.com/{username}?tab=followers&page={page}"
        log(f"Loading: {url}")

        html = get_html(url)
        soup = BeautifulSoup(html, "html.parser")

        page_count = 0

        for a in soup.select("a[href]"):
            href = a.get("href")

            if not href:
                continue

            # only user profiles
            if re.match(r"^/[a-zA-Z0-9-]+$", href):

                # block junk pages
                if any(x in href for x in [
                    "/features", "/topics", "/marketplace",
                    "/explore", "/pricing"
                ]):
                    continue

                profiles.add("https://github.com" + href)
                page_count += 1

        if page_count == 0:
            break

        time.sleep(DELAY)

        if len(profiles) >= MAX_PROFILES:
            break

    return list(profiles)


def get_profile(url):
    log(f"Scanning profile: {url}")

    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")

    bio_tag = soup.select_one("div.p-note")
    bio = bio_tag.get_text(strip=True).lower() if bio_tag else ""

    name_tag = soup.select_one("span.p-name")
    name = name_tag.get_text(strip=True) if name_tag else ""

    repos = []
    for r in soup.select("a[itemprop='name codeRepository']"):
        repos.append(r.get_text(strip=True).lower())

    return {
        "url": url,
        "name": name,
        "bio": bio,
        "repos": repos
    }

# =========================
# SCORE ENGINE (FIXED - SINGLE SYSTEM)
# =========================

def score_text(text):
    text = text.lower()
    score = 0
    matched = []

    for level in KEYWORDS:
        for keyword, weight in KEYWORDS[level].items():
            if keyword in text:
                score += weight
                matched.append(keyword)

    return score, matched

# =========================
# BOOST SYSTEM
# =========================

def apply_boost(text, score):
    text = text.lower()

    if "cert" in text or "oscp" in text:
        score += 2

    if "hackthebox" in text or "tryhackme" in text:
        score += 2

    if "github" in text:
        score += 1

    return score

# =========================
# MAIN SCANNER
# =========================

def scan(username):
    log("Starting scan...")

    followers = extract_followers(username)

    log(f"Total profiles found: {len(followers)}")

    results = []

    for i, profile in enumerate(followers):

        if i >= MAX_PROFILES:
            break

        data = get_profile(profile)

        combined = data["bio"] + " " + " ".join(data["repos"])

        score, matched = score_text(combined)
        score = apply_boost(combined, score)

        if score >= 6:
            results.append({
                "profile": profile,
                "name": data["name"],
                "score": score,
                "bio": data["bio"],
                "repos": data["repos"],
                "matched_keywords": matched
            })

            log(f"✔ Cyber profile: {profile} (score {score})")

        time.sleep(DELAY)

    return results



if __name__ == "__main__":
    user = input("Enter GitHub username: ").strip()

    results = scan(user)

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=4)

    log(f"Saved to {OUTPUT_FILE}")

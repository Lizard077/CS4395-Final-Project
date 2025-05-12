import json
import re

def clean_review(text):
    
    
    text = re.sub(r'\\u[0-9a-fA-F]{4}|\\', '', text)
    
    text = re.sub(r'[‘’]', "'", text)
    text = re.sub(r'[“”]', '"', text)

    text = text.lower()

    text = re.sub(r'<[^>]+>', '', text)

    text = re.sub(r'full\s+spoiler[-\s]?free\s+review\s*(at|@|of)?\s*["“][^"”]*["”]\s*','', text, flags=re.IGNORECASE)

    text = re.sub(r"http\S+|www\S+", "", text)

    text = re.sub(r'[^a-z0-9\s.,!?:\'"-]', ' ', text) # remove special characters
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)

    return text

def extract_rating(text):
    match = re.search(r'rating:\s*([a-fA-F][+-]?)', text, flags=re.IGNORECASE)
    if not match:
        return None
    letter = match.group(1).upper()

    if letter.startswith('A'):
        return 4
    elif letter.startswith('B'):
        return 3
    elif letter.startswith('C'):
        return 2
    elif letter.startswith('D'):
        return 1
    else:
        return 0

def preprocess_data(raw_data):
    cleaned_data = []

    for movie in raw_data:
        title = movie.get("title", "").strip()
        reviews = movie.get("reviews", [])

        cleaned_reviews = []
        for review in reviews:
            cleaned = clean_review(review)
            if cleaned:
                rating = extract_rating(cleaned)
                cleaned = re.sub(r'[^\w\s]', '', cleaned)
                cleaned_reviews.append({"text": cleaned, "rating": rating})

        if cleaned_reviews:
            cleaned_data.append({"title": title, "reviews": cleaned_reviews})
    return cleaned_data

with open("movies_with_reviews.json", "r", encoding="utf-8") as infile:
    raw_data = json.load(infile)

cleaned_data = preprocess_data(raw_data)

with open("cleaned_movies_with_reviews.json", "w", encoding="utf-8") as outfile:
    json.dump(cleaned_data, outfile, indent=2, ensure_ascii=False)
    

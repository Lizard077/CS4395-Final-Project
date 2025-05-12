import json
import re
from sklearn.model_selection import train_test_split

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
                cleaned = re.sub(r'rating:\s*[a-fA-F][+-]?', '', cleaned, flags=re.IGNORECASE)
                cleaned = re.sub(r'[^\w\s]', '', cleaned)
                cleaned_reviews.append({"text": cleaned, "rating": rating})

        if cleaned_reviews:
            cleaned_data.append({"title": title, "reviews": cleaned_reviews})
    return cleaned_data

def extract_rated_reviews(raw_data):
    rated_reviews = []

    for movie in raw_data:
        reviews = movie.get("reviews", [])
        for review in reviews:
            cleaned = clean_review(review)
            rating = extract_rating(cleaned)
            if rating is not None:
                cleaned = re.sub(r'rating:\s*[a-fA-F][+-]?', '', cleaned, flags=re.IGNORECASE)
                cleaned  = re.sub(r'[^\w\s]', '', cleaned)
                rated_reviews.append({"text": cleaned, "rating": rating})
    return rated_reviews

def split_data(rated_data):
    train_data, test_data = train_test_split(rated_data, test_size=.2, random_state=42)
    return train_data, test_data

with open("movies_with_reviews.json", "r", encoding="utf-8") as infile:
    raw_data = json.load(infile)

cleaned_data = preprocess_data(raw_data)

with open("cleaned_movies_with_reviews.json", "w", encoding="utf-8") as outfile:
    json.dump(cleaned_data, outfile, indent=2, ensure_ascii=False)

rated_reviews = extract_rated_reviews(raw_data)

with open("cleaned_rated_movies_with_reviews.json", "w", encoding="utf-8") as outfile:
    json.dump(rated_reviews, outfile, indent=2, ensure_ascii=False)

train_data, test_data = split_data(rated_reviews)
with open("train.json", "w", encoding="utf-8") as train_file:
    json.dump(train_data, train_file, indent=2, ensure_ascii=False)

with open("test.json", "w", encoding="utf-8") as test_file:
    json.dump(test_data, test_file, indent=2, ensure_ascii=False)
    

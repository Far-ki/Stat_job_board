import pandas as pd
import json
import spacy
from rapidfuzz import fuzz

nlp = spacy.load('pl_core_news_sm')

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

data = pd.read_csv('oferty_pracy.csv')

filters = config['filters']

if 'city' in filters and filters['city']:
    if isinstance(filters['city'], list):
        data = data[data['city'].isin(filters['city'])]
    else:
        data = data[data['city'] == filters['city']]

if 'experience' in filters and filters['experience']:
    if isinstance(filters['experience'], list):
        data = data[data['experience'].isin(filters['experience'])]
    else:
        data = data[data['experience'] == filters['experience']]

if 'type_of_work' in filters and filters['type_of_work']:
    if isinstance(filters['type_of_work'], list):
        data = data[data['type_of_work'].isin(filters['type_of_work'])]
    else:
        data = data[data['type_of_work'] == filters['type_of_work']]

if 'employment_type' in filters and filters['employment_type']:
    if isinstance(filters['employment_type'], list):
        data = data[data['employment_type'].isin(filters['employment_type'])]
    else:
        data = data[data['employment_type'] == filters['employment_type']]

if 'keywords' in filters and filters['keywords']:
    keywords = filters['keywords']


    lemmatized_keywords = {}
    for keyword, priority in keywords.items():
        doc = nlp(keyword.lower())
        lemmatized_keyword = ' '.join([token.lemma_ for token in doc])
        lemmatized_keywords[lemmatized_keyword] = priority

    def lemmatize_description(text):
        doc = nlp(str(text).lower())
        return ' '.join([token.lemma_ for token in doc])

    data['lemmatized_description'] = data['description'].apply(lemmatize_description)

    def fuzzy_match_with_priority(description):
        max_score = 0
        for keyword, priority in lemmatized_keywords.items():
            score = fuzz.partial_ratio(keyword, description) * (priority / 100)
            if score > max_score:
                max_score = score
        return max_score >= 80  

    data = data[data['lemmatized_description'].apply(fuzzy_match_with_priority)]

data.to_csv('oferty_filtered.csv', index=False, encoding='utf-8')
print("Zapisano przefiltrowane dane do pliku 'oferty_filtered.csv'.")

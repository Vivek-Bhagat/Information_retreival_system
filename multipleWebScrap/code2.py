# %%
import requests
from bs4 import BeautifulSoup
import csv

def scrape_page(page_number):
    url = f'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={page_number}'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []

    for article in soup.find_all('article', class_='c-card'):
        title_main = article.find('span', class_='c-meta__type')
        title_m = title_main.get_text(strip=True) if title_main else 'N/A'


        title_tag = article.find('h3', class_='c-card__title')
        title = title_tag.get_text(strip=True) if title_tag else 'N/A'
        
        summary_tag = article.find('div', class_='c-card__summary')
        summary = summary_tag.get_text(strip=True) if summary_tag else 'N/A'
        
        author_tag = article.find('ul', class_='c-author-list')
        authors = [author.get_text(strip=True) for author in author_tag.find_all('span', itemprop='name')] if author_tag else 'N/A'
        author = ', '.join(authors)
        
        date_tag = article.find('time', itemprop='datePublished')
        date = date_tag.get_text(strip=True) if date_tag else 'N/A'
        
        

        articles.append([title_m,title, summary, author, date])

    return articles

def main(start_page, end_page):
    all_articles = []

    for page_number in range(start_page, end_page + 1):
        print(f"Scraping page {page_number}...")
        articles = scrape_page(page_number)
        all_articles.extend(articles)

    
    with open('nature_articless.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Type','Title', 'Summary', 'Author', 'Publication Date'])
        writer.writerows(all_articles)

    print("Data has been written to nature_articles.csv")

if __name__ == "__main__":
   
    start_page = 1
    end_page = 50 
    main(start_page, end_page)


# %%
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import re
import contractions

# Load the dataset
df = pd.read_csv('nature_articless.csv')

# Normalize the text
def normalize_text(text):
    text = contractions.fix(text)
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

df['normalized_text'] = df['Title'].apply(normalize_text)

# Tokenization
df['tokens'] = df['normalized_text'].apply(word_tokenize)

# Stop-Word Removal
stop_words = set(stopwords.words('english'))
df['filtered_tokens'] = df['tokens'].apply(lambda x: [word for word in x if word not in stop_words])

# Stemming or Lemmatization
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

df['stemmed_words'] = df['filtered_tokens'].apply(lambda x: [stemmer.stem(word) for word in x])
df['lemmatized_words'] = df['filtered_tokens'].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])

# Save the processed DataFrame to a new CSV file
df.to_csv('processed_datasets.csv', index=False)

# %%




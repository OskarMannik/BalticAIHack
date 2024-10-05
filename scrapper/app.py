import requests
from bs4 import BeautifulSoup
import re
from flask import Flask, request, jsonify

PORT = 5000


app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape_titles():
    
    url = request.args.get('url', default='https://www.piletilevi.ee/eng/tickets/koik/', type=str)

    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        concert_list = soup.find('div', class_='concertslist_page events events_count_3')

        results = []
        for idx, event in enumerate(concert_list, start=0):
            article_link = event['href']
                        
            article_page = requests.get(article_link)
            article_page.raise_for_status()
            article_page_soup = BeautifulSoup(article_page.text, 'html.parser')

            article_title = article_page_soup.find('h1').get_text(strip=True)

            article_description = article_page_soup.find('div', class_='concert_details_description_description_inner')
            if article_description:

                article_description_text = article_description.get_text(strip=True)

                sentences = re.split(r'(?<=[.!?])\s+', article_description_text)

                clean_sentences = [
                        sentence for sentence in sentences 
                        if not re.search(r'(http[s]?://\S+|www\.\S+)', sentence)
                    ]
                clean_description = ' '.join(clean_sentences)

            results.append({
                'title': article_title,
                'description': clean_description,
                'link': article_link
            })

        return jsonify(results)
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
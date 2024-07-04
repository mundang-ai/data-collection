from webscraper import BibleWebscraper
import pandas as pd

class BibleDataExtractor:
    def __init__(self):
        self.muar_base_url = 'https://www.bible.com/bible/863/'
        self.en_base_url = 'https://www.bible.com/bible/1713/'
        self.fr_base_url = 'https://www.bible.com/bible/504/'

        self.muar_bible = BibleWebscraper(self.muar_base_url, 'MUAR')
        self.en_bible = BibleWebscraper(self.en_base_url, 'AMP')
        self.fr_bible = BibleWebscraper(self.fr_base_url, 'BCC1923')

    def extract_data(self):
        self.muar_bible.process(label='Mundang')
        self.en_bible.process(label='English')
        self.fr_bible.process(label= 'French')
        # self.muar_bible.process()
        # self.en_bible.process()
        # self.fr_bible.process()

        data = pd.merge(self.muar_bible.bible, self.fr_bible.bible, on=['book', 'chapter', 'verse'], how='outer')
        data = pd.merge(data, self.en_bible.bible, on=['book', 'chapter', 'verse'], how='outer')

        data.to_csv('../data/bible.csv', index=False)

if __name__ == "__main__":
    extractor = BibleDataExtractor()
    extractor.extract_data()
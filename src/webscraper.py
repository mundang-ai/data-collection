from bs4 import BeautifulSoup
import requests
import numpy as np

import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re

class webscraper():
  def __init__(self, url):
    self.url = url
    self.html_content = requests.get(url).text
    self.soup = BeautifulSoup(self.html_content, 'lxml')

  def remove_element(self, soup, tag, class_):
    element = soup.find(tag, class_=class_)
    if element is not None:
      element.extract()
    return soup

  def get_numbers_at_beginning(self, text):
    match = re.match(r'^\d+', text)
    if match:
      numbers_str = match.group()
      return int(numbers_str)
    else:
      return None

  def get_titles(self):
    titles_html = self.soup.find_all('span', class_='ChapterContent_heading__xBDcs')
    titles_text = [title.get_text() for title in titles_html if title.get_text().strip()]
    return titles_text

  def get_verses(self):
    verses_numbers_html = self.soup.find_all('span', class_='ChapterContent_label__R2PLt')
    verses_numbers = [verse.get_text() for verse in verses_numbers_html]
    return verses_numbers

  def get_verses_text(self, book:str, chapter:int, verse:int):
    # verses = [self.get_numbers_at_beginning(element) for element in verse.split('-')]
    verses = verse.split('-')
    pattern = f'{book}.{chapter}.{verses[0]}'
    # verses.pop(0)

    for item in range(int(verses[0])+1, int(verses[-1])+1):
      pattern += f'+{book}.{chapter}.{item}'
    verses_text_html = self.soup.find_all(name='span', attrs={'data-usfm': pattern}, recursive=True)
    verses_text_html = [self.remove_element(element, 'span', class_='ChapterContent_note__YlDW0') for element in verses_text_html]
    if len(verses_text_html) == 0:
      return ''
    else:
      verses_text = verses_text_html[0].get_text()
      return verses_text

class BibleWebscraper():
  def __init__(self,
               base_url:str,
               bible_code:str,
               bible_corpus:dict={
                                    'GEN': 50,  'EXO': 40,  'LEV': 27,    'NUM': 36,    'DEU': 34,    'JOS': 24,    'JDG': 21,
                                    'RUT': 4,   '1SA': 31,  '2SA': 24,    '1KI': 22,    '2KI': 25,    '1CH': 29,    '2CH': 36,
                                    'EZR': 10,  'NEH': 13,  'EST': 10,    'JOB': 42,    'PSA': 150,   'PRO': 31,    'ECC': 12,
                                    'SNG': 8,   'ISA': 66,  'JER': 52,    'LAM': 5,     'EZK': 48,    'DAN': 12,    'HOS': 14,
                                    'JOL': 3,   'AMO': 9,   'OBA': 1,     'JON': 4,     'MIC': 7,      'NAM': 3,    'HAB': 3,
                                    'ZEP': 3,   'HAG': 2,   'ZEC': 14,    'MAL': 4,     'MATEUS': 28,  'MRK': 16,   'LUK': 24,
                                    'JHN': 21,  'ACT': 28,  'ROM': 16,    '1CO': 16,    '2CO': 13,     'GAL': 6,    'EPH': 6,
                                    'PHP': 4,   'COL': 4,   '1TH': 5,     '2TH': 3,     '1TI': 6,      '1TI': 4,    'TIT': 3,
                                    'PHM': 1,   'HEB': 13,  'JAS': 5,     '1PE': 5,     '2PE': 3,      '1JN': 5,    '2JN': 1,
                                    '3JN': 1,   'JUD': 1,   'REV': 22
                                }
               ):
    self.base_url = base_url
    self.bible_code = bible_code
    self.bible_corpus = bible_corpus
    self.bible = []
    
  def _has_redirection(self,url):
    try:
      response = requests.head(url, allow_redirects=True)
      return response.history
    except requests.exceptions.RequestException:
      return []

  def _process_chapter(self, book:str, chapter:int, url:str):
    page = webscraper(url)
    titles_text = page.get_titles()
    verses_numbers = page.get_verses()
    verses_numbers_clean = [item for item in verses_numbers if item != '#']
    verses_text = [page.get_verses_text(book, chapter, verse) for verse in verses_numbers_clean]
    unique_verses_text = []
    for verse in verses_text:
      if verse not in unique_verses_text:
        unique_verses_text.append(verse)
    verses_text = unique_verses_text

    verses_text_cleaned = []
    for verse in verses_text:
      index = None
      try:
        index = verse.index('#')
        verses_text_cleaned.append(verse[:index])
      except ValueError:
        pass
      try:
        num = int(verse[0])
        verses_text_cleaned.append(verse[:index])
      except ValueError:
        if len(verses_text_cleaned)>0:
          verses_text_cleaned[-1] = verses_text_cleaned[-1] + verse[:index]

    if len(verses_text) != len(verses_numbers_clean):
      print(f'len(verses_text_cleaned)= {len(verses_text_cleaned)}, len(verses_numbers_clean)= {len(verses_numbers_clean)}')


    book_column = [book]*len(verses_numbers)
    chapter_column = [chapter]*len(verses_numbers)

    return list(zip(book_column, chapter_column, verses_numbers_clean, verses_text))

  def _process_book(self, book:str):
    for chapter in tqdm(range(1, self.bible_corpus[book]+1), desc=book, leave=False):
      url = self.base_url + book + '.' + str(chapter) + '.' + self.bible_code
      if self._has_redirection(url):
        print(' The link: '+ url+' has redirection')
        continue
      self.bible.extend(self._process_chapter(book, chapter, url))

  def process(self, label=''):
    for book in tqdm(self.bible_corpus.keys(), desc=f'{label} Bible'):
      self._process_book(book)
    self.bible = pd.DataFrame(self.bible, columns=['book', 'chapter', 'verse', 'text-'+self.bible_code])
    
#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from dataclasses import dataclass
import requests
import re
from bs4 import BeautifulSoup

@dataclass 
class Repository:
    # Common base data class for Repository
    url: str
    name: str
    about: str
    def print(self):
        print("URL   : ", self.url)
        print("Name  : ", self.name)
        print("About : ", self.about)
        
class GitHubCrawler:
    GITHUB_HOME = 'https://github.com'
    
    def __init__(self, username):
        self.username = username
        
    def getPage(self, url):
        try:
            req = requests.get(url, allow_redirects=True)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')
    
    def parse(self):
        """
        Extract repository information
        """
        repositories = []
        url = f'{self.GITHUB_HOME}/{self.username}?tab=repositories'
        soup = self.getPage(url)
        
        if not soup:
            return repositories
            
        # Find all repository items
        repo_list = soup.find('div', id='user-repositories-list')
        if not repo_list:
            return repositories
            
        items = repo_list.find_all('li', itemprop='owns')
        for item in items:
            # TODO: Extract specific details
            pass
        
        return repositories
        
crawler = GitHubCrawler('trungvdhp')
repositories = crawler.parse()
print("="*80)
print("List of repositories:")
for repo in repositories:
    print('-' * 80)
    repo.print()


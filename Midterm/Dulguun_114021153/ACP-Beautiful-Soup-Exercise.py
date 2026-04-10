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
    language: str = "Unknown"
    
    def print(self):
        print("URL      : ", self.url)
        print("Name     : ", self.name)
        print("About    : ", self.about)
        print("Language : ", self.language)
        
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
            # Extract name and URL
            name_tag = item.find('a', itemprop='name codeRepository')
            if name_tag:
                repo_name = name_tag.get_text(strip=True)
                repo_link = self.GITHUB_HOME + name_tag['href']
                
                # Extract "About" (description)
                desc_tag = item.find('p', itemprop='description')
                repo_about = desc_tag.get_text(strip=True) if desc_tag else ""
                
                # Extract Language
                lang_tag = item.find('span', itemprop='programmingLanguage')
                repo_lang = lang_tag.get_text(strip=True) if lang_tag else "N/A"
                
                repositories.append(Repository(
                    url=repo_link, 
                    name=repo_name, 
                    about=repo_about, 
                    language=repo_lang
                ))
        
        return repositories
        
crawler = GitHubCrawler('trungvdhp')
repositories = crawler.parse()
print("="*80)
print("List of repositories:")
for repo in repositories:
    print('-' * 80)
    repo.print()


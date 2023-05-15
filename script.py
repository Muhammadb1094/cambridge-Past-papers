import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from pathlib import Path
import os


def open_browser(url, base_folder):
    total = 0
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    paper_list = soup.find("ul", {"id": "paperslist"})
    all_links = paper_list.find_all('a')

    subject_links = []
    for link in all_links:
        subject_links.append(link['href'])

    for subject in subject_links:
        subject_link = url + subject + "/"

        res = requests.get(subject_link)
        soup = BeautifulSoup(res.text, "html.parser")
        pdfs_link = soup.select("a[href$='.pdf']")

        # Check if any pdf's are available then extract them... else go no next page.
        if pdfs_link:
            address = base_folder + subject
            for link in pdfs_link:
                if not os.path.exists(address):
                    os.makedirs(address)
                filename = os.path.join(address, link['href'])

                with open(filename, 'wb') as f:
                    file = requests.get(
                        urljoin(subject_link, link['href'])).content
                    f.write(file)
                # print("Downloading PDF => ", address)
                total = total+1
                print(total)
        else:
            years_list = soup.find("ul", {"id": "paperslist"})
            if years_list:
                all_years = years_list.find_all('a')

                for year in all_years:
                    year_pdf_link = subject_link + year['href']
                    res = requests.get(year_pdf_link)
                    soup = BeautifulSoup(res.text, "html.parser")
                    pdfs_link = soup.select("a[href$='.pdf']")
                    # Check if any pdf's are available then extract them... else go no next page.
                    if pdfs_link:
                        address = base_folder + subject + "/" + year['href']
                        for link in pdfs_link:
                            if not os.path.exists(address):
                                os.makedirs(address)
                            filename = os.path.join(address, link['href'])

                            with open(filename, 'wb') as f:
                                pdf = subject_link + \
                                    year['href'] + "/" + link['href']
                                file = requests.get(pdf).content
                                f.write(file)
                            # print("Downloading PDF => ", address)
                            total = total+1
                            print(total)


open_browser(url="https://papers.gceguide.com/A%20Levels/",
             base_folder='Cambridge International AS/A Levels/')

# open_browser(url="https://papers.gceguide.com/O%20Levels/")
# open_browser(url="https://papers.gceguide.com/Cambridge%20IGCSE/")

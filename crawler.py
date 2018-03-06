from bs4 import BeautifulSoup as bs
from selenium import webdriver
from pyvirtualdisplay import Display
import os
import time

base = "https://cs.illinois.edu"
directory = "htmls"
text_max_dist = 10

def extract_soup(link):
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(10)

    try:
        driver.get(link)
        html = driver.page_source

        display.stop()
        driver.quit()

        soup = bs(html, "html5lib")

        return soup
    except:
        return None

def extract_links(soup):
    links = []
    for a in soup.find_all("a", href=True):
        link = a['href']
        if link[0] == "/":
            link = base + link
        links.append(link)
    return links

def get_surr_text(tag):
    curr = tag.parent
    dist = 0
    text = []

    text_tags = {"h1", "h2", "h3", "h4", "h5", "p", "span"}

    while len(curr.text.strip()) == 0:
        if curr.parent:
            curr = curr.parent

    for line in curr.text.split("\n"):
        if len(line.split()) > 0:
            text.append(line.strip())
    return text


def crawl(start_link, depth, visited):
    if depth == 0 or start_link in visited:
        return

    print "sleeping"
    time.sleep(2)
    print "awake"
    visited.add(start_link)
    print start_link

    if not os.path.exists(directory):
        os.makedirs(directory)


    soup = extract_soup(start_link)
    if not soup:
        return
    links = extract_links(soup)

    new_filename = "{0}/{1}".format(directory, start_link.replace("/", "*"))
    if not os.path.exists(new_filename):
        file = open(new_filename, "w")
        file.write(str(soup))
        file.close()

        if start_link.find(base) > -1:
            for link in links:
                crawl(link, depth-1, visited)

if __name__ == "__main__":
    # crawl(base, 2, set())

    soup = extract_soup(base)

    for img in soup.find_all("img"):
        print get_surr_text(img)

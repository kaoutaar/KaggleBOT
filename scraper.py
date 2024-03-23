
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from kaggle.api.kaggle_api_extended import KaggleApi
import os
from lxml import html


"""
we use two techniques to get data from a competition webpage:
-API (when possible)
-scraping (when the data we want is not provided via the API);

This script take few minutes to complete executing, and stores data in folders in the current directory.
"""



api = KaggleApi()
api.authenticate()

options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
options.add_argument('--headless=new')
# # options.add_argument('--disable-gpu') 
driver = webdriver.Chrome(options=options)



####################################Scraping###################################
def get_overview_sec(comp):
    url = comp+"/overview"
    driver.get(url)
    wait = WebDriverWait(driver,60)
    wait.until(EC.presence_of_element_located((By.ID, "description")))
    ov_source = driver.page_source
    soup = BeautifulSoup(ov_source, "html.parser")
    ids = ["abstract", "description", "evaluation", "timeline", "prizes", "code-requirements","efficiency-prize-evaluation"]
    txt=""
    for id in ids:
        seg = soup.find("div", id=id)
        if seg is  None:
            continue
        seg = seg.get_text(" ")
        txt = txt+"\n\n\n"+seg
    return txt


def get_data_sec(comp):
    url = comp+"/data"
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    xpath = '//*[@data-testid="competition-detail-render-tid"]/div/div[6]/div[1]/div[1]/div/div[2]/div/div[1]/div/div/div'
    wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    dt_source = driver.page_source
    tree = html.fromstring(dt_source)
    elmts = tree.xpath(xpath)
    txt = elmts[0].text_content()
    return txt



def get_one_discussion():
    # show hidden replies
    ll = '//*[@id="site-content"]//button[span[contains(text(), "more replies")]]'
    try:
        list_more_replies_buttons = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, ll)))
    except:
        list_more_replies_buttons = []

    if len(list_more_replies_buttons)>=1:
        for button in list_more_replies_buttons:
            driver.execute_script("arguments[0].click();", button)
    #parse HTML
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    page = ""
   
    disc_text = soup.find(name="div", attrs = {"data-testid":"discussions-topic-header"})
    name = disc_text.find(name="a")["aria-label"]
    votes = disc_text.find_all(name="button")[1].string
    title = disc_text.find(name="h3").string

    tree = html.fromstring(page_source)
    xpath = "//*[@id=\"site-content\"]/div[2]/div/div/div[6]/div/div/div[1]/div[1]/div[3]/div/div"
    elmts = tree.xpath(xpath)
    text = elmts[0].text_content()
    review = f"-Discussion title : {title}\n-Text: {text}\n\n-Author: {name} ({votes} votes) = .\n\n-Comments:\n"
    page = page + review

    disc_comments = soup.find_all(name="div", attrs = {"data-testid":"discussions-comment"}) 
    for com in disc_comments:
        try:
            name = com.find(name="a")["aria-label"]
            votes = com.find_all(name="button")[1].string 
            xpath = "div/div/div[1]/div[3]/div/div"
            tree = html.fromstring(com)
            elmts = tree.xpath(xpath)
            comment = elmts[0].text_content()
            review = f"{name} ({votes} votes) : {comment}\n\n\n"
            page = page + review
        except TypeError as e:
            if str(e) == "'NoneType' object is not subscriptable":
                break
    return page 


def get_discussion_sec(comp):
    url = comp+"/discussion?sort=votes"
    driver.get(url)
    l = '//*[@id="site-content"]//ul[@role="list" and @class="km-list km-list--avatar-list km-list--two-line"]/li/div/a'
    l_disc = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, l)))
    l_disc = [elem.get_attribute("href") for elem in l_disc]
    list_disc = []
    for link in l_disc:
        driver.get(link)
        page = get_one_discussion()
        list_disc.append(page)
    return list_disc


####################################API####################################
def get_kernels(comp, comp_id):
    comp = comp.split("/")[-1]
    list_kernels = api.kernels_list(page=1,
                                    page_size=3,
                                    competition= comp,
                                    mine=False,
                                    user=None,
                                    language=None, #['all', 'python', 'r', 'sqlite', 'julia']
                                    kernel_type=None, #['all', 'script', 'notebook']
                                    output_type=None, # ['all', 'visualization', 'data']
                                    sort_by="voteCount") #['hotness', 'commentCount', 'dateCreated', 'dateRun', 'relevance','scoreAscending', 'scoreDescending', 'viewCount', 'voteCount']

    if not os.path.exists(f"./kernels/{comp_id}"):
        for kernel in list_kernels:
            api.kernels_pull(kernel.ref, f"./kernels/{comp_id}", metadata=False, quiet=True)
# %%
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

# %%
data = {"Name": [], "Job": [], "Company":[], "Link": []}

df = pd.DataFrame(data)

# %%
def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

# %%
###Please change the path according to where your driver is
path = "C:\\Python38\\geckodriver.exe"

driver = webdriver.Firefox(executable_path=path)
driver.get("https://www.linkedin.com/company/techstars/videos")

driver2 = webdriver.Firefox(executable_path=path)
driver2.get("https://www.linkedin.com/company/techstars/videos")

###Change your email and password below

username = ""
password = ""

###If you get a Location suspicion window, please login manually in both the new windows

if check_exists_by_xpath(driver, "//*[@class='btn__primary--large from__button--floating mercado-button--primary']"):
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_xpath("//*[@class='btn__primary--large from__button--floating mercado-button--primary']").click()
    
if check_exists_by_xpath(driver2, "//*[@class='btn__primary--large from__button--floating mercado-button--primary']"):
    driver2.find_element_by_id("username").send_keys(username)
    driver2.find_element_by_id("password").send_keys(password)
    driver2.find_element_by_xpath("//*[@class='btn__primary--large from__button--floating mercado-button--primary']").click()

# %%
###Increase the below scroll pause value if your webpages aren't loading quickly because of slow internet

SCROLL_PAUSE_TIME = 1.5

### To scroll all the videos

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

all_videos = driver.find_element_by_xpath("//*[@class='org-videos-see-all-module__list']")

for video in all_videos.find_elements_by_xpath(".//li[@class='org-videos-see-all-module__video-item-three-column']"):
    link = video.find_element_by_css_selector('a').get_attribute('href')
    driver2.get(link)
    if check_exists_by_xpath(driver2, "//*[contains(text(), 'Previously recorded live')]"):
    ###LIVE
        driver2.find_element_by_xpath("//*[@class='v-align-middle social-details-social-counts__reactions-count']").click()
        profiles = driver2.find_element_by_xpath("//*[@class='video-live-reactors-list__body social-details-reactors-tab-body ember-view']")
        prof = 0
        profnew = len(profiles.find_elements_by_css_selector('li'))
        
        ###Scrolling reactions
        
        while profnew != prof:
            prof = profnew
            driver2.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight);return arguments[0].scrollHeight;', profiles)
            time.sleep(SCROLL_PAUSE_TIME)
            profnew = len(profiles.find_elements_by_css_selector('li'))
            
        for profile in profiles.find_elements_by_css_selector('li'):
            Name = ""
            JobAt = ""
            Link = ""
            Job = ""
            Company = ""
            try:
                Name = profile.find_element_by_xpath(".//*[@class='artdeco-entity-lockup__title ember-view']").text
                JobAt = profile.find_element_by_xpath(".//*[@class='artdeco-entity-lockup__caption ember-view']").text
                Link = profile.find_element_by_css_selector('a').get_attribute('href')
                
                if " at " in JobAt:
                    Job = JobAt.split(" at ")[0]
                    Company = JobAt.split(" at ")[1]
                else:
                    Job = JobAt
            except:
                pass
            row = {'Name': Name, 'Job': Job, 'Company': Company, 'Link': Link}
            df = df.append(row, ignore_index=True)

    else:
        if check_exists_by_xpath(driver2, "//*[@id='ember1029']"):
            link = driver2.find_element_by_xpath(("//*[@id='ember1029']")).get_attribute("href")
            driver2.get(link)
            driver2.find_element_by_xpath("//*[@class='v-align-middle social-details-social-counts__reactions-count']").click()
            profiles = driver2.find_element_by_xpath("//*[@class='artdeco-modal__content social-details-reactors-modal__content ember-view']")
            prof = 0
            profnew = len(profiles.find_elements_by_css_selector('li'))
            
            ###Scrolling reactions

            while profnew != prof:
                prof = profnew
                driver2.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight);return arguments[0].scrollHeight;', profiles)
                time.sleep(SCROLL_PAUSE_TIME)
                profnew = len(profiles.find_elements_by_css_selector('li'))
                
            for profile in profiles.find_elements_by_css_selector('li'):
                Name = ""
                JobAt = ""
                Link = ""
                Job = ""
                Company = ""
                try:
                    Name = profile.find_element_by_xpath(".//*[@class='artdeco-entity-lockup__title ember-view']").text
                    JobAt = profile.find_element_by_xpath(".//*[@class='artdeco-entity-lockup__caption ember-view']").text
                    Link = profile.find_element_by_css_selector('a').get_attribute('href')
                    if " at " in JobAt:
                        Job = JobAt.split(" at ")[0]
                        Company = JobAt.split(" at ")[1]
                    else:
                        Job = JobAt
                except:
                    pass
            row = {'Name': Name, 'Job': Job, 'Company': Company, 'Link': Link}
            df = df.append(row, ignore_index=True)
        else:
            pass

# %%
df.to_csv("ProfileInfo.csv")

# %%

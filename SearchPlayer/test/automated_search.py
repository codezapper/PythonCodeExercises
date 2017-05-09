from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# create a new Firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.maximize_window()

# navigate to the application home page
driver.get("http://localhost:8000/lister/")

# get the search textbox
search_field = driver.find_element_by_id("main-input")
search_field.clear()

# enter search keyword and submit
search_field.send_keys("meta:one")
seaarch_results = driver.find_elements_by_class_name("search-results")

search_field.submit()

# get the list of elements which are displayed after the search
# currently on result page using find_elements_by_class_name  method
# lists= driver.find_elements_by_class_name("_Rm")
playlist = driver.find_elements_by_id("playlist")

# get the number of elements found
print('Found ' + str(len(search_results)) + ' search_results')
print('Found ' + str(len(playlist)) + ' playlist')

driver.quit()

from selenium import webdriver
from time import sleep

class InstaBot:
    def __init__(self, username, password):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(1)

        self.driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        sleep(3)

    def get_nonfollowers(self):
        self.driver.get("https://www.instagram.com/{}/".format(self.username))
        sleep(1)

        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()
        following = self._get_names()
        
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]").click()
        followers = self._get_names()

        nonfollowers = [user for user in following if user not in followers]
        self._save_names(nonfollowers)
         
    def _get_names(self):
        sleep(1)
        scroll_box = self.driver.find_element_by_xpath("//div[@role='dialog']/div/div[2]")
        prev_height, height = 0, 1
        while prev_height != height:
            prev_height = height
            sleep(0.5)
            height = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)

        names = [name.text for name in scroll_box.find_elements_by_xpath("//a[@title]")]
        self.driver.find_element_by_xpath("//div[@role='dialog']/div/div[1]//button").click()
        return names

    def _save_names(self, nonfollowers: list):
        print(nonfollowers)
        with open('nonfollowers.txt', 'w') as file:
            for user in nonfollowers:
                file.write('%s\n' % user)

# enter username and password
my_bot = InstaBot("", "")

try:
    my_bot.get_nonfollowers()
    my_bot.driver.close()
except:
    my_bot.driver.close()
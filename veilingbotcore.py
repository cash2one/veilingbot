import sys
import time
import datetime
import os
from selenium import webdriver
from raven import Client
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from credentials import MY_NAME as VV_NAME
from tv_credentials import MY_NAME as TV_NAME

RAVEN_ENABLED = False

if RAVEN_ENABLED:
    ravenclient = Client("http://1b6caf35463b4ea2b781d3f49efcc4ed:e8669c823ee04785997060943ba4a78a@localhost:9000/2")
else:
    ravenclient = None

class VeilingAPI(object):
    def __init__(self,
                 browser,
                 max_price,
                 action="dryrun"):
        self.browser = browser
        self.action = action
        self.max_price = max_price

    ## skeleton functions ##
    def do_place_bid(self, price):
        pass

    def get_current_bid(self):
        pass

    def get_latest_bidder(self):
        pass

    def get_remaining_secs(self):
        pass

    def do_login(self):
        pass

    def place_bid(self, price):
        log("Instructing API to place bid of %d EUR" % price)
        self.do_place_bid(price)
        time.sleep(0.1)
        if self.get_current_bid() > price:
            log("Fuck, somebody just overbid me! Returning.")
            return

        elif self.get_current_bid() < price or self.get_latest_bidder() not in (VV_NAME, TV_NAME):
            log("Uh oh, it seems that my bid did not register! Trying again just once.")
            self.do_place_bid(price)
            time.sleep(0.1)
            if not self.get_current_bid() >= price:
                log("Uh oh, it seems that my bid did not register! Screenshotting and failing hard.")
                make_screenshot(self.browser)
                raise RuntimeError("Placing bid failed")

        else:
            log("It seems that my bid was placed succesfully!")


def log(msg):
    if len(sys.argv) >= 2:
        url = sys.argv[1]
    else:
        url = "NO URL"
    last_url_part = url[-30:]
    try:
        logstring = "%s [%s] : %s" % (time.ctime(), last_url_part, str(msg))
        print logstring
    except:
        print time.ctime() + ' : Could not decode string!'


def make_screenshot(browser):
    # Ensure directory is created
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    filename = os.path.join("screenshots", str(time.time()) + '.png')
    browser.get_screenshot_as_file(filename)
    log('Created screenshot: %s' % filename)


def go_to_url(browser, url):
    log("Going to URL %s" % url)
    start_datetime = datetime.datetime.now()
    browser.get(url)
    elapsed_secs = datetime.datetime.now() - start_datetime
    log("Opening page succeeded in %s seconds." % elapsed_secs.seconds)
    close_cookie_dialogs(browser)


def close_cookie_dialogs(browser):
    try:
        # Hack to close cookie dialog, better for screenshots
        cookie_dialogs = browser.find_elements_by_class_name("acceptCookie")
        for dialog in cookie_dialogs:
            dialog.click()
            log("Closed one cookie law dialog")

        # Hack for PhantomJS which doesnt accept cookies with an empty name
        # and thus raises a dialog window which should be closed
        if browser.name == 'phantomjs':
            for dialog in browser.find_elements_by_class_name('DialogClose'):
                if dialog.is_displayed():
                    dialog.click()
                    log("Closed one cookie warning dialog")
    except:
        pass


def start_browser(url, browser="chrome"):
    log("Starting browser")

    if browser == "chrome":
        chrome_options = webdriver.ChromeOptions()
        #        chrome_options._arguments = ["--user-data-dir=/home/rik/.config/google-chrome/Default/", "--incognito"]
        chrome_options._arguments = ["--incognito"]
        browser = webdriver.Chrome(chrome_options=chrome_options)

    elif browser == "firefox":
        profile = webdriver.FirefoxProfile()
        profile.native_events_enabled = True
        browser = webdriver.Firefox(profile)

    elif browser == "phantomjs":
        uastring = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/28.0.1500.71 Chrome/28.0.1500.71 Safari/537.36"
        DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = uastring
        browser = webdriver.PhantomJS('./phantomjs-1.9.1-linux-x86_64/bin/phantomjs')

    elif browser == "htmlunit":
        browser = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNITWITHJS)

    else:
        log("Unknown browser specified")
        return

    # So we don't get directed to mobile sites
    browser.set_window_size(1680, 1050)

    # Set implicit wait to a few seconds, to prevent flooding of exceptions
    browser.implicitly_wait(time_to_wait=5)

    go_to_url(browser, url)
    return browser


def click_element_when_available(find_function, element, secs_between_tries=0.1, max_tries=20):
    counter = 0
    while not find_function(element):
        log("Element %s not (yet) found" % element)
        time.sleep(secs_between_tries)
        counter +=1
        if counter > max_tries:
            raise RuntimeError("Element not found")
    else:
        found = find_function(element)

    while not found.is_displayed():
        log("Element %s not (yet) visisble" % element)
        time.sleep(secs_between_tries)
        counter +=1
        if counter > max_tries:
            raise RuntimeError("Element not visible")
    else:
        log("Clicking element %s" % element)
        found.click()


def wait_for_element(find_function, element, max_secs=30):
#    log("DEBUG: using function %s to find element %s for %d seconds" % (find_function, element, max_secs))
    counter = 0
    found = None
    while not found:
        try:
            found = find_function(element)
        except NoSuchElementException:
            log("DEBUG: [%d] Element '%s' not found." % (counter, element))
            time.sleep(1)
            counter += 1
            if counter >= max_secs:
                raise
    else:
        return find_function(element)





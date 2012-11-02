"""
With the help of ``django-jasmine`` we can provide a URL ``/jasmine/`` which
we can access via Selenium. It will open your browser and run the tests and
it will be part of your normal Django test suite. There is no longer any
excuse to "forget" to run your Jasmine tests!

"""
from django.test import LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver


# We are currently not testing any JS related stuff as we assume that tag-it
# is tested well enough and we do nothing else on top of tag-it.

class JasmineSeleniumTests(object):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(JasmineSeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(JasmineSeleniumTests, cls).tearDownClass()
        cls.selenium.quit()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/jasmine/'))
        result = self.selenium.find_element_by_class_name('description')
        self.assertTrue('0 failures' in result.text)

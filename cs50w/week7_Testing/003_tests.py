### Does not work due to changes made to selenium

import os
import pathlib
import unittest

from selenium import webdriver


def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()


driver = webdriver.Chrome()


class WebpageTests(unittest.TestCase):

    def test_title(self):
        driver.get(file_uri("003_counter.html"))
        self.assertEqual(driver.title, "Counter")

    def test_increase(self):
        driver.get(file_uri("003_counter.html"))
        increase = driver.find_element("increase")
        increase.click()
        self.assertEqual(driver.find_element("h1").text, "1")

    def test_decrease(self):
        driver.get(file_uri("003_counter.html"))
        decrease = driver.find_element("decrease")
        decrease.click()
        self.assertEqual(driver.find_element("h1").text, "-1")

    def test_multiple_increase(self):
        driver.get(file_uri("003_counter.html"))
        increase = driver.find_element("increase")
        for i in range(3):
            increase.click()
        self.assertEqual(driver.find_element("h1").text, "3")


if __name__ == "__main__":
    unittest.main()

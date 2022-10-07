#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import time
from selenium import webdriver
import os


class BrowserHeadlessTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The phantomjs executable is assumed to be in your PATH:
        cls.driver = webdriver.PhantomJS('phantomjs')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_homepage(self):
        """Testing homepage functions"""
        self.driver.get("http://localhost:8000/")
        assert self.driver.title == 'Amigo - Create events for you and your friends with Amigo.'

    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Volitale test case, skip on travis")
    def test_rsvp_yes(self):
        """Testing accepting invitation with customized RSVP message"""
        self.driver.get("http://localhost:8000/invitation/?token=fdsa")
        yes_btn = self.driver.find_element_by_id("btn-rsvp-yes")
        print "Clicking Yes button..."
        yes_btn.click()
        time.sleep(1)

        rsvp_modal = self.driver.find_element_by_id('modal-rsvp')

        is_displayed = rsvp_modal.is_displayed()
        print "Ensure RSVP modal is displayed...{}".format(is_displayed)
        assert is_displayed is True

        rsvp_msg_textarea = rsvp_modal.find_element_by_id("rsvp-message")
        rsvp_msg_textarea.send_keys("YES RSVP message")
        print "Submitting YES RSVP message..."
        rsvp_modal.find_element_by_id("btn-submit-rsvp").click()
        time.sleep(2)

        is_displayed = rsvp_modal.is_displayed()
        print "Ensure RSVP modal is hidden...{}".format(is_displayed)
        assert is_displayed is False
        assert self.driver.find_element_by_id('modal-rsvp-success').is_displayed() is True
        # assert "RSVP msg is displayed" #TODO

        print "Browser testing RSVP with Yes message succeeded!"

# if __name__ == '__main__':
    # unittest.main()

from playwright.sync_api import sync_playwright
from hashlib import sha256
import csv
import re

def test_proxy_with_playwright():
    proxy_config = {
    "server": "host:port",
    "username": "user",
    "password": "pass"
    }
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")

    context = browser.new_context(
        viewpoint={'width': 1280, 'height': 1280},
        locale='en-US',
        extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
        )

        page = context.new_page()

        search_query = "starbucks london"
        number_of_reviews = 20

        title = ''
        star_rating = ''
        review_count = 0
        reviews = []

        try:
            page.goto("https://google.com/maps?hl=en")

            try:
                page.locator('div.VtwTSb > form:nth-of-type(2) span.UywwFc-vQzf8d').click(timeout=5000)
                page.wait_for_timeout(2000)
            except:
                pass
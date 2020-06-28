# RetirementUpdates

The project was created to allow me to automate a process I was doing each month, which was going into my two retirement accounts and copying/pasting some values into a Google Sheet where I track and project my account balances

# Downloads Required

1. geckodriver
    - This is required for Selenium to be able to open a browser window and navigate the webpages
    - Download link: https://github.com/mozilla/geckodriver/releases

2. Google Sheet API json File
    - This is required to update the Google Sheet using Selenium
    Download Instructions: https://developers.google.com/sheets/api/quickstart/go

# Python Packages Installed

    from selenium import webdriver
    import re
    import requests 
    import time
    import datetime
    from datetime import datetime
    from datetime import timedelta
    import sys
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials



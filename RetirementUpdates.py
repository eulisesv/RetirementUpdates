#!/usr/bin/env python
# coding: utf-8

#import packages required

from selenium import webdriver
import re
import requests
import time
import datetime
from datetime import datetime
from datetime import timedelta
import sys
import gspread # allows you to interact with Google Spreadsheets
# to authorize the Google Drive API
from oauth2client.service_account import ServiceAccountCredentials


# In[3]:


Fidelity_login = input('Enter Fidelity Login: ')
Vanguard_login = input('Enter Vanguard Login: ')


# In[4]:


Fidelity_password = input('Enter Fidelity Password: ')


# In[5]:


Vanguard_password = input('Enter Vanguard Password: ')


# # Grabbing the Fidelity data

# In[6]:


#open the webpage
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference("browser.privatebrowsing.autostart", True)

driver = webdriver.Firefox(firefox_profile=firefox_profile,executable_path=<path to geckodriver>)
driver.get('https://login.fidelity.com/ftgw/Fas/Fidelity/RtlCust/Login/Init')


# In[7]:


time.sleep(3) #wait 
loginElem = driver.find_element_by_id('userId-input') #find the user-id input element
passElem = driver.find_element_by_id('password') #find the password input element
enterElem = driver.find_element_by_id('fs-login-button') #this is the login button
loginElem.send_keys(Fidelity_login) #input the login id
passElem.send_keys(Fidelity_password) #input the PW
enterElem.submit() #click the submit button
time.sleep(3) #wait


# In[ ]:


while (driver.title).startswith('Error'): #this is needed in case of incorrect login info
    Fidelity_login = input('Please enter the correct Fidelity Login: ')
    Fidelity_password = input('Please enter the correct Fidelity Password: ')
    driver.get('https://login.fidelity.com/ftgw/Fas/Fidelity/RtlCust/Login/Init')
    time.sleep(3) #wait 
    loginElem = driver.find_element_by_id('userId-input') #find the user-id input element
    passElem = driver.find_element_by_id('password') #find the password input element
    enterElem = driver.find_element_by_id('fs-login-button') #this is the login button
    loginElem.send_keys(Fidelity_login) #input the login id
    passElem.send_keys(Fidelity_password) #input the PW
    enterElem.submit() #click the submit button
    time.sleep(3) #wait 10 seconds
else:
    #take the browser to the monthly statements page for the IRA account
    driver.get('https://retiretxn.fidelity.com/nbretail/savings2/navigation/dc/OnlineStatement?client=000400935&plan=35004')


# In[ ]:


time.sleep(3) #wait 10 seconds
#go to the prior month statement
Monthly_Elem = driver.find_element_by_id('monradio') #this is the button to select the monthly statement
Monthly_Elem.click() #this clicks that option
#the two lines below click the submit page button to take to the next page
Continue_Elem = driver.find_element_by_class_name('continueButton') 
Continue_Elem.submit()
time.sleep(3) #wait 


# In[ ]:


time.sleep(3) #wait 
#create a list of the 5 values that are needed
values_list = []
for tag_text in driver.find_elements_by_tag_name('td'): #all values are under the 'td' tag
        values_list.append(tag_text.text) 


# In[ ]:


#use RegEx to only find the first 5 number values
values_list = [text for text in values_list if re.match(r"-?\$\d.+\)?",text)][:5] 
#convert the number strings to floats and assign to correct variables
float_values = [float(value.replace('$',"").replace(',',"")) for value in values_list]


# In[ ]:


#create a dictionary to store values
value_dict = {"Beginning_Balance":0,
              "My_Contributions":0,
              "Oracle_Contributions":0,
              "Change_in_Market":0,
              "Ending_Balance":0}


# In[ ]:


#update the values in the dictionary 
for i,j in enumerate(value_dict.keys()): #.keys gives the names of the dict keys
    value_dict[j] = float_values[i] #update the value in each dict entry 
value_dict['Total_Contributions'] = value_dict['My_Contributions'] + value_dict['Oracle_Contributions']


# In[ ]:


time.sleep(3) #wait 10 seconds
#logout and close browser
driver.get('https://login.fidelity.com/ftgw/Fidelity/RtlCust/Logout/Init?AuthRedUrl=https://www.fidelity.com/customer-service/customer-logout')
time.sleep(3)
driver. close()


# # Grab the Vanguard Data

# In[ ]:


#open the webpage
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference("browser.privatebrowsing.autostart", True)

driver = webdriver.Firefox(firefox_profile=firefox_profile,executable_path=<path to geckodriver>)
driver.get('https://investor.vanguard.com/my-account/log-on')


# In[ ]:


time.sleep(3) #wait 
loginElem = driver.find_element_by_id('username') #find the user-id input element
passElem = driver.find_element_by_id('password') #find the password input element
enterElem = driver.find_element_by_xpath('/html/body/rps-root/psx-my-accounts-page/section/div[1]/div/section/form/div[3]/vui-button/button')
loginElem.send_keys(Vanguard_login) #input the login id
passElem.send_keys(Vanguard_password) #input the PW
enterElem.click() #click the submit button
time.sleep(3) #wait 

# In[ ]:


while driver.current_url == 'https://logon.vanguard.com/logon':
    Vanguard_login = input('Please enter the correct Vanguard Login: ')
    Vanguard_password = input('Please enter the correct Vanguard Password: ')
    driver.get('https://investor.vanguard.com/my-account/log-on')
    time.sleep(3) #wait 
    loginElem = driver.find_element_by_id('USER') #find the user-id input element
    passElem = driver.find_element_by_id('PASSWORD') #find the password input element
    enterElem = driver.find_element_by_id('login') #this is the login button
    loginElem.send_keys(Vanguard_login) #input the login id
    passElem.send_keys(Vanguard_password) #input the PW
    enterElem.submit() #click the submit button
    time.sleep(3) #wait 
else:
    try:
        # Enter the security code received by text
        SecurityCode = str(input('Enter the Security Code Received - '))
        #enter the security code to Vanguard and click yes and submit
        CodeElem = driver.find_element_by_id('LoginForm:ANSWER')
        CodeElem.send_keys(SecurityCode)
        RadioLoginElem = driver.find_element_by_id('LoginForm:DEVICE:0')
        RadioLoginElem.click() #this clicks that option
        ContinueElem = driver.find_element_by_id('LoginForm:ContinueInput')
        ContinueElem.click()
        time.sleep(3) #wait 
    except: 
        pass

# In[ ]:


#go to the performance page
time.sleep(5) #wait 
driver.get('https://personal.vanguard.com/web/cfv/personal-performance/performance-chart')
time.sleep(20)


# In[ ]:


#switch to the table mode
tableElem = driver.find_element_by_id('performance-table-toggle')
#click the button
tableElem.click()
time.sleep(3) #wait 


# In[ ]:


#get the prior month ending balance by the id Mon-YYYY-ending-balance
Prior_Month = (datetime.today().date() + timedelta(days=-(datetime.today().day))).strftime('%b-%Y')
PriorMonID = Prior_Month+'-ending-balance'
PriorMonthEndingBalance = driver.find_element_by_id(PriorMonID).text
#format the value into a float
Vanguard_PriorMonthEndingBalance = float(PriorMonthEndingBalance.replace('$',"").replace(',',""))

#get the prior month total deposits 
Prior_Deposit_ID = Prior_Month+'-purchases-and-withdrawals'
PriorMonthDeposit = driver.find_element_by_id(Prior_Deposit_ID).text
#format the value into a float
Vanguard_PriorMonthDeposit = float(PriorMonthDeposit.replace('$',"").replace(',',""))


# In[ ]:


#logout and close the browser
driver.get('https://personal.vanguard.com/us/faces/com/vanguard/logon/view/LogonLogoff.xhtml?scid=1576645558817AFBCCnwprd')
time.sleep(3)
driver. close()


# # Accessing the Google Sheet

# In[ ]:


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(<Google Sheet API json>, scope)
client = gspread.authorize(creds)

#find the workbook to be updated and open it
fidelity_sheet = client.open("Retirement").get_worksheet(2)
vanguard_sheet = client.open("Retirement").get_worksheet(3)


# In[ ]:


#find the prior month row to be updated
Fidelity_last_row = len(fidelity_sheet.col_values(8)) + 1  #this is the row after the last row with data in the Actual Value column
Vanguard_last_row = len(vanguard_sheet.col_values(8)) + 1


# In[ ]:


#this is the month of the prior month that needs to be updated
prior_month = (datetime.today() + timedelta(days=-datetime.today().day)).date().replace(day=1)


# In[ ]:


#update the 8th column with the new value for actual and the 3rd column for deposits
#check if the row for last month has already been populated
if (datetime.strptime(fidelity_sheet.row_values(Fidelity_last_row)[1],'%b-%y').date() == prior_month): 
    fidelity_sheet.update_cell(Fidelity_last_row,8,value_dict['Ending_Balance']); #update the ending balance
    fidelity_sheet.update_cell(Fidelity_last_row,3,value_dict['Total_Contributions']); #update the total deposit
    print('Fidelity Updated')
else:
    print('No update to Fidelity')
if (datetime.strptime(vanguard_sheet.row_values(Vanguard_last_row)[1],'%b-%y').date() == prior_month):
    vanguard_sheet.update_cell(Vanguard_last_row,8,Vanguard_PriorMonthEndingBalance); #update the ending balance
    vanguard_sheet.update_cell(Vanguard_last_row,3,Vanguard_PriorMonthDeposit); #update the total deposit
    print('Vanguard Updated')
else: #if it has, then no update is to be done
    print('No update to Vanguard')
import streamlit as st
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time

# selenium 4 changed the way to import the webdriver
# we got to import the service and options

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
load_dotenv()

# comment all streamlit lines
# create a simple streamlit page
st.title('Kredily Automation')
st.write('This is a simple page to show the Kredily Automation')

# this will run a selenium script to automate the uploading of the attendance
# open the url foetron.kredily.com

# calculate the time taken to upload th e attendance
start_time = time.time()


# create a chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# create a service
service = Service(ChromeDriverManager().install())

# create a driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# open the url and use dotenv to get the url, username and password

driver.get('KREDILY_URL')
# login
# find the username and password
username = driver.find_element(By.ID, 'username')
password = driver.find_element(By.ID, 'password')
# enter the username and password
username.send_keys('KREDILY_USERNAME')
password.send_keys('KREDILY_PASSWORD')
# click the login button
driver.find_element(By.ID, 'login').click()
# wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'attendance')))
# click the attendance button
driver.find_element(By.ID, 'attendance').click()
# wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'upload-attendance')))
# click the upload attendance button
driver.find_element(By.ID, 'upload-attendance').click()
# wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'upload-attendance-file')))
# click the upload attendance file
driver.find_element(By.ID, 'upload-attendance-file').send_keys('/home/arun/Downloads/attendance.csv')
# wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'upload-attendance-submit')))
# click the submit button
driver.find_element(By.ID, 'upload-attendance-submit').click()
# wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'attendance')))
# click the attendance button
driver.find_element(By.ID, 'attendance').click()
# wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'attendance-table')))
# get the attendance table
attendance_table = driver.find_element(By.ID, 'attendance-table')
# get the table rows
rows = attendance_table.find_elements(By.TAG_NAME, 'tr')
# get the table headers
header = rows[0].find_elements(By.TAG_NAME, 'th')
# get the table data
data = rows[1].find_elements(By.TAG_NAME, 'td')
# print the data
st.write('Attendance Uploaded')
st.write('Attendance Date:', data[0].text)
st.write('Total Employees:', data[1].text)
st.write('Present:', data[2].text)
st.write('Absent:', data[3].text)
st.write('Leaves:', data[4].text)
st.write('Half Day:', data[5].text)
st.write('Late:', data[6].text)
# close the driver
driver.quit()
# Path: pages/6_Face_Recognition.py

# time taken to upload the attendance
end_time = time.time()
st.write('Time taken to upload the attendance:', end_time - start_time)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EW
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert 
import HtmlTestRunner
import unittest
import argparse
import time
import sys

navegador = ""
titles =["Self Paced online Training",
"In Depth Material",
"Liftime Instructor Support",
"Resume Preparation",
"30 day Money Back Guarantee"]

def argumentOptions():
	parser = argparse.ArgumentParser()
	parser.add_argument("--browser", choices=["chrome", "firefox", "opera"],help="Open driver in browser")
	args = parser.parse_args()
	global navegador
	navegador = args.browser
	del sys.argv[1:]

class TechChallenge(unittest.TestCase):

	def setUp(self):
		global navegador
		if navegador == "chrome":
			print("Abrimos navegador chrome...")
			self.driver = webdriver.Chrome()
		elif navegador == "firefox":
			print("Abrimos navegador firefox...")
			self.driver = webdriver.Firefox()
		elif navegador == "opera":
			print("Abrimos navegador opera...")
			self.driver = webdriver.Opera()

		self.driver.get("https://rahulshettyacademy.com/AutomationPractice/")	
		self.driver.implicitly_wait(5)
		
	def test_ACONT_001(self):
		driver = self.driver
		
		input_suggestion =driver.find_element(By.XPATH,"//input[@id='autocomplete']")
		input_suggestion.click()
		input_suggestion.clear()
		input_suggestion.send_keys("Me")
		suggestion_list = driver.find_elements(By.XPATH,"//div[starts-with(@id,'ui-id-')]")
		for x in range(0,len(suggestion_list)):
			input_suggestion.send_keys(Keys.ARROW_DOWN)
			#driver.implicitly_wait(5)
			if "Mexico" in suggestion_list[x].text :
				print("Encontrado")
				input_suggestion.send_keys(Keys.ENTER)
				break	
		print("...............Fin de Test .............\n")

	def test_ACONT_002(self):
		driver = self.driver
		select = driver.find_element(By.XPATH,"//select[@id='dropdown-class-example']")
		select.click()
		options = driver.find_elements(By.XPATH,"//option[@value='']//following-sibling::option")
		nameOption2 = options[1].text
		options[1].click()
		select.click()
		nameOption3 = options[2].text
		options[2].click()
		if nameOption2 not in nameOption3:
			print("Se actualizo la opcion")
		else:
			raise ValueError("Error")
		time.sleep(2)	
		print("...............Fin de Test .............\n")
						
	def test_ACOUR_001(self):
		driver = self.driver	
		
		driver.find_element(By.ID,"openwindow").click()
		driver.switch_to.window(driver.window_handles[1])
		close_btn = WebDriverWait(driver, 20).until(EW.presence_of_element_located((By.CSS_SELECTOR,".sumome-react-wysiwyg-outside-horizontal-resize-handles div:nth-child(2)")))
		close_btn.click()
		driver.maximize_window()
		
		try:
			t4=driver.find_element(By.XPATH,"//*[text()='"+titles[4]+"']")
			a =t4.location["y"]
			driver.execute_script("window.scrollTo(0,"+str(a)+")")
			time.sleep(2)
			print("*** 4: ",t4.text,"***")
		except Exception:
			raise Exception("Titulo no coincide")

		try:
			t0=driver.find_element(By.XPATH,"//*[text()='"+titles[0]+"']")
			print("*** 1: ",t0.text,"***")
			t1=driver.find_element(By.XPATH,"//*[text()='"+titles[1]+"']")
			print("*** 2: ",t1.text,"***")
			t2=driver.find_element(By.XPATH,"//*[text()='"+titles[2]+"']")
			print("*** 3: ",t2.text,"***")
			t3=driver.find_element(By.XPATH,"//*[text()='"+titles[3]+"']")
			print("*** 4: ",t3.text,"***")
		except Exception:
			raise Exception("Titulo no coincide")

		time.sleep(3)
		driver.switch_to.window(driver.window_handles[0])
		print("...............Fin de Test .........	....\n")

	def test_ASTORE_001(self):
		driver = self.driver
		actions = ActionChains(driver)
		driver.maximize_window()

		driver.find_element(By.ID,"opentab").click()
		driver.switch_to.window(driver.window_handles[1])
		WebDriverWait(driver,10).until(EW.presence_of_element_located((By.XPATH,"//a[contains(text(),'Home')]")))
		time.sleep(1)

		counter_section=driver.find_element(By.XPATH,"//a[contains(text(),'VIEW ALL COURSES')]")
		driver.execute_script("window.scrollTo(0,"+str(counter_section.location["y"]-100)+")")
		
		time.sleep(4)
		try:
			driver.get_screenshot_as_file('./reports/ASTORE_001.png')
		except:
			raise Exception("No se pudo tomar captura")
		driver.switch_to.window(driver.window_handles[0])
		time.sleep(2)

	def test_ACONT_003(self):
		driver = self.driver

		input_name = driver.find_element(By.CSS_SELECTOR,"#name")
		input_name.click()
		input_name.send_keys("Stori Card")
		time.sleep(1)

		driver.find_element(By.CSS_SELECTOR,"#alertbtn").click()
		alert = Alert(driver) 
		print("btn_alert *************** ",alert.text,"**** ")
		alert.accept() 
		time.sleep(1)

		input_name = driver.find_element(By.CSS_SELECTOR,"#name")
		input_name.click()
		input_name.send_keys("Stori Card")
		time.sleep(1)

		driver.find_element(By.CSS_SELECTOR,"#confirmbtn").click()
		alert = Alert(driver) 
		aler_txt=alert.text
		print("btn_confirm *************** ",alert.text,"**** ")
		alert.accept() 
		time.sleep(1)

		txt_correct = "Hello Stori Card, Are you sure you want to confirm?"
		if txt_correct in aler_txt:
			print("Texto coincide")
		else:
			print("Texto NO coincide")

	def tearDown(self):
		self.driver.close()		


if __name__ == '__main__':
	argumentOptions()
	unittest.main(testRunner = HtmlTestRunner.HTMLTestRunner(output='./reports',report_name="MyReport_"+navegador))

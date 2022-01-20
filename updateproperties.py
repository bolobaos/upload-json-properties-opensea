import tkinter
import subprocess
from tkinter import *
from tkinter import filedialog
import os
import sys
import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from decouple import config
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import warnings
import json
import logging

root = Tk()
root.geometry('500x400')
root.title("NFTs Upload Properties to OpenSea  ")
input_save_list = ["NFTs folder :", 0, 0, 0, 0, 0, 0, 0, 0]
main_directory = os.path.join(sys.path[0])
is_polygon = BooleanVar()
is_polygon.set(False)

options = webdriver.ChromeOptions()
options.add_argument("start-maximized");
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

warnings.filterwarnings("ignore", category=DeprecationWarning) #turn off all deprecation warnings
logging.basicConfig(filename='std.log', level=logging.INFO, filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def open_chrome_profile():
    subprocess.Popen(
        [
            "start",
            "chrome",
            "--remote-debugging-port=8989",
            "--user-data-dir=" + main_directory + "/chrome_profile",
        ],
        shell=True,
    )

def save_file_path():
    return os.path.join(sys.path[0], "Save_file.cloud") 

# ask for directory on clicking button, changes button name.
def upload_folder_input():
    global upload_path
    upload_path = filedialog.askdirectory()
    Name_change_img_folder_button(upload_path)

def Name_change_img_folder_button(upload_folder_input):
    upload_folder_input_button["text"] = upload_folder_input

class InputField:
    def __init__(self, label, row_io, column_io, pos, master=root):
        self.master = master
        self.input_field = Entry(self.master)
        self.input_field.label = Label(master, text=label)
        self.input_field.label.grid(row=row_io, column=column_io)
        self.input_field.grid(row=row_io, column=column_io + 1)
        try:
            with open(save_file_path(), "rb") as infile:
                new_dict = pickle.load(infile)
                self.insert_text(new_dict[pos])
        except FileNotFoundError:
            pass

    def insert_text(self, text):
        self.input_field.delete(0, "end")
        self.input_field.insert(0, text)

    def save_inputs(self, pos):
        input_save_list.insert(pos, self.input_field.get())
        with open(save_file_path(), "wb") as outfile:
            pickle.dump(input_save_list, outfile)

###input objects###
collection_link_input = InputField("OpenSea Collection Link:", 2, 0, 1)
start_num_input = InputField("Start Number:", 3, 0, 2)
end_num_input = InputField("End Number:", 4, 0, 3)
price = InputField("Price:", 5, 0, 4)
title = InputField("Title:", 6, 0, 5)
description = InputField("Description:", 7, 0, 6)
file_format = InputField("NFT JSON Format:", 8, 0, 7)
external_link = InputField("External link:", 9, 0, 8)

collection_link = "https://opensea.io/collection/piggieland" #UPDATE COLLECTION LINK#
number_of_properties = 9

options = webdriver.ChromeOptions()
options.add_argument("start-maximized");
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

###save inputs###
def save():
    input_save_list.insert(0, upload_path)
    collection_link_input.save_inputs(1)
    start_num_input.save_inputs(2)
    end_num_input.save_inputs(3)
    price.save_inputs(4)
    title.save_inputs(5)
    description.save_inputs(6)
    file_format.save_inputs(7)
    external_link.save_inputs(8)
   
def wait_css_selector(code):
        wait.until(
            ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code))
        )
        
def wait_css_selectorTest(code):
        wait.until(
            ExpectedConditions.elementToBeClickable((By.CSS_SELECTOR, code))
        )    

def wait_xpath(code):
        wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))
  
def css_and_click(code, fail_message = "Css not found"):
        while True:
            try:
                x = wait.until(ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code)))
                x.click()
                break
            except:
                print(fail_message + ": " + code + "\nretrying...")
                time.sleep(1)
def xpath_and_key(code, key, fail_message = "Xpath not found"):
        while True:
            try:
                x = wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))
                x.send_keys(key)
                break
            except:
                print(fail_message + ": " + code + "\nretrying...")
                time.sleep(1)
                
def nested_replace( structure, original, new ):
        if type(structure) == list:
            return [nested_replace( item, original, new) for item in structure]

        if type(structure) == dict:
            return {key : nested_replace(value, original, new)
                         for key, value in structure.items() }

        if structure == original:
            return new
        else:
            return structure     
            
# _____MAIN_CODE_____
def main_program_loop():
    ###START###
    project_path = main_directory
    file_path = upload_path
    collection_link = collection_link_input.input_field.get()
    start_num = int(start_num_input.input_field.get())
    end_num = int(end_num_input.input_field.get())
    loop_price = float(price.input_field.get())
    loop_title = title.input_field.get()
    loop_file_format = file_format.input_field.get()
    loop_external_link = str(external_link.input_field.get())
    loop_description = description.input_field.get()

    ##chromeoptions
    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:8989")
    driver = webdriver.Chrome(
        executable_path=project_path + "/chromedriver.exe",
        chrome_options=opt,
    )
    wait = WebDriverWait(driver, 60)

          
    while end_num >= start_num:
        print("Start updating NFT " +  loop_title + str(start_num))
        logging.info("Start updating NFT " +  loop_title + str(start_num))
        
        driver.get(collection_link)
        
        driver.implicitly_wait(200) 
        #WAIT TO MAKE SURE PAGE LOADS PROPERLY
          
        ####OPENING CORRECT JSON FILE FOR UPLOAD  
        with open(file_path + "\\" + str(start_num) + ".json") as f:          
        
            file1 = json.load(f)
        
        #FOLLOWING CODE IS TO REPLACE SOME TEXT IN THE JSON FILES. EG., FIX SPELLING MISTAKES, ADD SPACES BEFORE THEY ARE INPUTTED INTO THE PROPERTIES PAGE# MAKE SURE SPELLING IS OR ELSE THE WORD WILL NOT BE FOUND AND REPLACED. CAPS MATTER TOO
        
            file2 = nested_replace(file1,'Cottoncandy', 'cotton candy')
            file3 = nested_replace(file2,'Multicolordaisies', 'multicolor daisies')
                   
        data1 = file3 #UPDATE FILENAME AS REQUIRED
      
        #PULLING UP JUST METATDATA IN JSON FILE      
        for attributes in data1:
            
            metadata = data1[attributes]
            print(metadata) #PRINT METADATA ON CONSOLE TO MAKE SURE IT IS CORRECT
            logging.info(metadata) #ALSO LOGGING INFORMATION IN CASE CONSOLE CRASHES
            
            
        #####SEARCH#### ####IMPORTANT: EDIT THE ALT NAME BELOW (REPLACE 'PIGGIE') SO THAT THE PROGRAM CAN SELECT THE APPROPRIATE IMAGE
        
        search_bar = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[4]/div/div/div/div[3]/div[1]/div[1]/input')
        search_bar.send_keys(start_num)
        search_bar.send_keys(Keys.RETURN)
        
        driver.implicitly_wait(200)
        
        #SEARCH FUNCTION NEEDS IMPROVEMENT AS OPENSEA DOESNT PULL UP EXACT NUMBERS. ANY SUGGESTIONS ARE APPRECIATED!!# 
        
        result = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(driver.find_element_by_xpath(".//img[contains(@alt, 'Piggie') and contains(@alt, start_num)]"))) 
        driver.implicitly_wait(200)                
        result.click()
           
        driver.implicitly_wait(200)
                            
        #####SELECTED NFT SHOULD SHOW ON PAGE AND EDIT BUTTON TO BE SELECTED
        
        edit = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[1]/div/span/a')
        print(driver.current_url) #FOR TRACKING AND LOGGING PURPOSES
        logging.info(driver.current_url) #FOR LOGGING TRACKING AND PURPOSES
        get_title = driver.title         
        print(get_title, " ", len(get_title))
        logging.info(get_title, " ", len(get_title))##FOR LOGGING TRACKING AND PURPOSES TO MAKE SURE CORRECT NFT IS SELECTED. IF BROWSER DOESNT REFRESH IN TIME, PROGRAM MAY SELECT WRONG NFT. THIS WILL ALLOW YOU TO DOUBLE CHECK
        edit.click()

        #####PROPERTIES SELECTED###
        
        driver.execute_script("window.scrollTo(0, 1000);")
        properties = driver.find_element_by_xpath('//*[@id="main"]/div/div/section/div[2]/form/section/div[1]/div/div[2]/button')
        properties.click()
                
        #####ADDING PROPERTIES#### #make sure the appropriate key names are listed below. e.g., update 'Trait_type' and 'value' as what is listed in your json file#
        add_p = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/section/button')  
    
        for i in range(len(metadata)):
       
            input1 = driver.find_element_by_xpath('//tbody[@class="AssetTraitsForm--body"]/tr[last()]/td[1]/div/div/input')
            input2 = driver.find_element_by_xpath('//tbody[@class="AssetTraitsForm--body"]/tr[last()]/td[2]/div/div/input')
            current_trait = metadata[i - 1]["trait_type"]
            current_value = metadata[i - 1]["value"]
            input1.send_keys(current_trait)
            input2.send_keys(current_value)
            if i != len(metadata) - 1:
                add_p.click()
        
        #SAVE BUTTON SELECTED
        save1 = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/footer/button')
        save1.click()
        
        submit = driver.find_element_by_xpath('//*[@id="main"]/div/div/section/div[2]/form/div[8]/div[1]/span/button')        
        submit.click()
        
        #go back a page to refresh metadata
        driver.back()
        
        refresh = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[1]/div/div[1]/div[2]/section[1]/div/div[2]/div/button[1]')
        refresh.click()
        time.sleep(2)
        
        print('Refresh completed')
        
        driver.get(collection_link)
            
        start_num = start_num + 1
        logging.info('NFT update completed!')
        print('NFT update completed!')
        

#####BUTTON ZONE#######
button_save = tkinter.Button(root, width=20, text="Save Form", command=save) 
button_save.grid(row=23, column=1)
button_start = tkinter.Button(root, width=20, bg="green", fg="white", text="Start", command=main_program_loop)
button_start.grid(row=25, column=1)
isPolygon = tkinter.Checkbutton(root, text='Polygon Blockchain', var=is_polygon)
isPolygon.grid(row=20, column=0)
open_browser = tkinter.Button(root, width=20,  text="Open Chrome Browser", command=open_chrome_profile)
open_browser.grid(row=22, column=1)
upload_folder_input_button = tkinter.Button(root, width=20, text="Add NFTs JSON Upload Folder", command=upload_folder_input)
upload_folder_input_button.grid(row=21, column=1)
try:
    with open(save_file_path(), "rb") as infile:
        new_dict = pickle.load(infile)
        global upload_path
        Name_change_img_folder_button(new_dict[0])
        upload_path = new_dict[0]
except FileNotFoundError:
    pass
#####BUTTON ZONE END#######
root.mainloop()

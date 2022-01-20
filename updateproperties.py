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
            file4 = nested_replace(file3,'Pinkflamingo', 'pink flamingo')
            file5 = nested_replace(file4,'Blueflamingo', 'blue flamingo')
            file6 = nested_replace(file5,'Grassskirt', 'grass skirt')
            file7 = nested_replace(file6,'Purpleskirt', 'purple skirt')
            file8 = nested_replace(file7,'Hotpinkhearts', 'hot pink hearts')
            file9 = nested_replace(file8,'Lightpinkhearts', 'light pink hearts')
            file10 = nested_replace(file9,'Redhearts', 'red hearts')
            file11 = nested_replace(file10, 'Blackglasses', 'black glasses')
            file12 = nested_replace(file11,'Blackshades', 'black shades')
            file13 = nested_replace(file12,'Blueglasses', 'blue glasses')
            file14 = nested_replace(file13,'Bluegoggles', 'blue goggles')
            file15 = nested_replace(file14,'Blueshades', 'blue shades')
            file16 = nested_replace(file15,'Greenglasses', 'green glasses')
            file17 = nested_replace(file16,'Greengoggles', 'green goggles')
            file18 = nested_replace(file17,'Greenshades', 'green shades')
            file19 = nested_replace(file18,'Pinkheartshades', 'pink heart shades')	
            file20 = nested_replace(file19,'Redheartshades', 'red heart shades')
            file21 = nested_replace(file20,'Pinkshades', 'pink shades')
            file22 = nested_replace(file21,'Yellowgoggles', 'yellow goggles')
            file23 = nested_replace(file22,'Yellowshades', 'yellow shades')
            file24 = nested_replace(file23,'Blackpatch', 'black patch')
            file25 = nested_replace(file24,'Blueheartshades', 'blue heart shades')
            file26 = nested_replace(file25,'Bluepatch', 'blue patch')
            file27 = nested_replace(file26,'Bluestarsshades', 'blue stars shades')
            file28 = nested_replace(file27,'Bronzemonocle', 'bronze monocle')
            file29 = nested_replace(file28,'Forestrobber', 'forest robber')
            file30 = nested_replace(file29,'Goldmonocle', 'gold monocle')
            file31 = nested_replace(file30,'Greenstarsshades', 'green stars shades')
            file32 = nested_replace(file31,'Greypatch', 'grey patch')
            file33 = nested_replace(file32,'Maroonrobber', 'maroon robber')
            file34 = nested_replace(file33,'Midnightrobber', 'midnight robber')
            file35 = nested_replace(file34,'Pinkstarsshades', 'pink stars shades')			
            file36 = nested_replace(file35,'Pridepatch', 'pride patch')
            file37 = nested_replace(file36,'Silvermonocle', 'silver monocle')
            file38 = nested_replace(file37,'Blackbeats', 'black beats')
            file39 = nested_replace(file38,'Bluebeats', 'blue beats')
            file40 = nested_replace(file39,'Blueberryicecream', 'blueberry ice cream')
            file41 = nested_replace(file40,'Blueberrymacarons', 'blueberry macarons')
            file42 = nested_replace(file41,'Caramelicecream', 'caramel ice cream')
            file43 = nested_replace(file42,'Chocolateicecream', 'chocolate ice cream')
            file44 = nested_replace(file43,'Cottonicecream', 'cotton ice cream')
            file45 = nested_replace(file44,'Grapemacarons', 'grape macarons')
            file46 = nested_replace(file45,'Minticecream', 'mint ice cream')
            file47 = nested_replace(file46,'Purplebeats', 'purple beats')
            file48 = nested_replace(file47,'Raspberryicecream', 'raspberry ice cream')
            file49 = nested_replace(file48,'Vanillaicecream', 'vanilla ice cream')
            file50 = nested_replace(file49,'Yellowbeats', 'yellow beats')
            file51 = nested_replace(file50,'Yellowmacarons', 'yellow macarons')
            file52 = nested_replace(file51,'Burgerheadphones', 'burger headphones')
            file53 = nested_replace(file52,'Cardboardbox', 'cardboard box')
            file54 = nested_replace(file53,'Clearastronaut', 'clear astronaut')
            file55 = nested_replace(file54,'Dayastronaut', 'day astronaut')
            file56 = nested_replace(file55,'Graffitibox', 'graffiti box')
            file57 = nested_replace(file56,'Nightastronaut', 'night astronaut')
            file58 = nested_replace(file57,'Pinkpartyhat', 'pink party hat')
            file59 = nested_replace(file58,'Redbeats', 'red beats')
            file60 = nested_replace(file59,'Yellowpartyhat', 'yellow party hat')
            file61 = nested_replace(file60,'Berryvanillaicecream', 'berry vanilla ice cream')
            file62 = nested_replace(file61,'Tuttifruiticecream', 'tuttifruiti ice cream')
            file63 = nested_replace(file62,'Wonderlandicecream', 'wonderland ice cream')
            file64 = nested_replace(file63,'Bitcoinbling1', 'Bitcoin bling v1')
            file65 = nested_replace(file64,'Bitcoinbling2', 'bitcoin bling v2')
            file66 = nested_replace(file65,'Dollarbling', 'dollar bling')
            file67 = nested_replace(file66,'Orangecarrots', 'orange carrots')
            file68 = nested_replace(file67,'Purplelettuce', 'purple lettuce')
            file69 = nested_replace(file68,'Purplelettucesalad', 'purple lettuce salad')
            file70 = nested_replace(file69,'Redcarrots', 'red carrots')
            file71 = nested_replace(file70,'Berrymacaron', 'berry macaron')
            file72 = nested_replace(file71,'Blueberrymacaron', 'blueberry macaron')
            file73 = nested_replace(file72,'Leftlobsterclaw', 'left lobster claw')
            file74 = nested_replace(file73,'Limemacaron', 'lime macaron')
            file75 = nested_replace(file74,'Mittens', 'blue mittens')
            file76 = nested_replace(file75,'Orangelobsterclaws', 'orange lobster claws')
            file77 = nested_replace(file76,'Pinkmittens', 'pink mittens')
            file78 = nested_replace(file77,'Redlobsterclaws', 'red lobster claws')
            file79 = nested_replace(file78,'Rightlobsterclaw', 'right lobster claw')
            file80 = nested_replace(file79,'Blackboxergloves', 'black boxing gloves')
            file81 = nested_replace(file80,'Blueboxergloves', 'blue boxing gloves')
            file82 = nested_replace(file81,'Bluelobsterclaws', 'blue lobster claws')
            file83 = nested_replace(file82,'Greenboxinggloves', 'green boxing gloves')
            file84 = nested_replace(file83,'Hotpinkheart', 'hot pink heart')
            file85 = nested_replace(file84,'Lightpinkheart', 'light pink heart')
            file86 = nested_replace(file85,'Orangeboxinggloves', 'orange boxing gloves')
            file87 = nested_replace(file86,'Redboxergloves', 'red boxing gloves')
            file88 = nested_replace(file86,'Redheart', 'red heart')
            file89 = nested_replace(file88,'Yellowboxinggloves', 'yellow boxing gloves')
            file90 = nested_replace(file89,'Bluemask', 'blue mask')
            file91 = nested_replace(file90,'Greensnorkelingtube', 'green snorkeling tube')
            file92 = nested_replace(file91,'Hospitalgreenmask', 'hospital green mask')
            file93 = nested_replace(file92,'Pinkmask', 'pink mask')
            file94 = nested_replace(file93,'Yellowmask', 'yellow mask')
            file95 = nested_replace(file94,'Yellowsnorkelingtube', 'yellow snorkeling tube')
            file187 = nested_replace(file95,'Redboxergloves', 'red boxing gloves')
            file188 = nested_replace(file187,'Redheart', 'red heart')
            file189 = nested_replace(file188,'Yellowboxinggloves', 'yellow boxing gloves')
            file190 = nested_replace(file189,'Bluemask', 'blue mask')
            file191 = nested_replace(file190,'Greensnorkelingtube', 'green snorkeling tube')
            file192 = nested_replace(file191,'Hospitalgreenmask', 'hospital green mask')
            file193 = nested_replace(file192,'Pinkmask', 'pink mask')
            file194 = nested_replace(file193,'Yellowmask', 'yellow mask')
            file195 = nested_replace(file194,'Yellowsnorkelingtube', 'yellow snorkeling tube')
        
        data1 = file195 #UPDATE FILENAME AS REQUIRED
      
        #PULLING UP JUST METATDATA IN JSON FILE      
        for attributes in data1:
            
            metadata = data1[attributes]
            print(metadata) #PRINT METADATA ON CONSOLE TO MAKE SURE IT IS CORRECT
            logging.info(metadata) #ALSO LOGGING INFORMATION IN CASE CONSOLE CRASHES
            
        #properties already included 4263, 1000-1224 cannot edit 1511 2000-2018
        
        #####SEARCH####
        
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
                
        #####ADDING PROPERTIES####
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

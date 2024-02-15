from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time

"""
Summary:
    This program uses selenium with the chrome webdriver to open up the url, and use the html
    elements to interact with the game. The program first verifies the site is running and that we
    have a connection to it, then verifies the order of the checkers in the game board. It then uses
    the move_piece() function to complete 5 moves, and waits until the messagebox shows "Make a move."
    to move again. The AI will always respond the same on each test, given the same user moves, so I 
    was able to hard-code the user moves. After the 5 user moves are completed, the restart button is 
    clicked and the program validates whether the checkers are in their initial position. Due to time 
    constraints and finicky behavior of the message box, I had to use static waits. With more time, 
    I would only use dynamic waits to cut down on testing time. I would also include checking for the
    validity of moves, additional handling for multi-jumps, verifying win conditions, and correct removal 
    of checkers. 
"""

# To run:
    # I used Python 3.9.1
    # pip install selenium
    # pip install webdriver_manager
    # Install browser driver (I used chromedriver) https://chromedriver.chromium.org/downloads

def move_piece(src, dest):
    # Get XPATH for source and destination squares
    src_XPATH = f'/html/body/div[1]/div[2]/div[1]/div[1]/div/div/div[{src[0]}]/img[{src[1]}]'
    dest_XPATH = f'/html/body/div[1]/div[2]/div[1]/div[1]/div/div/div[{dest[0]}]/img[{dest[1]}]'

    # Click the source square, wait until we can click destination square, then click destination square
    src_element = driver.find_element(By.XPATH, src_XPATH)
    
    src_element.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, dest_XPATH))).click()

    # If it's not the first move, wait until message box says we can make a move.
    try:
        wait.until(lambda driver: driver.find_element(By.ID, "message").text == "Make a move.")
    except TimeoutException:
        print("Timed out waiting for message to be 'Make a move.'")
    time.sleep(2)

def verify_restart():

    # Expected layout of checkers on board
    # 'P' represents the player's piece, 'C' represents the computer's piece, 'E' represents an empty space
    expected_layout = [
        ['C', 'E', 'C', 'E', 'C', 'E', 'C', 'E'],
        ['E', 'C', 'E', 'C', 'E', 'C', 'E', 'C'],
        ['C', 'E', 'C', 'E', 'C', 'E', 'C', 'E'],
        ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
        ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
        ['E', 'P', 'E', 'P', 'E', 'P', 'E', 'P'],
        ['P', 'E', 'P', 'E', 'P', 'E', 'P', 'E'],
        ['E', 'P', 'E', 'P', 'E', 'P', 'E', 'P']
    ]

    # Loop through html and create grid
    current_layout = []
    for row in range(8):
        current_row = []
        for col in range(8):
            piece = driver.find_element(By.NAME, f"space{7-col}{row}")
            src = piece.get_attribute('src')
            if 'you1.gif' in src:
                current_row.append('P')
            elif 'me1.gif' in src:
                current_row.append('C')
            else:
                current_row.append('E')
        current_layout.append(current_row)

    current_layout = current_layout[::-1] # Flip on y-axis

    # Check whether the current layout matches the expected layout and return
    for row in range(8):
        for col in range(8):
            if current_layout[row][col] != expected_layout[row][col]:
                return False
    return True

# set up ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open URL
driver.get("https://www.gamesforthebrain.com/game/checkers/")

# Set wait timeout to 10 sec.
wait = WebDriverWait(driver, 10)

time.sleep(2)
if verify_restart(): # Checking whether the pieces are in the right order
    print("The pieces are in the correct order.")
else:
    print("The pieces are NOT in the correct order.")

# Moves (AI will follow the same line every time)
move_piece((6,4), (5,5))
move_piece((5,5), (4,4))
move_piece((6,2), (4,4))
move_piece((6,6), (4,4))
move_piece((6,8), (5,7))
print("Successfully ran through 5 moves")

# Get the path of restart button and click it
restart_element = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[1]/p[2]/a[1]').click()
if verify_restart():
    print("The board has restarted correctly")
else:
    print("The board has NOT restarted correctly")

input("")

# Close browser
driver.quit()
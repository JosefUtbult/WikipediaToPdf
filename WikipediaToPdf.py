import os
import datetime

from sys import argv
from selenium import webdriver
from pyautogui import press
from time import sleep

# Insert the full path to the Downloads folder. On Windows it should be r"C:\Users\[Username]\Downloads"
#On Linux it should be /home/[Username]/Downloads
DOWNLOADPATH = r"C:\Users\josef\Downloads"
# DOWNLOADPATH = r"/home/josef/Downloads"

# Insert the full path to your gecko driver. Theese can be found at https://github.com/mozilla/geckodriver/releases
GECKODRIVERPATH = r'C:\Users\josef\Mega\Kod\Python\WikipediaToPdf\GeckodriverWindows\geckodriver.exe'
# GECKODRIVERPATH = '/home/josef/Python scripts/Wikipedia To Pdf/GeckodriverLinux/geckodriver'

def main():
    startValue = 0  # The first argument from start. Used to define where in the list the program shall start
    starTime = int(datetime.datetime.now().timestamp()) # Holds the time before running the download function
    deltaTime = 0   # Holds the calculated average time to download a page. Used to calculate an estimated time left
    nrOfArticlesDownloaded = 0  # The number of articles that has been downloaded this time running the program

    if len(argv) > 1:   # Adds a start value in the list if there is any

        try:
            startValue = int(argv[1])
        except:
            print("Define a startvalue")
            return -1

    print("Begin!")

    headers = openFile()    # Open the "headings.txt" file

    if not headers:         # Terminates the program if it just generated a "headings.txt" file
        return 0

    initErrorFile()         # Initializes the error file

    for i in range(startValue, len(headers)):

        # Generates an expected time left and prints some stuff
        print('Downloading "%s" (%d/%d)\t\tEstimated left: %s' % (headers[i].replace('_', ' '), i, len(headers), printTime(deltaTime * (len(headers) - i), nrOfArticlesDownloaded)))

        if not check_if_downloaded(headers[i]):                     # Checks if there already are a downloaded file with the headers name

            starTime = int(datetime.datetime.now().timestamp())     # Store the time before and after downloading the url and calculates an avrage
            downloadURL(headers[i])
            deltaTime = calculateDeltaTime(starTime, deltaTime, nrOfArticlesDownloaded)
            nrOfArticlesDownloaded += 1                             # Increments the number of downloaded articles

        else:
            print('"%s" is already downloaded.' % headers[i])


def printTime(secondsLeft, i):
    if i < 2:
        return "undefined"      # It can't calculate an accurate delta before at least two measurements, so it reurnss undefined

    else:

        output = ""             # Generates an output string, splits the hours, minutes and seconds from the seconds left (delta times nr of headings left) and puts the values between commas

        output += str(secondsLeft // 3600) + ":"
        secondsLeft = secondsLeft % 3600

        output += str(secondsLeft // 60) + ":"
        secondsLeft = secondsLeft % 60

        output += str(secondsLeft)

        return output


def calculateDeltaTime(startTime, deltaTime, i):

    # Generates a new delta by adding the time it took to download the last page (current time - startTime) to the old
    # deltaTime times the number of downloads before (i - 1) and divides it all with the total number of downloads
    # (Except if its zero, to not get a dividing by zero error)

    return int(((int(datetime.datetime.now().timestamp()) - startTime) + ((i - 1) * deltaTime)) / max(i, 1))


def downloadURL(header):

    driver = webdriver.Firefox(             # Opens the selenium webdriver with the file path to the geckodriver
        executable_path=GECKODRIVERPATH)
    driver.get(                             # Gets the site which is the following url with the header paste in as an argument
        'https://en.wikipedia.org/w/index.php?title=Special:ElectronPdf&page=%s&action=show-download-screen' % header)

    couldWrite = False                      # To make sure that it found at least one element with a submit

    for i in driver.find_elements_by_xpath("//*[@type='submit']"):
        try:
            i.click()           # Tries to activate the submit, aka "click" the button
            couldWrite = True

        except:
            pass

    press('enter')      # Presses the enter key to activate the "Do you really want to save" window
    sleep(5)            # Waits for good measure

    if not couldWrite or not check_if_downloaded(header):      # If it could not find a submit object or if it cant find any file with the headers name in downloads
        writeInErrorFile(header)                               # it writes it up in the error file
        print('Could not download the page "%s"' % header)
    else:
        print("Done")

    driver.quit()


def check_if_downloaded(header):
    for instance in os.listdir(DOWNLOADPATH):   # Goes through the downloaded folder

        if instance == header + '.pdf':         # If it finds a file with the same name as the header with the file ending pdf
            return True

    return False


def openFile():             # Open the "headings.txt" file if there exists one. Otherwise generates one and terminates the program
    if not checkFile():     # Checks if there are any "headers.txt" file

        print('Could not find "headings.txt". Generating new file. Go through the file to check correctness before '    # Prints some stuff
              'rerunning')
        writeFile(generate_URLs())  # Generates a new "headers.txt" file with the result from generate_URLs()
        print('Generated "headings-txt". Proofread the file before begining to download pdfs')

        return False    # Returns False for the program to terminate

    else:
        print('Found "headings.txt"\nBeginning to download')    # Returns the headers from the "headers.txt" file
        return readFile()


def initErrorFile():
    try:
        file = open("Errors.txt", "r")      # If it can't open the "Errors.txt" file as it dosn't exist
    except:
        file = open("Errors.txt", "w")      # Generates a new "Errors.txt" file and writes a start message
        file.write("Could not open pages:\n===========================\n")
        file.close()


def writeInErrorFile(heading):              # Writes the heading to the "Error.txt" file
    file = open("Errors.txt", "a")
    file.write(str(heading) + '\n')
    file.close()


def writeFile(headings):
    outputFile = open("headings.txt", "w")      # Opens the "headings.txt" file, goes through it and writes every header to it

    for instance in headings:
        outputFile.write(instance + '\n')

    outputFile.close()


def readFile():
    headings = []
    inputFile = open("headings.txt", "r")       # Opens the "headings.txt" file and appends every line to the headings

    while True:

        line = inputFile.readline()

        if (line == ""):
            break

        headings.append(line[:-1])

    inputFile.close()
    return headings


def checkFile():    # If the program can't read the "headers.txt" file it dosn't exist, and returns false
    try:
        open("headings.txt", "r")

        return True
    except IOError:
        return False


def generate_URLs():                # Generates the headings list from the most vital wikipedia site
    site = webdriver.Firefox(       # Opens the site as a selenium webdriver with the file path to the geckodriver
        executable_path=GECKODRIVERPATH)

    site.get('https://en.wikipedia.org/wiki/Wikipedia:Vital_articles')  # Gets the most vital wikipedia site

    headings = []                   # Creates the headings list

    groups = site.find_elements_by_class_name('multicol')       # Gets every element in the site with the class "mulitcol", which holds lists of every heading

    for group in groups:

        elements = group.find_elements_by_tag_name('li')        # Gets every element in the current group of the type "li"

        for element in elements:                                # Gets every "a" element int the current "li" element and
                                                                # extracts the text from its attribute "title", which is the heading of that page.
                                                                # Also replaces the spaces with underlines to make it url compatible

            headings.append(element.find_element_by_tag_name('a').get_attribute('title').replace(' ', '_'))

    site.quit()
    return headings


if __name__ == '__main__':
    main()

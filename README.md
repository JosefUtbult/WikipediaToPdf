# WikipediaToPdf

## Introduction
This is a program used to generate a list of the one thousand most vital articles from wikipedia and download them as pdf.
It uses https://en.wikipedia.org/wiki/Wikipedia:Vital_articles to generate the list and then pulls it down using firefox
and the selenium python library. In order to do this it uses the gecko drivers from https://github.com/mozilla/geckodriver/releases
These are included for Windows and Linux, but can also be downloaded manualy.

## Usage
To use this software the following is needed:

        1. The python file WikipediaToPdf.py
        
        2. The gecko drivers
        
        3. The selenium python library
        
        4. The pyautogui python library
        
        5. The time python library

First download the git folder. Then edit the parameters DOWNLOADPATH and GECKODRIVERPATH to refer to the download path and the path to
the gecko driver. Then run and leave for itself. The program will try to download every instance of headers in the "headers.txt" file,
and if is unsuccessful to do so, it will append the header to the "Errors.txt" file  for later inspection and validation.

## Tips
As the software needs to open new windows and press button it is not possible to be actively using the same environment as the program.
I therefore recommend you to run the software on an unused computer or on a virtual machine.

I also recommend you to run the software a couple of times, as an insufficient internet connection can make it unable to download a
certain page at a certain time. If run multiple times it will check for every page in the downloaded folder and skip every page that
already is there.

If you intend to use the pdf files in any way, I strongly recommend you to donate to the Wikipedia Foundation.

By Josef Utbult

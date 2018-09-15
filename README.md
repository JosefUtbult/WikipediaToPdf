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
the gecko driver. 

Upon execution the program will search for a file named “headers.txt” that contains a list of names of the article it shall download. If you want, you can keep the “headers.txt” file that is included in the project, but if you rather download an up to date version you can just delete the included file. Then the program will fail to find the file and generate a new one from The most vital articles page from Wikipedia. The program will terminate and have generated the “headers.txt” file. Go through the document and make sure that every instance is correct. The generating process makes some mistakes and have a bad time trying to comprehend special characters. When done, execute the program again and let it run. 

The program will try to download every instance of headers in the "headers.txt" file,
and if is unsuccessful to do so, it will append the header to the "Errors.txt" file  for later inspection and validation.

## Tips
You can define a starting value for the program to begin at any index in the “headers.txt” file. Just write the prefered number as an argument upon execution.

As the software needs to open new windows and press button it is not possible to be actively using the same environment as the program.
I therefore recommend you to run the software on an unused computer or on a virtual machine.

I also recommend you to run the software a couple of times, as an insufficient internet connection can make it unable to download a
certain page at a certain time. If run multiple times it will check for every page in the downloaded folder and skip every page that
already is there.

If you intend to use the pdf files in any way, I strongly recommend you to donate to the Wikipedia Foundation.

By Josef Utbult

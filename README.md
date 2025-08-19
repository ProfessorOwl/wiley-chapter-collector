# Wiley Chapter Collector
## Introduction
On Wiley you can only download books and "chaptered" articles chapter by chapter. This gets really annoying if you want to download multiple books. This is where this python script comes in.

## Dependencies
You will have to install the following packages:
```bash
pip install bs4
pip install selenium
pip install seleniumbase
pip install PyPDF2
```
## How it works
Choose a url to a book, like this one: https://onlinelibrary.wiley.com/toc/15213781/2025/59/4

This has to be given to the function `wileygetter`, along with a directory for the download path.
The script will first collect all the pdfs from the corresponding chapters and will finally merge them together. 

## To be done (but probably not by me)
- Implement a log-in procedure, so that you can download books with your own profile. My use case is that having a specific IP adress gives me acces to the files I am interested in, so I didn't need to bother with a login.
    - This could probably also be done by logging into the site once with `seleniumbase`, then downloading the cookies and adding them to session for downloading the files. This would probably be faster.
- Make it not start the chrome browser in front of everything else. The PC this runs on is pretty much useless.
  

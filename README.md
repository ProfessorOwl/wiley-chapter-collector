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
- Command line interface for downloading the chapters of a single book
- Option to remove the folder with the pdfs of every chapter
  
## Thanks
Thanks to [ashaherb's repository](https://github.com/ashaherb/Wiley-Downloader) for the inspiration! I didn't get his script to run, because it always spit out errors of some kind. But the structure in my project remains pretty much the same.

## Feedback
I would like to have feedback to this project! I will only update it for my usecases if I don't hear from any other person using it. So please tell me the problems that you have (and make a pull request if you want to)!

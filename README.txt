Installation instructions

Prequisites:
Python 3.8.10 or higher


1. Installing the libraries
	- Windows: run the command: pip install -r requirements.txt
2. Running the program. [arg1] is for the url [arg2] is optional and specifies how many times should we crawl the url
	- Windows: run the command: py crawler.py [arg1] [arg2] 
	- Linux: run the command: python3 crawler.py [arg1] [arg2]
3. Exiting the program:
	- Press crtl+c to exit. This will throw an error but will exit the program
        - Specify in [arg2] number of crawls before exiting


Testing:
1. In the root folder,
	- Windows: run the command: pytest
	- Linux: run the command: python3 -m pytest
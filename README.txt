Installation instructions

Prequisites:
Python 3


1. Installing the libraries
	- run the command: pip install -r requirements.txt
2. Running the program. [arg1] is for the url [arg2] is optional and specifies how many times should we crawl the url
	- Windows: run the command: py crawler.py [arg1] [arg2] 
	- Linux: run the command: python crawler.py [arg1] [arg2]
3. Exiting the program:
	- Press crtl+c to exit. This will throw an error but will exit the program
        - Specify in [arg2] number of crawls before exiting


Testing:
1. In the root folder, run the command: pytest
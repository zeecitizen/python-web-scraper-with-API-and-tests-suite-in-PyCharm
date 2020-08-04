# Python Code - Understanding the approach 
### This document explains the approach taken to implement code for Service Funnel Web Scraper With API and Tests Suite In PyCharm


## Details of the problem
	See the other README to understand the requirements specification for this project. This document is for the implementation only.

## Details of the approach we took to implement the code
	A test-driven-approach was taken to implement the code. After writing an initial test suite to start coding, we proceed with initially parsing the json and maintaining the
	hashes of the tags. Two hashes are then maintained. One for checking if the whole search tags 
	are matching with any of the input tags and also maintaing the refernce tags. The other one 
	is for partial matching

## Explaining our choice of Data Structure
	The data structures used for this in Dictionary / HashMaps to store the data and to reduce the
	complexity to O(1), which is constant time.

## Which IDE was used in Development. What tools should we have on our computer installed for this code to run.
	The IDE used to run this code was PyCharm and the noteable libraries used in this
	code are:
	1. BeautifulSoup
	2. itertools

## Step-by-Step guide: How to run this Code? 
	There are two ways to run the code.
	a. Through main.py
		1. Go the folder containing the main.py file
		2. Navigate terminal to same directory
		3. Run the command  'python3 main.py'

	b. Through sample test cases.
		1. Open PyCharm
		2. Goto the test folder and open
			i. 	test_1.py
			ii. test_2.py
			iii.test_3.py
			iv. test_4.py 
		3. Run the main function of each test cases to see the test results

## How, IF have we ensured "scrape_html is as performant as possible."
	1.  To make scrape_html performant, two different dictionaries are used
		to save the data: 
			i. 	complete_match
			ii.	partial_match
	2.	The first step was to parse the html using the bs4
	3.	The next was to maintain the refernce tags for every key tags,
		Hence making its complexity constant to get the subsets of the
		search tags within the key tags of dictionary
	4.	The next step to maintain a dict for partial tags and unique subset tags
	5.	Same as above after creating the dict with the partial and unique subsets
		the next step was to make subset tags accessible in constant time. So they
		were fetched out and saved in the dictionary as well w.r.t its keys
	6. 	All of this preprocessing reduced the complexity of handle_request to O(1)


## How, IF have we ensured "handle_request has constant time complexity."
	This thing was ensured by doing all the pre-processing and maitainng hashes of
	tags where possible to make handle_request not to do any iterations. Merely
	uses hashes to access all the data.

## A comment on the test cases and the approach we took to write the tests
	There are total of 4 sample test with 3 test cases each, making it 12 in total
	These test cases are built keeping in acccoun the boundary use cases and the 
	edge cases. The basic approach was using black box testing technique.
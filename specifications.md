### NASA ADS Client

Sometimes you don't want to pull up a browser to find a reference
or generate a AASTeX citation. This tool is a simple commandline 
interface for navigating ADS.

### What it needs to do
- Handle basic queries
- Easily copy bibliography information to the clipboard
- Config file for defaults

### Basic Interface
Loading configuration file..............[DONE]
Loading API_KEY file....................[FAIL]
Please go to your NASA/ADS account and retrieve
your API key. This will be stored in 
	~/.ads_cli.txt
by default. Is there another path you'd like it to take? [Y/N]
N
Please enter your API key:
asdfaslkjlii1923jalsfadsfasdf

File ~/.adi_cli.txt created.............[DONE]
Keywords:
Authors:
Title:
Year:

--------------------------------RESULTS---------------------------------
1. Paper 1 Title - Author 1, Author 2
	 Lorem ipsum dolor sit amet, consectetur adipiscing elit,
	 sed do eiusmod tempor incididunt ut labore et dolore magna 
	 aliqua. Ut enim ad minim veniam, ...
2. Paper 2 Title - Author 1, Author 2
	 Lorem ipsum dolor sit amet, consectetur adipiscing elit,
	 sed do eiusmod tempor incididunt ut labore et dolore magna 
	 aliqua. Ut enim ad minim veniam, ...
3. Paper 3 Title- Author 1, Author 2
	 Lorem ipsum dolor sit amet, consectetur adipiscing elit,
	 sed do eiusmod tempor incididunt ut labore et dolore magna 
	 aliqua. Ut enim ad minim veniam, ...

You may:
	Press [n] for next page of results.
	Press [s] to start a new search.
	Press [q] to quit this application.
	Enter a number for the relevant publication followed by:
		Nothing - Gives a summary page
		b - gives the default bib. info. [AAS/TeX] and copies to clipboard
		B - gives choice of bibliography template
		a - gives abstract
3b
Copy bib. info. to clipboard............[DONE]
You may:
	Press [n] for next page of results.
	Press [s] to start a new search.
	Press [q] to quit this application.
q
Exiting.................................[DONE]

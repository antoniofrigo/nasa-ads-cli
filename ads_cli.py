import os
import requests
import readline
import textwrap
from configparser import ConfigParser
import formatting as fmt

class ADS_CLI():
    def __init__(self):
        self.config_path = "ads_cli_config.txt"

        # SEARCH
        self.bib_style = "aastex"
        self.num_results = 32

        # INTERFACE
        self.num_cols = 72
        self.show_abstract = False
        self.num_lines_abs = 3
        self.results_per_page = 8
        self.show = {
            'title': 1,
            'author': 1,
            'abstract': 1,
            'bibcode': 1,
            'pubdate': 1,
            'citation': 1
        }

        # API
        self.api_key = ""
        self.returned = 'bibcode,author,pubdate,title, abstract, citation_count'

        self.all_article = {}
        self.max_ind = 0
        self.exit = False

    def load_config(self):
        # Loads configuration file
        parser = ConfigParser()
        parser.read(self.config_path)

        self.bib_style = parser.get("SEARCH","bib_style")
        self.api_key = parser.get("API","api_key")

        self.num_lines_abs = int(parser.get("INTERFACE","num_lines_abs"))
        self.num_cols = int(parser.get("INTERFACE","num_cols"))

        fmt.print_done("Loading config. file: {0}".format(self.config_path),
                        self.num_cols)

    def check_api(self):
        # Checks whether API key exists and prompts user if not
        while len(self.api_key) != 40:
            fmt.print_fail("Loading API_KEY", self.num_cols)
            self.api_key = input("Please enter your API Key "
                                 "(you will only need to do this once):\n"
                                 .expandtabs())

        parser = ConfigParser()
        parser.read(self.config_path)
        parser.set("API", "api_key", self.api_key)
        with open(self.config_path, 'w') as config_file:
            parser.write(config_file)

        fmt.print_done("Loading API_KEY", self.num_cols)

    def ads_prompt(self):
        fmt.print_load("Search", self.num_cols)
        prompt = fmt.color(" ADS", 'OKCYAN') + fmt.color(" > ", "MAGENTA")
        query = input(prompt)
        headers = { 'Authorization':
                   'Bearer:{0}'.format(self.api_key)}
        params = ( ('q', query),('rows', self.num_results) , ('fl', self.returned))
        response = requests.get('https://api.adsabs.harvard.edu/v1/search/query', headers=headers, params=params)
        fmt.print_load("Result", self.num_cols)

        self.all_article = response.json()['response']['docs']
        self.max_ind = len(self.all_article)

        self.show_results(1)

    def show_results(self, page_num):
        if (page_num * self.results_per_page > self.num_results):
            print("Error: Undefined page.")
        else:
            total = (self.num_results + 1)//self.results_per_page
            start = (page_num - 1) * self.results_per_page
            end = page_num  * self.results_per_page
            for i in range(start, end):
                fmt.print_article(self.all_article[i], i+1, self.max_ind, self.show,
                                  self.num_cols)
            fmt.print_done("Fetching page {0} of {1}".format(page_num, total), 
                           self.num_cols)

    def cmd_prompt(self):
        prompt = fmt.color(" CMD", 'OKCYAN') + fmt.color(" > ", "MAGENTA")
        result = input(prompt)

        text  = result.strip('0123456789')
        l_ind = len(result) - len(result.lstrip('0123456789'))
        r_ind = l_ind + len(text)
        left =  result[0:l_ind]
        right = result[r_ind:]

        if (result == 'q' or result == 'quit' or result == 'exit'):
            self.exit = True
        elif (left != '' and text != '' and right == ''):
            self.handle_article(int(left), text)
            self.cmd_prompt()
        elif (left == '' and text != '' and right != ''):
            self.handle_page(text, int(right))
        elif (left != '' and text == '' and right == ''):
            left = int(left)
            self.handle_number(left)
        elif (left == '' and text != '' and right == ''):
            self.handle_text(text)
        else:
            print("Undefined input: {0}".format(result))
            self.cmd_prompt()

    def get_bibliography(self, index, bib_type):
        headers = { 'Authorization':
                   'Bearer:{0}'.format(self.api_key)}
        data = '{"bibcode":["2015RaSc...50..916A"]}'
        response = requests.post(
                                 'https://api.adsabs.harvard.edu/v1/export/{0}'.format(bib_type), 
                                 headers=headers, data=data)
        fmt.print_bibliography(response.json(), self.num_cols)

    def handle_article(self, left, text):
        if (text == 'b'):
            self.get_bibliography(left, self.bib_style)
        else:
            print("Undefined input: {0}".format(text))

    def handle_number(self, number):
        if number > self.max_ind:
            print("Out of Bounds: {0}, Max: {1}".format(number, self.max_ind))
        else:
            article = self.all_article[number - 1]
            show = {
                'title': 10,
                'author': 3,
                'abstract': 10,
                'bibcode': 1,
                'pubdate': 1,
                'citation': 1
            }
            fmt.print_article(article, number, number, show,
                              self.num_cols)
        self.cmd_prompt()

    def handle_page(self, text, right):
        if (text == 'p'):
            self.show_results(right)
        else:
            print("Undefined input: {0}".format(text))
        self.cmd_prompt()

    def handle_text(self, text):
        if (text == 's' or text == 'search'): # Search again 
            self.ads_prompt() 
            self.cmd_prompt()
        elif (text == 'r' or text == 'repeat'): 
            for i in range(0, self.max_ind):
                fmt.print_article(self.all_article[i], i+1, self.max_ind, self.show,
                              self.num_cols)
            self.cmd_prompt()
        else:
            print("Undefined input: {0}".format(text))
            self.cmd_prompt()
        
    def run(self):
        # Runs entire script
        fmt.print_load("Preliminary Checks", self.num_cols)
        self.load_config()
        self.check_api()
        self.ads_prompt()
        self.cmd_prompt()

ads = ADS_CLI()
ads.run()

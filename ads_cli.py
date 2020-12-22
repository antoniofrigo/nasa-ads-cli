import os
import sys
import requests
import readline
import textwrap
from configparser import ConfigParser
import formatting as fmt
import configuration as conf

class ADS_CLI():
    def __init__(self):
        self.config_path = "ads_cli_config.txt"
        # The following will be defined after configuration load
        # SEARCH:
        #   num_results: int, results_per_page: int, database: str
        # INTERFACE:
        #   num_cols: int, show: Dict
        # API:
        #   api_key: str

        self.returned = 'bibcode,author,pubdate,title, abstract, citation_count'
        self.all_article = {}
        self.max_ind = 0
        self.prompt = 1 # 0 = don't show ADS prompt, 1 = show ADS prompt
        self.exit = False

    def load_config(self):
        # Loads configuration file
        conf.check_config_file(self.config_path)
        parser = ConfigParser()
        parser.read(self.config_path)
        conf.check_config_values(parser)

        self.set_config(parser)
        fmt.print_done("Loading config. file: {0}".format(self.config_path),
                        self.num_cols)

    def set_config(self, parser):
        # SEARCH
        self.num_results = parser.getint('SEARCH', 'num_results', fallback=32)
        self.results_per_page = parser.getint('SEARCH', 'results_per_page',fallback= 8)
        self.database = parser.get('SEARCH', 'database', fallback='astronomy')

        # INTERFACE
        self.show = {}
        self.num_cols = parser.getint('INTERFACE', 'num_cols', fallback=72)
        self.show['title'] = parser.getint('INTERFACE', 'lines_title', fallback=1)
        self.show['author'] = parser.getint('INTERFACE', 'lines_author', fallback=1)
        self.show['abstract'] = parser.getint('INTERFACE', 'lines_abstract', fallback=1)
        self.show['bibcode'] = parser.getint('INTERFACE', 'show_bibcode', fallback=1)
        self.show['pubdate'] = parser.getint('INTERFACE', 'show_pubdate', fallback=1)
        self.show['citation'] = parser.getint('INTERFACE', 'show_citation', fallback=1)

        # BIBLIOGRAPHY
        self.bib_style = parser.get('BIBLIOGRAPHY', 'bib_style', fallback='aastex')
        self.clipboard = parser.get('BIBLIOGRAPHY', 'clipboard', fallback='clipboard')
        self.single_line = parser.getint('BIBLIOGRAPHY', 'single_line', fallback=0)
        self.term_show = parser.getint('BIBLIOGRAPHY', 'term_show', fallback=1)

        # API
        self.api_key = parser.get('API', 'api_key', fallback='')

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
        # NASA/ADS Query Prompt
        fmt.print_load("Search", self.num_cols)
        prompt = fmt.color(" ADS", 'OKCYAN') + fmt.color(" > ", "MAGENTA")
        query = input(prompt)

        headers = { 'Authorization': 'Bearer:{0}'.format(self.api_key)}
        params = (('q', query),
                  ('rows', self.num_results), 
                  ('fl', self.returned),
                  ('fq', self.database))
        url = 'https://api.adsabs.harvard.edu/v1/search/query'
        response = requests.get(url, headers=headers, params=params)
        fmt.print_load("Result", self.num_cols)

        self.all_article = response.json()['response']['docs']
        self.max_ind = len(self.all_article)
        self.show_results(1)

    def show_results(self, page_num):
        total = (self.max_ind)//self.results_per_page 
        total += (self.max_ind % self.results_per_page != 0)

        if (page_num * self.results_per_page > self.num_results):
            fmt.print_error("Page undefined.", self.num_cols)
        elif self.max_ind == 0:
            fmt.print_load("No Results Found", width = self.num_cols, fill=" ")
        else:
            start = (page_num - 1) * self.results_per_page
            end = min(page_num  * self.results_per_page, self.max_ind)
            for i in range(start, end):
                fmt.print_article(self.all_article[i], i+1, self.max_ind, self.show,
                                  self.num_cols)

            text = "Fetching page {0} of {1}".format(page_num, total)
            fmt.print_done(text, self.num_cols)

    def cmd_prompt(self):
        prompt = fmt.color(" CMD", 'OKCYAN') + fmt.color(" > ", "MAGENTA")
        result = input(prompt)

        left, text, right = fmt.split_cmd_input(result)

        if (result == 'q' or result == 'quit' or result == 'exit'):
            self.exit = True
        elif (left != '' and text != '' and right == ''):
            self.handle_article(int(left), text)
            self.prompt = 0
        elif (left == '' and text != '' and right != ''):
            self.handle_page(text, int(right))
        elif (left != '' and text == '' and right == ''):
            left = int(left)
            self.handle_number(left)
        elif (left == '' and text != '' and right == ''):
            self.handle_text(text)
        else:
            print("Undefined input: {0}".format(result))
            self.prompt = 0

    def get_bibliography(self, index, bib_type):
        headers = { 'Authorization':
                   'Bearer:{0}'.format(self.api_key)}
        bibcode = self.all_article[index]['bibcode']
        data = {"bibcode": bibcode}
        response = requests.post(
                                 'https://api.adsabs.harvard.edu/v1/export/{0}'.format(bib_type), 
                                 headers=headers, data=data)
        fmt.print_bibliography(response.json(), 
                               self.num_cols, 
                               self.clipboard,
                               self.single_line,
                               self.term_show)

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
        self.prompt = 0

    def handle_page(self, text, right):
        if (text == 'p'):
            self.show_results(right)
        else:
            print("Undefined input: {0}".format(text))
        self.prompt = 0

    def handle_text(self, text):
        if (text == 's' or text == 'search'): # Search again 
            self.prompt = 1
        elif (text == 'r' or text == 'repeat'): 
            for i in range(0, self.max_ind):
                fmt.print_article(self.all_article[i], i+1, self.max_ind, self.show,
                              self.num_cols)
            self.prompt = 0
        else:
            print("Undefined input: {0}".format(text))
            self.prompt = 0
        
    def run(self):
        # Runs entire script
        try:
            fmt.init_art()
            fmt.print_load("Preliminary Checks", 72)
            self.load_config()
            self.check_api()
            while self.exit != True:
                if (self.prompt == 1):
                    self.ads_prompt() 
                self.cmd_prompt()
        except KeyboardInterrupt:
            print("\n")
            sys.exit(0)

if __name__ == "__main__":
    ads = ADS_CLI()
    ads.run()

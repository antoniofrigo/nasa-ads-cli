from configparser import ConfigParser
import os

def get_default_config():
    config = ConfigParser()

    # SEARCH
    config.add_section('SEARCH')
    config.set('SEARCH', 'num_results', '32')
    config.set('SEARCH', 'results_per_page', '8')
    config.set('SEARCH', 'database', 'astronomy')

    # INTERFACE
    config.add_section('INTERFACE')
    config.set('INTERFACE', 'num_cols', '72')
    config.set('INTERFACE', 'lines_title', '1')
    config.set('INTERFACE', 'lines_author', '1')
    config.set('INTERFACE', 'lines_abstract', '1')
    config.set('INTERFACE', 'show_bibcode', '1')
    config.set('INTERFACE', 'show_pubdate', '1')
    config.set('INTERFACE', 'show_citation', '1')

    # BIBLIOGRAPHY
    config.add_section('BIBLIOGRAPHY')
    config.set('BIBLIOGRAPHY', 'bib_style', 'aastex')
    config.set('BIBLIOGRAPHY', 'clipboard', 'clipboard')
    config.set('BIBLIOGRAPHY', 'single_line', '0')
    config.set('BIBLIOGRAPHY', 'term_show', '1')

    # API
    config.add_section('API')
    config.set('API', 'api_key', "")

    return config

def write_default_config(path):
    # If configuration file not found, write this default one
    config = get_default_config()
    with open(path, 'w') as config_file:
        config.write(config_file)

def check_config_file(path):
    # Check if config file exists and create if not
    if not os.path.exists(path):
        write_default_config(path)

def check_config_values(config):
    # Checks all configuration parameters for suitable values 
    # and errors out if not.
    
    # SEARCH
    if config.getint('SEARCH', 'num_results') < 0:
        raise ValueError('num_results must be nonnegative')
    if config.getint('SEARCH', 'results_per_page') < 0:
        raise ValueError('results_per_page must be nonnegative')
    if config.get('SEARCH', 'database') not in ['astronomy', 'physics', 'general']:
        raise ValueError('database must be one of: astronomy, physics, general')

    # INTERFACE
    if config.getint('INTERFACE', 'num_cols') < 50:
        raise ValueError('num_cols must be greater than or equal to 50')
    if config.getint('INTERFACE', 'lines_title') < 0:
        raise ValueError('lines_title must be nonnegative')
    if config.getint('INTERFACE', 'lines_author') < 0:
        raise ValueError('lines_author must be nonnegative')
    if config.getint('INTERFACE', 'lines_abstract') < 0:
        raise ValueError('lines_abstract must be nonnegative')
    config.getboolean('INTERFACE', 'show_bibcode')
    config.getboolean('INTERFACE', 'show_pubdate')
    config.getboolean('INTERFACE', 'show_citation')

    # BIBLIOGRAPHY
    bib_types = ['bibtext', 'bibtexabs', 'ads', 'endnote', 'procite', 'ris',
                 'refworks', 'rss', 'medlars', 'dcxml', 'refxml', 'refabsxml',
                 'aastex', 'icarus', 'mnras', 'soph', 'votable']
    clips = ['primary', 'secondary', 'clipboard']

    if config.get('BIBLIOGRAPHY', 'bib_style') not in bib_types:
        raise ValueError("bib_style must be one of {0}".format(bib_types))
    if config.get('BIBLIOGRAPHY', 'clipboard') not in clips:
        raise ValueError("bib_style must be one of {0}".format(clips))
    config.getboolean('BIBLIOGRAPHY', 'single_line')

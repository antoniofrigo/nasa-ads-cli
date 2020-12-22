import textwrap as tw
import subprocess
import sys
import os
# Specially formatted prints

def init_art():
    # Nice and pretty ASCII art on initialization
    art = [
    "                   **********                                           ",
    "                 **************                                         ",
    "                ****         ****                                       ",
    "                **             ***   *            *****                 ",
    "                **              **                      ***             ",
    "                **             ***                          **          ",
    "                ***           ***  ****************          **        ",
    "                ******    ******   *********************        **      ",
    "                   ************  ****((((((((((/**********        **    ",
    "                 *   ****** *****(((((//////////////********       **   ",
    "                *       *******((////           ////((*******       **  ",
    "               **      ******((////               /(((((******       ** ",
    "               *      ******((////     //////     ((((///******      ** ",
    "              **      ******((/////////           ((/////******       * ",
    "              **      ******((/////       //(     ///////******       * ",
    "               *      ******((////     /(((((     ///////******      ** ",
    "                      *******((///                //////******       ** ",
    "                       *******((((((       (//     ////******/      **  ",
    "                  *  ***/*******((((((((((///////////*******       **   ",
    "             /*******///   ********/(((///////////********        **    ",
    "          **********//       ***************************        **      ",
    "      ***********///             *******************          **        ",
    "  ***********///                                            **          ",
    "  *******///               ***                          ***             ",
    "   /////                       *****              ****/                 ",
    "                                         ***                            "]

    print("\n")
    for line in art:
        print(line)
    print("\n")
    print_load("An Unofficial Command Line Interface for NASA/ADS", 72,
               fill = " ", text_color = 'WARNING')
    print("\n")

def color(text, color):
    # Colors text using terminal codes
    codes = {'HEADER' : '\033[95m',
             'OKBLUE' : '\033[94m',
             'OKCYAN' : '\033[96m',
             'OKGREEN': '\033[92m',
             'WARNING': '\033[93m',
             'MAGENTA': '\033[95m',
             'FAIL'   : '\033[91m',
             'ENDC'   : '\033[0m' ,
             'BOLD'   : '\033[1m' ,
             'ITALIC' : '\033[3m' ,
             'UNDERLINE': '\033[4m',
             'NONE': '',
             }
    return "{0}{1}{2}".format(codes[color],text,codes['ENDC'])

def copy_to_clipboard(text, width, clipboard):
    # Handles clipboards for different operating systems
    # Windows is not supported.
    flag = 0
    if sys.platform.startswith('freebsd'):
        process = subprocess.Popen(['xclip', '-selection', clipboard],
                             stdin=subprocess.PIPE, close_fds=True)
        process.communicate(input=text.encode('utf-8'))
    elif sys.platform.startswith('linux'):
        process = subprocess.Popen(['xclip', '-selection', 'clipboard'],
                             stdin=subprocess.PIPE, close_fds=True)
        process.communicate(input=text.encode('utf-8'))
    elif sys.platform.startswith('win32'):
        print_warning("Windows is not supported.", width)
        flag = 1
    elif sys.platform.startswith('cygwin'):
        print_warning("Cygwin is not supported.", width)
        flag = 1
    elif sys.platform.startswith('darwin'):
        process = subprocess.Popen(['pbcopy', 'w'],
                             stdin=subprocess.PIPE, close_fds=True)
        process.communicate(input=text.encode('utf-8'))
    else:
        print_warning("OS not supported.", width)
        flag = 1
    return flag

def print_done(text, width):
    # Job competed message
    done = "[" + color('DONE', 'OKGREEN') + "]"
    dots = "." * (width - len(text) - len("\t".expandtabs()) - 6)
    print("\t" + text + dots + done)

def print_fail(text, width):
    # Job failed message
    fail = "[" + color("FAIL", 'FAIL') + "]"
    dots = "." * (width - len(text) - len("\t".expandtabs()) - 6)
    print("\t" + text + dots + fail)

def print_load(text, width, fill="-", text_color='NONE'):
    # Prints bar of hyphens with text centered
    left = fill * ((width - len(text))//2)
    right = fill * (width - len(text) - len(left))
    print(left + color(text.upper(), text_color) + right)

def print_warning(text, width):
    # Prints error message
    text = "WARNING: " + text
    text = color(text.center(width, " "), "WARNING")
    print(text)

def print_error(text, width):
    # Prints error message
    text = "ERROR: " + text
    text = color(text.center(width, " "), "FAIL")
    print(text)

def shorten_end(text_list, width, num_item):
    # Clips the enter of wrapped paragraph and adds placeholder if needed
    placeholder = " [...]"
    mod_width = width - len(placeholder)
    if num_item < len(text_list):
        text_list = text_list[0:num_item]
        text_list[-1] = tw.shorten(text_list[-1], width = mod_width,
                                   placeholder="") + placeholder
    return text_list

def print_bibliography(response, width, clipboard, single_line, term_show):
    msg = response['msg']
    if not single_line:
        export = tw.fill(response['export'])
    else:
        export = response['export']
    print_done("Fetching bibliography", width)

    flag = copy_to_clipboard(export, width, clipboard)
    if flag ==  0:
        print_done("Copying to clipboard", width)
    elif flag ==  1:
        print_fail("Copying to clipboard", width)

    if term_show:
        print_load("Bibliography Entry", width, fill=" ", text_color="UNDERLINE")
        print(export)


def print_article(article, index, max_ind, show, width):
    num = str(index).rjust(len(str(max_ind)) + 1) + ". "
    col_remain = width - len(num)
    indent = " " * len(num)
    delim = "\n" + indent

    # Title
    if article['title'][0] and show['title'] > 0:
        title_w = tw.wrap(article['title'][0], width = col_remain)
        title_w = shorten_end(title_w, col_remain, show['title'])
        title = delim.join(title_w) + "\n"
        title = color(color(title, 'BOLD'),'OKCYAN')
    else :
        title = ""

    # Author
    if 'author' in article and show['author'] > 0:
        author_w = tw.wrap("; ".join(article['author']), width = col_remain - 5)
        author_w = shorten_end(author_w, col_remain, show['author'])
        author = indent + delim.join(author_w)
        author = color(author, "ITALIC")
    else :
        author = ""

    # Abstract
    if 'abstract' in article and show['abstract'] > 0:
        abstract_w = tw.wrap("   " + article['abstract'], width = col_remain)
        abstract_w = shorten_end(abstract_w, col_remain, show['abstract'])
        abstract = delim + delim.join(abstract_w)
    else :
        abstract = ""

    # Citation Bibcode Date
    if 'pubdate' in article and show['pubdate'] > 0:
        pubdate = article['pubdate']
    else:
        pubdate = ''
    if 'citation_count' in article and show['citation'] > 0:
        citation = str(article['citation_count']) + " cit."
    else:
        citation = ''
    if 'bibcode' in article and show['bibcode'] > 0:
        bibcode = article['bibcode']
        space_len = col_remain - len(bibcode) - len(citation) - len(pubdate)
        spaces  = " "*(space_len//2)
        pubdate += spaces + article['bibcode']
    spaces = " " * (col_remain - len(citation) - len(pubdate))
    citation_date = delim + pubdate + spaces + citation

    # Final output
    output = num + title + author + abstract + citation_date + "\n"
    print(output)

def split_cmd_input(result):
    text  = result.strip('0123456789')
    l_ind = len(result) - len(result.lstrip('0123456789'))
    r_ind = l_ind + len(text)
    left =  result[0:l_ind]
    right = result[r_ind:]

    return left, text, right

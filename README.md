```
                   **********                                           
                 **************                                         
                ****         ****                                       
                **             ***   *            *****                 
                **              **                      ***             
                **             ***                          **          
                ***           ***  ****************          **        
                ******    ******   *********************        **      
                   ************  ****((((((((((/**********        **    
                 *   ****** *****(((((//////////////********       **   
                *       *******((////           ////((*******       **  
               **      ******((////               /(((((******       ** 
               *      ******((////     //////     ((((///******      ** 
              **      ******((/////////           ((/////******       * 
              **      ******((/////       //(     ///////******       * 
               *      ******((////     /(((((     ///////******      ** 
                      *******((///                //////******       ** 
                       *******((((((       (//     ////******/      **  
                  *  ***/*******((((((((((///////////*******       **   
             /*******///   ********/(((///////////********        **    
          **********//       ***************************        **      
      ***********///             *******************          **        
  ***********///                                            **          
  *******///               ***                          ***             
   /////                       *****              ****/                 
                                         ***                            


           AN UNOFFICIAL COMMAND LINE INTERFACE FOR NASA/ADS   
```
*Getting a bibliography reference should not require a web browser...*

### Usage Instructions

Run the script with `python3 ads_cli.py`.

On the first initialization, the script will prompt for the API_KEY from
NASA/ADS. This can be found in the user settings on their website. 

There are two types of prompts. The first is the ADS search prompt, as 
shown below. This prompt is used to query the database to compute
``` 
 ADS >
```
Enter your query as you would with the standard ADS website. The first page of results
will then be shown and you'll be given a command prompt
```
 CMD >
```
List of commands:
- `q`, `exit`, `quit`: quits the utility
- `s`, `search`: perform another search
- `r`: display all results at ocne
- `[index]`: displays more detailed information about a specific paper with that index
- `p[page_number]`: go  to page 'page_number'
- `[index]b`: copy bibliographic information and copy to clipboard

### Configuration

On the first initialization, a configuration file `ads_cli_config.txt` will be
generated. The default configuration is as follows:
```
[SEARCH]
num_results = 32 # Number of results per query (integer > 0)
results_per_page = 8 # Number of results per age (integer > 0)
database = astronomy # One of 'astronomy', 'physics', 'general'

[INTERFACE]
num_cols = 72 # Max number of columns
lines_title = 1 # Total lines of title shown (at maximum)
lines_author = 1 # Total lines of author shown (at maximum)
lines_abstract = 1 # Total lines of abstract shown (at maximum)
show_bibcode = 1 # Whether or not to show bibcode (0 or 1)
show_pubdate = 1 # Whether or not to show publication date (0 or 1 )
show_citation = 1# Whether or not to show citation count (0 or 1 )

[BIBLIOGRAPHY]
bib_style = aastex # Default bib. style (i.e. aastex, bibtex, etc)
clipboard = clipboard # Type of system keyboard on Unix (primary, secondary, clipboard)
single_line = 0 # Whether to automatically wrap citations based on num_cols
term_show = 1 # Whether to show bib. information in terminal

[API]
api_key = # API Key (you will be prompted for this)
```

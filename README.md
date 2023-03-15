# RoScraperPDF
Small Python project for scraping info from pdf files on web

1. Run a cron script several times a day
2. Request to the specified web page and check for posting new pdf files
3. Downloading and opening new files
4. Search in files and clean up the necessary information (using regular expressions)
5. Connecting to the bubble.io api service and adding the necessary information from files and links to them to the     
   database
6. Logging the work of the scraper to a log file
7. Sending messages to the admin about the completed work of the script via telegram bot
8. Deploy and configure the script for hosting. 

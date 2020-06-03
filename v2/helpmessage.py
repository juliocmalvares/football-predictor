
help_message = """
usage: python3 crawler.py [option] [initial data] [final data]

-a [initial_data] [final data]\t\t:This option downloads all desired links and news using urllib3 as a background. If you omit the dates, the 20 latest news available on the site will be downloaded.
-n                            \t\t:This option downloads all news using the existent links. Place the links in a .csv file using a comma as a delimiter between each one and leave the file inside a folder called "links" in the same path as this file.
"""
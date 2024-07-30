
from configparser import ConfigParser
# This function looks at the database.ini file which contains the login info for the database and parses the data to be used during connection

# The info from "database.ini" is specific to the database I setup including username and password
def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read("/Users/Zach/Desktop/Database Design/Project/database.ini")
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
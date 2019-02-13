
# DB-Saver

## Table of content

  * [Description](#description)
  * [Installing](#installing)
  * [Running](#running)
  * [License](#license)


## Description

DB Saver is a small Python script that I developed to save easily and simply my databases.

You are more than welcome to copy and modify it as you please.

## Installing

* Clone or download the repository 
* In a terminal, go to the project's root 
* Run `pip install -r requirements.txt` to install the dependencies
* If you want to use the email functionality, you should define your SMTP server info in the `config.py` file

## Running

* Running the prompt :
    * In a terminal, go to the project's root. 
    * Run `py main.py`.
    * Enter the name of the file containing the databases.
    * Enter the password used to protect this folder. If it's the first time you are running the script, just type the password you want to use.
    
    Once you have done all this steps you can add, delete, show and backup your databases just by following the instructions.
    
* Running as a command line : 
    * In a terminal, go to the project's root.
    * Run `py main.py -f your_database_path -p your_database_password [-e your_email]`.
    * The file and password are required but not the email. You can specify one if you wish to receive an email once your backup is done.

Notes : 
* If you are using the default file `database.txt` (stored in `./storage`), clear it before adding a new database.
* The generated backups are stored in `./storage/backups`.


## License

[MIT](https://github.com/malain96/DB-Saver/blob/master/LICENSE)



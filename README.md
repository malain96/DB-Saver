
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

## Running

* In a terminal, go to the project's root 
* Run `py main.py`
* Enter the name of the file containing the databases
* Enter the password used to protect this folder. If it's the first time you are running the script, just type the password you want to use.

Once you have done all this steps you can add, delete, show and backup your databases just by following the instructions. 

Notes : 
* If you are using the default file `database.txt` (stored in `./storage`), clear it before adding a new database.
* The generated backups are stored in `./storage/backups`.


## License

[MIT](https://github.com/malain96/DB-Saver/blob/master/LICENSE)



# nkcrawler
nkcrawler is a container batch application for collecting [netkeiba.com](https://www.netkeiba.com/) data. nkcrawler depend on [nkparser](https://github.com/new-village/nkparser) which is a python library.   
  
## Description
This application execute below:  
1. Download SQLite database file from Azure Blob Storage, if the database file is exists on Azure.  
2. Collect netkeiba.com data by defined year of environment variables.  
3. Insert collected data to SQLite Database.  
4. Upload SQLite database file to Azure Blob Storage.  
  
## Usage
RECCOMEND: You shoud use async execution like tmux due to long time execution (over 4-5 hours for run).
```sh:
$ export CONNECTION_STRING="YOUR CONNECTION STRING"
$ export YEAR="2021"
$ pip install -U pip
$ pip install -r requirements.txt
$ python run.py
```

# Multitran converter
Converts data from the Multitran Android app database to JSON

Designed to provide readable backup of your dictionary

[Multitran on Google Play](https://play.google.com/store/apps/details?id=com.suvorov.newmultitran)

## How to use
1. Find your database in `/data/data/com.suvorov.newmultitran/databases/user_data`
2. Run `python main.py json <path to database> -o save_to.json`
3. For help type `python main.py --help`
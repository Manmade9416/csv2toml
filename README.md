# csv2toml
This is a simple script to make it easy to work with large or small csv files.
You don't need a gui app that will hog your memory or take a long time to load on large csv files.

# Motivation
I have a bunch of data in csv files I wanted to work through but couldn't on my fairly low powered devices because
the files were rather large. Opening the in gui viewers would take a while or crash, reading the csv raw was ugly.
So I made this script to help with that. other more sophisticated options like [Miller](https://github.com/johnkerl/miller) exist
and offer a lot more, but it was a lot more than I needed atleast for when I decided to make this.

# What it does
All it does is take the rows in the csv and parse them in a toml like style making it easy to read and search through large files

# How to use
1. clone this repo or copy the contents of the `csto.py` file to your own local .py file
2. run the script once without any args to see the help page.

# Example use cases
1. help page
```bash
$ ./csto.py
usage: csto.py [-h] [-f F] [-r R] [-R R R] [-w]

options:
  -h, --help  show this help message and exit
  -f F        Path to csv file
  -r R        Number of rows you want, if -r >
              number of rows in csv it will stop at
              the end
  -R R R      -R {start} {stop} start and stop are
              the row you want to start at and the                  row to stop at
  -w          Write to file, file passed to -f with                 be used as file name prepended to
              '.toml'
```

2. List all columns in the csv
```bash
$ ./csto.py -f test.csv
[columns]
number_of_columns = 4
cl0 = artist
cl1 = song
cl2 = date
cl3 = label
```

3. List 3 rows
```bash
$ ./csto.py -f test.csv -r 3
[columns]
number_of_columns = 4
cl0 = artist
cl1 = song
cl2 = date
cl3 = label


[row.0]
col.0 = Ariana Grande
col.1 = Sunrise
col.2 = 2024-01-12
col.3 = Cloud Nine Records


[row.1]
col.0 = The Weeknd
col.1 = Midnight Drive
col.2 = 2024-02-03
col.3 = Starline Music


[row.2]
col.0 = Lana Del Rey
col.1 = Velvet Sky
col.2 = 2024-02-28
col.3 = Blue Hour Label
```

4. List a range of rows
```bash
$ ./csto.py -f test.csv -R 2 5
[columns]
number_of_columns = 4
cl0 = artist
cl1 = song
cl2 = date
cl3 = label


[row.2]
col.0 = Ariana Grande
col.1 = Sunrise
col.2 = 2024-01-12
col.3 = Cloud Nine Records


[row.3]
col.0 = The Weeknd
col.1 = Midnight Drive
col.2 = 2024-02-03
col.3 = Starline Music


[row.4]
col.0 = Lana Del Rey
col.1 = Velvet Sky
col.2 = 2024-02-28
col.3 = Blue Hour Label


[row.5]
col.0 = Drake
col.1 = City Lights
col.2 = 2024-03-15
col.3 = Northstar Entertainment
```

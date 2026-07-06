#!/usr/bin/python3
import argparse
import csv
import os
import sys

path = os.path

red = "\033[31m"
green = "\033[32m"
blue = "\033[34m"
yellow = "\033[33m"
close = "\033[0m"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",help="Path to csv file")
    parser.add_argument("-r", type=int, default=0, help="Number of rows you want, if -r > number of rows in csv it will stop at the end")
    parser.add_argument("-R", type=int, nargs=2, help="-R {start} {stop} start and stop are the row you want to start at and the row to stop at")
    parser.add_argument("-w", help="Write to file, file passed to -f with be used as file name prepended to '.toml'", action="store_true")
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    else:
        valid_path = get_path(args.f)

    if valid_path:
        if args.r <= 0:
            if args.R:
                return get_columns(valid_path, args.w), get_range_of_rows(valid_path, args.R[0], args.R[1], args.w)
            else:
                return get_columns(valid_path, args.w)
        else:
            if args.R:
                print("Cannot use -r and -R together")
                return 1
            else:
                return get_columns(valid_path, args.w), get_rows(valid_path, args.r, args.w)
 
def get_path(path_to_file):
    if "~" in path_to_file:
        path_to_file = path_to_file.replace("~", os.getenv("HOME"))

    path_to_file = path.abspath(path_to_file)

    if path.exists(path_to_file) and path.isdir(path_to_file) != True:
        return path_to_file
    else:
        return None

def get_columns(path_to_file, write_to_file):
    with open(path_to_file, "r", errors="replace") as csv_file:
        text = csv.reader(csv_file, skipinitialspace=True)
        columns = next(text)
        columns_count = len(columns)
    
    if write_to_file:
        file_name = path_to_file + ".toml"
        with open(file_name, "w", encoding="utf-8") as toml_file:
            if columns:
                toml_file.write(f"[columns]\nnumber_of_columns = {columns_count}")
                for ind, column in enumerate(columns):
                    if column:
                        toml_file.write(f"\ncl{ind} = {column}")
    else:
        if columns:
            print(f"{yellow}[columns]{close}\n{blue}number_of_columns{close} = {green}{columns_count}{close}")
            for ind, column in enumerate(columns):
                if column:
                    print(f"{blue}cl{ind}{close} = {green}{column}{close}")



def get_rows(path_to_file, nrows, write_to_file):
    with open(path_to_file, "r", errors="replace") as csv_file:
        text = csv.reader(csv_file, skipinitialspace=True)
        next(text)
        if write_to_file:
            file_name = path_to_file + ".toml"
            with open(file_name, "w", encoding="utf-8") as toml_file:
                for i in range(nrows):
                    curr_row = next(text)
                    if curr_row:
                        toml_file.write(f"\n\n[row.{i}]")
                        for ind, column in enumerate(curr_row):
                            if column:
                                toml_file.write(f"\ncol.{ind} = {column}")
        else:
            for i in range(nrows):
                curr_row = next(text)
                if curr_row:
                    print(f"\n\n{yellow}[row.{i}]{close}")
                    for ind, column in enumerate(curr_row):
                        if column:
                            print(f"{blue}col.{ind}{close} = {green}{column}{close}")


def get_range_of_rows(path_to_file, start, stop, write_to_file):
    with open(path_to_file, "r", errors="replace") as csv_file:
        text = csv.reader(csv_file, skipinitialspace=True)
        while text.line_num < start:
            curr_row = next(text)
        while text.line_num <= stop:
            if write_to_file:
                file_name = path_to_file + ".toml"
                with open(file_name, "w", encoding="utf-8") as toml_file:
                    if curr_row:
                        toml_file.write(f"\n\n[row.{text.line_num}]")
                        for ind, column in enumerate(curr_row):
                            if column:
                                print(f"\ncol.{ind} = {column}")
                    curr_row = next(text)
            else:
                if curr_row:
                    print(f"\n\n{yellow}[row.{text.line_num}]{close}")
                    for ind, column in enumerate(curr_row):
                        if column:
                            print(f"{blue}col.{ind}{close} = {green}{column}{close}")
                curr_row = next(text)

if __name__ == "__main__":
    main()

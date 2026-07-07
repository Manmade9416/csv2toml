#!/usr/bin/python3
import argparse
from datetime import datetime
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
 
def format_cols(columns):
    if columns:
        result = f"[columns]\nn_cols = {len(columns)}\n"
        for ii, col in enumerate(columns):
            result += f"col.{ii} = {col}\n"
        result += "\n"
        return result
    else:
        return f"No Columns: {columns}"

def format_cols_color(columns):
    if columns:
        result = f"{yellow}[columns]{close}\n{blue}n_cols{close} = {green}{len(columns)}{close}\n"
        for ii, col in enumerate(columns):
            result += f"{blue}col.{ii}{close} = {green}{col}{close}\n"
        return result
    else:
        return f"{red}No Columns: {columns}{close}"

def format_row(row, i):
    if row:
        result = f"[row.{i}]\n"
        for ii, col in enumerate(row):
            result += f"col.{ii} = {col}\n"
        return result
    else:
        return f"Empty row: {row}\n"

def format_row_color(row, i):
    if row:
        result = f"{yellow}[row.{i}]{close}\n"
        for ii, col in enumerate(row):
            result += f"{blue}col.{ii}{close} = {green}{col}{close}\n"
        return result
    else:
        return f"{red}Empty row: {row}{close}\n"

def get_path(path_to_file):
    if "~" in path_to_file:
        path_to_file = path_to_file.replace("~", os.getenv("HOME"))

    path_to_file = path.abspath(path_to_file)

    if path.exists(path_to_file) and path.isdir(path_to_file) != True:
        return path_to_file
    else:
        return None

def create_output(csv_path):
    output_file = "csv2toml_" + datetime.now().strftime("%Y%m%d%H%M%S") + path.split(csv_path)[1] 
    output_path = path.split(csv_path)[0] + "/" + output_file + ".toml"
    return output_path

def get_columns(path_to_file, write_to_file):
    with open(path_to_file, "r", errors="replace") as csv_file:
        text = csv.reader(csv_file, skipinitialspace=True)
        columns = next(text)

    if write_to_file:
        out = create_output(path_to_file)
        with open(out, "w", encoding="utf-8") as output:
            output.write(format_cols(columns))
    else:
        print(format_cols_color(columns))
            
def get_rows(path_to_file, nrows, write_to_file):
    with open(path_to_file, "r", errors="replace") as csv_file:
        text = csv.reader(csv_file, skipinitialspace=True)
        next(text)
        if write_to_file:
            out = create_output(path_to_file)
            with open(out, "a", encoding="utf-8") as output:
                for i in range(nrows):
                    curr_row = next(text)
                    output.write(format_row(curr_row, text.line_num))
        else:
            for i in range(nrows):
                curr_row = next(text)
                print(format_row_color(curr_row, text.line_num))                

def get_range_of_rows(path_to_file, start, stop, write_to_file):
    with open(path_to_file, "r", errors="replace") as csv_file:
        text = csv.reader(csv_file, skipinitialspace=True)
        while text.line_num <= start:
            curr_row = next(text)
        if write_to_file:
            out = create_output(path_to_file)
            with open(out, "a", encoding="utf-8") as output:
                while text.line_num <= stop:
                    output.write(format_row(curr_row, text.line_num))
                    curr_row = next(text)
        else:
            while text.line_num <= stop:
                print(format_row_color(curr_row, text.line_num))
                curr_row = next(text)
                
if __name__ == "__main__":
    main()

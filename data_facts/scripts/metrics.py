#!/usr/bin/env python

# CREATED BY ORESTIS
# ADDITIONS BY YORGOS

import argparse
import sys
import collections
import matplotlib.pyplot as plt

# parse command line arguments
parser = argparse.ArgumentParser(description='Give me a .work path')
parser.add_argument('path', metavar='P', type=str, nargs='+',
                   help='a path for the accumulator')

args = parser.parse_args()

if len(sys.argv) > 2:
    sys.exit(1)

path = sys.argv[1]

# Dictionary that maps number of joins
# to their frequency in the queries
total_join_dict = {}
# Dictionary that maps number of filters
# to their frequency in the queries
total_filter_dict = {}
# Dictionary that maps number of tables
# to their frequency in the queries
total_tables_dict = {}
# Dictionary that maps number of columns
# to their respective tables
columns_dict = {}
# Dictionary that maps the number of columns of each table
# to their frequency in that table
columns_in_table_dict = {}

queries_counter = 0

# Open the file that contains the queries
with open(path, "r") as file:
    for line in file:
        # Remove the trailing newline character
        line = line.split("\n")[0];

        # Skip lines with an "F"
        if line == "F":
            continue

        # Set that collects the different tables in each query
        tables = set()

        # Extract the predicates
        line = line.split("|")[1]
        predicates = line.split("&")

        # update counters
        join_counter = 0
        filter_counter = 0
        queries_counter += 1

        # Count the join predicates
        for predicate in predicates:
            # Check for equality and inequalities
            if "=" in predicate:
                predicate = predicate.split("=")

                # Check if both sides of the predicate
                # contain a dot (.) which means
                # it is a join predicate
                # otherwise, it is a filter predicate
                if (("." in predicate[0]) and ("." in predicate[1])):
                    join_counter += 1
                    # Update the dictionary
                    if join_counter in total_join_dict:
                        total_join_dict[join_counter] += 1
                    else:
                        total_join_dict[join_counter] = 1

                    # Extract the tables
                    left_predicate = predicate[0].split(".")
                    right_predicate = predicate[1].split(".")
                    tables.add(left_predicate[0])
                    tables.add(right_predicate[0])

                    if left_predicate[0] in columns_dict:
                        columns_dict[left_predicate[0]] += 1
                    else:
                        columns_dict[left_predicate[0]] = 1

                    if right_predicate[0] in columns_dict:
                        columns_dict[right_predicate[0]] += 1
                    else:
                        columns_dict[right_predicate[0]] = 1

                elif (("." in predicate[0]) and not ("." in predicate[1])) or (not ("." in predicate[0]) and ("." in predicate[1])):
                    filter_counter += 1

                    # Update the dictionary
                    if filter_counter in total_filter_dict:
                        total_filter_dict[filter_counter] += 1
                    else:
                        total_filter_dict[filter_counter] = 1

                    if "." in predicate[0]:
                        left_predicate = predicate[0].split(".")
                        if left_predicate[0] in columns_dict:
                            columns_dict[left_predicate[0]] += 1
                        else:
                            columns_dict[left_predicate[0]] = 1
                    else:
                        right_predicate = predicate[1].split(".")
                        if right_predicate[0] in columns_dict:
                            columns_dict[right_predicate[0]] += 1
                        else:
                            columns_dict[right_predicate[0]] = 1

            elif ">" in predicate:
                predicate = predicate.split(">")

                # Confirm that not both sides of the predicate
                # contain a dot (.) which means
                # it is a filter predicate indeed
                if (("." in predicate[0]) and not ("." in predicate[1])) or (not ("." in predicate[0]) and ("." in predicate[1])):
                    filter_counter += 1
                    # Update the dictionary
                    if filter_counter in total_filter_dict:
                        total_filter_dict[filter_counter] += 1
                    else:
                        total_filter_dict[filter_counter] = 1

                    if "." in predicate[0]:
                        left_predicate = predicate[0].split(".")
                        if left_predicate[0] in columns_dict:
                            columns_dict[left_predicate[0]] += 1
                        else:
                            columns_dict[left_predicate[0]] = 1
                    else:
                        right_predicate = predicate[1].split(".")
                        if right_predicate[0] in columns_dict:
                            columns_dict[right_predicate[0]] += 1
                        else:
                            columns_dict[right_predicate[0]] = 1
            elif "<" in predicate:
                predicate = predicate.split("<")

                # Confirm that not both sides of the predicate
                # contain a dot (.) which means
                # it is a filter predicate indeed
                if (("." in predicate[0]) and not ("." in predicate[1])) or (not ("." in predicate[0]) and ("." in predicate[1])):
                    filter_counter += 1
                    # Update the dictionary
                    if filter_counter in total_filter_dict:
                        total_filter_dict[filter_counter] += 1
                    else:
                        total_filter_dict[filter_counter] = 1

                    if "." in predicate[0]:
                        left_predicate = predicate[0].split(".")
                        if left_predicate[0] in columns_dict:
                            columns_dict[left_predicate[0]] += 1
                        else:
                            columns_dict[left_predicate[0]] = 1
                    else:
                        right_predicate = predicate[1].split(".")
                        if right_predicate[0] in columns_dict:
                            columns_dict[right_predicate[0]] += 1
                        else:
                            columns_dict[right_predicate[0]] = 1
            # END if

        # Update the dictionary
        if queries_counter in total_tables_dict:
            total_tables_dict[len(tables)] += 1
        else:
            total_tables_dict[len(tables)] = 1
        #END for
    #END for
# END with

# close .work file
file.close()

# Sort dictionaries
sorted_join_dict = collections.OrderedDict(sorted(total_join_dict.items()))
sorted_filter_dict = collections.OrderedDict(sorted(total_filter_dict.items()))
sorted_tables_dict = collections.OrderedDict(sorted(total_tables_dict.items()))
sorted_columns_dict = collections.OrderedDict(sorted(columns_dict.items()))

# Plot the join data
plt.bar(range(len(sorted_join_dict)), list(sorted_join_dict.values()), align='center')
plt.xticks(range(len(sorted_join_dict)), list(sorted_join_dict.keys()))
plt.title("Frequency I")
plt.xlabel("Number of joins")
plt.ylabel("Frequency of joins")
plt.show()

# Plot the filter data
plt.bar(range(len(sorted_filter_dict)), list(sorted_filter_dict.values()), align='center')
plt.xticks(range(len(sorted_filter_dict)), list(sorted_filter_dict.keys()))
plt.title("Frequency II")
plt.xlabel("Number of filters")
plt.ylabel("Frequency of filters")
plt.show()

# Plot the tables data
plt.bar(range(len(sorted_tables_dict)), list(sorted_tables_dict.values()), align='center')
plt.xticks(range(len(sorted_tables_dict)), list(sorted_tables_dict.keys()))
plt.title("Frequency III")
plt.xlabel("Number of tables")
plt.ylabel("Frequency of tables")
plt.show()

# Plot the columns data
plt.bar(range(len(sorted_columns_dict)), list(sorted_columns_dict.values()), align='center')
plt.xticks(range(len(sorted_columns_dict)), list(sorted_columns_dict.keys()))
plt.title("Columns per table")
plt.xlabel("Number of table")
plt.ylabel("Number of columns")
plt.show()
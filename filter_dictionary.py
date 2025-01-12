import csv
dictionary = 'English_dictionary.csv'
result_file = 'Filtered_English_dictionary.csv'
with open(dictionary, 'r') as csvfile:
    result = []
    reader = csv.reader(csvfile)
    for row in reader:
        suffix = row[0][-2:]
        if suffix != 'er' and suffix != 'ed' and suffix[-1] != 's':
            result.append(row[0])

with open(result_file, 'w') as csvfile:
    writer = csv.writer(csvfile)
    for i in result:
        writer.writerow([i])
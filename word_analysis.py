import csv

words_file = 'word_occurrences_test_cubes.csv'
result = []
with open(words_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader: 
                result.append(row)
longest = list(sorted(result, key=lambda x: len(x[0]), reverse=True))
most_common = list(sorted(result, key=lambda x: int(x[1]), reverse=True))
fifteen_letters = list(filter(lambda x: len(x[0])==15, longest))
fourteen_letters = list(filter(lambda x: len(x[0])==14, longest))
thirteen_letters = list(filter(lambda x: len(x[0])==13, longest))
common_counts = [list(filter(lambda x: len(x[0])==i, most_common)) for i in range(4, 16)]
counts = []
for i in common_counts:
        acc = 0
        for word in i:
                acc += int(word[1])
        counts.append(acc)
total_words = sum(counts)
#print(longest[:20])
import csv
def write_puzzle(matrix, filename):
    file = filename
    with open (file, 'a') as output:
        writer = csv.writer(output, delimiter = ' ')
        writer.writerows(matrix)
        writer.writerow('\n')
def write_eval(eval, filename):
    file = filename
def write_time(time, filename):
    file = filename
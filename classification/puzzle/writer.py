import csv
def write_puzzle(matrix, filename):
    with open (filename, 'a') as output:
        writer = csv.writer(output, delimiter = ' ')
        writer.writerows(matrix)
        writer.writerow([])
def write_eval(eval, filename):
    with open (filename, 'a') as output:
        writer = csv.writer(output, delimiter = ' ')
        writer.writerow([eval])
def write_time(time, filename):
    with open(filename, 'a') as output:
        writer = csv.writer(output, delimiter = ' ')
        writer.writerow([time])

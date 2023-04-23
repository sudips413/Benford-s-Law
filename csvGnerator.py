# import csv
# import random

# # Define the expected Benford's Law percentages for the first digits
# BENFORD_PERCENTAGES = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]

# # Generate a dataset of 1000 random numbers that satisfy Benford's Law
# data = []
# for i in range(50000):
#     first_digit = random.randint(1, 9)
#     remaining_digits = random.randint(0, 999)
#     number = int(str(first_digit) + str(remaining_digits).zfill(3))
#     data.append(number)

# # Write the data to a CSV file
# with open('data/benford_data.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['Number'])
#     for number in data:
#         writer.writerow([number])

##not satisfying Benford's law data
import csv
import random

def generate_data(count):
    data = []
    for i in range(count):
        num = str(random.randint(1000, 9999))
        data.append(num)
    return data

def write_csv(filename, data):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow([row])

if __name__ == '__main__':
    data = generate_data(1000)
    write_csv('random_numbers.csv', data)
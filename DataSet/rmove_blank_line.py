import os

# remove blank line in file
def remove_blank_line(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    non_empty_lines = [line.strip() for line in lines if line.strip()]

    with open('../DataSet/train_dataset_0.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(non_empty_lines))

for file_path in os.listdir('../DataSet'):
    if file_path.endswith('.txt'):
        remove_blank_line(file_path)
    else:
        print('please check the file path.')


# remove_blank_line()


# This is a sample Python script.


import argparse
from DataFormatter import DataFormatter


def main():
    #by default you will only need to run: python main.py, without arguments
    #just in case you want to switch the default file, you can add a --data_dir argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='./data/Pulley_Post_Y2.xlsm - Sheet1.csv',
                        help='data_directory')
    args = parser.parse_args()

    #Once the data directory is determined, the DataFormatter class will be called.
    dataFormat = DataFormatter(args.data_dir)
    print('Data Directory: ', dataFormat.formattedData)


# Running main.py will call the main() function
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import pandas as pd

db_paths = '/Users/sofinico/tesis/db/'


class DataBase:

    # initialiation

    def __init__(self, file_name, path=db_paths):
        self.path = path
        self.file_name = file_name
        self.df = pd.read_csv(self.path + self.file_name)
        print('\nLoad database ' + file_name + '\n')

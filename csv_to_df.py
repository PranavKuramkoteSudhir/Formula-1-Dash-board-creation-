import pandas as pd
class CsvToDf:
    def __init__(self):
        self. csv_list = ["circuits", "constructor_results", "constructor_standings", "constructors",  "drivers", "lap_times", "pit_stops", "qualifying", "races", "results"]
        df_dictionary = {}
        self.df_alctn()


    def csv_import(self,path):
        df = pd.read_csv(path)
        return df
    def df_alctn(self):
        df_dict={}
        for csv in self.csv_list:
            path=f"/Users/pranav/Downloads/archive (2)/"+f"df_{csv}.csv"
            df_dict[f"{csv}"] = self.csv_import(path)
            self.df_dictionary= df_dict
    def get_df_dict(self):
        return self.df_dictionary



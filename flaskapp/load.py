'''
Testing to see if we can load csv to sqlite
'''


import pandas as pd
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()



# connection_name = "root:root@127.0.0.1:3306/peep"
# engine = create_engine(f'mysql+pymysql://{connection_name}')
# print(engine.table_names())


def loadzone(csvdata):
    try:

        engine = create_engine("sqlite:///peep.sqlite")
        conn = engine.connect()

        csvdata.to_sql(name='timeline', con= engine, if_exists='replace', index=False)
        print("All loaded into database")

    except:
        print("This shiet failed")


if __name__ == '__main__':
    data = pd.read_csv("timeline.csv")
    loadzone(data)

import pandas as pd
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()

import extract_timeline as et


# connection_name = "root:root@127.0.0.1:3306/peep"
# engine = create_engine(f'mysql+pymysql://{connection_name}')
# print(engine.table_names())

def loadzone(data):
    try:

        engine = create_engine("sqlite:///peep.sqlite")
        conn = engine.connect()

        data.to_sql(name='timeline', con= engine, if_exists='replace', index=True)
        print("All loaded into database")

    except:
        print("This shiet failed")


if __name__ == '__main__':
    data = et.get_timeline("_lsun")
    loadzone(data)

from sqlalchemy import create_engine, inspect
from backend.config.config import Config

if __name__ == '__main__':
    c = Config()
    engine = create_engine(c.SQLALCHEMY_DATABASE_URI)
    ins = inspect(engine)
    print('DB URI:', c.SQLALCHEMY_DATABASE_URI)
    print('Tables:')
    for t in ins.get_table_names():
        print('-', t)

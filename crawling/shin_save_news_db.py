import sqlalchemy.types
from sqlalchemy import create_engine
import pymysql
import pandas as pd

def save_news_db():
    db_connection_str = 'mysql+pymysql://root:774100@localhost/news_data_2'
    # 'mysql+pymysql://[db유저이름]:[db password]@[host address]/[db name]'
    db_connection = create_engine(db_connection_str)
    conn = db_connection.connect()

    # db 예시
    df = pd.DataFrame({'news_category': '뉴스카테고리',
                       'press': '언론사',
                       'today_date': ['2022-04-07'],
                       'title': '제목',
                       'sub_title': '소제목',
                       'content': '본문',
                       'summary_content': '본문요약',
                       'articles_response': 12,
                       'comment': '댓글'
                       }, index=[0])

    # type 지정
    dtypesql = {'news_category': sqlalchemy.types.VARCHAR(10),
                'press': sqlalchemy.types.VARCHAR(20),
                'today_date': sqlalchemy.Date(),
                'title': sqlalchemy.types.VARCHAR(100),
                'sub_title' :sqlalchemy.types.VARCHAR(100),
                'content' : sqlalchemy.types.VARCHAR(65535),
                'summary_content' : sqlalchemy.types.VARCHAR(65535),
                'articles_response' : sqlalchemy.types.VARCHAR(10),
                'comment' : sqlalchemy.types.VARCHAR(65535)
                }

    df.to_sql(name='news_data_save', con=db_connection, if_exists='append', index=False, dtype=dtypesql)

save_news_db()
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select, and_

engine = create_engine("postgresql+psycopg2://postgres:12345@127.0.0.1/testbase", echo=True)
meta = MetaData(engine)
#meta.create_all(engine)

certificates = Table("certificates", meta, autoload=True)
maxim = []
conn = engine.connect()
s = certificates.select().where(certificates.columns.full_name == "Illia Pastushok")
result = conn.execute(s)

for row in result:
    print(row)
    print(row[1])

id = certificates.select()
ide = conn.execute(id)

for rew in ide:
    #print(rew[0])
    maxim = []
    maxim.append(rew[0])

print(maxim[0])

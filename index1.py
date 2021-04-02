import time
from flask import Flask, render_template

from sqlalchemy import create_engine, Table, MetaData
app = Flask(__name__)
nowisday = time.strftime("%x", time.localtime())
coursename = ""
FullName = ""

maxim = []

engine = create_engine("postgresql+psycopg2://postgres:12345@127.0.0.1/testbase", echo=False)
meta = MetaData(engine)

certificates = Table("certificates", meta, autoload=True)

conn = engine.connect()
id = certificates.select()
ide = conn.execute(id)

for rew in ide:
    maxim = []
    maxim.append(rew[0])



s = certificates.select().where(certificates.columns.ident == maxim[0])
result = conn.execute(s)
for row in result:
    FullName = row[1]

print(FullName, "+++++++++++++++++++")
d = certificates.select().where(certificates.columns.ident == maxim[0])
result = conn.execute(d)
for row1 in result:
    coursename = row1[2]
print(coursename, "+++++++++++++++++++")

html = f'''<!doctype html>
<html lang="en">
<head>
      <meta charset="UTF-8">
     <meta name="viewport"
           content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <link rel="photo" href="{{ url_for('static', filename='static/cert.png') }}">
     <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css')}}">
     <meta http-equiv="X-UA-Compatible" content="ie=edge">
     <title>Document</title>

</head>
<body>
<    <div style="width:800px; height:600px; padding:20px; text-align:center; border: 10px solid #787878">
 <div style="width:750px; height:550px; padding:20px; text-align:center; border: 5px solid #787878">
       <span style="font-size:50px; font-weight:bold">Certificate of Completion</span>
       <br><br>
       <span style="font-size:25px"><i>This is to certify that</i></span>
       <br><br>
       <span style="font-size:30px"><b>{FullName}</b></span><br/><br/>
       <span style="font-size:25px"><i>has completed the course</i></span> <br/><br/>
       <span style="font-size:30px">{coursename}</span> <br/><br/>
       <span style="font-size:25px"><i>dated</i></span><br>
       <span style="font-size:30px">{nowisday}</span>
       <span style="font-size:25px"><i>                                Term</i></span><br>
       <span style="font-size:30px">indefinite</span>
</div>
</div>
</body>
</html>
'''

with open(f'templates/{maxim}.html', 'w'.format(maxim[0])) as file:
    file.write(html)

path = "[" + str(maxim[0]) + "]" + ".html"

@app.route('/')
def index():
    return render_template(path)
if __name__ == '__main__':
    app.run(debug=True)
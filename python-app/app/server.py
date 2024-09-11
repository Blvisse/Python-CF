import os
from flask import Flask
from cfenv import AppEnv
from hdbcli import dbapi

app = Flask(__name__)
env = AppEnv()
port = int(os.environ.get('PORT', 3000))

hana_service='hana'
hana=env.get_service(label=hana_service)



@app.route('/')
def hello_world():
    if hana is None:
        return "Can't connect to HANA service {} -- check service name".format(hana_service)

    else:
        conn = dbapi.connect(
            address=hana.credentials['host'],
            port=int(hana.credentials['port']),
            user=hana.credentials['user'],
            password=hana.credentials['password'],
            encrypt = 'true',
            sslTrueStore=hana.credentials['certificate']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_UTCTIMESTAMP FROM DUMMY")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return 'Hello World! \n Current time is: '+str(row["CURRENT_UTCTIMESTAMP"])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

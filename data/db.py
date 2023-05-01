import sqlite3
import json
import uuid
import os

class DB:
    def __init__(self,db,script):
        self.script = script
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS IPs
        (ip TEXT PRIMARY KEY)
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ScanData
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip text,
            port text,
            state text,
            reason text,
            name text,
            product text,
            version text,
            extrainfo text,
            conf text,
            cpe text,
            script text,
            FOREIGN KEY (ip) REFERENCES IPs(ip)
        )
        ''')

        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def add_ip(self,ip):
        self.cursor.execute('''
        INSERT INTO IPs (ip) VALUES (?)
        ''', (ip,))
        self.conn.commit()

    def ip_exists(self,ip):
        self.cursor.execute('''
        SELECT * FROM IPs WHERE ip=?
        ''',(ip,))
        return self.cursor.fetchone() is not None

    def add_scan_data(self,ip,port,state,reason,name,product,version,extrainfo,conf,cpe,scriptd):
        script = ""
        if not len(scriptd) == 0:
            s = str(uuid.uuid4()) + ".json"
            script = self.script + "/" + s
            with open(script,'w') as f:
                json.dump(scriptd,f,indent=4)

        self.cursor.execute('''
        INSERT INTO ScanData 
        (ip,port,state,reason,name,product,version,extrainfo,conf,cpe,script)
        VALUES
        (?,?,?,?,?,?,?,?,?,?,?)
        ''',(ip,port,state,reason,name,product,version,extrainfo,conf,cpe,s))
        self.conn.commit()

    def get_scan_data(self, limit=None, offset=None):
        query = 'SELECT * FROM ScanData'
        if limit is not None:
            query += f' LIMIT {limit}'
        if offset is not None:
            query += f' OFFSET {offset}'
        self.cursor.execute(query)
        c = self.cursor.fetchall()

        for i,f in enumerate(c):
            f = list(f)
            if not len(f[11]) == 0:
                with open(f[11],'r') as ff:
                    con = ff.read()
                    f[11] = json.loads(con)
                    c[i] = f
        rr = [
            {
                "ip":t[1],
                "port":t[2],
                "state":t[3],
                "reason":t[4],
                "name":t[5],
                "product":t[6],
                "version":t[7],
                "extrainfo":t[8],
                "conf":t[9],
                "cpe":t[10],
                "script":t[11]

            } for t in c
        ]

        return {
            r['ip']: r for r in rr
        }

    def update_scan_data(self, old_pattern, new_pattern):
        self.cursor.execute('''
            UPDATE ScanData
            SET script = REPLACE(script, ?, ?)
        ''', (old_pattern, new_pattern))
        self.conn.commit()
#Use the following python program in order to create a keyspace and a table inside it.

import logging

log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

KEYSPACE = "mykeyspace"

def createKeySpace():
    cluster = Cluster(contact_points=['127.0.0.1'],port=9142)
    session = cluster.connect()

    log.info("Creating keyspace...")
    try:
        session.execute("""
            CREATE KEYSPACE %s
            WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
            """ % KEYSPACE)

        log.info("setting keyspace...")
        session.set_keyspace(KEYSPACE)

        log.info("creating table...")
        session.execute("""
            CREATE TABLE mytable (
                mykey text,
                col1 text,
                col2 text,
                PRIMARY KEY (mykey, col1)
            )
            """)
    except Exception as e:
        log.error("Unable to create keyspace")
        log.error(e)

createKeySpace()


#use python to delete the created table

def deleteTable():
    cluster = Cluster(contact_points=['127.0.0.1'],port=9142)
    session = cluster.connect()

    log.info("setting keyspace...")
    session.set_keyspace(KEYSPACE)

    try:
        log.info("Deleting a table...")
        session.execute('''DROP TABLE mytable''')
    except Exception as e:
        log.error("Unable to delete a table")
        log.error(e)


#use python to delete the created keyspace

def deleteKeyspace():
    cluster = Cluster(contact_points=['127.0.0.1'],port=9142)
    session = cluster.connect()

    try:
        log.info("Deleting a keyspace...")
        session.execute('''DROP KEYSPACE %s''' % KEYSPACE)
    except Exception as e:
        log.error("Unable to delete a keyspace")
        log.error(e)



#use python to insert a few records in our table

def insertData(number):
    cluster = Cluster(contact_points=['127.0.0.1'],port=9142)
    session = cluster.connect()

    log.info("setting keyspace...")
    session.set_keyspace(KEYSPACE)

    prepared = session.prepare("""
    INSERT INTO mytable (mykey, col1, col2)
    VALUES (?, ?, ?)
    """)

    for i in range(number):
        if(i%5 == 0):
            log.info("inserting row %d" % i)
        session.execute(prepared.bind(("rec_key_%d" % i, 'aaa', 'bbb')))

insertData(20)



#Reading the freshly inserted data is not that difficult using a function similar to the one below:

def readRows():
    cluster = Cluster(contact_points=['127.0.0.1'],port=9142)
    session = cluster.connect()

    log.info("setting keyspace...")
    session.set_keyspace(KEYSPACE)

    rows = session.execute("SELECT * FROM mytable")
    log.info("key\tcol1\tcol2")
    log.info("---------\t----\t----")

    count=0
    for row in rows:
        if(count%100==0):
            log.info('\t'.join(row))
        count=count+1

    log.info("Total")
    log.info("-----")
    log.info("rows %d" %(count))

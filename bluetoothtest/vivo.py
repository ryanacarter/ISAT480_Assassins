from jnius import autoclass

#Load java classes
#Database setup
DBConnection = autoclass('com.hp.hpl.jena.db.DBConnection')
LayoutType = autoclass('com.hp.hpl.jena.sdb.store.LayoutType')
DatabaseType = autoclass('com.hp.hpl.jena.sdb.store.DatabaseType')
SDBConnection = autoclass('com.hp.hpl.jena.sdb.sql.SDBConnection')
SDBFactory = autoclass('com.hp.hpl.jena.sdb.SDBFactory')
StoreDesc = autoclass('com.hp.hpl.jena.sdb.StoreDesc')

storeDesc = StoreDesc(LayoutType.LayoutTripleNodesHash, DatabaseType.MySQL)
conn = SDBConnection(DB_URL, DB_USER, DB_PASSWD)
store = SDBFactory.connectStore(conn, storeDesc)
dataset = SDBFactory.connectDataset(store)
model = dataset.getNamedModel('http://vitro.mannlib.cornell.edu/default/vitro-kb-2')

namespaces = model.listNameSpaces()
while namespaces.hasNext():
    print namespaces.next()

model.close()
store.close()
conn.close()

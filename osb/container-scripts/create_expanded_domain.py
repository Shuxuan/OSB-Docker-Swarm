
import java.lang.String as jstring
import java.lang.System as jsystem
import socket

WL_HOME=ORACLE_HOME +'/wlserver'
APPLICATION_DIR=DOMAIN_DIR
MACHINENAME=socket.gethostname()

# oracle_xe_db_host=str(sys.argv[1])
# oracle_xe_db_port=int(sys.argv[2])

# ! -------------------------------------------------------
# ! SET NODEMANAGER CREDENTIALS
# ! -------------------------------------------------------

def setNodeManagerCredentials(domainHome, domainName, username, password):
	try:
		create(domainName, 'SecurityConfiguration')
		cd('/SecurityConfiguration/' + domainName)
		print '  + NodeManager Username ' + username
		set('NodeManagerUsername', username)
		set('NodeManagerPasswordEncrypted', password)
	except Exception, e:
		print e
		print 'Error while trying to NodeManager credentials!!!'
		dumpStack()
		raise



def createServer(serverName, listenPort):
        if serverName not in SERVERS:
                cd('/')
                create(serverName, 'Server')
        cd('/Server/' + serverName)
        server = cmo
        server.setListenPort(listenPort)
#!-----------------------------------------
#!To track HA configuration.
#!-----------------------------------------
def setJDBCStorePrefixName():
	cd('/')
	allJDBCResources = cmo.getJDBCStores()
	for jdbcResource in allJDBCResources:
        	dsname = jdbcResource.getTargets()
		if dsname!=None:
			server_name = dsname[0].getName().split()[0]
			jdbcResource.setPrefixName('REP_'+server_name+'_')

def setTLOGDataSource():
	cd('/')
	managedServers=cmo.getServers()
	for ms in managedServers:
        	print ms.getName()
	        if( ADMIN_SERVER_NAME!=ms.getName() and 'ics_proxy'!=ms.getName()):
			cd('/Servers/'+ms.getName())
			create(ms.getName(),'TransactionLogJDBCStore')
			cd ('TransactionLogJDBCStore/'+ms.getName())
			set('DataSource','SOALocalTxDataSource')
			set('PrefixName','TLOG_'+ms.getName()+'_')
			set('MaxRetrySecondsBeforeTLogFail',14400)
			set('MaxRetrySecondsBeforeTxException',300)
			set('RetryIntervalSeconds',30)
			cmo.setEnabled(true)

def setDeterminer():
	cd('/')
	DOMAIN_NAME=cmo.getName()
	create(DOMAIN_NAME,'JTA')
	cd('/JTA/'+DOMAIN_NAME)
	determiner=['SOADataSource_' + DOMAIN_NAME]
	set('Determiners',determiner)
	set('TimeoutSeconds',300)


#!----------------------------------------------
#! Configure Migratable targets
#!----------------------------------------------
def configMigratableTargets():
	cd('/')
	targets = cmo.getMigratableTargets()
	for target in targets:
		cd('/MigratableTargets/'+target.getName())
		set('RestartOnFailure','true')
		set('SecondsBetweenRestarts',60)
		set('NumberOfRestartAttempts',240)

#!----------------------------------------------
#! Update datasource configuration
#!----------------------------------------------


def updateDataSource(DRIVERNAME, URL, SCHEMA_POSTFIX):
	print 'drivername='+DRIVERNAME
	print 'url='+URL
	print 'schema-postfix='+SCHEMA_POSTFIX
	cd('JdbcDriverParams/NO_NAME')
	cmo.setDriverName(DRIVERNAME)
	cmo.setUrl(URL)
	cmo.setPasswordEncrypted(DB_SCHEMA_PASSWORD)
	cd('Properties/NO_NAME')
	cd('Property/user')
	cmo.setValue(DB_SCHEMA_PREFIX + '_' + SCHEMA_POSTFIX)


def dsExists(dsName):
  try:
    cd('/JdbcSystemResource/' + dsName + '/JdbcResource/' + dsName + '/JdbcDriverParams/NO_NAME')
    doesDsExist = true
  except Exception, err:
    doesDsExist = false

  return doesDsExist

def appendJndiName(ds, jndiName):
  cd('/JdbcSystemResource/' + ds + '/JdbcResource/' + ds + '/JDBCDataSourceParams/NO_NAME')
  jndiNames=cmo.getJNDINames()
  #jndiNames.append(jndiName)
  if jndiName: jndiNames.append(str(jndiName).strip())
  # cmo.setJNDINames(jndiNames)
  cmo.setJNDINames(array(jndiNames, java.lang.String))
  cd('/')

def printJndiNames(ds):
    cd('/JdbcSystemResource/' + ds + '/JdbcResource/' + ds + '/JDBCDataSourceParams/NO_NAME')
    jndiNames=cmo.getJNDINames()
    for s in jndiNames:
      print "jndi name in owsm: " + s
    cd('/')

#!----------------------------------------------
#! START
#!----------------------------------------------
readTemplate(WL_HOME + '/common/templates/wls/wls.jar', 'Expanded')
cmo.setName(DOMAIN_NAME)
cd('Security/'+DOMAIN_NAME+'/User/'+WL_USER)
cmo.setPassword(WL_PWD)

#!----------------------------------------------
#! Create Admin server
#!----------------------------------------------
cd('/')
create(MACHINENAME, 'Machine')
cd('/Server/AdminServer')
cmo.setName(ADMIN_SERVER_NAME)
set('Machine', MACHINENAME)
SERVERS = ls('/Server', 'true', 'c')
create(ADMIN_SERVER_NAME,'SSL')
cd('SSL/'+ADMIN_SERVER_NAME)
set('Enabled', 'True')
set('ListenPort', int(ADMIN_SERVER_PORT)+1)

writeDomain(DOMAIN_DIR)
closeTemplate()
ICS_TEMPLATE_PATH=ORACLE_HOME+'/osb/common/templates/wls/'+'oracle.ics_template.jar'
SOA_TEMPLATE_PATH=ORACLE_HOME+'/soa/common/templates/wls/oracle.soaics_template.jar'
readDomain(DOMAIN_DIR)
addTemplate(ICS_TEMPLATE_PATH)
addTemplate(SOA_TEMPLATE_PATH)

cd('/Machine/'+MACHINENAME)

create(MACHINENAME, 'NodeManager')
cd('NodeManager/'+MACHINENAME)
set('ListenAddress',MACHINENAME)
set('ListenPort', 5556)
set('NodeManagerHome', DOMAIN_DIR+'/nodemanager')
setNodeManagerCredentials(DOMAIN_DIR, DOMAIN_NAME, WL_USER, WL_PWD)

cd('/')
ADMIN_SERVER_NAME = cmo.getAdminServerName()
DOMAIN_NAME = cmo.getName()
SERVERS = ls('/Server', 'true', 'c')


createServer(MANAGED_SERVER_NAME, int(MANAGED_SERVER_PORT))
cd('/Servers/'+MANAGED_SERVER_NAME)
set('Machine', MACHINENAME)
set('ListenAddress', MACHINENAME)
create(MANAGED_SERVER_NAME,'SSL')
cd('SSL/'+MANAGED_SERVER_NAME)
set('Enabled', 'True')
set('ListenPort', int(MANAGED_SERVER_PORT)+1)

#  make sure both SOA and OSB are included in the group
soaServerGroup = "SOA-MGD-SVRS"
group = getServerGroups(MANAGED_SERVER_NAME);
group.append(soaServerGroup)
print "set Server Groups for serverName to include:"
for eachGroup in group:
    print eachGroup
setServerGroups(MANAGED_SERVER_NAME, group)

CLUSTER_NAME = 'icsCluster'

cd ('/')
cluster = create(CLUSTER_NAME,'Cluster')
cd ('Cluster/' + CLUSTER_NAME)
cluster=cmo

clusterAddress=MACHINENAME+":"+MANAGED_SERVER_PORT
cluster.setClusterAddress(clusterAddress)
cluster.setClusterMessagingMode('unicast')
cluster.setWeblogicPluginEnabled(true)

assign('Server',MANAGED_SERVER_NAME,'Cluster',CLUSTER_NAME)




# delete SOA server
soaServerName = 'soa_server1'
cd('/Servers')
servers = ls()
if (servers.find(soaServerName) != -1):
   print 'Default server ' +  soaServerName + ' exists, deleting it...'
   cd ('/')
   delete(soaServerName, 'Server')
else:
   print 'no default soa server found !'
   pass



#! #######################################################################################
#! DATA SOURCES
#! #######################################################################################
PROPERTIES = ""
XADRIVERNAME = 'oracle.jdbc.xa.client.OracleXADataSource'
DRIVERNAME = 'oracle.jdbc.OracleDriver'
URL = 'jdbc:oracle:thin:@' + oracle_xe_db_host + ':' + str(oracle_xe_db_port) + '/' + oracle_xe_db_service


cd('/JdbcSystemResource/LocalSvcTblDataSource/JdbcResource/LocalSvcTblDataSource')
updateDataSource(DRIVERNAME, URL, 'STB')

print 'first cd=/JdbcSystemResource/mds-owsm/JdbcResource/mds-owsm'
cd('/JdbcSystemResource/mds-owsm/JdbcResource/mds-owsm')
updateDataSource(DRIVERNAME, URL, 'MDS')
cd('/JdbcSystemResource/mds-owsm/JdbcResource/mds-owsm/JDBCConnectionPoolParams/NO_NAME')
cmo.setMaxCapacity(2) 
cd ('../..')

appendJndiName('mds-owsm', 'jdbc/mds/MDS_LocalTxDataSource')
appendJndiName('mds-owsm', 'jdbc/mds-ESS_MDS_DS')
appendJndiName('mds-owsm', 'jdbc/mds/ESS_MDS_DS')

cd('/JdbcSystemResource/SOADataSource/JdbcResource/SOADataSource')
updateDataSource(XADRIVERNAME, URL, 'SOAINFRA')

cd('/JdbcSystemResource/SOALocalTxDataSource/JdbcResource/SOALocalTxDataSource')
updateDataSource(DRIVERNAME, URL, 'SOAINFRA')

cd('/JdbcSystemResource/opss-data-source/JdbcResource/opss-data-source')
updateDataSource(DRIVERNAME, URL, 'OPSS')

cd('/JdbcSystemResource/opss-audit-viewDS/JdbcResource/opss-audit-viewDS')
updateDataSource(DRIVERNAME, URL, 'IAU_VIEWER')

cd('/JdbcSystemResource/opss-audit-DBDS/JdbcResource/opss-audit-DBDS')
updateDataSource(DRIVERNAME, URL, 'IAU_APPEND')


setOption('BackupFiles','false')

setJDBCStorePrefixName()
setTLOGDataSource()
setDeterminer()

configMigratableTargets()

printJndiNames('mds-owsm')
updateDomain()
closeDomain()
exit()


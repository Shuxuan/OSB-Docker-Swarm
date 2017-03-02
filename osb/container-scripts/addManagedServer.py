import os

mwHome = os.getenv('MW_HOME', '/u01/oracle/weblogic')
localTemplate = os.getenv('OSB_TEMPLATE', mwHome + '/user_projects/osbManagedTemplate.jar')
domainPath = os.getenv('DOMAIN_DIR', mwHome + '/user_projects/osbDomain')
adminHostname = os.getenv('ADMIN_HOSTNAME', 'wlsadmin')
adminPort = os.getenv('ADMIN_PORT', '7001')
adminUsername = os.getenv('ADMIN_USERNAME', 'weblogic')
adminPassword = os.getenv('ADMIN_PASSWORD', 'Welcome1')
managedServername = os.getenv('MS_NAME', 'osb_server1')
machineName = os.getenv('MACHINE_NAME', 'osb1Machine')
hostname = os.getenv(("HOSTNAME', 'localhost')
 
#Substitute the administrator user name and password values below as needed
connect(adminUsername, adminPassword, adminHostname+':'+adminPort)
 
#The path on the local machine where the template will be created, 
#it should not already exist.
templatePath = localTemplate
 
#get the packed template from the Administration Server
writeTemplate(templatePath)
 
#disconnect from online WLST connection to the Administration Server
disconnect()
 
#select and load the template that was downloaded from the Administration 
#Server. 
selectCustomTemplate(templatePath)
loadTemplates()

# set the Node Manager listen address and listen port.
cd('/')
cd('NMProperties')
set('ListenAddress', hostname) 

#create the domain
writeDomain(domainPath)

# Connect to domain
connect(adminUsername, adminPassword, adminHostname+':'+adminPort)

# Start Edit Session
edit()
startEdit()

# Create Machine
cd('/')
machine = create(machineName, 'UnixMachine')
cd('Machines/'+machineName+'/NodeManager/'+machineName)
cmo.setName(machineName)
cmo.setListenAddress(hostname)

# Create Managed Server
cd('/')

# Change Target Host
cd('/Servers/'+managedServername)
cmo.setListenAddress(hostname)
cmo.setMachine(getMBean('/Machines/'+machineName)
 
# Close Session
save()
activate(block='true')

#disconnect from online WLST connection to the Administration Server
disconnect()

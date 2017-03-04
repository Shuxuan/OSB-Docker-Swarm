import os

execfile('/u01/oracle/commonfuncs.py')

connectAdmin()
 
#get the packed template from the Administration Server
writeTemplate(localTemplate)
 
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
connectAdmin()

# Start Edit Session
edit()
startEdit()

# Create Machine
createMachine()

# Create Managed Server
cd('/')

# Change Target Host
cd('/Servers/'+managedServername)
cmo.setListenAddress(hostname)
cmo.setMachine(getMBean('/Machines/'+machineName))
 
# Close Session
save()
activate(block='true')

#disconnect from online WLST connection to the Administration Server
disconnect()

import os

mwHome = os.getenv('MW_HOME', '/u01/oracle/weblogic')
localTemplate = os.getenv('OSB_TEMPLATE', mwHome + '/user_projects/osbManagedTemplate.jar')
domainPath = os.getenv('DOMAIN_DIR', mwHome + '/user_projects/osbDomain')
adminHostname = os.getenv('ADMIN_HOSTNAME', 'localhost')
adminPort = os.getenv('ADMIN_PORT', '7001')
adminUsername = os.getenv('ADMIN_USERNAME', 'weblogic')
adminPassword = os.getenv('ADMIN_PASSWORD', 'welcome1')
managedServername = os/getenv('MS_NAME', 'osb1')
 
#Substitute the administrator user name and password values below as needed
connect(adminUsername, adminPassword, adminstHostname+':'+adminPort)
 
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
 
#create the domain
writeDomain(domainPath)

# Connect to domain
connect(adminUsername, adminPassword, adminstHostname+':'+adminPort)

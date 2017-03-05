import os
import socket

# Initialize Variables
# ====================
# Environment Vars
hostname       = socket.gethostname()
# Admin Vars
admin_username = os.environ.get('ADMIN_USERNAME', 'weblogic')
admin_password = os.environ.get('ADMIN_PASSWORD', 'Welcome1') # this is read only once when creating domain (during docker image build)
admin_host     = os.environ.get('ADMIN_HOST', 'wlsadmin')
admin_port     = os.environ.get('ADMIN_PORT', '7001')
# Node Manager Vars
nmname         = os.environ.get('NM_NAME', 'Machine-' + hostname)
# Domain Template Vars
localTemplate  = os.environ.get('OSB_TEMPLATE', '/u01/oracle/osbManagedTemplate.jar')
domainPath = os.getenv('DOMAIN_HOME', '/u01/oracle/domains/osb_domain')
# Machine Vars
machineName = os.environ.get('MACHINE_NAME', 'osb1Machine')
# Managed Server Vars
managedServername = os.environ.get('MS_NAME', 'osb_server1')
managedServerPort = os.environ.get('MS_PORT', '8011')
# Cluster Vars
cluster_name = os.environ.get("CLUSTER_NAME", "osb_cluster")

# Enter Edit Mode
# Should be Paired with saveActivate
def editMode():
    edit()
    startEdit(waitTimeInMillis=60000,
              timeOutInMillis=300000,
              exclusive="true")

def saveActivate():
    """ Save and Activate Changes
        Should be Paired with editMode
    """
    save()
    activate(block="true")

def connectToAdmin():
    """ Connect to Admin Server
    """
    connect(url='t3://' + admin_host + ':' + admin_port,
            adminServerName='AdminServer',
            username=admin_username,
            password=admin_password)

def createMachine():
    """ Create a WebLogic Machine
        Set the machine address
    """
    cd('/')
    machine = create(machineName, 'UnixMachine')
    cd('Machines/'+machineName+'/NodeManager/'+machineName)
    cmo.setName(machineName)
    cmo.setListenAddress(hostname)

def registerServer():
    """ Register Server with Machine
        Configure Server to Listen on Hostname
        Associate server with a machine
    """
    cd('/')
    cd('/Servers/'+managedServername)
    cmo.setListenAddress(hostname)
    cmo.setMachine(getMBean('/Machines/'+machineName))

def createServer():
    """ Create a Server
        Add it to the cluster
        Set the Listen Port
    """
    cd('/')
    cmo.createServer(managedServername)    
    cd('/Servers/' + managedServername)
    cmo.setCluster(getMBean('/Clusters/%s' % cluster_name))
    cmo.setListenPort(managedServerPort)

def writeDomainFile():
    """ Write the domain file
        get the packed template from the Administration Server
    """
    writeTemplate(localTemplate)

def createManagedDomain():
    """ "Apply the template to create the domain
        Set the NodeManager listen address
        select and load the template that was downloaded from the Administration 
        Server.
    """
    selectCustomTemplate(localTemplate)
    loadTemplates()
    # set the Node Manager listen address and listen port.
    cd('/')
    cd('NMProperties')
    set('ListenAddress', hostname) 
    #create the domain
    writeDomain(domainPath)

def createBootPropertiesFile():
    directoryPath = domainPath+'/servers/'+managedServername+'/security'
    serverDir = File(directoryPath)
    bool = serverDir.mkdirs()
    fileNew=open(directoryPath + '/boot.properties', 'w')
    fileNew.write('username=%s\n' % admin_username)
    fileNew.write('password=%s\n' % admin_password)
    fileNew.flush()
    fileNew.close()

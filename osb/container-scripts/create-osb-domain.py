# Copyright (c) 2014-2015 Oracle and/or its affiliates. All rights reserved.
#
# WebLogic on Docker Default Domain
#
# Domain, as defined in DOMAIN_NAME, will be created in this script. Name defaults to 'base_domain'.
#
# Since : October, 2014
# Author: bruno.borges@oracle.com
# ==============================================
oracle_home = '/u01/oracle/weblogic'
wl_home = oracle_home +'/wlserver'
domain_name  = os.environ.get("DOMAIN_NAME", "osb_domain")
domain_path  = '/u01/oracle/domains/%s' % domain_name
admin_port   = int(os.environ.get("ADMIN_PORT", "7001"))
admin_pass   = os.environ.get("ADMIN_PASSWORD")
cluster_name = os.environ.get("CLUSTER_NAME", "osb_cluster")
production_mode = os.environ.get("PRODUCTION_MODE", "prod")
osb_port = '8011'
wls_template = oracle_home + '/wlserver/common/templates/wls/wls.jar'    
    
def main():
    

    print('domain_name : [%s]' % domain_name);
    print('admin_port  : [%s]' % admin_port);
    print('cluster_name: [%s]' % cluster_name);
    print('domain_path : [%s]' % domain_path);
    print('production_mode : [%s]' % production_mode);

    # Open default domain template
    # ======================
    readTemplate("/u01/oracle/weblogic/wlserver/common/templates/wls/wls.jar")

    set('Name', domain_name)
    setOption('DomainName', domain_name)
    
    # Disable Admin Console
    # --------------------
    # cmo.setConsoleEnabled(false)
    
    # Configure the Administration Server and SSL port.
    # =========================================================
    cd('/Servers/AdminServer')
    set('ListenAddress', '')
    set('ListenPort', admin_port)
    
    # Define the user password for weblogic
    # =====================================
    cd('/Security/%s/User/weblogic' % domain_name)
    cmo.setPassword(admin_pass)
    
    # Write the domain and close the domain template
    # ==============================================
    setOption('OverwriteDomain', 'true')
    setOption('ServerStartMode',production_mode)
    
    cd('/NMProperties')
    set('ListenAddress','')
    set('ListenPort',5556)
    set('CrashRecoveryEnabled', 'true')
    set('NativeVersionEnabled', 'true')
    set('StartScriptEnabled', 'false')
    set('SecureListener', 'false')
    set('LogLevel', 'FINEST')
    
    # Set the Node Manager user name and password (domain name will change after writeDomain)
    cd('/SecurityConfiguration/osb_domain')
    set('NodeManagerUsername', 'weblogic')
    set('NodeManagerPasswordEncrypted', admin_pass)
    
    # Define a WebLogic Cluster
    # =========================
    cd('/')
    create(cluster_name, 'Cluster')
    
    cd('/Clusters/%s' % cluster_name)
    cmo.setClusterMessagingMode('unicast')
    
    # Write Domain
    # ============
    writeDomain(domain_path)
    closeTemplate()
    
    # Create OSB Cluster
    OSB_TEMPLATE_PATH='/u01/oracle/weblogic/osb/common/templates/wls/oracle.osb_template.jar'
    readDomain(domain_path)
    addTemplate(OSB_TEMPLATE_PATH)

# call main() and then exit WLST
# Exit WLST
# =========
main()
exit()    


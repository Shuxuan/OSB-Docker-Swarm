execfile(os.path.dirname(os.path.realpath(sys.argv[0]))+'/commonfuncs.py')

# Create Domain File
connectToAdmin()
writeDomainFile()
disconnect()

#Create Managed Server Domain
createManagedDomain()

# Start edit session
connectToAdmin()
editMode()

# Test if not node 1 so need to create server
if hostname != 'wls1':
    createServer()

# Register server and create machine
createMachine()
registerServer()

# Save and activate
saveActivate()

disconnect()

# Create boot properties
createBootPropertiesFile()
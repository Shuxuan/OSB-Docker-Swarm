execfile(os.path.dirname(os.path.realpath(sys.argv[0]))+'/commonfuncs.py')

# Start edit session
connectToAdmin()
editMode()

# Create machine
print("Creating Machine")
createMachine()

# Test if not node 1 so need to create server
if hostname != 'wls1':
    print("Creating Server")
    srv = createServer()
    # Register server
    print("Assigning Server to Machine")
    registerServer(srv)
else:
    # Register server
    print("Assigning Server to Machine")
    registerExistingServer()

# Save and activate
print("Activating Changes")
saveActivate()

disconnect()

connectToAdmin()

# Create Domain File
print("Creating domain file")
writeDomainFile()

disconnect()

#Create Managed Server Domain
print("Creating Managed Server Domain")
createManagedDomain()

# Create boot properties
print("Creating Boot Properties File")
createBootPropertiesFile()


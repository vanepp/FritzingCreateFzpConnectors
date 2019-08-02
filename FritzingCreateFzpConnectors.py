#!/usr/bin/env python3

# Generate the connector fzp xml for Fritizng connectors. Optionally start
# at a connector other than 0.

Version = '0.0.0'  # Version number of this file.
	
# Set up the requested debug level

# Import os and sys to get file rename and the argv stuff, re for regex and
# logging for logging support

import getopt, os, os.path, sys, re, logging 

# Configure the root logging instance, even though we won't be using it
# (we will create loggers for each module) as this is said to be best 
# practice.

logging.basicConfig(stream=sys.stderr, format='  %(levelname)s: %(filename)s line %(lineno)d \n   %(message)s', level=logging.DEBUG)
    
# Create a child logger for this routine.
    
logger = logging.getLogger(__name__)

# Set the logging level.

logger.setLevel(logging.WARNING)
#logger.setLevel(logging.DEBUG)     

def Usage():

    print ('Usage: FritzingCreateFzpConnectors.py <-bops> Output-file Number-of-connectors <starting-connector-number>\n\nWhere:\n    -b | --breadboard-terminalId   : Emit breadboard TerminalId\n    -o | --overwrite               : Overwrite the output file if it exists\n    -p | --no-pcb-layer            : omit pcb layer\n    -s | --no-schematic-terminalId : Don\'t emit schematic terminalId\n')

    exit(1)

# End of def Useage():

def ProcessArgs(Argv):

    logger.info ('Entering ProcessArgs\n')

    logger.debug ('ProcessArgs: Argv %s\n',Argv)

    # Set the default values of the getopt options

    BreadBoardTerminalId = "n"

    PcbView = "y"

    SchematicTerminalId = "y"

    FileOverwrite = 'n'

    print ('\n')

    if len (Argv) < 3:

        print ('Too few arguments\n') 

        Usage()
        
        exit(1)

    # End of if len (Argv) < 3:

    # Process any - type flags on the command line with getopt.

    try:

        # Options are in alphabetical order to make adding new ones easier.

        Options, Remainder = getopt.gnu_getopt(sys.argv[1:], 'bops', ['breadboard-terminalId', 'overwrite', 'no-pcb-layer', 'no-schematic-terminalId'])

    except getopt.GetoptError as Err:

        print ('Error: {0:s}\n'.format(str(Err)))

        logger.debug ('ProcessArgs: getopt except\n')

        Usage()

    # End of try:

    for Opt in Options:

        logger.debug ('ProcessArgs: Opt \'%s\'\n', Opt)

        if Opt[0] in ('-b', '--breadboard-terminalId'):

            # Enable breadboard terminalId

            BreadBoardTerminalId = "y"

            logger.debug ('ProcessArgs: Set BreadBoardTerminalId = %s\n', BreadBoardTerminalId)

        elif Opt[0] in ('-o', '--overwrite'):

            FileOverwrite = "y"

            logger.debug ('ProcessArgs: Set FileOverwrite = %s\n', FileOverwrite)

        elif Opt[0] in ('-p', '--no-pcb-layer'):

            PcbView = "n"

            logger.debug ('ProcessArgs:  PcbView = %s\n', PcbView)

        elif Opt[0] in ('-s', '--no-schematic-terminalId'):

            SchematicTerminalId = "n"

            logger.debug ('ProcessArgs: SchematicTerminalId  = %s\n', SchematicTerminalId)

        else:

            print('Error: Unknown option {0:s}\n'.format(Opt[0]))

            logger.debug ('ProcessArgs: if statement else\n')

            Usage()

    # End of for Opt in Options:

    if len(Remainder) < 2 or len(Remainder) > 4:

        print ("too few or too many arguments\n");

        Usage()

    # End of if len(Remainder) < 2 or len(Remainder) > 4:

    logger.debug ('ProcessArgs: Remainder %s\n', Remainder)

    OutFileName = Remainder[0]

    NumberOfConnectors = Remainder[1]

    if not NumberOfConnectors.isdigit():

        print ('Error: NumberOfConnectors must be an integer value\n')

        Usage()

    # End of if not NumberOfConnectors.isdigit():
        
    StartingConnector = 0

    if len (Remainder) > 2:
        
        StartingConnector = Remainder[2]

        if not StartingConnector.isdigit():

            print ('Error: StartingConnector must be an integer value\n')

            Usage()

        # End of if not StartingConnector.isdigit():
    
    # End of if len (Remainder) > 2:

    if FileOverwrite == 'n':

        if os.path.exists(OutFileName):

            print ('Error: File {0:s} already exists.\n'.format(OutFileName))

            Usage()

        # End of if os.path.exists(OutFileName):

    # End of if OverWrite == 'n':
   
    try:

        OutFile = open(OutFileName, 'w')

    except os.error as e:

        print ('\nError: Can not open file\n\n\'{0:s}\'\n\nto write {1:s} ({2:d})\n'.format(e.filename, e.strerror, e.errno))

        Usage()

    # end of try:

    logger.debug ('ProcessArgs:\n\nOutput file \'%s\'\nNumber of Connectors %s\nStartingConnector %s BreadBoardTerminalId %s FileOverwrite %s PcbView = %s SchematicTerminalId %s\n', OutFileName, NumberOfConnectors, StartingConnector, BreadBoardTerminalId, FileOverwrite, PcbView, SchematicTerminalId)

    return OutFile, NumberOfConnectors, StartingConnector, BreadBoardTerminalId, PcbView, SchematicTerminalId

# End of def ProcessArgs(Argv):

def CreateConnector(Connector, OutFile, BreadBoardTerminalId, PcbView, SchematicTerminalId):

    logger.debug ('CreateConnector:\n\nConnector %s BreadBoardTerminalId %s PcbView = %s SchematicTerminalId %s\n', Connector, BreadBoardTerminalId, PcbView, SchematicTerminalId)

    # Create the intial connector id with blank name and description fields.

    print ('      <connector id="connector{0:d}" type="male" name="">'.format(Connector), file = OutFile)
    print ('        <description></description>', file = OutFile)

    # Then create the connector views

    print ('        <views>',  file = OutFile)
    print ('          <breadboardView>', file = OutFile)

    if BreadBoardTerminalId == "y":

        # If a Breadboard teminalId is requested generate one. 

        print ('            <p svgId="connector{0:d}pin" layer="breadboard" terminalId="connector{0:d}terminal"/>'.format(Connector), file = OutFile)

    else:

        # Breadboard terminalId not wanted (the normal case)
        
        print ('            <p svgId="connector{0:d}pin" layer="breadboard"/>'.format(Connector), file = OutFile)

    # End of if BreadBoardTerminalId == "y":

    print ('          </breadboardView>', file = OutFile)
    print ('          <schematicView>', file = OutFile)

    if SchematicTerminalId == "n":

        # Schematic terminalId not wanted

        print ('            <p svgId="connector{0:d}pin" layer="schematic"/>'.format(Connector), file = OutFile)

    else:

        # Schematic terminalId wanted (the normal case)

        print ('            <p svgId="connector{0:d}pin" layer="schematic" terminalId="connector{0:d}terminal"/>'.format(Connector), file = OutFile)
    print ('          </schematicView>', file = OutFile)

    # optionally skip creating the pcbview entries for when your part doesn't
    # fit on a pcb (such as a module with screw terminals where pcb view 
    # doesn't make sense.)

    if PcbView == "y":

        # Pcb view wanted (the normal case), create a pcb view entry

        print ('          <pcbView>', file = OutFile)
        print ('            <p svgId="connector{0:d}pin" layer="copper0"/>'.format(Connector), file = OutFile)
        print ('            <p svgId="connector{0:d}pin" layer="copper1"/>'.format(Connector), file = OutFile)
        print ('          </pcbView>', file = OutFile)

    # End of if not PcbView == "n":

    print ('        </views>', file = OutFile)
    print ('      </connector>', file = OutFile)

# End of def CreateConnector(Connector, OutFile):

	
def Main():

    (OutFile, NumberOfConnectors, StartingConnector, BreadBoardTerminalId, PcbView, SchematicTerminalId) = ProcessArgs(sys.argv)

    logger.debug ('Main:\n\nNumber of Connectors %s\nStartingConnector %s BreadBoardTerminalId %s PcbView = %s SchematicTerminalId %s\n', NumberOfConnectors, StartingConnector, BreadBoardTerminalId, PcbView, SchematicTerminalId)

    for Connector in range (int(StartingConnector), int(StartingConnector) + int(NumberOfConnectors)):

#        print ('Doing connector {0:d}\n'.format(Connector))

        CreateConnector(Connector, OutFile, BreadBoardTerminalId, PcbView, SchematicTerminalId)

    # End of for Connector in range (StartingConnector, StartingConnector + NumberOfConnectors):

    OutFile.close()

    exit (0)

# End of def Main():

# call the main procedure. 

if __name__ == "__main__":    Main()

    

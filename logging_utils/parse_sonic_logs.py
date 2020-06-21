#!/usr/bin/python3

import getopt, sys, re, os, glob

# Big log help message.
#
helpMsg='\n\
#  Examples:\n\
#  \n\
#  Generate a list of all \'git\' references.\n\
#\n\
parse_sonic_logs.py -t ./sonic-buildimage -g  > git_ref.txt\n\
\n\
#  Generate a list of all \'wget\' references.\n\
#\n\
parse_sonic_logs.py -t ./sonic-buildimage -w  > wget_ref.txt\n\
\n\
#  Search the tree for all \'get\' references, specifyig the\n\
#  entire path minues the \'https://\' (-f) in the search string.\n\
#  and only search \'*akefile\', \'Dockerfile*\' and \'*.mk\' (-b)\n\
#  files in the search.\n\
#\n\
#  Note that <git_ref.txt> was generated from command shown\n\
#  above.\n\
#\n\
parse_sonic_logs.py -t ./sonic-buildimage/src -b -f -g -i git_ref.txt\n\
'

class parserOps:

    def __init__( self ):
        self.treeRoot = None
        self.searchTreeRoot = None
        self.logFileRoot = 'logs'
        self.gitReport = False
        self.wgetReport = False
        self.pipReport = False
        self.inFile = None
        self.humanReadable = False
        self.fullPath = False
        self.buildOnly = False
        self.verbose = False

    def dumpOptions( self ):
        print( '(-t:) treeRoot: <%s>' % self.treeRoot )
        print( '(-s:) searchTreeRoot: <%s>' % self.searchTreeRoot )
        print( '(-l:) logFileRoot: <%s>' % self.logFileRoot ) 
        print( '(-g) gitReport: %s' % self.gitReport )
        print( '(-w) wgetReport: %s' % self.wgetReport )
        print( '(-p) pipReport: %s' % self.pipReport )
        print( '(-n) humanReadable %s' % self.humanReadable )
        print( '(-i:) inFile <%s>' % self.inFile )
        print( '(-f) Use Full (https://xx.xx/component> path in search <%s>' % self.fullPath )
        print( '(-b) Only search Docker.* *.mk and *akefile* [%s]' % self.buildOnly )
        print( helpMsg )

    def findUrl( self, inString ):
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall( regex,inString )       
        return [x[0] for x in url] 

    def parseHttpLog( self, httpLog ):
        fullPath = os.path.join( self.treeRoot, self.logFileRoot, httpLog );
        with open( fullPath, 'r' ) as inFile:
            content = inFile.readlines()

        inFile.close()
        
        for lineItem in content:
            urlList = self.findUrl( lineItem )
            if len( urlList ) > 0:
                   print( '%s' % urlList[ 0 ] )

    def parsePipLog( self, pipLog ):
        fullPath = os.path.join( self.treeRoot, self.logFileRoot, pipLog );
        with open( fullPath, 'r' ) as inFile:
            content = inFile.readlines()

        inFile.close()

        for lineItem in content:
            splitLine = lineItem.split()
            if lineItem.find( 'Downloading from URL' ) > 0:
                urlList = self.findUrl( lineItem )
                t = urlList[ 1 ].rstrip( '/' )
                j = t.rfind( '/' )
                print( t[j+1:] )

    def printGitLog( self ):
        if self.humanReadable:
            print( '===' )
            print( 'git references from sonic-slave-stretch creation (make configure PLATFORM=broadcom):' )
            print( ' ')

        logParser.parseHttpLog( 'db_git_log.txt' )

        if self.humanReadable:
            print( '===' )
            print( 'git references from building target/sonic-broadcom.bin (make target/sonic-broadcom.bin):' )
            print( ' ')

        logParser.parseHttpLog( 'rt_git_log.txt' )

    def printWgetLog( self ):
        if self.humanReadable:
            print( '===' )
            print( 'wget references from sonic-slave-stretch creation (make configure PLATFORM=broadcom):' )
            print( ' ')

        logParser.parseHttpLog( 'db_wget_log.txt' )

        if self.humanReadable:
            print( '===' )
            print( 'wget references from building target/sonic-broadcom.bin (make target/sonic-broadcom.bin):' )
            print( ' ')

        logParser.parseHttpLog( 'rt_wget_log.txt' )

    def printPipLog( self ):
        if self.humanReadable:
            print( '===' )
            print( 'pip references from sonic-slave-stretch creation (make configure PLATFORM=broadcom):' )
            print( ' ')

        logParser.parsePipLog( 'db_pip_install_log.txt' )

        if self.humanReadable:
            print( '===' )
            print( 'pip references from building target/sonic-broadcom.bin (make target/sonic-broadcom.bin):' )
            print( ' ')

        logParser.parsePipLog( 'rt_pip_install_log.txt' )

    def stringCheck( self, inFile, inString ):
        datafile = open( inFile, 'r', encoding='latin-1' )
        found = False
        for line in datafile:
            if inString in line:
                return True

        return False

    def searchTree( self, searchString ):

        for dirName, subdirList, fileList in os.walk( self.treeRoot ):

            if '.git' in dirName:
                continue;

            if '.github' in dirName:
                continue;

            if not os.path.isdir( dirName ):
                print( 'bad path: <%s>' % dirName )
                sys.exit( 1 );

            if self.buildOnly == True:
                buildFlist = ''.join( glob.glob( '%s/*.mk' % dirName ) )
                buildFlist += ''.join( glob.glob( '%s/Dockerfile.*' % dirName ) )
                buildFlist += ''.join( glob.glob( '%s/Dockerfile' % dirName ) )
                buildFlist += ''.join( glob.glob( '%s/*akefile' % dirName ) )

                splitBuildList=buildFlist.split()
                if len( splitBuildList ) > 0:
                    for fname in splitBuildList:
                        fPath = os.path.join( dirName, fname )
                        if os.path.isfile( fPath ):
                            if self.stringCheck( fPath, searchString ) == True:
                                print( 'Found %s in: %s' % (searchString, fPath) )

            else:
                for fname in fileList:
                    fPath = os.path.join( dirName, fname )
                    if os.path.isfile( fPath ):
                        if self.stringCheck( fPath, searchString ) == True:
                            print( 'Found %s in: %s' % (searchString, fPath) )
 

    def findNth( self, inString, findString, n ):
        start = inString.find( findString )
        while start >= 0 and n > 1:
            start = inString.find( findString, start+len( findString ) )
            n -= 1
        return start

    def searchGitReferences( self ):
        with open( self.inFile, 'r' ) as f:
            content = f.readlines()
            for item in content:

                if self.fullPath == True:
                    index = self.findNth( item, '/', 2 )
                else:
                    index = self.findNth( item, '/', 3 )

                searchString=item[ (index + 1):-1 ]
                sourceString=item[ 0:index ]

                if self.verbose == True:
                    print( 'Source URL [%s], search string [%s]' % (sourceString, searchString) )

                self.searchTree( searchString )

        f.close()

    def logMessage( self, msg ):
        if self.verbose == True:
            print( '%s' % msg )

    def checkVerbose( self ):
        return( self.verbose )

    def parseArgs( self ):
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'ht:s:l:wgpni:fbv' )
        except getopt.GetoptError as err:
            print( err )  
            self.dumpOptions()
            sys.exit( 2 )

        for o, a in opts:
            if o == "-v":
                self.verbose = True
            elif o in '-h':
                print( 'Help Options:' )
                print( ' ')
                self.dumpOptions()
                sys.exit( 0 )
            elif o in '-l':
                self.logFileRoot = a
            elif o in '-t':
                self.treeRoot = a
            elif o in '-s':
                self.searchTreeRoot = a
            elif o in '-g':
                self.gitReport = True
            elif o in '-w':
                self.wgetReport = True
            elif o in '-p':
                self.pipReport = True
            elif o in '-n':
                self.humanReadable = True
            elif o in '-i':
                self.inFile = a
            elif o in '-f':
                self.fullPath = True
            elif o in '-b':
                self.buildOnly = True
            else:
                assert False, "unhandled option"

    def execute( self ):
        #  At a minium, we need some sort of tree root to
        #  base operations off off.
        #
        if self.treeRoot == None:
            print( ' ' )
            print( 'No Sonic-2 root directory specified - Please specify options' )
            print( ' ' )
            logParser.dumpOptions()
            sys.exit( 1 );


        #  If we have an input file, assume we are
        #  searching for refernces based on 'git' or 'wget'
        #  toggle.  Assumption is inFile is in CWD.
        #
        if self.inFile != None:
            if self.gitReport == True:
                self.searchGitReferences()

            #  Always return True if we parse input file;
            #  no further processing.
            #
            return True

        #  We fell through, no input file - format logs
        #  based on toggle specifiers.
        #
        if self.gitReport == True:
            self.printGitLog()

        if self.wgetReport == True:
            self.printWgetLog() 

        if self.pipReport == True:
            self.printPipLog()

if __name__ == "__main__":

    logParser = parserOps()
 
    # Parse all input before processing.
    #
    logParser.parseArgs()

    #  If verbose, dump options.
    #
    if logParser.checkVerbose() == True:
        logParser.dumpOptions()

    # Execute Operations.
    #
    logParser.execute()



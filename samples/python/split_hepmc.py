'''Split HEPMC files
'''

# Standard imports
import os
import zipfile
import pickle

# Logger
import logging
logger = logging.getLogger(__name__)

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def file_open( filename, counter ):
   
    if not filename.endswith('.hepmc'):
        raise RuntimeError( "Need .hepmc file")
    
    dirname = filename.rstrip('.hepmc')
    if not os.path.exists( dirname ):
        os.makedirs( dirname )
    
    fname = os.path.basename( dirname )

    filename = os.path.join( dirname, fname + '_' + str( counter ) + '.hepmc' ) 

    return open( filename, 'w')

def split_file( inputFile, maxEvents):
    event_counter = 0
    with open( inputFile ) as infile:

        file_counter = 0
        outfile = file_open( inputFile, file_counter)

        for iline, line in enumerate(infile):
            if iline==0:
                version = line
            if line.startswith( 'E ' ) and RepresentsInt(line.split()[1]): # new event

                if event_counter>0 and event_counter%maxEvents == 0: # need new file
                    # write last line
                    outfile.write('HepMC::IO_GenEvent-END_EVENT_LISTING\n')
                    outfile.close()
                    logger.info( "After a total of %i events wrote %i events to file %s", event_counter, maxEvents, outfile.name )
                    file_counter += 1
                    outfile = file_open( inputFile, file_counter)
                    logger.info( "Opened new file %s", outfile.name ) 
                    outfile.write(version) 
                    outfile.write('HepMC::IO_GenEvent-START_EVENT_LISTING\n') 
                event_counter += 1            

            outfile.write( line )

        outfile.write('HepMC::IO_GenEvent-END_EVENT_LISTING')
        outfile.close()
        logger.info( "After a total of %i events wrote %i events to file %s", event_counter, maxEvents, outfile.name )

def count_events( filename ):
    count=0
    logger.debug( "Counting events in file %s", filename )
    with open( filename ) as f:
        for line in f.readlines():
            if line.startswith( 'E ' ): count+=1

    return count

def process_zip_directory( directory, maxEvents):
    # Loop over all zip files, unzip, split
    for zfilename in os.listdir( directory ):
        if zfilename.endswith( '.zip' ):
            logger.info( "Working on file %s", zfilename)
            zfile = zipfile.ZipFile(os.path.join( directory, zfilename))
            output_tmp_name = zfile.namelist()[0]
            output_name     = zfilename.replace('.zip', '.hepmc')
            output_dir      = zfilename.replace('.zip', '')
            if os.path.exists( os.path.join(directory, output_dir) ):
                logger.info( "Found %s, do nothing", os.path.join(directory, output_dir) )
            else:
                logger.info( "Extracting file %s", zfilename)
                zfile.extract( output_tmp_name, path = directory )
                os.rename( os.path.join(directory, output_tmp_name), os.path.join(directory, output_name))
                logger.info( "Created %s", output_name)
                # split
                split_file( os.path.join(directory, output_name), maxEvents)
                # delete unzipped hepmc file
                os.remove( os.path.join(directory, output_name) )

            #count events
            pkl_filename = os.path.join(directory, output_dir+'.pkl')
            nEvents = None
            if not os.path.exists( pkl_filename ):
                logger.info( "Counting events in %s", os.path.join(directory, output_dir) )
                nEvents = sum( [count_events(os.path.join( directory, output_dir, filename )) for filename in os.listdir( os.path.join(directory, output_dir) )], 0)
                pickle.dump( nEvents, file( pkl_filename, 'w' ) ) 

if __name__ == '__main__':

    # Arguments
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser")
    argParser.add_argument('--logLevel',           action='store',      default='INFO',          nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
    argParser.add_argument('--maxEvents',          action='store',      nargs='?', type=int, default=1000,  help="Maximum number of events")
#    argParser.add_argument('--inputFile',          action='store',      nargs='?', required = True)
    args = argParser.parse_args()
#
#    from TTXPheno.samples.hepmc_samples import *
#
    # Logger
    import TTXPheno.Tools.logger as _logger
    logger = _logger.get_logger(   args.logLevel, logFile = None)

#    for sample in [ttbarZ, bbar]: #ttbar
#       for subsample in sample.samples:
#            for filename in subsample.files:
#                split_file( filename, args.maxEvents )

    process_zip_directory( "/afs/hephy.at/data/cms01/TTXPheno/HEPMC/12_05/DATA_TTBARZ/full_range/C6/without_massterm/HEPMC", args.maxEvents)

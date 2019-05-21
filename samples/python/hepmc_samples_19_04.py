''' Read Simon Fernbachs HEPMC directories.
Boring but must be done.
'''

hepmc_directory = "/afs/hephy.at/data/rschoefbeck01/TTXPheno/HEPMC"

# RootTools
from RootTools.core.standard import *

# Standard imports
import os
import pickle

# Logging
import logging
logger = logging.getLogger(__name__)

# Logging
if __name__ == "__main__":
    import TTXPheno.Tools.logger as logger
    logger = logger.get_logger('DEBUG')
    import RootTools.core.logger as logger_rt
    logger_rt = logger_rt.get_logger('DEBUG')

class HEPMCData(object):

    pdfs      = ["1d0", "10d0", "100d0", "0d1", "0d01"]
    processes = ["GH", "HG", "HH"]

    def __init__ ( self, name, hepmc_directory, sub_directory, root_directory = None, isSplit = False):

        self.name         = name

        # a .hepmc single file or, if I split it up, a directory of the same name
        # Add PP:
        self.samples_dict = { 'PP':\
            HEPMCSample.fromFiles( name+"_PP", os.path.join( hepmc_directory, sub_directory, 'PP.hepmc') ) if not isSplit else  HEPMCSample.fromDirectory( name+"_PP", os.path.join( hepmc_directory, sub_directory, 'PP') ) }
        # Add root file for PP
        if root_directory is not None:
            self.root_samples_dict = {'PP': Sample.fromDirectory( name+"_PP", os.path.join( root_directory, name+"_PP" ) )}
        # Add the variations 
        for pdf in HEPMCData.pdfs:
            for process in HEPMCData.processes:
                self.samples_dict[pdf+'_'+process] = HEPMCSample.fromDirectory( name+'_'+pdf+'_'+process, os.path.join( hepmc_directory, sub_directory, '%s_%s'%(pdf, process)) )
                # Add the root files for the variations
                if root_directory is not None:
                    for process in HEPMCData.processes:
                        self.root_samples_dict[pdf+'_'+process] = Sample.fromDirectory( name+'_'+pdf+'_'+process, os.path.join( root_directory, name+'_%s_%s'%(pdf, process)) )

            # Read nEvents, xsec but we rather count ourselves
            _, xsecs = HEPMCData.read_crosssection(  os.path.join( hepmc_directory, sub_directory, '%s_crosssections.txt'%pdf) )
            if xsecs is not None:
                if hasattr( self.samples_dict['PP'], "xsec"):
                    if xsecs[0]!=self.samples_dict['PP'].xsec:
                        logger.waring( "Inconsistent PP cross sections! file: %s", os.path.join( hepmc_directory, sub_directory, '1d0_%s_crosssections.txt'%pdf) )

                self.samples_dict['PP'].xsec      = xsecs[0]
                self.samples_dict[pdf+"_GH"].xsec = xsecs[1]
                self.samples_dict[pdf+"_HG"].xsec = xsecs[2]
                self.samples_dict[pdf+"_HH"].xsec = xsecs[3]
            self.samples_dict['PP'].nEvents      = pickle.load(file( os.path.join( hepmc_directory, sub_directory, 'PP.pkl') ))
            self.samples_dict[pdf+"_GH"].nEvents = pickle.load(file( os.path.join( hepmc_directory, sub_directory, '%s_GH.pkl'%pdf) )) 
            self.samples_dict[pdf+"_HG"].nEvents = pickle.load(file( os.path.join( hepmc_directory, sub_directory, '%s_HG.pkl'%pdf) )) 
            self.samples_dict[pdf+"_HH"].nEvents = pickle.load(file( os.path.join( hepmc_directory, sub_directory, '%s_HH.pkl'%pdf) )) 

    def __getitem__( self, key ):
        return self.samples_dict[key]

    @staticmethod
    def read_crosssection( filename ):

        nEvents = None
        xsecs   = None
        with open(filename) as fp:
            for i, line in enumerate(fp):
                if i == 1: #Simon writes the x-sec in the 2nd line
                    line = line.rstrip().lstrip()
                    vals = map( float, line.split() )
                    nEvents, xsecs = vals[0], vals[1:]

        return nEvents, xsecs 

    @property
    def samples( self ):
        return self.samples_dict.values() 

    @property
    def files( self ):
        return sum( [s.files for s in self.samples], [] ) 

    @property
    def root_samples( self ):
        return self.root_samples_dict.values() 

    @property
    def root_files( self ):
        return sum( [s.files for s in self.root_samples], [] ) 
               
hepmc_directory = "/afs/hephy.at/data/cms01/TTXPheno/HEPMC/12_05/"
root_directory  = "/afs/hephy.at/data/rschoefbeck01/TTXPheno/skims/gen/RunII_v01/19_04/"
#bbar   = HEPMCData( "bbbar", os.path.join( hepmc_directory, "C89_BBBAR" ) )
#ttbar  = HEPMCData( "ttbar", os.path.join( hepmc_directory, "C89_TTBAR" ), isSplit = True, root_directory = root_directory)


ttbarZ_fr_C6_woMT = HEPMCData(  "ttbarZ_fr_C6_woMT", 
                                hepmc_directory = hepmc_directory, 
                                sub_directory   = "DATA_TTBARZ/full_range/C6/without_massterm/HEPMC", 
                                isSplit         = True, 
                                root_directory  = root_directory, 
                             )
ttbarZ_fr_C6_wMT = HEPMCData(  "ttbarZ_fr_C6_wMT", 
                                hepmc_directory = hepmc_directory, 
                                sub_directory   = "DATA_TTBARZ/full_range/C6/with_massterm/HEPMC", 
                                isSplit         = True, 
                                root_directory  = root_directory, 
                             )

''' 3rd directory structure from KFU 
'''

hepmc_directory = "/afs/hephy.at/data/cms06/TTXPheno/HEPMC/22_08/"

# RootTools
from RootTools.core.standard import *

# Standard imports
import os
import re
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

## HEPMC directory content:

#ttbar
#ttbarZ

#in each of these:

#base
#pdf-0.01
#pdf-0.1
#pdf-1
#pdf-10
#pdf-30
#pdf-35
#pdf-37
#pdf-40
#pdf-42
#pdf-43
#pdf-44
#pdf-45
#pdf-50
#pdf-75
#pdf-100

#in each of these:
#GH.hepmc.gz  GH.out  HG.hepmc.gz  HG.out  HH.hepmc.gz  HH.out
#(except in base where there is only PP)

# xsec file:
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>> Toolkit for HEP Event Generation - ThePEG eea16346ccff (release-2-1) <<<<
#>>>> Tue Jul 23 16:38:53 2019                                             <<<<
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#
#>> Herwig 3d69fbe18c68 (herwig-7-1) / ThePEG eea16346ccff (release-2-1)
#
#==============================================================================
#Statistics for event handler 'EventHandler':
#                                       generated    number of    Cross-section
#                                          events     attempts             (nb)
#==============================================================================
#Total (from attempted events): including vetoed events           0.684(3)e+00

class HEPMCData(object):

    pdfs      = ["0.01", "0.1", "1", "10", "30", "35", "37", "40", "42", "43", "44", "45", "50", "50", "75", "100"]
    #pdfs      = ["0.01", "0.1", "1", "10", "30", "35", "37", "42", "43", "44", "45", "50", "50", "75", "100"]
#    processes = ["GH", "HG", "HH"]

    def __init__ ( self, name, directory, root_directory = None, processes = ["GH", "HG", "HH"] ):

        self.processes = processes
        self.samples_dict = { 'PP':\
            HEPMCSample.fromDirectory( name+"_PP", os.path.join( directory, 'base', 'PP') ) }
        self.samples_dict['PP'].xSection = HEPMCData.read_crosssection(  os.path.join( directory, 'base', "PP.out") ) 
        self.samples_dict['PP'].nEvents  = pickle.load( file(os.path.join( directory, 'base', "PP.pkl")) )
        if root_directory is not None:
            self.root_samples_dict = {'PP': Sample.fromDirectory( name+"_PP", os.path.join( root_directory, name+"_PP" ))}
        
        self.name         = name
        for pdf in HEPMCData.pdfs:
            for process in self.processes:
                self.samples_dict['pdf-'+pdf+'_'+process]          = HEPMCSample.fromDirectory( name+'_pdf-'+pdf+'_'+process, os.path.join( directory, 'pdf-%s'%pdf, process) )
                self.samples_dict['pdf-'+pdf+'_'+process].xSection = HEPMCData.read_crosssection(  os.path.join( directory, 'pdf-%s'%pdf, "%s.out"%process) )
                self.samples_dict['pdf-'+pdf+'_'+process].nEvents  = pickle.load( file(os.path.join( directory, 'pdf-%s'%pdf, "%s.pkl"%process)) )
                if root_directory is not None:
                    self.root_samples_dict['pdf-'+pdf+'_'+process] = Sample.fromDirectory( name+'_pdf-'+pdf+'_'+process, os.path.join( root_directory, '%s_pdf-%s_%s'%(name, pdf, process)) )

        for sample in self.samples:
            sample.xsec = sample.xSection

    def __getitem__( self, key ):
        return self.samples_dict[key]

    @staticmethod
    def read_crosssection( filename ):
        xsec = None
        with open(filename) as fp:
            for i, line in enumerate(fp):
                if not line.startswith( 'Total (from generated events):' ):
                    continue
                xsec = float(re.sub(r'\([^)]*\)', '', line.rstrip().split()[-1]))
        return xsec

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
               
root_directory = "/afs/hephy.at/data/rschoefbeck01/TTXPheno/skims/gen/RunII_v02/22_05/"
#root_directory = None

ttbar  = HEPMCData( "ttbar", os.path.join( hepmc_directory, "ttbar" ), root_directory = root_directory)
#ttbarZ = HEPMCData( "ttbarZ", os.path.join( hepmc_directory, "ttbarZ" ), root_directory = root_directory)


# Phase II Delphes Simulation
root_directory = "/afs/hephy.at/data/rschoefbeck01/TTXPheno/skims/gen/PhaseII/22_05/"

ttbar_phase2 = HEPMCData( "ttbar", os.path.join( hepmc_directory, "ttbar" ), root_directory = root_directory, processes = [])

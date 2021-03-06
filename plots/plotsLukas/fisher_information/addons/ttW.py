#!/usr/bin/env python
''' Analysis script for standard plots
'''

# Standard imports and batch mode
import ROOT, os, itertools
ROOT.gROOT.SetBatch(True)
from math                                import pi, sqrt

# RootTools
from RootTools.core.standard             import *

def getVariableList( level ):
   
    # List of variables where gen is replaced by reco for reco
    read_variables_gen = [
        "ref_lumiweight1fb/F",
        "genMet_pt/F", "genMet_phi/F",
    
        "ngenJet/I", "genJet[pt/F,eta/F,phi/F]",
        "ngenLep/I", "genLep[pt/F,eta/F,phi/F,pdgId/I]",
    
        "genW_pt/F", "genW_eta/F", "genW_phi/F", "genW_mass/F",
    
        "genBj0_pt/F", "genBj0_phi/F", "genBj0_eta/F",
        "genBj1_pt/F", "genBj1_phi/F", "genBj1_eta/F",
    ]
     
    # List of variables where genLep is replaced by reco for reco
    read_variables_genLep = [
    ]
    
    if level == 'reco':
        read_variables_gen    = [ variable.replace('gen', 'reco') for variable in read_variables_gen ]
        read_variables_genLep = [ variable.replace('genLep', 'reco') for variable in read_variables_genLep ]

    read_variables = read_variables_gen + read_variables_genLep
    read_variables = list( set( read_variables ) ) # remove double entries
    read_variables.append( VectorTreeVariable.fromString('p[C/F]', nMax=2000) )

    return read_variables


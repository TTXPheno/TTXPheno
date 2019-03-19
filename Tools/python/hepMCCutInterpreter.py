''' Class to interpret string based cuts
'''

import logging
logger = logging.getLogger(__name__)

special_cuts = {
    "lepSel1":            "nrecoLep==1",#"Sum$(recoLep_pt>10&&(abs(recoLep_pdgId)==11||abs(recoLep_pdgId)==13)&&abs(recoLep_eta)<2.5)==1",
    "lepSel2":            "nrecoLep==2",#"Sum$(recoLep_pt>10&&(abs(recoLep_pdgId)==11||abs(recoLep_pdgId)==13)&&abs(recoLep_eta)<2.5)==2&&Sum$(recoLep_pt>20&&(abs(recoLep_pdgId)==11||abs(recoLep_pdgId)==13)&&abs(recoLep_eta)<2.5)>=1",
    "lepSel3":            "nrecoLep==3",#"Sum$(recoLep_pt>10&&(abs(recoLep_pdgId)==11||abs(recoLep_pdgId)==13)&&abs(recoLep_eta)<2.5)==3&&Sum$(recoLep_pt>20&&(abs(recoLep_pdgId)==11||abs(recoLep_pdgId)==13)&&abs(recoLep_eta)<2.5)>=2&&Sum$(recoLep_pt>40&&(abs(recoLep_pdgId)==11||abs(recoLep_pdgId)==13)&&abs(recoLep_eta)<2.5)>=1",
    "lepSel4":            "nrecoLep==4",#"Sum$(recoLep_pt>10&&(abs(recoLep_pdgId)==11||abs(recoLep_pdgId)==13)&&abs(recoLep_eta)<2.5)==4&&Sum$(recoLep_pt>40&&(abs(recoLep_pdgId)==11||abs(recoLep_pdgId)==13)&&abs(recoLep_eta)<2.5)>=1",
    "onZ":                "abs(recoZ_mass-91.2)<=15",
    "offZ":               "abs(recoZ_mass-91.2)>15",
    "all":                "(1)",
    "mumumu":             "Sum$(abs(recoLep_pdgId)==13)==3",
    "mumue":              "Sum$(abs(recoLep_pdgId)==11)==1&&Sum$(abs(recoLep_pdgId)==13)==2",
    "muee":               "Sum$(abs(recoLep_pdgId)==11)==2&&Sum$(abs(recoLep_pdgId)==13)==1",
    "eee":                "Sum$(abs(recoLep_pdgId)==11)==3",
  }

continous_variables = [ ("mll", "recoZ_mass"), ("met", "recoMet_pt"), ("Zpt","recoZ_pt"), ("gammaeta","abs(recoPhoton_eta[0])"), ("gammapt","recoPhoton_pt[0]") ]
discrete_variables  = [ ("nLep", "nrecoLep"), ("njet", "nrecoJet"), ("nbjet", "Sum$(recoJet_bTag)") ]

from TTXPheno.Tools.CutInterpreter import CutInterpreter
cutInterpreter = CutInterpreter( continous_variables, discrete_variables, special_cuts)

#print cutInterpreter.cutString("lepSel3-onZ-njet3p-nbjet1p-Zpt0")

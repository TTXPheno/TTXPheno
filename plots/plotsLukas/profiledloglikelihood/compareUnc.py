import os
from plot_helpers import *

TTXCardFile = 'TTXPhenoCardFile_ctZ.txt'
#TTXCardFile = 'TTXPhenoCardFile_cpt.txt'
TopCardFile = 'TopEFTCardFile.txt'
scaleFactor = 0.109392261

#uncertainties = ['trigger_2016','scale','scale_sig','PDF','PartonShower','nonprompt','WZ_xsec', 'ttX']
uncertainties = ['JES', 'btagging', 'mistagging', 'muonId', 'electronId']
processes = ['signal', 'WZ_lep', 'tWZ_LO', 'tZq_LO', 'ttgamma_bg', 'nonPrompt']

ttXPheno = []
for binNr in range(12):
    for proc in processes:
        for unc in uncertainties:
            ttXPheno.append( ('Bin%i'%binNr, unc, proc, getUncertaintyValue( TTXCardFile, binNr, proc, unc ) ) )



topEFT = []
for binNr in range(12):
    for proc in processes:

        if proc == 'tZq_LO' or proc == 'ttgamma_bg' or proc == 'tWZ_LO': procTop = 'TTX'
        elif proc == 'WZ_lep': procTop = 'WZ'
        elif proc == 'nonPrompt': procTop = 'nonPromptDD'
        else: procTop = proc

        for unc in uncertainties:
            if unc == 'JES': uncTop = 'JEC_2016'
            elif unc == 'btagging': uncTop = 'btag_heavy_2016'
            elif unc == 'mistagging': uncTop = 'btag_light_2016'
            elif unc == 'muonId': uncTop = 'leptonSF'
            elif unc == 'electronId': uncTop = 'leptonSF'

            topEFT.append( ('Bin%i'%binNr, unc, proc, getUncertaintyValue( TopCardFile, binNr, procTop, uncTop ) ) )


for i, top in enumerate(topEFT):
#    if (top[3] == 1. or top[3] == '-') and :

        topVal = (top[3]-1)*scaleFactor+1
        if ttXPheno[i][3] < 1:
            ttXVal = 1./(ttXPheno[i][3])        
        else:
            ttXVal = ttXPheno[i][3]
        if not topVal<=ttXVal:
            print top, 'scaled unc:', topVal
            print ttXPheno[i]
            print

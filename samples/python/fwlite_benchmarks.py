''' Benchmark samples for TTXPheno (EDM)'''

# standard imports
import os

# RootTools
from RootTools.core.standard import *

# TTXPheno
from TTXPheno.Tools.user import results_directory 

# sqlite3 sample cache file
dbFile = os.path.join( results_directory, 'sample_cache', 'fwlite_benchmarks.db')

# Logging
if __name__ == "__main__":
    import TTXPheno.Tools.logger as logger
    logger = logger.get_logger('DEBUG')
    import RootTools.core.logger as logger_rt
    logger_rt = logger_rt.get_logger('DEBUG')

# TTZ 931 gen with weights - high stats!
fwlite_ttZ_ll_LO_highStat_scan     = FWLiteSample.fromDAS("fwlite_ttZ_ll_LO_highStat_scan", "/ttZ0j_rwgt_patch_625_highStat_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/schoef-dim6top_07April18-37d73f7f997f18e72dbfd34806877f87/USER", "phys03", dbFile = dbFile)
fwlite_ttZ_ll_LO_highStat_scan.reweight_pkl = "/afs/hephy.at/data/rschoefbeck02/TopEFT/results/gridpacks/ttZ0j_rwgt_patch_625_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"

# TTZ 931 gen with weights - current plane high stats!
fwlite_ttZ_ll_LO_currentplane_highStat_scan     = FWLiteSample.fromDAS("fwlite_ttZ_ll_LO_currentplane_highStat_scan", "/ttZ0j_rwgt_patch_currentplane_highStat_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/schoef-dim6top_07April18-b9d79c4e9bec84f06f452ff39977163a/USER", "phys03", dbFile = dbFile)
fwlite_ttZ_ll_LO_currentplane_highStat_scan.reweight_pkl = "/afs/hephy.at/data/rschoefbeck02/TopEFT/results/gridpacks/ttZ0j_rwgt_patch_currentplane_highStat_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"

# test for Lukas
test = FWLiteSample.fromFiles("test", files = ["/afs/hephy.at/work/r/rschoefbeck/CMS/gen/CMSSW_9_3_1/src/TopEFT/Generation/production/GEN_LO_0j.root"])
test.reweight_pkl = '/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/07052018/ttZ/order3/ttZ0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl'
test.nEvents = 10
test.xsec = 200


# no reference point samples 8/3
fwlite_ttZ_ll_LO_order3_8weights               = FWLiteSample.fromDAS("fwlite_ttZ_ll_LO_order3_8weights", "/ttZ0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-ttZ0j_order3_8weights-7a5fde3f5bf89006ee3acec926ca87d8/USER", "phys03", dbFile = dbFile)
fwlite_ttZ_ll_LO_order3_8weights.reweight_pkl  = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/07052018/ttZ/order3/ttZ0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_ttZ_ll_LO_order3_8weights.nEvents       = 995000
fwlite_ttZ_ll_LO_order3_8weights.xsec          = 0.0915 #pb ttZ, Z->ll

fwlite_ttW_LO_order3_8weights                  = FWLiteSample.fromDAS("fwlite_ttW_LO_order3_8weights", "/ttW0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-ttW0j_order3_8weights-593ea75549b4c51667dffc93040bbda1/USER", "phys03", dbFile = dbFile)
fwlite_ttW_LO_order3_8weights.reweight_pkl     = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/07052018/ttW/order3/ttW0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_ttW_LO_order3_8weights.nEvents          = 1000000
fwlite_ttW_LO_order3_8weights.xsec             = 0.2043 #pb ttW, W->lnu

fwlite_ttgamma_LO_order3_8weights              = FWLiteSample.fromDAS("fwlite_ttgamma_LO_order3_8weights", "/ttgamma0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-ttgamma0j_order3_8weights-10fcfa1a1c01204983ea66975abf2caf/USER", "phys03", dbFile = dbFile)
fwlite_ttgamma_LO_order3_8weights.reweight_pkl = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/07052018/ttgamma/order3/ttgamma0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_ttgamma_LO_order3_8weights.nEvents      = 1000000
fwlite_ttgamma_LO_order3_8weights.xsec         = 3.697 #pb ttgamma


# no reference point samples 15/2
fwlite_ttZ_ll_LO_order2_15weights               = FWLiteSample.fromDAS("fwlite_ttZ_ll_LO_order2_15weights", "/ttZ0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-ttZ0j_order2_15weights_18052018-7a5fde3f5bf89006ee3acec926ca87d8/USER", "phys03", dbFile = dbFile)
fwlite_ttZ_ll_LO_order2_15weights.reweight_pkl  = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/18052018/ttZ/order2/ttZ0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_ttZ_ll_LO_order2_15weights.nEvents	= 975000
fwlite_ttZ_ll_LO_order2_15weights.xsec          = 0.0915 #pb ttZ, Z->ll

fwlite_ttW_LO_order2_15weights                  = FWLiteSample.fromDAS("fwlite_ttW_LO_order2_15weights", "/ttW0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-ttW0j_order2_15weights_18052018-593ea75549b4c51667dffc93040bbda1/USER", "phys03", dbFile = dbFile)
fwlite_ttW_LO_order2_15weights.reweight_pkl     = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/18052018/ttW/order2/ttW0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_ttW_LO_order2_15weights.nEvents          = 1000000
fwlite_ttW_LO_order2_15weights.xsec             = 0.2043 #pb ttW, W->lnu

fwlite_ttgamma_LO_order2_15weights              = FWLiteSample.fromDAS("fwlite_ttgamma_LO_order2_15weights", "/ttgamma0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-ttgamma0j_order2_15weights_18052018-10fcfa1a1c01204983ea66975abf2caf/USER", "phys03", dbFile = dbFile)
fwlite_ttgamma_LO_order2_15weights.reweight_pkl = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/18052018/ttgamma/order2/ttgamma0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_ttgamma_LO_order2_15weights.nEvents	= 990000
fwlite_ttgamma_LO_order2_15weights.xsec         = 3.697 #pb ttgamma


# reference point samples 15/2
fwlite_ttZ_ll_LO_order2_15weights_ref               = FWLiteSample.fromDAS("fwlite_ttZ_ll_LO_order2_15weights_ref", "/ttZ0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-ttZ0j_order2_15weights_18052018_ref-7a5fde3f5bf89006ee3acec926ca87d8/USER", "phys03", dbFile = dbFile)
fwlite_ttZ_ll_LO_order2_15weights_ref.reweight_pkl  = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/18052018_ref/ttZ/order2/ttZ0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_ttZ_ll_LO_order2_15weights_ref.nEvents       = 990000
fwlite_ttZ_ll_LO_order2_15weights_ref.xsec          = 0.8815 #pb ttZ, Z->ll, xsec_SM_NNLO * xsec_BSM_LO / xsec_SM_LO

fwlite_ttW_LO_order2_15weights_ref                  = FWLiteSample.fromDAS("fwlite_ttW_LO_order2_15weights_ref", "/ttW0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-ttW0j_order2_15weights_18052018_ref-593ea75549b4c51667dffc93040bbda1/USER", "phys03", dbFile = dbFile)
fwlite_ttW_LO_order2_15weights_ref.reweight_pkl     = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/18052018_ref/ttW/order2/ttW0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_ttW_LO_order2_15weights_ref.nEvents          = 945000
fwlite_ttW_LO_order2_15weights_ref.xsec             = 0.6327 #pb ttW, W->lnu, xsec_SM_NNLO * xsec_BSM_LO / xsec_SM_LO

fwlite_ttgamma_LO_order2_15weights_ref              = FWLiteSample.fromDAS("fwlite_ttgamma_LO_order2_15weights_ref", "/ttgamma0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-ttgamma0j_order2_15weights_18052018_ref-10fcfa1a1c01204983ea66975abf2caf/USER", "phys03", dbFile = dbFile)
fwlite_ttgamma_LO_order2_15weights_ref.reweight_pkl = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/18052018_ref/ttgamma/order2/ttgamma0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_ttgamma_LO_order2_15weights_ref.nEvents      = 970000
fwlite_ttgamma_LO_order2_15weights_ref.xsec         = 11.8807 #pb ttgamma, xsec_SM_NNLO * xsec_BSM_LO / xsec_SM_LO

# background samples no WC no ref point
#leptonic decays W > lnu, Z > ll, t > Wb
fwlite_tt_lep_LO_order2_15weights                  = FWLiteSample.fromDAS("fwlite_tt_lep_LO_order2_15weights", "/tt_lep_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-bg_lep_dim6top_06July18-399ed716eb7225402bb4416ff36fe4d6/USER", "phys03", dbFile = dbFile)
fwlite_tt_lep_LO_order2_15weights.reweight_pkl     = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/06072018/tt/order2/tt_lep_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_tt_lep_LO_order2_15weights.nEvents          = 1000000 #? not checked!
fwlite_tt_lep_LO_order2_15weights.xsec             = 831.76*((3*0.108)**2) #pb TTLep_pow, tt, both W->lnu, xsec_SM_NNLO

fwlite_tt_semilep_LO_order2_15weights                  = FWLiteSample.fromDAS("fwlite_tt_semilep_LO_order2_15weights", "/tt_semilep_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-bg_dim6top_06July18-61f6d1f3cc6e0e3d29066ed21db166d3/USER", "phys03", dbFile = dbFile)
fwlite_tt_semilep_LO_order2_15weights.reweight_pkl     = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/06072018/tt_semilep/order2/tt_semilep_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_tt_semilep_LO_order2_15weights.nEvents          = 1000000 #? not checked!
fwlite_tt_semilep_LO_order2_15weights.xsec             = 2*831.76*(3*0.108)#*(1-3*0.108) #pb TTSemiLep_pow, tt, one W->lnu, xsec_SM_NNLO

fwlite_WZ_lep_LO_order2_15weights                  = FWLiteSample.fromDAS("fwlite_WZ_lep_LO_order2_15weights", "/WZ_lep_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-bg_dim6top_06July18-6dade6042d6868e7bb87de85663e8a54/USER", "phys03", dbFile = dbFile)
fwlite_WZ_lep_LO_order2_15weights.reweight_pkl     = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/06072018/WZ/order2/WZ_lep_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_WZ_lep_LO_order2_15weights.nEvents          = 1000000 #? not checked!
fwlite_WZ_lep_LO_order2_15weights.xsec             = 4.666 #pb WZTo3LNu_amcatnlo, WZ, W->lnu, Z->ll, xsec_SM_NNLO

fwlite_tZq_LO_order2_15weights                  = FWLiteSample.fromDAS("fwlite_tZq_LO_order2_15weights", "/tZq_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-bg_lep_dim6top_06July18-622c407898c13833e0c43092e83c38c5/USER", "phys03", dbFile = dbFile)
fwlite_tZq_LO_order2_15weights.reweight_pkl     = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/06072018/tZq/order2/tZq_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_tZq_LO_order2_15weights.nEvents          = 1000000 #? not checked!
fwlite_tZq_LO_order2_15weights.xsec             = 0.09418 #pb tZq_ll_ext

fwlite_tW_LO_order2_15weights                  = FWLiteSample.fromDAS("fwlite_tW_LO_order2_15weights", "/tW_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-bg_dim6top_06July18-c93c9d5de5b5d5ea926359481176f094/USER", "phys03", dbFile = dbFile)
fwlite_tW_LO_order2_15weights.reweight_pkl     = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/06072018/tW/order2/tW_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_tW_LO_order2_15weights.nEvents          = 1000000 #? not checked!
fwlite_tW_LO_order2_15weights.xsec             = 35.6*(3*0.108) #pb T_tWch_ext*BR(W->lnu)

fwlite_tWZ_LO_order2_15weights                  = FWLiteSample.fromDAS("fwlite_tWZ_LO_order2_15weights", "/tWZ_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-bg_dim6top_06July18-083eb65e1bdfcfc8fcf3d4f572bc27da/USER", "phys03", dbFile = dbFile)
fwlite_tWZ_LO_order2_15weights.reweight_pkl     = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/06072018/tWZ/order2/tWZ_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_tWZ_LO_order2_15weights.nEvents          = 1000000 #? not checked!
fwlite_tWZ_LO_order2_15weights.xsec             = 0.01123 #pb tWll

fwlite_Zgamma_LO_order2_15weights                  = FWLiteSample.fromDAS("fwlite_Zgamma_LO_order2_15weights", "/Zgamma_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-bg_dim6top_06July18-d4a3491b99ce351d59c2f3c59adf0bd3/USER", "phys03", dbFile = dbFile)
fwlite_Zgamma_LO_order2_15weights.reweight_pkl     = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/06072018/Zgamma/order2/Zgamma_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_Zgamma_LO_order2_15weights.nEvents          = 1000000 #? not checked!
fwlite_Zgamma_LO_order2_15weights.xsec             = 131.3 #pb ZGTo2LG_ext

fwlite_ttgamma_bg_LO_order2_15weights                  = FWLiteSample.fromDAS("fwlite_ttgamma_bg_LO_order2_15weights", "/ttgamma_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-bg_lep_dim6top_06July18-7c92494a0b9e35a525af35a2e83e005b/USER", "phys03", dbFile = dbFile)
fwlite_ttgamma_bg_LO_order2_15weights.reweight_pkl     = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/06072018/ttgamma/order2/ttgamma_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_ttgamma_bg_LO_order2_15weights.nEvents          = 1000000 #? not checked!
fwlite_ttgamma_bg_LO_order2_15weights.xsec             = 3.697 #pb TTGJets_ext

# background samples 0/2 (WZ) or 15/2 (ttbar with reference point)
#leptonic decays W > lnu, Z > ll, t > Wb
fwlite_tt_lep_LO_order2_15weights_ref              = FWLiteSample.fromDAS("fwlite_tt_lep_LO_order2_15weights_ref", "/tt_lep_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-bg_lep_dim6top_05June18-399ed716eb7225402bb4416ff36fe4d6/USER", "phys03", dbFile = dbFile)
fwlite_tt_lep_LO_order2_15weights_ref.reweight_pkl = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/05062018_ref/tt/order2/tt_lep_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_tt_lep_LO_order2_15weights_ref.nEvents      = 1000000 #? not checked!
fwlite_tt_lep_LO_order2_15weights_ref.xsec         = 87.3148 * 735.1 / 46.57 #pb tt, W->lnu, xsec_SM_NNLO * xsec_BSM_LO / xsec_SM_LO

#hadronic and leptonic decays
fwlite_tt_LO_order2_15weights_ref              = FWLiteSample.fromDAS("fwlite_tt_LO_order2_15weights_ref", "/tt_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-bg_dim6top_04June18-db4155f01c4c21dc10125760597b536e/USER", "phys03", dbFile = dbFile)
fwlite_tt_LO_order2_15weights_ref.reweight_pkl = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/04062018/tt/order2/tt_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_tt_LO_order2_15weights_ref.nEvents      = 1000000 #? not checked!
fwlite_tt_LO_order2_15weights_ref.xsec         = 831.76 * 735.1 / 46.57 #pb tt, xsec_SM_NNLO * xsec_BSM_LO / xsec_SM_LO

fwlite_WZ_LO_order2_15weights                  = FWLiteSample.fromDAS("fwlite_WZ_LO_order2_15weights", "/WZ_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball/llechner-bg_dim6top_04June18-a4eb1cf113188459e4c517c4aa52c31c/USER", "phys03", dbFile = dbFile)
fwlite_WZ_LO_order2_15weights.reweight_pkl     = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/04062018/WZ/order2/WZ_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl"
fwlite_WZ_LO_order2_15weights.nEvents          = 1000000 #? not checked!
fwlite_WZ_LO_order2_15weights.xsec             = 47.13 #pb WZ, xsec_SM_NNLO

TTGJets_Summer16                                = FWLiteSample.fromDAS("TTGJets_Summer16", "/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", dbFile = dbFile)


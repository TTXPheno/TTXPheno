#!/bin/sh

#use cardfile delphes_card_ATLAS or delphes_card_CMS

#######
##CMS##
#######


# ttZ Signal samples with reference point
#python genPostProcessing.py --overwrite target --targetDir v23 --logLevel DEBUG --sample fwlite_ttZ_ll_LO_order2_15weights_ref --addReweights --interpolationOrder 2  --delphes --delphesCard CMS_PhaseII/CMS_PhaseII_200PU_v03 #SPLIT200

### ttZ background samples without reference point
#python genPostProcessing.py --overwrite target --targetDir v23 --logLevel DEBUG --sample fwlite_WZ_lep_LO_order2_15weights --interpolationOrder 2  --delphes --delphesCard CMS_PhaseII/CMS_PhaseII_200PU_v03 #SPLIT200
#python genPostProcessing.py --overwrite target --targetDir v23 --logLevel DEBUG --sample fwlite_tZq_LO_order2_15weights --interpolationOrder 2  --delphes --delphesCard CMS_PhaseII/CMS_PhaseII_200PU_v03 #SPLIT200
#python genPostProcessing.py --overwrite target --targetDir v23 --logLevel DEBUG --sample fwlite_tWZ_LO_order2_15weights --interpolationOrder 2  --delphes --delphesCard CMS_PhaseII/CMS_PhaseII_200PU_v03 #SPLIT200
#python genPostProcessing.py --overwrite target --targetDir v23 --logLevel DEBUG --sample fwlite_ttgamma_bg_LO_order2_15weights --interpolationOrder 2  --delphes --delphesCard CMS_PhaseII/CMS_PhaseII_200PU_v03 #SPLIT200



# ttgamma Signal samples with reference point
#python genPostProcessing.py --overwrite target --targetDir v18 --removeDelphesFiles --logLevel DEBUG --sample fwlite_ttgamma_LO_order2_15weights_ref --addReweights --interpolationOrder 2  --delphesCard delphes_card_CMS #SPLIT200
# large sample
#python genPostProcessing.py --overwrite target --targetDir v18 --logLevel DEBUG --sample fwlite_ttgammaLarge_LO_order2_15weights_ref --addReweights --interpolationOrder 2  --delphes --delphesCard CMS_PhaseII/CMS_PhaseII_200PU_v03 #SPLIT2000

# ttgamma background samples without reference point
#python genPostProcessing.py --overwrite target --targetDir v18 --logLevel DEBUG --sample fwlite_Zgamma_LO_order2_15weights --interpolationOrder 2  --delphes --delphesCard CMS_PhaseII/CMS_PhaseII_200PU_v03 #SPLIT200
#python genPostProcessing.py --overwrite target --targetDir v20 --logLevel DEBUG --sample fwlite_tt_dilep_LO_order2_15weights --interpolationOrder 2  --delphes --delphesCard CMS_PhaseII/CMS_PhaseII_200PU_v03 #SPLIT200
#python genPostProcessing.py --overwrite target --targetDir v20 --logLevel DEBUG --sample fwlite_tt_nonhad_LO_order2_15weights --interpolationOrder 2  --delphes --delphesCard CMS_PhaseII/CMS_PhaseII_200PU_v03 #SPLIT200
#python genPostProcessing.py --overwrite target --targetDir v20 --logLevel DEBUG --sample fwlite_tW_LO_order2_15weights --interpolationOrder 2  --delphes --delphesCard CMS_PhaseII/CMS_PhaseII_200PU_v03 #SPLIT200
# large sample
#python genPostProcessing.py --overwrite target --targetDir v18 --logLevel DEBUG --sample fwlite_tt_full_LO_order2_15weights --interpolationOrder 2  --delphes --delphesCard CMS_PhaseII/CMS_PhaseII_200PU_v03 #SPLIT2000

#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_tt_full_LO_order2_15weights #SPLIT200
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_WZ_lep_LO_order2_15weights #SPLIT200
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_tZq_LO_order2_15weights #SPLIT200
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_tW_LO_order2_15weights #SPLIT200
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_tWZ_LO_order2_15weights #SPLIT200
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_Zgamma_LO_order2_15weights #SPLIT200
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_ttZ_ll_LO_order3_8weights #SPLIT200
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_WJetsToLNu_order2_15weights #SPLIT200
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --addReweights --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_ttZ_ll_LO_order2_15weights_ref_ext #SPLIT1999
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --addReweights --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_ttZ_ll_LO_order2_15weights_ref #SPLIT200
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_ttW_LO_order3_8weights #SPLIT200
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_ttgamma_bg_LO_order2_15weights #SPLIT200

#python genPostProcessing.py --overwrite target --targetDir RunII_v02 --logLevel DEBUG --sample  hepmc_1event --HEPMC PP --delphes --delphesCard CMS_PhaseII/CMS_PhaseII_200PU_v03 

#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --sample  ttbarZ --HEPMC PP       --delphes --delphesEra RunII #SPLIT100
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --sample  ttbarZ --HEPMC 10d0_HH  --delphes --delphesEra RunII #SPLIT50
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --sample  ttbarZ --HEPMC 10d0_GH  --delphes --delphesEra RunII #SPLIT50
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --sample  ttbarZ --HEPMC 10d0_HG  --delphes --delphesEra RunII #SPLIT50
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --sample  ttbarZ --HEPMC 1d0_GH   --delphes --delphesEra RunII #SPLIT50
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --sample  ttbarZ --HEPMC 1d0_HG   --delphes --delphesEra RunII #SPLIT50
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --sample  ttbarZ --HEPMC 1d0_HH   --delphes --delphesEra RunII #SPLIT50
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --sample  ttbarZ --HEPMC 0d1_HG   --delphes --delphesEra RunII #SPLIT50
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --sample  ttbarZ --HEPMC 0d1_GH   --delphes --delphesEra RunII #SPLIT50
#python genPostProcessing.py --targetDir RunII_v02 --logLevel DEBUG --sample  ttbarZ --HEPMC 0d1_HH   --delphes --delphesEra RunII #SPLIT50

python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC PP #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-0.01_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-0.1_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-1_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-10_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-30_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-35_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-37_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-40_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-42_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-43_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-44_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-45_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-50_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-75_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-100_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-0.01_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-0.1_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-1_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-10_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-30_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-35_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-37_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-40_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-42_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-43_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-44_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-45_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-50_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-75_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-100_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-0.01_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-0.1_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-1_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-10_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-30_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-35_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-37_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-40_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-42_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-43_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-44_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-45_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-50_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-75_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbar --delphes --delphesEra RunII --HEPMC pdf-100_HH #SPLIT5

python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC PP #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-0.01_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-0.1_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-1_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-10_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-30_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-35_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-37_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-40_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-42_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-43_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-44_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-45_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-50_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-75_HG #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-100_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-0.01_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-0.1_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-1_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-10_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-30_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-35_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-37_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-40_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-42_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-43_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-44_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-45_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-50_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-75_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-100_GH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-0.01_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-0.1_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-1_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-10_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-30_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-35_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-37_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-40_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-42_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-43_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-44_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-45_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-50_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-75_HH #SPLIT5
python genPostProcessing.py --targetDir RunII_v02/22_05 --logLevel DEBUG --sample  ttbarZ --delphes --delphesEra RunII --HEPMC pdf-100_HH #SPLIT5


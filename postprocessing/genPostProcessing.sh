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

#python genPostProcessing.py --targetDir RunII_v01 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_tt_full_LO_order2_15weights #SPLIT200
#python genPostProcessing.py --targetDir RunII_v01 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_WZ_lep_LO_order2_15weights #SPLIT200
#python genPostProcessing.py --targetDir RunII_v01 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_tZq_LO_order2_15weights #SPLIT200
#python genPostProcessing.py --targetDir RunII_v01 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_tW_LO_order2_15weights #SPLIT200
#python genPostProcessing.py --targetDir RunII_v01 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_tWZ_LO_order2_15weights #SPLIT200
#python genPostProcessing.py --targetDir RunII_v01 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_Zgamma_LO_order2_15weights #SPLIT200
#python genPostProcessing.py --targetDir RunII_v01 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_ttZ_ll_LO_order3_8weights #SPLIT200
#python genPostProcessing.py --targetDir RunII_v01 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_WJetsToLNu_order2_15weights #SPLIT200
#python genPostProcessing.py --targetDir RunII_v01 --logLevel DEBUG --addReweights --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_ttZ_ll_LO_order2_15weights_ref_ext #SPLIT1999
#python genPostProcessing.py --targetDir RunII_v01 --logLevel DEBUG --addReweights --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_ttZ_ll_LO_order2_15weights_ref #SPLIT200
#python genPostProcessing.py --targetDir RunII_v01 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_ttW_LO_order3_8weights #SPLIT200
#python genPostProcessing.py --targetDir RunII_v01 --logLevel DEBUG --interpolationOrder 2  --delphes --delphesEra RunII --sample fwlite_ttgamma_bg_LO_order2_15weights #SPLIT200

#python genPostProcessing.py --overwrite target --targetDir RunII_v01 --logLevel DEBUG --sample  hepmc_1event --HEPMC PP --delphes --delphesCard CMS_PhaseII/CMS_PhaseII_200PU_v03 

#python genPostProcessing.py --overwrite all --targetDir RunII_v01 --logLevel DEBUG --sample  ttbarZ --HEPMC PP       --delphes --delphesEra RunII #SPLIT100
#python genPostProcessing.py --overwrite all --targetDir RunII_v01 --logLevel DEBUG --sample  ttbarZ --HEPMC 10d0_HH  --delphes --delphesEra RunII #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01 --logLevel DEBUG --sample  ttbarZ --HEPMC 10d0_GH  --delphes --delphesEra RunII #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01 --logLevel DEBUG --sample  ttbarZ --HEPMC 10d0_HG  --delphes --delphesEra RunII #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01 --logLevel DEBUG --sample  ttbarZ --HEPMC 1d0_GH   --delphes --delphesEra RunII #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01 --logLevel DEBUG --sample  ttbarZ --HEPMC 1d0_HG   --delphes --delphesEra RunII #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01 --logLevel DEBUG --sample  ttbarZ --HEPMC 1d0_HH   --delphes --delphesEra RunII #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01 --logLevel DEBUG --sample  ttbarZ --HEPMC 0d1_HG   --delphes --delphesEra RunII #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01 --logLevel DEBUG --sample  ttbarZ --HEPMC 0d1_GH   --delphes --delphesEra RunII #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01 --logLevel DEBUG --sample  ttbarZ --HEPMC 0d1_HH   --delphes --delphesEra RunII #SPLIT50

#python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_woMT --delphes --delphesEra RunII --HEPMC PP #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_woMT --delphes --delphesEra RunII --HEPMC 0d1_HG #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_woMT --delphes --delphesEra RunII --HEPMC 0d1_GH #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_woMT --delphes --delphesEra RunII --HEPMC 0d1_HH #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_woMT --delphes --delphesEra RunII --HEPMC 100d0_GH #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_woMT --delphes --delphesEra RunII --HEPMC 100d0_HG #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_woMT --delphes --delphesEra RunII --HEPMC 100d0_HH #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_woMT --delphes --delphesEra RunII --HEPMC 10d0_HG #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_woMT --delphes --delphesEra RunII --HEPMC 10d0_GH #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_woMT --delphes --delphesEra RunII --HEPMC 10d0_HH #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_woMT --delphes --delphesEra RunII --HEPMC 0d01_HH #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_woMT --delphes --delphesEra RunII --HEPMC 0d01_HG #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_woMT --delphes --delphesEra RunII --HEPMC 0d01_GH #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_woMT --delphes --delphesEra RunII --HEPMC 1d0_HH #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_woMT --delphes --delphesEra RunII --HEPMC 1d0_HG #SPLIT50
#python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_woMT --delphes --delphesEra RunII --HEPMC 1d0_GH #SPLIT50

python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_wMT --delphes --delphesEra RunII --HEPMC PP #SPLIT50
python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_wMT --delphes --delphesEra RunII --HEPMC 0d1_HG #SPLIT50
python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_wMT --delphes --delphesEra RunII --HEPMC 0d1_GH #SPLIT50
python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_wMT --delphes --delphesEra RunII --HEPMC 0d1_HH #SPLIT50
python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_wMT --delphes --delphesEra RunII --HEPMC 100d0_GH #SPLIT50
python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_wMT --delphes --delphesEra RunII --HEPMC 100d0_HG #SPLIT50
python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_wMT --delphes --delphesEra RunII --HEPMC 100d0_HH #SPLIT50
python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_wMT --delphes --delphesEra RunII --HEPMC 10d0_HG #SPLIT50
python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_wMT --delphes --delphesEra RunII --HEPMC 10d0_GH #SPLIT50
python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_wMT --delphes --delphesEra RunII --HEPMC 10d0_HH #SPLIT50
python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_wMT --delphes --delphesEra RunII --HEPMC 0d01_HH #SPLIT50
python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_wMT --delphes --delphesEra RunII --HEPMC 0d01_HG #SPLIT50
python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_wMT --delphes --delphesEra RunII --HEPMC 0d01_GH #SPLIT50
python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_wMT --delphes --delphesEra RunII --HEPMC 1d0_HH #SPLIT50
python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_wMT --delphes --delphesEra RunII --HEPMC 1d0_HG #SPLIT50
python genPostProcessing.py --overwrite all --targetDir RunII_v01/19_04 --logLevel DEBUG --sample  ttbarZ_fr_C6_wMT --delphes --delphesEra RunII --HEPMC 1d0_GH #SPLIT50

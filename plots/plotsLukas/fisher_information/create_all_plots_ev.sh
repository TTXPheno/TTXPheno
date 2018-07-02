#!/bin/sh

#####################################################################################

# create bin and cut plots with plotting variables given in process_variables_ROC.py
# script loops over all indices in the range of [startIndex, endIndex]
# indices which are not specified are skipped in the python script

#small="--small"
small=""

declare -a variables=("cpt" "cpQM" "ctZ" "ctW" "cpt cpQM" "ctZ ctZI ctW ctWI" "cpt cpQM ctZ ctZI" "cpt cpQM ctW ctWI" "ctZ ctW" "ctZ ctZI" "ctW ctWI" "cpt cpQM ctZ ctW")
#declare -a variables=("cpt cpQM ctZ ctW")

declare -a levels=("reco" "gen")
#declare -a levels=("reco" "genLep" "gen")
#declare -a levels=("gen")
version="v7"

#####################################################################################

for variable in "${variables[@]}"
do

    for level in "${levels[@]}"
    do

    submitBatch.py --dpm "python fisher_information_EVec_full.py ${small} --level ${level} --version ${version} --sample fwlite_ttZ_ll_LO_order2_15weights_ref  --process ttZ     --order 2 --selection lepSel3-onZ-njet3p-nbjet1p-Zpt0 --variables ${variable}"
    submitBatch.py --dpm "python fisher_information_EVec_full.py ${small} --level ${level} --version ${version} --sample fwlite_ttW_LO_order2_15weights_ref     --process ttW     --order 2 --selection nlep2p-njet2p-nbjet1p-Wpt0      --variables ${variable}"
    submitBatch.py --dpm "python fisher_information_EVec_full.py ${small} --level ${level} --version ${version} --sample fwlite_ttgamma_LO_order2_15weights_ref --process ttgamma --order 2 --selection gammapt40-nlep1p-njet3p-nbjet1p --variables ${variable}"

    done
done

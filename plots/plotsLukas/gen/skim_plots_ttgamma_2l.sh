#!/bin/bash

##############################################

#parameters
cpQM=10
cpt=10
ctW=5
ctWI=5
ctZ=10
ctZI=10
ctG=1
ctGI=1

# declare samples to analyze
declare -a samples2=('') #fwlite_ttgamma_ll_LO_order2_15weights')
declare -a samples3=('fwlite_ttgamma_LO_order3_8weights')

# declare selection strings to analyze
declare -a selections=('gammapt40-nlep2p-njet2p-nbjet1p' 'gammapt40to100-nlep2p-njet2p-nbjet1p' 'gammapt100to200-nlep2p-njet2p-nbjet1p' 'gammapt200to300-nlep2p-njet2p-nbjet1p' 'gammapt300-nlep2p-njet2p-nbjet1p')

# declare sample size to analyze
declare -a samplesizes=('--small' '')
#declare -a samplesizes=('--small')
#declare -a samplesizes=('')

# define program to run by python
prog=skim_plots_ttgamma_2l.py

#################################################

# 2nd order samples
order=2
for sample in "${samples2[@]}"
do

   if [ -z $sample ]; then
      continue
   fi

   for samplesize in "${samplesizes[@]}"
   do
      for selection in "${selections[@]}"
      do

         if [ -z $selection ]; then
            continue
         fi

         python ${prog} ${samplesize}             --sample ${sample} --order ${order} --selection ${selection} --parameters cpQM ${cpQM} cpt ${cpt} ctW ${ctW} ctWI ${ctWI} ctZ ${ctZ} ctZI ${ctZI} ctG ${ctG} ctGI ${ctGI}
         python ${prog} ${samplesize} --scaleLumi --sample ${sample} --order ${order} --selection ${selection} --parameters cpQM ${cpQM} cpt ${cpt} ctW ${ctW} ctWI ${ctWI} ctZ ${ctZ} ctZI ${ctZI} ctG ${ctG} ctGI ${ctGI}

      done
   done
done

# 3rd order samples
order=3
for sample in "${samples3[@]}"
do

   if [ -z $sample ]; then
      continue
   fi

   for samplesize in "${samplesizes[@]}"
   do
      for selection in "${selections[@]}"
      do

         if [ -z $selection ]; then
            continue
         fi

         python ${prog} ${samplesize}             --sample ${sample} --order ${order} --selection ${selection} --parameters cpQM ${cpQM} cpt ${cpt} ctW ${ctW} ctWI ${ctWI} ctZ ${ctZ} ctZI ${ctZI} ctG ${ctG} ctGI ${ctGI}
         python ${prog} ${samplesize} --scaleLumi --sample ${sample} --order ${order} --selection ${selection} --parameters cpQM ${cpQM} cpt ${cpt} ctW ${ctW} ctWI ${ctWI} ctZ ${ctZ} ctZI ${ctZI} ctG ${ctG} ctGI ${ctGI}

      done
   done
done
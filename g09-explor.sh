#!/bin/bash

for filename in ${@};
do
   nf="${filename%.*}"
   echo ${nf}

   ##input file
   G09GJF=${nf}.gjf
   ##output file
   G09LOG=${nf}.log
   ##check File
   G09CHK=${nf}.chk

   curdir=$PWD
   tmpdir=$SCRATCHDIR/${nf}

   cat > ${nf}.sh << END
#!/bin/bash
#SBATCH -p hf
#SBATCH -N 1
#SBATCH -n 8
#SBATCH -J "${nf}"
#SBATCH -t 15-00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ciceke@itu.edu.tr

## Unload all modules
module purge
## Loads module 
module load g09/D01

hostname

## temporary directory 
mkdir -p ${tmpdir}
cd ${tmpdir}

## Run the program 
g09 < $curdir/${G09GJF} > $curdir/${G09LOG}

if [ -e $G09CHK ]; then
  mv $G09CHK $curdir/
fi

END

sbatch ${nf}.sh
rm ${nf}.sh
done


#!/bin/bash


#USER VARIABLES----just change these vars---------

JOB_NAME="g16jobs"
PROJECT_TITLE="sadtma"
QUEUE_NAME="core40q"
N_NODE=1
N_CORE=40

#--------------------------------

req_core=0
max_core=$((N_NODE*N_CORE))

control_request_node(){
for file in ${@}; 
   do 
      file_core=$(awk '/nprocshared=/ {print $1}' FPAT='[0-9]+' ${file})
      req_core=$((req_core+file_core))
   done

if [[ ${req_core} -gt ${max_core} ]]
then
   echo "ERROR: number of the requested node: ${req_core}, max node: ${max_core}, check input files"
   exit 1
fi
}

create_sbatch(){

cat > run.sh << END
#!/bin/bash
#SBATCH -J ${JOB_NAME}
#SBATCH -A ${PROJECT_TITLE}
#SBATCH -p ${QUEUE_NAME}
#SBATCH -N ${N_NODE}
#SBATCH -n ${N_CORE}

PIDler=""

source /okyanus/progs/gaussian/g16/bsd/g16.sariyer.profile

END

for file in ${@}; 
   do 
cat >> run.sh << END
echo ${file}
(      
g16 ${file}
 ) &            
END
echo 'PIDler="$PIDler $!"' >> run.sh
echo '' >> run.sh
   done

echo '' >> run.sh
echo 'wait $PIDler' >> run.sh
}

[ -f run.sh ] && rm run.sh
control_request_node ${@}
create_sbatch ${@}
sbatch run.sh

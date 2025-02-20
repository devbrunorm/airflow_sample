################### HOW TO USE ###################
# NAVIGATE THROUGH THE COMMAND LINE TO THE REPOSITORY FOLDER WHERE THE .sh FILE FOR DEPLOY IS LOCATED
# GIVE EXECUTION PERMISSION TO THE FILE IF YOU DON'T ALREADY HAVE IT: chmod 777 <name_ shellscritp_deploy>.sh
# MODIFY THE VALUE OF THE repo_folder_name VARIABLE WITH THE NAME OF THE REPOSITORY YOU WANT TO DEPLOY IN DEV
# EXECUTE THE FILE FROM THE COMMAND LINE TO PERFORM THE DEPLOY: ./<nome_ shellscritp_deploy>.sh

repo_folder_name='airflow_sample' #INSERT THE NAME OF THE REPOSITORY FOLDER YOU DESIRE TO DEPLOY ON AIRFLOW DEV
echo 'Deploying DAGs from repo '"$repo_folder_name"' on DEV Environment...'

var_user=$(kubectl auth whoami | grep 'pod-name' | cut -d '[' -f2 | cut -d ']' -f1 | cut -d '-' -f1)
echo 'USER:'"$var_user"

rm -rf /home/coder/airflow/dags/"$repo_folder_name"'_'"$var_user"
cp -R ./dags/"$repo_folder_name" '/home/coder/airflow/dags/'"$repo_folder_name"'_'"$var_user"

sudo find '/home/coder/airflow/dags/'"$repo_folder_name"'_'"$var_user" -type f -name 'dag_*' -exec sed -i -e '/dag_id=/ s/.$/ + "_" + "'"$var_user"'",/' -e '/dag_id = / s/.$/ + "_" + "'"$var_user"'",/' -e '/tags=/ s/,$/ + [ "'"$var_user"'"],/' -e '/tags = / s/$/ + [ "'"$var_user"'"],/' {} +
echo 'DAG '"$repo_folder_name"'_'"$var_user"' deployed successfully!'
echo 'Deployment finished!'
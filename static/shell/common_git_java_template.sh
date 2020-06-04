# !bin/bash
source /etc/profile

git_address=$1
arr=(${git_address//// })
git_name=${arr[-1]}
arr=(${git_name//./ })
project_name=${arr[0]}

if [ -d "$project_name" ]
then
rm -rf  $project_name
fi

git clone -b $2 $git_address
cd $project_name
mvn clean package
cp target/$project_name*.jar ../
cd ..

jar_name=$(ls | grep jar | grep $project_name)

nohup java -jar $jar_name > nohup.out &
tail -f /dev/null
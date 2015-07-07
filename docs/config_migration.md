#Migrating into the config.yml




```bash
docker run \
  -ti \
  -v `pwd`/JOB_DIRECTORY:/JOB_DIRECTORY \
  --entrypoint="bash" \
  verigreen/jenkins-tomcat-nginx -c "python xml2jobDSL.py JOB_DIRECTORY" > myjob.groovy
```
#!/bin/bash

function build_path {
	NODE_PATH=$1

	INCREMENTAL_PATH=''

	IFS=$'/'
	for i in $NODE_PATH; do
		if [[ ! -z $i ]] && [[ "$i" != "attributes" ]]; then
			NODE="$i"
			cPATH="${INCREMENTAL_PATH}"
    		INCREMENTAL_PATH="${cPATH}/${NODE}"
    		COUNT=$(xmlstarlet sel -t -v "count(${INCREMENTAL_PATH})" config_copy.xml)
    		echo "INCREMENTAL_PATH: ${INCREMENTAL_PATH}"
    		[[ $COUNT -eq 0 ]] && \
    			echo -e "$(xmlstarlet ed -s "$cPATH" -t elem -n "$NODE" config_copy.xml)" > config_copy.xml
		fi
	done
	unset IFS

	return 0
}


build_path "/hudson/clouds/com.nirima.jenkins.plugins.docker.DockerCloud/templates/com.nirima.jenkins.plugins.docker.DockerTemplate"
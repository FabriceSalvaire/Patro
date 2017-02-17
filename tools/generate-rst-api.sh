api=doc/sphinx/source/api
##old_api=doc/sphinx/old-api

##mkdir -p ${old_api}
#mv --backup=numbered $api ${old_api}

echo
echo Generate RST API files
./tools/generate-rst-api

echo
echo Run Sphinx
pushd doc/sphinx/
./make-html #--clean
popd

##echo
##echo Old api directory moved to
##ls -l -h ${old_api}

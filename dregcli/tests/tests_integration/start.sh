#!/usr/bin/env bash
function upRegistry() {
    # IMPORTANT: REGISTRY_STORAGE_DELETE_ENABLED=true mandatory for delete rights
    docker run -d -p ${port}:5000 -e REGISTRY_STORAGE_DELETE_ENABLED=true --restart=always --name ${containerName} registry:2
}

function downRegistry() {
    docker stop ${containerName}
    docker rm ${containerName}
}

# setImage source targetTag
function setImage() {
    docker pull alpine:$1
    docker tag alpine:$1 localhost:${port}/test-project:$2
    docker push localhost:${port}/test-project:$2
}

function setTestImages() {
    # adhoc with fixtures.py
    setImage 3.5 master-6da64c000cf59c30e4841371e0dac3dd02c31aaa-1385
    setImage 3.6 master-b2a7d05ca36cdd3e8eb092f857580b3ed0f7159a-1386
    setImage 3.7 master-1c48755c0b257ccd106badcb973a36528f833fc0-1387

    # same layer
    setImage 3.8 master-128a1e13dbe96705917020261ee23d097606bda2-1388
    setImage 3.8 latest
}

function setdeleteTestImages() {
    # adhoc with fixtures.py

    # layer with only commit tags
    setImage 3.2 master-2ze98e000wx39d60a7390925d0czr3qs03j90aaa-1382

    # a layer with a release tag between 2 layers with only commit tags
    setImage 3.3 master-2yu50j111dy72e70b9623522e0zdt9wz29h71ddd-1383
    setImage 3.3 alpha

    # layer with only commit tags
    setImage 3.4 master-2bd32d000ez93c50h8486935f0fda5ee09z98bbb-1384

    # layers with release tags
    # old-prod layer
    setImage 3.5 master-6da64c000cf59c30e4841371e0dac3dd02c31aaa-1385
    setImage 3.5 old-prod

    # prod layer
    setImage 3.6 master-b2a7d05ca36cdd3e8eb092f857580b3ed0f7159a-1386
    setImage 3.6 prod

    # old-staging layer
    setImage 3.7 master-1c48755c0b257ccd106badcb973a36528f833fc0-1387
    setImage 3.7 old-staging

    # staging/latest layer
    setImage 3.8 master-128a1e13dbe96705917020261ee23d097606bda2-1388
    setImage 3.8 staging
    setImage 3.9 latest
}

# mainTest 'name' python_script_name.py
function mainTest() {
    echo "________________________________________________________________________________"
    echo ""
    echo "TEST $1"
    echo "________________________________________________________________________________"

    upRegistry
    setTestImages
    ${DREGCLI_VENV}/bin/py.test --pep8 -vv dregcli/tests/tests_integration/$2 --ignore dregcli/tests/tests_integration/tests_delete/
    downRegistry
}

# deleteTest 'name' python_script_name.py
function  deleteTest() {
    echo "________________________________________________________________________________"
    echo ""
    echo "DELETE TEST $1"
    echo "________________________________________________________________________________"

    upRegistry
    setdeleteTestImages
    ${DREGCLI_VENV}/bin/py.test --pep8 -vv dregcli/tests/tests_integration/tests_delete/$2
    downRegistry
}


#
# SCRIPT
#
containerName=dregcli_ci_registry
port=5002

#
# CONSOLE
#
mainTest 'CONSOLE' test_console.py

#
# DREGCLI
#
mainTest 'DREGCLI' test_dregcli.py

#
# single_tagBAGE ALL
#
deleteTest 'ALL' test_delete_all.py
deleteTest 'ALL COTAGS RESULT' test_delete_all_cotags.py
deleteTest 'ALL SINGLE TAG (commit tag)' test_delete_all_single_tag.py

#
# DELETE INCLUDE
#
deleteTest 'INCLUDE' test_delete_include.py
deleteTest 'INCLUDE' test_delete_include_single_tag.py

#
# DELETE EXCLUDE
#
# exclude desactivated: for layers with multiple tags,
# deletion of an unexcluded tag could cause deletion of an excluded tag
#deleteTest 'EXCLUDE' test_delete_exclude.py
#deleteTest 'EXCLUDE' test_delete_exclude_single_tag.py

#
# DELETE FROM COUNT
#
deleteTest 'FROM COUNT' test_delete_from_count.py
deleteTest 'FROM COUNT SINGLE TAG (commit tag)' test_delete_from_count_single_tag.py

#
# DELETE FROM DATE
#
deleteTest 'FROM DATE' test_delete_from_date.py
deleteTest 'FROM DATE SINGLE TAG (commit tag)' test_delete_from_date_single_tag.py

#
# DELETE DRY RUN
#
deleteTest 'DRY RUN' test_delete_dry_run.py

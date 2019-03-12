import datetime
import json
import os
import sys
import pytest

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        os.pardir + os.sep + os.pardir
    )
)
import tools
from fixtures import (
    fixture_registry_url,
    fixture_client,
    fixture_repository,
    fixture_garbage_tags,
)
from dregcli.console.garbage import GarbageCommandHandler


class TestGarbageFromDateIncludeLayerSingleTag:
    @pytest.mark.usefixtures(
        'fixture_registry_url',
        'fixture_client',
        'fixture_repository',
        'fixture_garbage_tags',
    )
    def test_from_date_include_layer_single_tag(
        self,
        fixture_registry_url,
        fixture_client,
        fixture_repository,
        fixture_garbage_tags,
        capsys
    ):
        # check data set adhoc state
        repo = fixture_client.repositories()[0]
        repo_tags = repo.tags()
        assert sorted(repo_tags) == sorted(fixture_garbage_tags)

        # tags by date desc (and their name should match fixtures)
        tags_by_desc_date = repo.get_tags_by_date()
        expected_tag_names_by_desc_date = [
            tag_data['tag'] for tag_data in tags_by_desc_date
        ]
        assert sorted(expected_tag_names_by_desc_date) == \
            sorted(fixture_garbage_tags)

        from_index = 1
        from_date = tags_by_desc_date[from_index]['date']
        # remove one sec from frontier date (see garbage command helper)
        from_date = from_date - datetime.timedelta(seconds=1)
        from_date = from_date.strftime('%Y-%m-%d %H:%M:%S.%f')

        handler = GarbageCommandHandler()
        deleted = handler.run(
            fixture_registry_url,
            fixture_repository,
            False,
            from_date=from_date,
            include_layer_single_tag='^master'
        )

        # 'commit tags' to be removed
        # (no other release tags like 'staging' on them)
        commit_tag_only_tags = [
            'master-2ze98e000wx39d60a7390925d0czr3qs03j90aaa-1382',
            'master-2bd32d000ez93c50h8486935f0fda5ee09z98bbb-1384',
        ]

        # check commit_tags_only tags deleted
        assert sorted(deleted) == sorted(commit_tag_only_tags)

        # check repo should have over tags than commit_tags_only left now
        should_left_tags = [
            t for t in fixture_garbage_tags if t not in commit_tag_only_tags
        ]
        assert sorted(repo.tags()) == sorted(should_left_tags)

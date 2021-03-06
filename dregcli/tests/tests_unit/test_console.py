import os
import sys
from unittest import mock
import pytest

sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
)
from fixtures import (
    fixture_registry_url,
    fixture_repository,
    fixture_tags
)
from dregcli.console import main as console_main


class TestConsoleCommandLine:
    @pytest.mark.usefixtures('fixture_registry_url')
    def test_reps(self, fixture_registry_url):
        with mock.patch(
            'sys.argv',
            ['dregcli', 'reps', fixture_registry_url]
        ):
            with mock.patch(
                'dregcli.console.RepositoriesCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    False,
                    user=None,
                    debug=False
                )

        # json
        with mock.patch(
            'sys.argv',
            ['dregcli', 'reps', fixture_registry_url, '-j']
        ):
            with mock.patch(
                'dregcli.console.RepositoriesCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    True,
                    user=None,
                    debug=False
                )

    @pytest.mark.usefixtures('fixture_registry_url')
    def test_user(self, fixture_registry_url):
        # user
        with mock.patch(
            'sys.argv',
            ['dregcli', '-u', 'login:pwd', 'reps', fixture_registry_url]
        ):
            with mock.patch(
                'dregcli.console.RepositoriesCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    False,
                    user='login:pwd',
                    debug=False
                )

    @pytest.mark.usefixtures('fixture_registry_url')
    def test_debug(self, fixture_registry_url):
        # user
        with mock.patch(
            'sys.argv',
            ['dregcli', '--debug', 'reps', fixture_registry_url]
        ):
            with mock.patch(
                'dregcli.console.RepositoriesCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    False,
                    user=None,
                    debug=True
                )

    @pytest.mark.usefixtures('fixture_registry_url', 'fixture_repository')
    def test_tags(self, fixture_registry_url, fixture_repository):
        with mock.patch(
            'sys.argv',
            [
                'dregcli',
                'tags',
                fixture_registry_url,
                fixture_repository,
            ]
        ):
            with mock.patch(
                'dregcli.console.TagsCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    fixture_repository,
                    False,
                    user=None,
                    debug=False
                )

        # json
        with mock.patch(
            'sys.argv',
            [
                'dregcli',
                'tags',
                fixture_registry_url,
                fixture_repository,
                '-j',
            ]
        ):
            with mock.patch(
                'dregcli.console.TagsCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    fixture_repository,
                    True,
                    user=None,
                    debug=False
                )

    @pytest.mark.usefixtures('fixture_registry_url', 'fixture_repository')
    def test_images(self, fixture_registry_url, fixture_repository):
        with mock.patch(
            'sys.argv',
            [
                'dregcli',
                'images',
                fixture_registry_url,
                fixture_repository,
            ]
        ):
            with mock.patch(
                'dregcli.console.ImagesCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    fixture_repository,
                    False,
                    user=None,
                    debug=False
                )

        # json
        with mock.patch(
            'sys.argv',
            [
                'dregcli',
                'images',
                fixture_registry_url,
                fixture_repository,
                '-j',
            ]
        ):
            with mock.patch(
                'dregcli.console.ImagesCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    fixture_repository,
                    True,
                    user=None,
                    debug=False
                )

    @pytest.mark.usefixtures(
        'fixture_registry_url',
        'fixture_repository',
        'fixture_tags'
    )
    def test_image(
        self,
        fixture_registry_url,
        fixture_repository,
        fixture_tags
    ):
        with mock.patch(
            'sys.argv',
            [
                'dregcli',
                'image',
                fixture_registry_url,
                fixture_repository,
                fixture_tags[0],
            ]
        ):
            with mock.patch(
                'dregcli.console.ImageCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    fixture_repository,
                    fixture_tags[0],
                    False,
                    False,
                    False,
                    False,
                    user=None,
                    debug=False
                )

        # manifest
        with mock.patch(
            'sys.argv',
            [
                'dregcli',
                'image',
                fixture_registry_url,
                fixture_repository,
                fixture_tags[0],
                '-m',
            ]
        ):
            with mock.patch(
                'dregcli.console.ImageCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    fixture_repository,
                    fixture_tags[0],
                    True,
                    False,
                    False,
                    False,
                    user=None,
                    debug=False
                )

        # json
        with mock.patch(
            'sys.argv',
            [
                'dregcli',
                'image',
                fixture_registry_url,
                fixture_repository,
                fixture_tags[0],
                '-j',
            ]
        ):
            with mock.patch(
                'dregcli.console.ImageCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    fixture_repository,
                    fixture_tags[0],
                    False,
                    True,
                    False,
                    False,
                    user=None,
                    debug=False
                )

        # delete
        with mock.patch(
            'sys.argv',
            [
                'dregcli',
                'image',
                fixture_registry_url,
                fixture_repository,
                fixture_tags[0],
                '-d',
            ]
        ):
            with mock.patch(
                'dregcli.console.ImageCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    fixture_repository,
                    fixture_tags[0],
                    False,
                    False,
                    True,
                    False,
                    user=None,
                    debug=False
                )

        # always yes
        with mock.patch(
            'sys.argv',
            [
                'dregcli',
                'image',
                fixture_registry_url,
                fixture_repository,
                fixture_tags[0],
                '-y',
            ]
        ):
            with mock.patch(
                'dregcli.console.ImageCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    fixture_repository,
                    fixture_tags[0],
                    False,
                    False,
                    False,
                    True,
                    user=None,
                    debug=False
                )

    @pytest.mark.usefixtures('fixture_registry_url', 'fixture_repository')
    def test_delete(
        self,
        fixture_registry_url,
        fixture_repository
    ):
        with mock.patch(
            'sys.argv',
            [
                'dregcli',
                'delete',
                fixture_registry_url,
                fixture_repository,
            ]
        ):
            with mock.patch(
                'dregcli.console.DeleteCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    fixture_repository,
                    False,
                    user=None,
                    dry_run=False,
                    yes=False,
                    all=False,
                    from_count=0,
                    from_date=0,
                    single_tag='',
                    include='',
                    # exclude='',
                    debug=False
                )

        # json
        with mock.patch(
            'sys.argv',
            [
                'dregcli',
                'delete',
                fixture_registry_url,
                fixture_repository,
                '-j'
            ]
        ):
            with mock.patch(
                'dregcli.console.DeleteCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    fixture_repository,
                    True,
                    user=None,
                    dry_run=False,
                    yes=False,
                    all=False,
                    from_count=0,
                    from_date=0,
                    single_tag='',
                    include='',
                    # exclude=''
                    debug=False
                )

        # null
        with mock.patch(
            'sys.argv',
            [
                'dregcli',
                'delete',
                fixture_registry_url,
                fixture_repository,
                '-n'
            ]
        ):
            with mock.patch(
                'dregcli.console.DeleteCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    fixture_repository,
                    False,
                    user=None,
                    dry_run=True,
                    yes=False,
                    all=False,
                    from_count=0,
                    from_date=0,
                    single_tag='',
                    include='',
                    # exclude=''
                    debug=False
                )

        # yes
        with mock.patch(
            'sys.argv',
            [
                'dregcli',
                'delete',
                fixture_registry_url,
                fixture_repository,
                '-y'
            ]
        ):
            with mock.patch(
                'dregcli.console.DeleteCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    fixture_repository,
                    False,
                    user=None,
                    dry_run=False,
                    yes=True,
                    all=False,
                    from_count=0,
                    from_date=0,
                    single_tag='',
                    include='',
                    # exclude=''
                    debug=False
                )

        # all
        with mock.patch(
            'sys.argv',
            [
                'dregcli',
                'delete',
                fixture_registry_url,
                fixture_repository,
                '-a'
            ]
        ):
            with mock.patch(
                'dregcli.console.DeleteCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    fixture_repository,
                    False,
                    user=None,
                    dry_run=False,
                    yes=False,
                    all=True,
                    from_count=0,
                    from_date=0,
                    single_tag='',
                    include='',
                    # exclude=''
                    debug=False
                )

        # from_count
        with mock.patch(
            'sys.argv',
            [
                'dregcli',
                'delete',
                fixture_registry_url,
                fixture_repository,
                '--from-count=10'
            ]
        ):
            with mock.patch(
                'dregcli.console.DeleteCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    fixture_repository,
                    False,
                    user=None,
                    dry_run=False,
                    yes=False,
                    all=False,
                    from_count=10,
                    from_date=0,
                    single_tag='',
                    include='',
                    # exclude=''
                    debug=False
                )

        # from_date
        with mock.patch(
            'sys.argv',
            [
                'dregcli',
                'delete',
                fixture_registry_url,
                fixture_repository,
                '--from-date=2018-06-30'
            ]
        ):
            with mock.patch(
                'dregcli.console.DeleteCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    fixture_repository,
                    False,
                    user=None,
                    dry_run=False,
                    yes=False,
                    all=False,
                    from_count=0,
                    from_date='2018-06-30',
                    single_tag='',
                    include='',
                    # exclude=''
                    debug=False
                )

        # include
        include_option_val = "^staging-[0-9]\{4\}"
        with mock.patch(
            'sys.argv',
            [
                'dregcli',
                'delete',
                fixture_registry_url,
                fixture_repository,
                '--include="{include}"'.format(include=include_option_val)
            ]
        ):
            with mock.patch(
                'dregcli.console.DeleteCommandHandler.run'
            ) as mo:
                console_main()
                mo.assert_called_once_with(
                    fixture_registry_url,
                    fixture_repository,
                    False,
                    user=None,
                    dry_run=False,
                    yes=False,
                    all=False,
                    from_count=0,
                    from_date=0,
                    single_tag='',
                    include=include_option_val,
                    # exclude=''
                    debug=False
                )

        # exclude desactivated: for layers with multiple tags,
        # deletion of an unexcluded tag could cause deletion of an excluded
        # tag
        # exclude
        # exclude_option_val = "^stable-[0-9]\{4\}"
        # with mock.patch(
        #     'sys.argv',
        #     [
        #         'dregcli',
        #         'delete',
        #         fixture_registry_url,
        #         fixture_repository,
        #         '--exclude="{exclude}"'.format(exclude=exclude_option_val)
        #     ]
        # ):
        #     with mock.patch(
        #         'dregcli.console.DeleteCommandHandler.run'
        #     ) as mo:
        #         console_main()
        #         mo.assert_called_once_with(
        #             fixture_registry_url,
        #             fixture_repository,
        #             False,
        #             user=None,
        #             dry_run=False,
        #             yes=False,
        #             all=False,
        #             from_count=0,
        #             from_date=0,
        #             single_tag='',
        #             include='',
        #             exclude=exclude_option_val
        #             debug=False
        #         )

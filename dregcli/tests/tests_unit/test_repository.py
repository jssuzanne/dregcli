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
    fixture_repositories,
    fixture_tags,
    fixture_digest,
    fixture_tags_url,
    fixture_tags_json,
    fixture_image_url,
    fixture_image_json,
)
from dregcli.dregcli import DRegCliException, Client, Repository, Image


class TestRepository:
    @pytest.mark.usefixtures(
        'fixture_registry_url',
        'fixture_repository',
        'fixture_tags_url',
        'fixture_tags_json'
    )
    def test_tags(
        self,
        fixture_registry_url,
        fixture_repository,
        fixture_tags_url,
        fixture_tags_json
    ):
        expected_url = fixture_registry_url + fixture_tags_url
        mock_res = mock.MagicMock()
        mock_res.status_code = 200
        mock_res.json = mock.MagicMock(return_value=fixture_tags_json)

        with mock.patch('requests.get', return_value=mock_res) as mo:
            repository = Repository(
                Client(fixture_registry_url),
                fixture_repository
            )
            tags = repository.tags()
            assert isinstance(tags, list) and \
                tags == fixture_tags_json['tags']

    @pytest.mark.usefixtures(
        'fixture_registry_url',
        'fixture_repository',
        'fixture_tags',
        'fixture_digest',
        'fixture_image_url',
        'fixture_image_json'
    )
    def test_image(
        self,
        fixture_registry_url,
        fixture_repository,
        fixture_tags,
        fixture_digest,
        fixture_image_url,
        fixture_image_json
    ):
        expected_url = fixture_registry_url + fixture_image_url
        mock_res = mock.MagicMock()
        mock_res.status_code = 200
        mock_res.json = mock.MagicMock(
            return_value=fixture_image_json
        )

        # mock response headers
        response_headers = {}
        response_headers[Repository.Meta.manifest_response_header_digest] = \
            fixture_digest
        mock_res.headers.__getitem__.side_effect = response_headers.__getitem__
        mock_res.headers.get.side_effect = response_headers.get  # mock get
        mock_res.headers.__iter__.side_effect = response_headers.__iter__

        expected_image_name = "{repo}:{tag}".format(
            repo=fixture_repository,
            tag=fixture_tags[0]
        )

        with mock.patch('requests.get', return_value=mock_res) as mo:
            repository = Repository(
                Client(fixture_registry_url),
                fixture_repository
            )
            image = repository.image(fixture_tags[0])
            mo.assert_called_once_with(
                expected_url,
                headers=Repository.Meta.manifests_headers
            )
            assert type(image) == Image and \
                image.name == fixture_repository and \
                image.tag == fixture_tags[0] and \
                image.digest == fixture_digest and \
                image.data == fixture_image_json and \
                str(image) == "{repo}:{tag}".format(
                    repo=fixture_repository,
                    tag=fixture_tags[0])

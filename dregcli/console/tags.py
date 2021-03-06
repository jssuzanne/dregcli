import json
from tabulate import tabulate

from .handler import CommandHandler
from dregcli.dregcli import DRegCliException, Repository


class TagsCommandHandler(CommandHandler):
    class Meta:
        command = "tags"

    @classmethod
    def set_parser(cls, subparsers):
        subparser_tags = subparsers.add_parser(
            cls.Meta.command, help='List repository tags'
        )

        subparser_tags.add_argument(
            'url',
            help="Url in the form protocol://host:port\n"
                 'example: http://localhost:5001'
        )
        subparser_tags.add_argument(
            'repo',
            help='Repository, example: library/alpine'
        )
        subparser_tags.add_argument(
            '-j', '--json',
            action='store_true',
            help='Json output'
        )

        subparser_tags.set_defaults(
            func=lambda args: cls().run(
                args.url,
                args.repo,
                args.json,
                user=args.user,
                debug=args.debug
            )
        )
        return subparser_tags

    def run(self, url, repo, json_output, user=False, debug=False):
        super().run(url, json_output, user=user, debug=debug)

        tags_by_date = []
        try:
            repository = Repository(self.client, repo)
            tags_by_date = repository.get_tags_by_date()

            if json_output:
                res = json.dumps({
                    'result': [
                        {
                            'tag': tag_data['tag'],
                            'date': self.date2str(tag_data['date'])
                        } for tag_data in tags_by_date
                    ]
                })
            else:
                res = tabulate([
                    [tag_data['tag'], self.date2str(tag_data['date'])]
                    for tag_data in tags_by_date
                ], headers=['Tag', 'Date'])
        except DRegCliException as e:
            res = str(e)
            if json_output:
                res = json.dumps({'error': res})
        print(res)
        return tags_by_date

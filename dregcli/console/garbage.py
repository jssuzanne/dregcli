import json

from .handler import CommandHandler
from dregcli.dregcli import DRegCliException, Repository


class GarbageCommandHandler(CommandHandler):
    class Meta:
        command = "garbage"

    @classmethod
    def set_parser(cls, subparsers):
        subparser_garbage = subparsers.add_parser(
            'garbage', help='garbage image tags'
        )
        subparser_garbage.add_argument(
            'url',
            help='Url in the form protocol://host:port, '
                 'example: http://localhost:5001'
        )
        subparser_garbage.add_argument(
            'repo',
            help='Repository, example: library/alpine'
        )
        subparser_garbage.add_argument(
            '-y', '--yes',
            action='store_true',
            help='Force yes, no confirmation'
                 'WARNING: proceed with caution and particulary with --all'
        )
        subparser_garbage.add_argument(
            '-n', '--null',
            action='store_true',
            help='Do no run actions and feedbacks actions that will be done'
        )
        subparser_garbage.add_argument(
            '-j', '--json',
            action='store_true',
            help='Json output'
        )
        subparser_garbage.add_argument(
            '-a', '--all',
            action='store_true',
            help='WARNING: delete all image'
        )
        subparser_garbage.add_argument(
            '--from-count',
            type=int,
            help='delete from count tags: '
                 '--from-count=11 to keep last 10 tags'
        )
        subparser_garbage.add_argument(
            '--from-day',
            type=int,
            help='delete from day: '
                 '--from-day=11 to keep last 10 days tags'
        )
        subparser_garbage.add_argument(
            '--include',
            type=str,
            help='delete tags including python regexp: '
                 '--include="^staging-[0-9]\{4\}"'
        )
        subparser_garbage.add_argument(
            '--exclude',
            type=str,
            help='delete tags excluding python regexp: '
                 'if regexp does not select anything, exclude does nothing'
                 '(no implicit --all'
                 '--exclude="^stable-[0-9]\{4\}"'
        )
        subparser_garbage.set_defaults(
            func=lambda args: GarbageCommandHandler().run(
                args.url, args.repo, args.json,
                user=args.user,
                null=args.null,
                yes=args.yes,
                all=args.all,
                from_count=args.from_count or 0,
                from_day=args.from_day or 0,
                include=args.include and args.include.strip("\"'") or '',
                exclude=args.exclude and args.exclude.strip("\"'") or '',
            )
        )
        return subparser_garbage

    def run(
        self,
        url,
        repo,
        json_output,
        null=False,
        yes=False,
        user=False,
        all=False,
        from_count=0,
        from_day=0,
        include='',
        exclude=''
    ):
        super().run(url, json_output, user=user)

        if not (all or from_count or from_day or include or exclude):
            msg = 'no option selected (criteria). --delete aborted'
            if json_output:
                msg = json.dumps({'error': msg})
            print(msg)
            return

        try:
            repository = Repository(self.client, repo)
            tags = repository.tags()

            res = []
            if all:
                res = self._all(repository, tags)
            if json_output:
                res = json.dumps({'result': res})
        except DRegCliException as e:
            res = str(e)
            if json_output:
                res = json.dumps({'error': res})
        print(res)

    def _delete_image(self, repository, tag):
        try:
            repository.image(tag).delete()
        except DRegCliException as e:
            if str(e) != 'Status code error 404':
                raise e
            # 404 tolerated during image(tag) or delete():
            # tag in common with same commit tag
            # and already deleted by previous tag
            # exemple:
            # master-6da64c000cf59c30e4841371e0dac3dd02c31aaa-1385 old-prod
            # representing same image

    def _all(self, repository, tags):
        deleted = []
        for tag in tags:
            self._delete_image(repository, tag)
            deleted.append(tag)
        return deleted
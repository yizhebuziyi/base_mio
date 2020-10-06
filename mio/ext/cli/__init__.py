# -*- encoding: utf-8 -*-
from flask import current_app
from flask_script import Manager

CliCommand = Manager(usage=u'Execute Command line.')


@CliCommand.option('-cls', '--clazz', dest='clazz', default=None,
                   help=u'Class name. like: cli.Hello.World.me, file in cli folder and name is Hello.py.')
@CliCommand.option('-arg', '--args', dest='args', default=None,
                   help=u'Arguments. using k=v. If you have multiple parameters, you need to use "||".'
                        u' like: "k1=v1||k2=v2..."')
def exe(clazz=None, args=None):
    if clazz is None:
        print(u'Execute cli function, like: shell.py cli exe -cls=cli.Hello.World.me')
        return
    tmp = clazz.split('.')
    file = '.'.join(tmp[0:-2])
    clazz = tmp[-2]
    method = tmp[-1]
    kwargs = {}
    if args is not None:
        args = args.split('||')
        for arg in args:
            tmp = arg.split('=')
            if len(tmp) != 2:
                continue
            key = tmp[0]
            value = '='.join(tmp[1:])
            kwargs[key] = value
    try:
        obj = __import__(file, globals(), locals(), clazz)
        cls = getattr(obj, clazz)
        obj = cls()
        execute = getattr(obj, method)
        execute(app=current_app, kwargs=kwargs)
    except Exception as e:
        print(e)

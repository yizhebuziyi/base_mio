# -*- encoding: utf-8 -*-
from flask import current_app
from flask_script import Manager

CliCommand = Manager(usage=u'执行命令行操作')


@CliCommand.option('-cls', '--clazz', dest='clazz', default=None,
                   help="设置运行的class，例：cli.Hello.World.me，文件放在cli")
@CliCommand.option('-arg', '--args', dest='args', default=None,
                   help="要传入的参数，一般是k=v的形式传入，连词符为||，为了避免出问题，最好加\"\"传入")
def exe(clazz=None, args=None):
    if clazz is None:
        print('请指定要执行的类名，例：-cls=cli.Hello.World.me')
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

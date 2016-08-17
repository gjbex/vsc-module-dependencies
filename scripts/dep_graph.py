#!/usr/bin/env python

import os


DIR_ERROR = 1

def show_graph(graph, root, reverse=False, prune=True,
               prefix='', done=set()):
    if prefix:
        if reverse:
            infix = '-> '
        else:
            infix = '<- '
    else:
        infix = ''
    print '{0}{1}{2}'.format(prefix, infix, root)
    if root not in done:
        if prune:
            done.add(root)
        for _, to_node in graph.edges(root):
            show_graph(graph, to_node, reverse, prune,
                       prefix + '  ', done)
    

def show_list(graph, root, no_natsort=False, prefix=''):
    modules = set(graph.nodes())
    modules.remove(root)
    if no_natsort:
        module_list = sorted(modules, key=lambda x: x.lower())
        print '\n'.join((prefix + x for x in module_list))
    else:
        from natsort import versorted
        module_list = versorted(modules, key=lambda x: x.lower())
        print '\n'.join((prefix + x for x in module_list))

if __name__ == '__main__':
    from argparse import ArgumentParser
    import os.path, sys
    import networkx as nx
    from vsc.module.dependencies import ModuleDependencies
    from vsc.module.parser import ModuleParser

    arg_parser = ArgumentParser(description='compute dependency graph '
                                            'for a module')
    arg_parser.add_argument('module',
                            help='module to compute  dependency graph for')
    arg_parser.add_argument('--dir', '-d',
                            help='module file directory list, default is '
                                 'MODULEPATH')
    arg_parser.add_argument('--reverse', '-r', action='store_true',
                            help='compute reverse dependencies')
    arg_parser.add_argument('--no_prune', '-P', action='store_true',
                            help='do not prune dependency tree')
    arg_parser.add_argument('--flatten', '-f', action='store_true',
                            help='faltten dependency tree')
    arg_parser.add_argument('--no_natsort', '-N', action='store_true',
                            help='do not use natsort')
    arg_parser.add_argument('--verbose', action='store_true',
                            help='generate extra debugging output')
    options = arg_parser.parse_args()
    if not options.dir:
        dir_names = os.getenv('MODULEPATH', '.').split(os.pathsep)
    else:
        dir_names = options.dir.split(os.pathsep)
        for dir_name in dir_names:
            if not os.path.exists(dir_name):
                msg = "### error: directory '{0}' does not exist"
                sys.stderr.write(msg.format(dir_name))
                sys.exit(DIR_ERROR)
            if not os.path.isdir(dir_name):
                msg = "### error: '{0}' is not directory"
                sys.stderr.write(msg.format(dir_name))
                sys.exit(DIR_ERROR)
    parser = ModuleParser()
    for dir_name in dir_names:
        print('Module path: {0}'.format(dir_name))
        modules = parser.parse_dir(dir_name)
        dependencies = ModuleDependencies(modules)
        dependencies.is_verbose = options.verbose
        if options.reverse:
            graph = dependencies.get_reverse_dependencies(options.module)
        else:
            graph = dependencies.get_dependencies(options.module)
        if options.flatten:
            show_list(graph, options.module, options.no_natsort,
                      prefix='  ')
        else:
            show_graph(graph, options.module, reverse=options.reverse,
                       prune=not(options.no_prune), prefix='  ')

#!/usr/bin/env python

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
    arg_parser.add_argument('--dir', help='module file directory')
    arg_parser.add_argument('--reverse', action='store_true',
                            help='compute reverse dependencies')
    arg_parser.add_argument('--no_prune', action='store_true',
                            help='do not prune dependency tree')
    arg_parser.add_argument('--verbose', action='store_true',
                            help='generate extra debugging output')
    options = arg_parser.parse_args()
    if not os.path.exists(options.dir):
        msg = "### error: directory '{0}' does not exist"
        sys.stderr.write(msg.format(options.dir))
        sys.exit(DIR_ERROR)
    if not os.path.isdir(options.dir):
        msg = "### error: '{0}' is not directory"
        sys.stderr.write(msg.format(options.dir))
        sys.exit(DIR_ERROR)
    parser = ModuleParser()
    modules = parser.parse_dir(options.dir)
    dependencies = ModuleDependencies(modules)
    dependencies.is_verbose = options.verbose
    if options.reverse:
        graph = dependencies.get_reverse_dependencies(options.module)
    else:
        graph = dependencies.get_dependencies(options.module)
    show_graph(graph, options.module, reverse=options.reverse,
               prune=not(options.no_prune))
import sqlite3, sys
import networkx as nx

class ModuleDependencies(object):

    def __init__(self, modules):
        '''Constructor, takes a dict of module names as keys and lists
           of modules as values'''
        self._is_verbose = False
        self._conn = sqlite3.connect(':memory:')
        self._init_module_table(modules)
        self._init_dependencies_table(modules)

    @property
    def is_verbose(self):
        return self._is_verbose

    @is_verbose.setter
    def is_verbose(self, is_verbose):
        self._is_verbose = is_verbose

    def _init_module_table(self, modules):
        cursor = self._conn.cursor()
        all_modules = set()
        all_modules.update(modules.keys())
        for module_list in modules.values():
            all_modules.update(module_list)
        cursor = self._conn.cursor()
        cursor.execute(
            '''CREATE TABLE modules (
                   module TEXT NOT NULL,
                   UNIQUE(module)
               )''' 
        )
        insert_stmt = '''INSERT INTO modules (module) VALUES (?)'''
        for module in all_modules:
            cursor.execute(insert_stmt, (module, ))
        self._conn.commit()
        cursor.close()

    def _init_dependencies_table(self, modules):
        cursor = self._conn.cursor()
        cursor.execute(
            '''CREATE TABLE dependencies (
                   module TEXT NOT NULL,
                   depends_on TEXT NOT NULL,
                   FOREIGN KEY (module)
                       REFERENCES modules (module),
                   FOREIGN KEY (depends_on)
                       REFERENCES modules (module),
                   UNIQUE (module, depends_on)
               )'''
        )
        for module, dependency_list in modules.iteritems():
            for depends_on in dependency_list:
                cursor.execute(
                    '''INSERT INTO dependencies
                           (module, depends_on) VALUES (?, ?)''',
                    (module, depends_on)
                )
        self._conn.commit()
        cursor.close()

    def get_all_modules(self):
        modules = []
        cursor = self._conn.cursor()
        results = cursor.execute('''SELECT module FROM modules''')
        for row in results:
            modules.append(row[0])
        cursor.close()
        return modules

    def get_direct_dependencies(self, module):
        dependencies = []
        cursor = self._conn.cursor()
        results = cursor.execute(
            '''SELECT depends_on FROM dependencies WHERE module = ?''',
            (module, )
        )
        for row  in results:
            dependencies.append(row[0])
        cursor.close()
        return dependencies

    def get_direct_reverse_dependencies(self, module):
        dependencies = []
        cursor = self._conn.cursor()
        results = cursor.execute(
            '''SELECT module FROM dependencies WHERE depends_on = ?''',
            (module, )
        )
        for row  in results:
            dependencies.append(row[0])
        cursor.close()
        return dependencies

    def get_dependencies(self, module, graph=None):
        if not graph:
            graph = nx.DiGraph()
            graph.add_node(module)
        if self.is_verbose:
            sys.stderr.write('handling {0}...\n'.format(module))
            print self.get_direct_dependencies(module)
        for depends_on in self.get_direct_dependencies(module):
            graph.add_edge(module, depends_on)
            self.get_dependencies(depends_on, graph)
        return graph

    def get_reverse_dependencies(self, module, graph=None):
        if not graph:
            graph = nx.DiGraph()
            graph.add_node(module)
        if self.is_verbose:
            sys.stderr.write('handling {0}...\n'.format(module))
            print self.get_direct_reverse_dependencies(module)
        for depends_on in self.get_direct_reverse_dependencies(module):
            graph.add_edge(module, depends_on)
            self.get_reverse_dependencies(depends_on, graph)
        return graph

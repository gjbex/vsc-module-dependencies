import sqlite3

class ModuleDependencies(object):

    def __init__(self, modules):
        '''Constructor, takes a dict of module names as keys and lists
           of modules as values'''
        self._conn = sqlite3.connect(':memory:')
        self._init_module_table(modules)
        self._init_dependency_table(modules)

    def _init_module_table(self, modules):
        cursor = self._conn.cursor()
        all_modules = set()
        all_modules.update(modules.keys())
        for module_list in modules.values():
            all_modules.update(module_list)
        cursor.execute(
            '''CREATE TABLE modules (
                   module_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   module_name TEXT NOT NULL,
                   module_version TEXT NOT NULL,
                   UNIQUE(module_name, module_version)
               )''' 
        )
        insert_stmt = '''INSERT INTO modules
                             (module_name, module_version) VALUES (?, ?)'''
        for module in all_modules:
            module_name, module_version = module.split('/')
            cursor.execute(insert_stmt, (module_name, module_version))
        cursor.close()
        self._conn.commit()

    def _init_dependency_table(self, modules):
        cursor = self._conn.cursor()
        cursor.execute(
            '''CREATE TABLE dependencies (
                   dependency_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   module_id INTEGER NOT NULL,
                   depends_on_id INTEGER NOT NULL,
                   FOREIGN KEY (module_id)
                       REFERENCES modules (module_id),
                   FOREIGN KEY (depends_on_id)
                       REFERENCES modules (module_id),
                   UNIQUE (module_id, depends_on_id)
               )'''
        )
        for module, dependency_list in modules.iteritems():
            module_id = self.get_module_id(module)
            for depends_on in dependency_list:
                depends_on_id = self.get_module_id(depends_on)
                cursor.execute(
                    '''INSERT INTO dependencies
                           (module_id, depends_on_id) VALUES (?, ?)''',
                    (module_id, depends_on_id)
                )
        cursor.close()
        self._conn.commit()

    def get_module_id(self, module):
        module_name, module_version = module.split('/')
        cursor = self._conn.cursor()
        results = cursor.execute(
            '''SELECT module_id FROM modules
                   WHERE module_name = ? AND module_version = ?''',
            (module_name, module_version)
        )
        module_id = results.fetchone()
        if module_id:
            return module_id[0]
        else:
            return None
        
    def all_modules(self):
        modules = []
        cursor = self._conn.cursor()
        results = cursor.execute(
            '''SELECT module_name, module_version FROM modules'''
        )
        for row in results:
            modules.append((row[0], row[1]))
        return modules

import sqlite3

class ModuleDependencies(object):

    def __init__(self, modules):
        '''Constructor, takes a dict of module names as keys and lists
           of modules as values'''
        self._conn = sqlite3.connect(':memory:')
        self._init_module_table(modules)

    def _init_module_table(self, modules):
        cursor = self._conn.cursor()
        all_modules = set()
        all_modules.update(modules.keys())
        for module_list in modules.values():
            all_modules.update(module_list)
        cursor.execute(
            '''CREATE TABLE modules
                   (module_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    module_name TEXT NOT NULL,
                    module_version TEXT NOT NULL,
                    UNIQUE(module_name, module_version))''' 
        )
        insert_stmt = '''INSERT INTO modules
                             (module_name, module_version) VALUES (?, ?)'''
        for module in all_modules:
            module_name, module_version = module.split('/')
            cursor.execute(insert_stmt, (module_name, module_version))
        cursor.close()
        self._conn.commit()

    def all_modules(self):
        modules = []
        cursor = self._conn.cursor()
        results = cursor.execute(
            '''SELECT module_name, module_version FROM modules'''
        )
        for row in results:
            modules.append((row[0], row[1]))
        return modules

'''module for parsing module files'''
import os, re

class ModuleParser(object):
    '''class to do rudimentory parsing of module files'''

    def __init__(self):
        '''constrcutor'''
        self._module_deps = {}
        self._module_regex = re.compile(r'module\s+load\s+(.+)')

    def parse_file(self, file_name):
        '''parse the given module file to find the modules it loads,
           returns the list of module names'''
        modules = []
        with open(file_name, 'r') as module_file:
            for line in module_file:
                line = line.strip()
                if match := self._module_regex.match(line):
                    module_cands = re.split(r'\s+', match.group(1))
                    for module_cand in module_cands:
                        if module_cand.startswith('#'):
                            break
                        else:
                            modules.append(module_cand)
        return modules

    def parse_dir(self, dir_name):
        '''parses all module files in the given directory, returns a
           dict with module names as keys, and lists of modules as
           values'''
        dependencies = {}
        for dir_name, _, file_names in os.walk(dir_name):
            package_name = os.path.basename(dir_name)
            for file_name in file_names:
                module_name = '{0}/{1}'.format(package_name, file_name)
                deps = self.parse_file(os.path.join(dir_name, file_name))
                dependencies[module_name] = deps
        return dependencies

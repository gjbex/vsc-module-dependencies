#!/usr/bin/env python
'''module to test the vsc.module.parser.ModuleParser parser'''

import unittest
from vsc.module.parser import ModuleParser
from vsc.module.dependencies import ModuleDependencies

class ModuleTest(unittest.TestCase):
    '''Tests for the gbalance output parser'''

    def test_parse_file(self):
        file_name = 'modules/Boost/1.57.0-foss-2015a-Python-2.7.9'
        expected_modules = [
            'foss/2015a',
            'bzip2/1.0.6-foss-2015a',
            'zlib/1.2.8-foss-2015a',
            'Python/2.7.9-foss-2015a',
        ]
        parser = ModuleParser()
        modules = parser.parse_file(file_name)
        self.assertListEqual(expected_modules, modules)

    def test_parse_dir(self):
        dir_name = 'modules/'
        expected_modules = {
            'Boost/1.57.0-foss-2015a-Python-2.7.9': [
                'foss/2015a',
                'bzip2/1.0.6-foss-2015a',
                'zlib/1.2.8-foss-2015a',
                'Python/2.7.9-foss-2015a',
            ],
            'cURL/7.40.0-intel-2015a': [
                'intel/2015a',
            ],
            'Java/1.8.0_31': [],
        }
        parser = ModuleParser()
        modules = parser.parse_dir(dir_name)
        for module in expected_modules:
            self.assertIn(module, modules)
            self.assertListEqual(expected_modules[module], modules[module])

    def test_module_list(self):
        dir_name = 'modules/'
        parser = ModuleParser()
        modules = parser.parse_dir(dir_name)
        expected_modules = set()
        expected_modules.update(modules.keys())
        for module_list in modules.values():
            expected_modules.update(module_list)
        dependencies = ModuleDependencies(modules)
        all_modules = dependencies.all_modules()
        self.assertEqual(len(expected_modules), len(all_modules))

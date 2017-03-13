import unittest

from setup import parse_version, SetupException


class TestParseVersion(unittest.TestCase):

    def test_parseversion(self):
        version = {}
        version['1.0.0'] = '1.0.0'
        version['1.0'] = '1.0.0'
        version['1.0-3-gd5f2eac-dirty'] = '1.0.3.dirty'
        version['1.2'] = '1.2.0'
        version['1.2-dirty'] = '1.2.0.dirty'
        version['1.2.3'] = '1.2.3'
        version['1.2.3-dirty'] = '1.2.3.dirty'
        version['1.2-3-gd5f2eac'] = '1.2.3'
        version['1.2-3-gd5f2eac-dirty'] = '1.2.3.dirty'
        for k, v in version.items():
            version = parse_version(k)
            self.assertEqual(v, version, "version does not match")

    def test_invalid_values(self):
        version = []
        version.append('akfjaksjfasf')
        version.append('1')
        version.append('1.a')
        version.append('a.a')
        version.append('1.2-sdfkjsfkjskfj')

        for k in version:
            self.assertRaises(SetupException, parse_version, k)


# def main():
#     unittest.main()
#
#
# if __name__ == "__main__":
#     main()

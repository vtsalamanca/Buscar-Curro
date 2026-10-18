import unittest
from ate_public import toledo_links
class PublicSourceTests(unittest.TestCase):
    def test_province_and_host(self):
        html = '<a href="/toledo.pdf">Toledo</a><a href="https://evil.invalid/toledo.pdf">Toledo</a><a href="/gu.pdf">Guadalajara</a>'
        self.assertEqual(toledo_links(html), ['https://empleopublico.castillalamancha.es/toledo.pdf'])
    def test_label_and_deduplication(self):
        self.assertEqual(len(toledo_links('<a href="/list.pdf"><b>Toledo</b></a><a href="/list.pdf">Toledo</a>')),1)
    def test_empty_is_failure(self):
        with self.assertRaises(ValueError): toledo_links('<html>Maintenance</html>')
if __name__ == '__main__': unittest.main()

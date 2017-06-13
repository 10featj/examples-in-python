import io
import unittest
import sys

import re
from bs4 import BeautifulSoup
from naive_bayes.email_object import EmailObject


class TestHTMLEmail(unittest.TestCase):
    def setUp(self):
        with open('./tests/fixtures/html.eml', 'r') as html_file:
            self.html = html_file.read()
            html_file.seek(0)
            self.html_email = EmailObject(html_file)

    def test_parses_stores_inner_text_html(self):
        body = "\n\n".join(self.html.split("\n\n")[1:])
        if sys.version_info > (3, 0):
            # Python 3 code in this block
            expected = BeautifulSoup(body, 'html.parser').text.encode('raw-unicode-escape').decode('iso-8859-1')
        else:
            # Python 2 code in this block
            expected = BeautifulSoup(body, 'html.parser', from_encoding="iso-8859-1").text
        actual_body = self.html_email.body()
        self.assertEqual(actual_body, expected)

    def test_stores_subject(self):
        expected_subject = re.search("Subject: (.*)", self.html).group(1)
        actual_subject = self.html_email.subject()
        self.assertEqual(actual_subject, expected_subject)

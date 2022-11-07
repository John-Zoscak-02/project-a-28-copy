import csv
from django.test import TestCase

from .utils import search_for_section

class SearchTests(TestCase):
	def test_open_csv(self):
		out = search_for_section({})
		self.assertIsNotNone(out)

	def test_specific_search(self):
		out = search_for_section({'department': 'AAS', 'catalog_number': '1010'})
		for section in out:
			self.assertTrue(section['Mnemonic'] == 'AAS' and section['Number'] == '1010')

	def test_invalid_search_crit(self):
		out = search_for_section({'some other criteria': 'nothing'})
		self.assertIsNone(out)

	def test_empty_search(self):
		csvfile = open('static/searchData.csv')
		reader = csv.DictReader(csvfile)
		sections = []
		for row in reader:
			sections.append(row)
		out = search_for_section({})
		self.assertEquals(sections, out)

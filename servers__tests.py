#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer, TooManyProductsFoundError

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

    def test_if_get_entries_returns_sorted_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(entries, [products[2], products[1]])

    def test_if_get_entries_returns_TooManyProductsFoundError_when_more_than_three_are_founded(self):
        products = [Product('PP234', 2), Product('PP235', 1), Product('PP236', 1.5), Product('PP237', 2.5)]
        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(TooManyProductsFoundError):
                server.get_entries(2)


class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))

    def test_get_total_prices_returns_none_when_TooManyProductsFoundError(self):
        products = [Product('PP234', 2), Product('PP235', 1), Product('PP236', 1.5), Product('PP237', 2.5)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(client.get_total_price(2), None)


if __name__ == '__main__':
    unittest.main()

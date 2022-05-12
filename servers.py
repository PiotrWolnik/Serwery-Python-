#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, TypeVar, List, Dict
from abc import ABC, abstractmethod
import re


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str)
    #  i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str)
    #  oraz `price` (typu float)

    def __init__(self, name: str, price: float):
        # Tworzymy listę ze składowej name
        name_characters = list(name)

        # Sprawdzamy czy nazwa zaczyna się literą, w przeciwnym wypadku
        # zgłaszamy wyjątek
        if not name_characters[0].isalpha():
            raise ValueError

        # Sprawdzamy czy w nazwie produktu znajduje się przynajmniej jedna cyfra
        check_if_any_letter = [char.isdigit() for char in name]
        if not any(check_if_any_letter):
            raise ValueError

        # Następnie iterujemy po liście znaków, by sprawdzić, czy któryś
        # ze znaków jest albo literą alfabetu albo cyfrą i czy nie jest
        # białym znakiem. W przeciwnym wypadku zgłaszamy wyjątek ValueError
        for char in name_characters:
            if char.isalpha() or char.isalnum() and not char.isspace():
                continue
            else:
                raise ValueError
        self.name: str = name
        self.price: float = price

    # Produkty są takie same jeśli mają taką samą nazwę i cenę
    def __eq__(self, other) -> bool:
        if self.name == other.name:
            if self.price == other.price:
                return True
            else:
                return False
        return False

    # FIXME: zwróć odpowiednią wartość

    def __hash__(self):
        return hash((self.name, self.price))


class ServerError(Exception):
    pass


class TooManyProductsFoundError(ServerError):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    def __init__(self, msg=None):
        if msg is None:
            msg = f"Too many products were founded for that pattern"
        super().__init__()


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products`
#   zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający
#   maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów
#   spełniających kryterium wyszukiwania


class Server(ABC):
    n_max_returned_entries: int = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Wewnętrzna funkcja wywoływana przez get_products
    def get_entries(self, n_letters: int = 1) -> List[Product]:
        searching_pattern = '^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters)
        entries = [product for product in self.get_products(n_letters)
                   if re.match(searching_pattern, product.name)]
        if len(entries) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError
        if entries:
            return sorted(entries, key=lambda product: product.price)
        return []

    @abstractmethod
    def get_products(self, n_letters: int = 1) -> List[Product]:
        return self.get_entries(n_letters)


class ListServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products = products

    def get_products(self, n_letters: int = 1) -> List[Product]:
        return self.products


class MapServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products: Dict[str, Product] = {
            product.name: product for product in products
        }

    def get_products(self, n_letters: int = 1) -> List[Product]:
        return list(self.products.values())


# Tworzymy nowy typ danych
ServerType = TypeVar('ServerType', bound=Server)


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def __init__(self, server: ServerType):
        self.server: ServerType = server

    def get_total_price(self, n_letters: Optional[int]) -> float:
        try:
            founded = self.server.get_entries(n_letters)
            price_sum = 0.0
            if founded:
                for product in founded:
                    price_sum += product.price
                return price_sum
            return None
        except TooManyProductsFoundError:
            return None

from project import Coffee, Receipt, validator, remove_from_order, add_to_order, get_class
import pytest


def test_coffee_init():
    coffee = Coffee("Name", 99)
    assert coffee.name == "Name"
    assert coffee.price == 99

def test_receipt_init():
    receipt = Receipt()
    assert receipt.total == 0
    assert receipt.name == ""
    assert receipt.order_number == 0

def test_validator():
    assert validator(378282246310005) == "AMEX"
    assert validator(4111111111111111) == "VISA"
    assert validator(5555555555554444) == "MASTERCARD"
    assert validator(0000) == False

def test_remove_from_order():
    assert remove_from_order({"foo": 0, "bar": 0, "baz":0}) == -1
    assert remove_from_order({}) == -1

def test_add_to_order():
    coffee1 = Coffee("test", 1)
    coffee2 = Coffee("test2", 2)
    assert add_to_order(-1, [coffee1,coffee2]) == False
    assert add_to_order("",[coffee1,coffee2]) == False
    assert add_to_order(1, []) == False

def test_get_class():
    assert get_class("") == None

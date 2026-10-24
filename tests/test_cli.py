import requests
from unittest.mock import patch, Mock

import cli


def test_get_int_asks_again_for_bad_input(capsys):
    with patch("builtins.input", side_effect=["abc", "-5", "10"]):
        number = cli.get_int("Enter a number: ")

    assert number == 10
    output = capsys.readouterr().out
    assert "Please enter a whole number" in output
    assert "can't be negative" in output

def test_view_all(capsys):
    fake_response = Mock()
    fake_response.json.return_value = [{"id": 1, "name": "Banana", "price": 0.25, "stock": 100}]

    with patch("cli.requests.get", return_value=fake_response):
        cli.view_all()

    assert "Banana" in capsys.readouterr().out

def test_view_one_not_found(capsys):
    fake_response = Mock()
    fake_response.status_code = 404
    fake_response.json.return_value = {"error": "Item not found"}

    with patch("builtins.input", return_value="99"):
        with patch("cli.requests.get", return_value=fake_response):
            cli.view_one()

    assert "Item not found" in capsys.readouterr().out

def test_add_item():
    fake_response = Mock()
    fake_response.status_code = 201
    fake_response.json.return_value = {"id": 3, "name": "Milk", "price": 2.99, "stock": 10}

    # barcode (skip), name, price, stock
    with patch("builtins.input", side_effect=["", "Milk", "2.99", "10"]):
        with patch("cli.requests.post", return_value=fake_response) as mock_post:
            cli.add_item()

    mock_post.assert_called_once_with(
        "http://localhost:5555/inventory",
        json={"name": "Milk", "price": 2.99, "stock": 10}
    )

def test_update_item_stock():
    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"id": 1, "name": "Banana", "price": 0.25, "stock": 50}

    # item id, choose stock, new stock
    with patch("builtins.input", side_effect=["1", "2", "50"]):
        with patch("cli.requests.patch", return_value=fake_response) as mock_patch:
            cli.update_item()

    mock_patch.assert_called_once_with("http://localhost:5555/inventory/1", json={"stock": 50})

def test_delete_item():
    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"message": "Item 1 deleted"}

    with patch("builtins.input", side_effect=["1", "y"]):
        with patch("cli.requests.delete", return_value=fake_response) as mock_delete:
            cli.delete_item()

    mock_delete.assert_called_once_with("http://localhost:5555/inventory/1")

def test_delete_item_cancelled():
    with patch("builtins.input", side_effect=["1", "n"]):
        with patch("cli.requests.delete") as mock_delete:
            cli.delete_item()

    mock_delete.assert_not_called()

def test_find_on_api_by_name(capsys):
    fake_response = Mock()
    fake_response.json.return_value = [{"barcode": "1", "product_name": "Almond Milk", "brands": "Silk"}]

    with patch("builtins.input", side_effect=["2", "almond milk"]):
        with patch("cli.requests.get", return_value=fake_response):
            cli.find_on_api()

    assert "Almond Milk" in capsys.readouterr().out

def test_main_server_not_running(capsys):
    # View all products, then exit
    with patch("builtins.input", side_effect=["1", "7"]):
        with patch("cli.requests.get", side_effect=requests.exceptions.ConnectionError):
            cli.main()

    output = capsys.readouterr().out
    assert "Could not connect to the server" in output
    assert "Goodbye!" in output

def test_main_invalid_choice(capsys):
    with patch("builtins.input", side_effect=["abc", "7"]):
        cli.main()

    assert "Invalid choice" in capsys.readouterr().out

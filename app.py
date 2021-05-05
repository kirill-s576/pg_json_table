# Settings
from config import *
# Standard lib
import json
import os
import argparse
from typing import List
# Custom packages
from src.database.postgres import PostgresConnection
from src.models.my_json_table import MyJsonTable
from src.serializers.input import InputJsonDatabaseConnector, InputJsonSerializer
from src.exceptions import InputFileDoesntExists, InputDataIsNotValid


def get_file_path_from_argv():
    """
    Argparser. Returns file_path from run attributes.
    """
    parser = argparse.ArgumentParser(description='App arguments')
    parser.add_argument('--file',
                        metavar='N',
                        type=str,
                        required=True,
                        help='Path to file with objects')
    args = parser.parse_args()
    file_path = args.file
    return file_path

def is_file_exists(file_path) -> bool:
    """
    Check for file exists
    :param file_path:
    :return:
    """
    return os.path.exists(file_path)

def get_input_objects_from_file(file_path: str) -> List[dict]:
    """
    Read file and return objects from it
    :param file_path:
    :return:
    """
    if not is_file_exists(file_path):
        raise InputFileDoesntExists("Insert correct file path.")
    with open('input.json', "r") as f:
        json_data = json.load(f)
    if isinstance(json_data, list):
        return json_data
    elif isinstance(json_data, dict):
        return [json_data]
    else:
        raise InputDataIsNotValid("Data must be in a List[dict] or dict format")

def main() -> None:
    """
    Main function.
    Business logic:
    - Get path to input file from argv
    - Get prepared objects for inserting to database.
    - Make database connection.
    - Initialize table class with connection.
    - Serialize each object and insert to database.
    """
    file_path = get_file_path_from_argv()
    dict_objects_list = get_input_objects_from_file(file_path)
    connection = PostgresConnection(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        db_name=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    table = MyJsonTable(
        connection=connection
    )
    for dict_input_object in dict_objects_list:
        serializer = InputJsonSerializer(**dict_input_object)
        obj = InputJsonDatabaseConnector(serializer)
        table.insert_row(obj)


if __name__ == '__main__':
    main()

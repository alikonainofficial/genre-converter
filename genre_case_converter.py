"""
This module provides functionality to fetch, convert, and update genre names
from a Supabase database. It includes functions to handle camelCase to Title Case
conversion with special cases for certain genre names.
"""

import re
import argparse
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def create_supabase_client(url: str, key: str) -> Client:
    """
    Creates and returns a Supabase client to interact with the database.

    Args:
        url (str): The Supabase project URL.
        key (str): The Supabase project API key.

    Returns:
        Client: A Supabase client instance.
    """
    return create_client(url, key)


def fetch_genre_data(supabase_client: Client, table_name: str) -> list:
    """
    Fetches the genres column data and row IDs from the specified table.

    Args:
        supabase_client (Client): The Supabase client to interact with the database.
        table_name (str): The name of the table to fetch the genre data from.

    Returns:
        list: A list of tuples containing (id, genres) pairs.
    """
    response = supabase_client.table(table_name).select("id, genres").execute()
    # Extract id and genre arrays from the response
    genre_data = [(item["id"], item["genres"]) for item in response.data]
    return genre_data


def update_genre_data(
    supabase_client: Client,
    table_name: str,
    row_id: str,
    converted_genres: list,
) -> None:
    """
    Updates the genre data in the specified table.

    Args:
        supabase_client (Client): The Supabase client to interact with the database.
        table_name (str): The name of the table to update the genre data in.
        row_id (str): The id of the row to update.
        converted_genres (list): The converted genre data to be updated.
    """
    supabase_client.table(table_name).update({"genres": converted_genres}).eq(
        "id", row_id
    ).execute()
    print(f"Updated genre data for {row_id} in {table_name}")


def convert_genre_names(genre_list: list) -> list:
    """
    Converts genre names from camelCase to Title Case, with special handling for certain cases.

    Args:
        genre_list (list): A list of genre strings.

    Returns:
        list: A new list of genre strings where camelCase is converted to title case.
    """
    converted_list = []

    for genre in genre_list:
        if genre == "childrensFiction":
            # Special case for 'childrensFiction'
            converted_list.append("Children's Fiction")
        elif genre == "gothic":
            converted_list.append("Gothic Fiction")
        elif " " not in genre and not (genre[0].isupper() and genre[1:].islower()):
            # Convert only if:
            # 1. It doesn't contain spaces AND
            # 2. It's not already in Title Case (first letter upper, rest lower)
            converted_genre = re.sub(r"(?<!^)(?=[A-Z])", " ", genre).title()
            converted_list.append(converted_genre)
        else:
            # If genre already contains spaces or is in Title Case, append as-is
            converted_list.append(genre)

    return converted_list


def process_genres(table_name: str) -> None:
    """
    Fetches genre data from Supabase, processes it, and converts camelCase genres to Title Case.

    Args:
        table_name (str): The name of the table containing genre data.
    """
    supabase_client = create_supabase_client(SUPABASE_URL, SUPABASE_KEY)
    genre_data = fetch_genre_data(supabase_client, table_name)

    for row_id, genre_list in genre_data:
        converted_genres = convert_genre_names(genre_list)
        print(f"Original: {genre_list}")
        print(f"Converted: {converted_genres}\n")
        update_genre_data(supabase_client, table_name, row_id, converted_genres)


def main():
    """
    Main function to handle command-line arguments and invoke the genre processing.
    """
    parser = argparse.ArgumentParser(description="Fetch and convert genre names from Supabase.")
    parser.add_argument("table_name", type=str, help="Name of the table to fetch genre data from")

    args = parser.parse_args()

    # Call the process_genres function with the provided arguments
    process_genres(args.table_name)


if __name__ == "__main__":
    main()

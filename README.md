Genre Conversion Tool

This Python module is designed to fetch, convert, and update genre names from a Supabase database. It processes genre names by converting camelCase to Title Case, with special handling for certain cases, and updates the processed data back into the database.

Features

	•	Fetch Genres: Retrieves genre data from a specified table in a Supabase database.
	•	Convert Genres: Converts genre names from camelCase to Title Case, with special rules for specific genres like “childrensFiction” and “gothic”.
	•	Update Genres: Updates the processed genre names back to the database.
	•	Command-line Interface: Allows you to specify the table name via command-line arguments.

Requirements

	•	Python 3.x
	•	Supabase Python SDK
	•	Python dotenv package

Installation

	1.	Clone the repository.
	2.	Install the required dependencies:

pip install -r requirements.txt


	3.	Set up your environment variables by creating a .env file in the project root:

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key



Usage

To process genres from a specified table, use the following command:

python genre_conversion.py <table_name>

Replace <table_name> with the actual name of the table containing genre data.

Example

python genre_conversion.py books

This will fetch genres from the books table, convert camelCase genre names to Title Case, and update the table with the modified data.

Functions Overview

	•	create_supabase_client(url, key): Creates a Supabase client instance.
	•	fetch_genre_data(supabase_client, table_name): Fetches genre data from the specified table.
	•	convert_genre_names(genre_list): Converts camelCase genre names to Title Case.
	•	update_genre_data(supabase_client, table_name, row_id, converted_genres): Updates the table with the converted genre names.
	•	process_genres(table_name): Orchestrates the fetch, convert, and update steps.
	•	main(): Handles command-line arguments to trigger genre processing.

License

This project is licensed under the MIT License.

Feel free to contribute by submitting issues or pull requests!
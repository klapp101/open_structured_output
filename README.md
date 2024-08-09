
# Query Generator App

This is a Streamlit application that generates SQL queries based on natural language input using OpenAI's GPT-4o model. The app allows users to enter a query in plain English, and it translates that query into a Snowflake SQL statement.

## Features

- **Natural Language Querying**: Users can input a question or request in plain English, and the app will generate the corresponding SQL query.
- **Support for Complex SQL Operations**: The app supports conditions, aggregations, ordering, and ranking in the generated SQL.
- **Interactive Interface**: The app provides an easy-to-use interface with real-time query generation.

## Installation

To run this application locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install the required packages**:
   Make sure you have Python 3.7 or later. Install the dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory of your project and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

4. **Run the app**:
   Start the Streamlit app by running:
   ```bash
   streamlit run app.py
   ```

## How It Works

1. **User Input**: The user inputs a query in natural language through the text area provided in the Streamlit interface.

2. **Query Parsing**: The input is passed to OpenAI's GPT-4o model, which parses the request and determines the appropriate SQL components, such as table names, columns, conditions, and operations.

3. **SQL Query Generation**: Based on the parsed components, the app generates a SQL query formatted for Snowflake.

4. **Output**: The generated SQL query is displayed in the app interface, where users can copy it for use in their database.

## Example Queries

Here are some example queries you can input into the app:

- **Rank Top Users**:
  "Can you rank the top users by the number of questions they have answered in July 2024?"

- **Sum of Values**:
  "What is the total number of questions asked in June 2024?"

- **Filtered Data**:
  "Show all entries where the feedback was negative and the date is after August 1, 2024."

## Dependencies

- **Streamlit**: A web framework for building interactive data applications.
- **OpenAI**: For accessing the GPT-4o model to interpret and generate SQL queries.
- **Pydantic**: For data validation and settings management.
- **Python Dotenv**: For loading environment variables from a `.env` file.

## Contributing

If you would like to contribute to this project, feel free to open a pull request or report issues on the GitHub repository.

## About

This app was developed as a tool to help users generate SQL queries effortlessly using natural language. It leverages the power of OpenAI's GPT-4o model and provides a simple, yet powerful, interface for generating complex SQL queries without needing to write SQL manually.

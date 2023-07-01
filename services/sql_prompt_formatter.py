from typing import NewType

"""
Added an optional refined str type; a SQLPrompt

It represents a SQLPrompt meant to be passed to openai, 

to suggest the SQL query to be executed against the postgres server to explore what the user wants to explore
"""
SQLPrompt = NewType("SQLPrompt", str)

class SQLPromptFormatter:
    """
    Responsible for formatting a given instruction from an operations professional
    into a prompt to be sent to openai, to request for an appropriate SQL query to execute
    """
    @staticmethod
    def format(instructions: str) -> SQLPrompt:
        return SQLPrompt(f"""
Database: customer_usage_data
Tables:
- user_data: Contains user information.
    * user_id: Unique identifier for each user. Type: Serial (INTEGER)
    * name: User's name. Type: VARCHAR(255)
    * email: User's email address. Type: VARCHAR(255)
    * account_creation_date: Date the user's account was created. Type: DATE
    CREATE TABLE user_data (
        user_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        account_creation_date DATE NOT NULL
    );
- usage_data: Contains usage information.
    * usage_id: Unique identifier for each usage event. Type: Serial (INTEGER)
    * user_id: Foreign key to the user_data table. Type: INTEGER
    * usage_date: Date the usage event occurred. Type: DATE
    * usage_time: Time the usage event occurred. Type: TIME
    * usage_duration: Duration of the usage event. Type: INTERVAL
    CREATE TABLE usage_data (
        usage_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES user_data(user_id),
        usage_date DATE NOT NULL,
        usage_time TIME NOT NULL,
        usage_duration INTERVAL NOT NULL
    );
- payment_data: Contains payment information.
    * payment_id: Unique identifier for each payment event. Type: Serial (INTEGER)
    * user_id: Foreign key to the user_data table. Type: INTEGER
    * payment_amount: Amount of the payment. Type: DECIMAL(10,2)
    * payment_date: Date the payment was made. Type: DATE
    * payment_method: Payment method used. Type: VARCHAR(255)
    CREATE TABLE payment_data (
        payment_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES user_data(user_id),
        payment_amount DECIMAL(10,2) NOT NULL,
        payment_date DATE NOT NULL,
        payment_method VARCHAR(255) NOT NULL
    );

Instruction from user: "{instructions}"

Please provide a SQL query that will return the total usage duration for user John in the last 30 days, using the available tables and columns in the database.

Please don't explain it, just provide the SQL query. I will be parsing the output from you to be executed on psql

Also, please edit the query such that it defaults to an appropriate value, if there are no results.
""")
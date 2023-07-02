from typing import Any

import streamlit as st

from services.openai_completor import OPENAI_COMPLETOR
from services.postgres_query_executor import POSTGRESQL_QUERY_EXECUTOR
from services.result_prompt_formatter import ResultPrompt, ResultPromptFormatter
from services.sql_prompt_formatter import SQLPrompt, SQLPromptFormatter

st.header("Auto PostgreSQL")

st.text("""
Hello! This is a MVP for enabling operation professions to independently conduct data analysis on customer-usage data in a sample database.
""")

if st.checkbox("Debugging - Show Database"):
    st.text(
        """    
        For debugging purposes, here is the schema of the database:
    
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
    
        Sample Data
    
        ```
        customer_usage_data=# SELECT * FROM user_data;
         user_id | name |      email       | account_creation_date 
        ---------+------+------------------+-----------------------
               1 | John | john@example.com | 2020-01-01
               2 | Jane | jane@example.com | 2020-02-01
               3 | Bob  | bob@example.com  | 2020-03-01
        ```
    
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
    
        Sample Data
    
        ```
        customer_usage_data=# SELECT * FROM usage_data;
         usage_id | user_id | usage_date | usage_time | usage_duration 
        ----------+---------+------------+------------+----------------
                1 |       1 | 2020-01-01 | 08:00:00   | 01:00:00
                2 |       1 | 2020-01-02 | 08:00:00   | 02:00:00
                3 |       2 | 2020-02-01 | 08:00:00   | 03:00:00
        ```
    
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
    
        Sample Data
    
        ```
        customer_usage_data=# SELECT * FROM payment_data;
         payment_id | user_id | payment_amount | payment_date | payment_method 
        ------------+---------+----------------+--------------+----------------
                  1 |       1 |         100.00 | 2020-01-01   | Credit Card
                  2 |       2 |         200.00 | 2020-02-01   | PayPal
                  3 |       3 |         300.00 | 2020-03-01   | Bank Transfer
        ```
        """
    )

st.text("""
Please include instructions below on what you would like to explore.
""")

instructions: str = st.text_area(label="Instructions")

if st.button("Get Results"):
    # make a request to openai
    sql_prompt: SQLPrompt = SQLPromptFormatter.format(instructions)
    sql_query: str = OPENAI_COMPLETOR.complete(sql_prompt)
    sql_results: list[tuple[Any]] = POSTGRESQL_QUERY_EXECUTOR.execute(sql_query)
    formatted_sql_results: str = str(sql_results)
    result_prompt: ResultPrompt = ResultPromptFormatter.format(instructions, formatted_sql_results)
    interpreted_results: str = OPENAI_COMPLETOR.complete(result_prompt)
    st.text(interpreted_results)
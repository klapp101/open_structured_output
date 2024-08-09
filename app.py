import streamlit as st
import openai
from openai import OpenAI
from enum import Enum
from typing import Union
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

class Table(str, Enum):
    support_engineer_metrics = "ASSISTANT_METRICS"

class Column(str, Enum):
    id = "USER_ID"
    assistant_name = "ASSISTANT_NAME"
    assistant_id = "ASSISTANT_ID"
    question = "QUESTION"
    answer = "ANSWER"
    feedback = "FEEDBACK"
    date = "DATE"


class Operator(str, Enum):
    eq = "="
    gt = ">"
    lt = "<"
    le = "<="
    ge = ">="
    ne = "!="


class OrderBy(str, Enum):
    asc = "asc"
    desc = "desc"

class Aggregate(str, Enum):
    count = "count"
    sum = "sum"
    avg = "avg"
    min = "min"
    max = "max"

class RankType(str, Enum):
    rank = "rank"
    dense_rank = "dense_rank"

class DynamicValue(BaseModel):
    column_name: str


class Condition(BaseModel):
    column: str
    operator: Operator
    value: Union[str, int, DynamicValue]


class Query(BaseModel):
    table_name: Table
    columns: list[Column]
    conditions: list[Condition]
    aggregate: Aggregate
    rank_type: RankType
    order_by: OrderBy

client = OpenAI()

def generate_query(user_input):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. The current date is August 9, 2024. You help users query for the data they are looking for by calling the query function.",
            },
            {
                "role": "user",
                "content": user_input,
            },
        ],
        tools=[
            openai.pydantic_function_tool(Query),
        ],
    )
    
    # Extract query details
    parsed_args = completion.choices[0].message.tool_calls[0].function.parsed_arguments
    table_name = parsed_args.table_name.value
    column_names = [column.value for column in parsed_args.columns]
    operators_and_conditions = [[condition.column, condition.operator.value, condition.value] for condition in parsed_args.conditions]
    aggregate_function = parsed_args.aggregate.value
    order_by = parsed_args.order_by.value
    rank_type = parsed_args.rank_type.value
    
    # Generate SQL query
    query_gen_prompt = f"""You are tasked with generating a Snowflake SQL query based on the provided information. Follow these steps to create the query:

    1. The table name you will be querying is:
    <table_name>
    {table_name}
    </table_name>

    2. You will be selecting the following columns:
    <columns>
    {column_names}
    </columns>

    3. The query should include the following conditions:
    <conditions>
    {operators_and_conditions}
    </conditions>

    4. The query should use the following aggregate function (if applicable):
    <aggregate_function>
    {aggregate_function}
    </aggregate_function>

    5. The query should be ordered by the following column:
    <order_by>
    {order_by}
    </order_by>

    6. The query should use the following rank type (if applicable):
    <rank_type>
    {rank_type}
    </rank_type>

    7. Format your SQL query as follows:
    - Start with the SELECT statement, listing all the columns.
    - Follow with the FROM clause, specifying the table name.
    - If there are conditions, include a WHERE clause with the conditions.
    - If the user is asking about an aggregate function, include it in the SELECT statement.
    - Use proper SQL syntax, including semicolons at the end of the query.

    8. Here's an example of how your output should be formatted:

    <example without aggregate function>
    SELECT column1, column2, column3
    FROM table_name
    WHERE column1 = 'value1'
    AND column2 > 10;
    </example without aggregate function>

    <example with aggregate function>
    SELECT column1, SUM(column2)
    FROM table_name
    WHERE column2 = 'value2'
    GROUP BY column1;
    </example with aggregate function>

    <example with rank type>
    SELECT 
        SLACK_ID,
        COUNT(*) AS QUESTION_COUNT,
        DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS RANK
    FROM 
        ASSISTANT_METRICS
    WHERE 
        DATE >= '2024-07-01' AND DATE <= '2024-07-31'
    GROUP BY 
        SLACK_ID
    ORDER BY 
        QUESTION_COUNT DESC;
    </example with rank type>

    9. Now, generate the Snowflake SQL query based on the provided information. Write your query inside <query> tags.

    Remember to use the exact table name, columns, and conditions provided. Do not add any columns, conditions, or tables that were not specified in the input."""
    
    sql_completion = client.chat.completions.create(
        model='gpt-4o-2024-08-06',
        messages=[
            {"role": "system", "content": query_gen_prompt}
        ]
    )
    
    return sql_completion.choices[0].message.content

st.title('Query Generator App')
user_query = st.text_area("Enter your query:", "Can you rank the top users by the number of questions they have answered in July 2024?")

if st.button('Generate Query'):
    if user_query:
        with st.spinner('Generating query...'):
            generated_sql = generate_query(user_query)
            st.subheader('Generated SQL Query:')
            st.code(generated_sql, language='sql')
    else:
        st.warning('Please enter a query.')

st.sidebar.header('About')
st.sidebar.info('This app generates SQL queries based on natural language input using OpenAI GPT-4o.')

import snowflake.connector
import pandas as pd
import streamlit as st

connection_params = {
    'user': 'julia',
    'password': 'Julia0801.',
    'account': 'vszwjrl-aws',
    'warehouse': 'COMPUTE_WH',
    'database': 'PROD_DB',
    'schema': 'MAGENTO'
}

conn = snowflake.connector.connect(
    user=connection_params['user'],
    password=connection_params['password'],
    account=connection_params['account'],
    warehouse=connection_params['warehouse'],
    database=connection_params['database'],
    schema=connection_params['schema']
)

@st.cache_data
def generate_master_table(conn=conn):
    q1 = """
    with first_orders as (
        select 
            customer_id,
            min(date(created_at)) as first_order
        from
            orders
        where
            ba_site = 'UK'
        group by customer_id
        ),
    customers as (
        select *
        from 
            first_orders
        )
    SELECT
        DATE(o.created_at) AS order_date,
        o.customer_id,
        DATE(c.first_order) AS first_order
    FROM
        orders o
    JOIN
        customers c
    ON
        o.customer_id = c.customer_id
    WHERE
        o.ba_site = 'UK';
    """

    df = pd.read_sql(q1, conn)
    df['ORDER_DATE'] = pd.to_datetime(df['ORDER_DATE'])
    df['FIRST_ORDER'] = pd.to_datetime(df['FIRST_ORDER'])
    df['FIRST_ORDER_WEEK'] = df['FIRST_ORDER'].dt.to_period('W')
    df['ORDER_WEEK'] = df['ORDER_DATE'].dt.to_period('W')

    df['FIRST_ORDER_MONTH'] = df['FIRST_ORDER'].dt.to_period('M')
    df['ORDER_MONTH'] = df['ORDER_DATE'].dt.to_period('M')

    df['FIRST_ORDER_QUARTER'] = df['FIRST_ORDER'].dt.to_period("Q")
    df['ORDER_QUARTER'] = df['ORDER_DATE'].dt.to_period("Q")

    return df

def get_matrix(df, cohort_size):
  
  cohort_size = cohort_size.replace("ly", "")

  if cohort_size == "Month":
    col_cs = "FIRST_ORDER_MONTH"
    col_tp = "ORDER_MONTH"
  elif cohort_size == "Week":
    col_cs = "FIRST_ORDER_WEEK"
    col_tp = "ORDER_WEEK"
  elif cohort_size == "Quarter":
    col_cs = "FIRST_ORDER_QUARTER"
    col_tp = "ORDER_QUARTER"
    
  cohort_groups = df[['CUSTOMER_ID', col_cs, col_tp]].groupby([col_cs, col_tp]).agg(n_customers=('CUSTOMER_ID', 'nunique')).reset_index()

  cohort_groups['ORDER_SEQ'] = cohort_groups[col_tp].astype(int)-cohort_groups[col_cs].astype(int)

  return cohort_groups
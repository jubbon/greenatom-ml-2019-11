#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from clickhouse_driver import Client


client = Client(
    host=os.getenv("CLICKHOUSE_HOST", "localhost"),
    port=int(os.getenv("CLICKHOUSE_PORT", 9000))
)


def init_db(database_name, table_name):
    '''
    '''
    print(f"Initialize database '{database_name}'", flush=True)
    client.execute(
        f'CREATE DATABASE IF NOT EXISTS {database_name};'
    )
    print(f"Creating table '{table_name}'", flush=True)
    client.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {database_name}.{table_name} (
            event_date  Date,
            event_time  DateTime,
            user_uid    String
        ) engine=MergeTree(event_time, (user_uid), 8192);
        '''
    )

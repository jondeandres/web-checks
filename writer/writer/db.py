import psycopg2
import typing


def connect(database: str,
            user: str,
            password: str,
            host: str,
            port: str,
            sslmode: typing.Optional[str] = None,
            sslrootcert: typing.Optional[str] = None,
            ) -> psycopg2.extensions.connection:
    return psycopg2.connect(database=database,
                            user=user,
                            password=password,
                            host=host,
                            port=port,
                            sslmode=sslmode,
                            sslrootcert=sslrootcert)


def prepare_db(conn: psycopg2.extensions.connection) -> None:
    """
    Creates needed tables in DB
    """
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS http_check_result (
                url text,
                timestamp timestamp default current_timestamp,
                response_time int,
                status_code integer NULL,
                re_match bool NULL,
                error text NULL
            );
        """)


def drop_table(conn: psycopg2.extensions.connection) -> None:
    """
    Drops tables in DB

    This is a convenient function to use in functional tests
    """
    with conn.cursor() as cur:
        cur.execute('drop table http_check_result')

import psycopg2


def creat_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE IF EXISTS Phone;
            DROP TABLE IF EXISTS Client;
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Client(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(40),
                last_name VARCHAR(40),
                email VARCHAR(40) UNIQUE
            );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Phone(
        id SERIAL PRIMARY KEY,
        phone_number VARCHAR(12),
        client_id INTEGER NOT NULL REFERENCES Client(id)
        );
        """)
        return conn.commit()


def add_client(conn, first_name, last_name, email, phone_number=None):
    with conn.cursor() as cur:
        cur.execute("""
           INSERT INTO Client(first_name, last_name, email)
           VALUES(%s, %s, %s)
           RETURNING id, first_name, last_name, email;
         """, (first_name, last_name, email))
        return cur.fetchone()


def add_phone(conn, client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute("""
           INSERT INTO Phone(client_id, phone_number)
           VALUES(%s, %s)
           RETURNING id, client_id, phone_number;
         """, (client_id, phone_number))
        return cur.fetchone()


def change_client(conn, id, first_name=None, last_name=None, email=None, phone_number=None):
    with conn.cursor() as cur:
        cur.execute("""
              UPDATE Client SET first_name=%s, last_name=%s, email=%s WHERE id=%s
              RETURNING id, first_name, last_name, email;
              """, (first_name, last_name, email, id))
        return cur.fetchall()


def delete_phone(conn, client_id, phone_number=None):
    with conn.cursor() as cur:
        cur.execute("""
                DELETE FROM Phone WHERE id=%s
                ;
                """, (client_id,))
        cur.execute("""
                SELECT * FROM Phone
                """, (phone_number, client_id,))
        return cur.fetchall()


def delete_client(conn, id, first_name=None, last_name=None, email=None, phone_number=None):
    with conn.cursor() as cur:
        cur.execute("""
                DELETE FROM Client WHERE id=%s;
                """, (id,))
        cur.execute("""
                        SELECT * FROM Client
                        """, (first_name, last_name, email, id))
        return cur.fetchall()


def find_client(conn, first_name=None, last_name=None, email=None, phone_number=None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.first_name, c.last_name, c.email, p.phone_number FROM Client AS c
            LEFT JOIN Phone AS p ON c.id = p.client_id
            WHERE c.first_name=%s OR c.last_name=%s OR c.email=%s OR p.phone_number=%s;
            """, (first_name, last_name, email, phone_number))
        return cur.fetchall()


with psycopg2.connect(database='netologydb', user='postgres', password='') as conn:
    print(creat_db(conn))
    print(add_client(conn, 'dima', 'nikiforov', 'mkvmek@ec'))
    print(add_phone(conn, 1, '34534534543'))
    print(change_client(conn, 1, 'mimi', 'nik', 'skdmv@km', '2834'))
    # delete_phone(conn, 1, '2834')
    # delete_client(conn, 1)
    print(find_client(conn, '', 'nik'))
conn.close()

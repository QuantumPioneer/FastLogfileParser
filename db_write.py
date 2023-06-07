import sqlite3
import sys
import argparse
import ast

from tqdm import tqdm

FILE_DESCRIPTORS = (
    "rxn_id",
    "converged",
    "gibbs",
    "e0_zpe",
    "e0",
    "zpe",
    "cpu_time",
    "wall_time",
    "num_atoms",
    "frequencies",
    "std_forces",
    "std_xyz",
    "xyz",
    "steps",
)


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Exception as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_and_commit(conn, sql, values=None):
    cursor = conn.cursor()
    if values is None:
        cursor.execute(
            sql,
        )
    else:
        cursor.execute(
            sql,
            values,
        )
    conn.commit()


def execute_read_query(connection, query, values=None):
    cursor = connection.cursor()
    result = None
    if values is None:
        cursor.execute(query)
    else:
        cursor.execute(query, values)
    result = cursor.fetchall()
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Access a SQLite DB.")
    parser.add_argument("-d", "--db-file")
    parser.add_argument("-s", "--semi-dir")
    parser.add_argument("-t", "--dft-dir")
    parser.add_argument("--screen-file-fstring")
    parser.add_argument("--dft-file-fstring")
    parser.add_argument("--new-table-name")
    parser.add_argument("-a", "--already-init", action="store_true")
    args = parser.parse_args()

    conn = create_connection(args.db_file)

    if not args.already_init:
        execute_and_commit(
            conn,
            f"""CREATE TABLE IF NOT EXISTS {args.new_table_name} (
                rxn_id INTEGER PRIMARY KEY,
                converged TEXT,
                gibbs TEXT,
                e0_zpe TEXT,
                e0 TEXT,
                zpe TEXT,
                cpu_time TEXT,
                wall_time TEXT,
                num_atoms TEXT,
                frequencies TEXT,
                std_forces TEXT,
                std_xyz TEXT,
                xyz TEXT,
                steps TEXT
                );
                """,
        )
        from preprocess_logs import preprocess_logs

        data = preprocess_logs(
            args.semi_dir,
            args.dft_dir,
            args.screen_file_fstring,
            args.dft_file_fstring,
        )
        for rxn_id, row in tqdm(data.items(), "Writing to DB..."):
            execute_and_commit(
                conn,
                f"""INSERT INTO {args.new_table_name} (
                    rxn_id,
                    converged,
                    gibbs,
                    e0_zpe,
                    e0,
                    zpe,
                    cpu_time,
                    wall_time,
                    num_atoms,
                    frequencies,
                    std_forces,
                    std_xyz,
                    xyz,
                    steps)
                    VALUES (
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?
                    );
                """,
                (
                    rxn_id,
                    str(row["converged"]),
                    str(row["gibbs"]),
                    str(row["e0_zpe"]),
                    str(row["e0"]),
                    str(row["zpe"]),
                    str(row["cpu_time"]),
                    str(row["wall_time"]),
                    str(row["num_atoms"]),
                    str(row["frequencies"]),
                    str(row["std_forces"]),
                    str(row["std_xyz"]),
                    str(row["xyz"]),
                    str(row["steps"]),
                ),
            )

    # get the data back and post-process it
    # use ast.literal_eval to get the list dtype back
    # out = execute_read_query(
    #     conn,
    #     f"""    SELECT * FROM {args.new_table_name} WHERE rxn_id=?;""",
    #     (0,),
    # )
    # out_dict = {}
    # for row in tqdm(out, "Post-processing data..."):
    #     rxn_id = row[0]
    #     out_dict[rxn_id] = {}
    #     for i, name in zip(row[1:], FILE_DESCRIPTORS[1:]):
    #         if type(i) != int:
    #             out_dict[rxn_id][name] = ast.literal_eval(i)

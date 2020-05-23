# t0m
_Ssshh_

---

## About

Another fun project - very similar to [d4v1d](https://github.com/MattMoony/d4v1d). Could be quite useful for recon, but even if not, it was just nice to experiment with.

## Setup

Assuming that you have Python 3.* already installed on your system, the first thing you should do is run the following in the project's base directory:

```bash
$ python -m pip install -r requirements.txt
```

Afterwards, create a new sqlite db with `create_tables.sql` (keep in mind that you need to specify the db's location in `lib.db.DB_PATH`).

```bash
$ sqlite3 tmp/info.db < create_tables.sql
```

## Usage

Enter the pash terminal by executing the main script ...

```bash
$ python t0m.py
```

... and whenever you feel lost, feel free to use the `help` command or the `-h` / `--help` parameter.

---

... MattMoony (May, 2020)
# Make PyMySQL (a pure-Python library) act as a drop-in replacement for
# mysqlclient. This makes the project much easier to run on systems like
# Windows/XAMPP, since it avoids needing C++ build tools.
import pymysql

pymysql.install_as_MySQLdb()

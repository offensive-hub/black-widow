# SQL injection

SQL injection is a way to execute a not expected and malicious SQL
query on a database.

Usually this method is used by exploiting a vulnerable web application
page.

To understand how this method works, you should have notion about the
following things:
 * Website
 * Relational database
 * SQL query

## Website

A website is a web application that provides contents and, sometime,
services.
For example **[https://www.amazon.com/](https://www.amazon.com/)**
is a web application which provides both, because you can look at
products (content) and buy them (service).

Typically, a web application which provides services or many complex
contents, interfaces with a database, where stores the data, by
launching **queries** on that.

## Database

A database is a storage of structured data, saved on a computer.

Now there are **3 categories** of database:
 * Relational
 * Business intelligence
 * NoSQL

To explain the **SQL injection**, I'll focus only on **relational**
databases.

#### Relational database list:
 * MySQL
 * Oracle
 * PostgreSQL
 * Microsoft SQL Server
 * Microsoft Access
 * IBM DB2
 * SQLite
 * Firebird
 * Sybase
 * SAP MaxDB
 * Informix
 * MariaDB
 * Percona
 * MemSQL
 * TiDB
 * CockroachDB
 * HSQLDB
 * H2
 * MonetDB
 * Apache Derby
 * Vertica
 * Mckoi
 * Presto
 * Altibase
 * ...


## Database Query

A database query is a way to interact with a database.
Through that, you can get, edit and delete a database records.

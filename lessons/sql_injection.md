# SQL injection

SQL injection is a way to execute a not expected and malicious SQL
query on a database.

Usually this method is used by exploiting a vulnerable web application
page.

To understand how this method works, you should have notion about the
following things:
 * [Website](#website)
 * [Relational database](#database)
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

An SQL database is primarily a set of tables.
Each table contains records, which can referer to records from other
tables. This is the reason of the name "relation database".
Usually, every relational database table has the column "**id**"
(a diminuitive of **identifier**), because every record needs to have
an unique identifier, to identify easily and fastly that.

For example, imagine to have have the database "**shop**" inside your
computer.
It has the following tables:
 * **product_categories**
 * **products**
 * **customers**
 * **orders**
 * **receipts**

Every record of the table **receipts** will referer from a record
of the table **orders**, because every receipt is linked to an order.
So the table **receipts**, will contains the column **order_id**,
which contains the **id** of the order.

An order referer to a customer, so the table **orders** will has the 
column **customer_id**.

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
Through that, you can get, edit and delete the database records.

The relational databases use the SQL (Structured Query Language).

How you can get the receipt of order with **id** 130 ?
```sql
SELECT * FROM TABLE receipts
WHERE order_id = 130;
```

With `SELECT *` we are selecting all columns of the found record.
But you can specify the columns that you want:
```sql
SELECT
  id,
  amount
FROM TABLE receipts
WHERE order_id = 130;
```

There are many complex queries that you can launch on a relational
database, but for now, we don't need to know everything about those.

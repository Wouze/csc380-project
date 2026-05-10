# Library Management System (Java Swing + MySQL)

Original CSC 380 coursework app: tabbed Swing client for authors, books, members, library cards, and book–author links.

## Layout

- **`src/`** — Java sources (`DBMS_GUI.java` is the entry point).
- **`bin/`** — Compiled `.class` files (rebuild or delete as you prefer).
- **JARs** — MySQL connector, JCalendar, MigLayout, JGoodies, JUnit (add to classpath when compiling/running).

## Database

`DBMS_GUI.java` connects to MySQL (adjust URL, user, and password in code for your machine). Create the database and tables your course materials specify before running the GUI.

## Compile and run (example)

From this folder, with all JARs on the classpath:

```bash
javac -encoding UTF-8 -cp ".:mysql-connector-j-9.3.0.jar:jcalendar-1.4.jar:miglayout15-swing.jar:jgoodies-common-1.2.0.jar:jgoodies-looks-2.4.1.jar" -d bin src/*.java
java -cp "bin:mysql-connector-j-9.3.0.jar:jcalendar-1.4.jar:miglayout15-swing.jar:jgoodies-common-1.2.0.jar:jgoodies-looks-2.4.1.jar" DBMS_GUI
```

On **Windows**, replace `:` with `;` in `-cp` paths and use `\` in paths if needed.

The hotel schema and Python port live in **`python-hotel-project/`** at the repo root.

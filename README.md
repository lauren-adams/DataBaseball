# Wii Baseball - Group Project

## Project Files
 - `python-code/`: contains the Flask project
 - `add_wii_baseball.sql`: creates the `wii_baseball` database (schema)
 - `add_user_support.sql`: creates the `user` table in the `wii_baseball` database
 - `.editorconfig`: ensures whitespace consistency for developers

## Admin Account
```
username: admin
password: nintendo
```

## Running the webapp
1. Enter the virtual environment
```bash
$ cd python-code
$ . ./venv/Scripts/activate
```

2. Install the dependencies
```bash
$ pip install -r requirements.txt
```

3. Configure your MYSQL environment

Add a file under `python-code/` called `config.py` with the following contents, replacing `'<PASSWORD>'` with your password:
```py
mysql = {'location':'localhost','user':'root','password':'<PASSWORD>','database':'baseball'}
```

4. Start the MYSQL server

Just launch the usual `SQL.bat` from class

5. Add the `wii_baseball` database from the MYSQL console

```batch
\. add_wii_baseball.sql
```

6. Add user support to the database

```batch
\. add_user_support.sql
```

7. Start the Flask server
```bash
$ flask --app main run
```
 
8. Navigate to http://localhost:5000 with your browser

## TODO

Make a script to automate the setup?

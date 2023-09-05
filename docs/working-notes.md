# working notes

collection of notes for set up and working with the project

## local dev work

```bash
source venv/bin/activate
```

## db

run the docker-compose.yaml file to start the db

```bash
docker-compose up -d
```

## db migrations

```bash
flask db init
flask db migrate
flask db upgrade
```

## db seed

```bash
flask seed run
```

## run the app

```bash
python app.py
```

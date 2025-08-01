# ODPRTI RAČUNI OBČINE

## Aplikacija za občine, ki želijo prikazovati proračune in primerjave skozi leta

Lite verzija: https://github.com/danesjenovdan/odprti-racuni-obcine-lite/

---

### How to run?

```
docker-compose up
```

### SETUP

This will migrate and seed the database, collect static files, and createa a superuser with the username `admin`, email `admin@example.dev`, and password `changeme`.

```
docker-compose run odprti-racuni-obcine ./setup.sh
```

You can then start the app with `docker-compose up` if you haven't already.

Visit `http://localhost:8000/admin/`, log in with `admin` and `changeme` and edit the municipality in order to be able to see something rendered at one of the urls below.

### URLS

### Adding new Konto
./manage.py parse_revenue_definition_from_pdf https://www.uradni-list.si/files/RS_-2024-081-02384-OB~P001-0000.PDF

#### Admin
http://localhost:8000/admin/

#### Front end
http://localhost:8000/pregled/1/1/

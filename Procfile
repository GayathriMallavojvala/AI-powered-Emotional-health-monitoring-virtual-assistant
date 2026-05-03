web: python manage.py migrate --run-syncdb && python manage.py collectstatic --noinput && gunicorn Mental_Health_Support.wsgi --log-file - --bind 0.0.0.0:8080

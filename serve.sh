if [ "$ENV" == "production" ]
then
  echo "Starting server"
  # FLASK_APP="server/server.py" FLASK_RUN_PORT=80 FLASK_ENV=development flask run --with-threads
  #  gunicorn --threads 10 --workers 1 --timeout=1000000 server:app
  uwsgi --workers 1 --threads 10 --wsgi-file server/server.py --callable app --http :80
else
  FLASK_APP="server/server.py" FLASK_ENV=development flask run --with-threads
fi
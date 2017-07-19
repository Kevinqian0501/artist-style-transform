FROM venv:latest

# Copy our service code
ADD ./transform-service /opt/transform-service

# start supervisor to run our wsgi server, nginx, supervisor-stdout
CMD supervisord -c /etc/supervisor.conf -n

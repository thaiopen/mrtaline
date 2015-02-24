# Makefile for building and deploying
#

UWSGI=/etc/init.d/uwsgi
NGINX=/etc/init.d/nginx

deploy: dependencies clean minified_static_files

restart: $(UWSGI) $(NGINX)
	$(UWSGI) restart
	$(NGINX) restart

stop: $(UWSGI) $(NGINX)
	$(NGINX) stop
	$(UWSGI) stop

dependencies: dependencies.pip
	pip install -r dependencies.pip # Or requirements.txt

resources:
	python resources_build.py # Minifies static files.

minified_static_files: resources
	python manage.py collectstatic # Collect into static_files/

clean:
	@-rm -rf static_files/
	@-find . -name '__pycache__' -exec /bin/rm -rf {} ;
	@echo 'Successfully Cleaned!'

.PHONY: clean resources dependencies restart stop deploy

frontend_deps:
	-bower install
	-mkdir -p static/js
	-mkdir -p static/css
	-mkdir -p static/fonts
	cp "frontend/bower/jquery/dist/jquery.min.js" static/js
	cp "frontend/bower/jquery/dist/jquery.min.map" static/js
	cp "frontend/bower/bootstrap/dist/js/bootstrap.min.js" static/js
	cp "frontend/bower/bootstrap/dist/css/bootstrap.min.css" static/css
	cp "frontend/bower/bootstrap/dist/css/bootstrap-theme.min.css" static/css
	cp "frontend/bower/font-awesome/css/font-awesome.min.css" static/css
	cp "frontend/bower/bootstrap/dist/fonts/glyphicons-halflings-regular.eot" static/fonts
	cp "frontend/bower/bootstrap/dist/fonts/glyphicons-halflings-regular.svg" static/fonts
	cp "frontend/bower/bootstrap/dist/fonts/glyphicons-halflings-regular.ttf" static/fonts
	cp "frontend/bower/bootstrap/dist/fonts/glyphicons-halflings-regular.woff" static/fonts
	cp "frontend/bower/bootstrap/dist/fonts/glyphicons-halflings-regular.woff2" static/fonts
	cp "frontend/bower/font-awesome/fonts/fontawesome-webfont.eot" static/fonts
	cp "frontend/bower/font-awesome/fonts/fontawesome-webfont.svg" static/fonts
	cp "frontend/bower/font-awesome/fonts/fontawesome-webfont.ttf" static/fonts
	cp "frontend/bower/font-awesome/fonts/fontawesome-webfont.woff" static/fonts
	cp "frontend/bower/font-awesome/fonts/fontawesome-webfont.woff2" static/fonts
	rm -rf frontend

test:
	-rm -rf htmlcov
	pytest -s --cov-report term-missing --cov=garagesale --cov-report html --cov=apps

travis_test_pipenv:
	pipenv lock
	pipenv install --dev
	pipenv run py.test

createdb:
	-dropdb garagesale_dev
	-dropdb garagesale_test
	-dropdb garagesale_prod
	createdb -O postgres garagesale_dev
	createdb -O postgres garagesale_test
	createdb -O postgres garagesale_prod

test1:
	@echo token=$(TOKEN)
	./vaccine.py http://localhost:8080/vulnerabilities/sqli/index.php

test2:
	./vaccine.py http://altoromutual.com/login.jsp -x post

test3:
	./vaccine.py http://localhost:8181 -x post

run:
	-docker run -it -d -p 8080:80 vulnerables/web-dvwa
	-docker run -d -p 8181:80 gitlab.cylab.be:8081/cylab/play/sqlite-injection

fclean:
	docker system prune -a -f

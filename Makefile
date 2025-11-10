run:
	docker run -it -d --env-file .env --restart=unless-stopped --name bot kruti_koles_bot_aio
stop:
	docker stop easy_refer
attach:
	docker attach easy_refer
dell:
	docker rm easy_refer
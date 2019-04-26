IMAGE_NAME = flaskapp
S2I_IMAGE = flaskprod
FLASK_ID = flask-instance

run:
	docker run -d --name ${FLASK_ID} -p 9000:9000 ${S2I_IMAGE}


.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

s2i-build:
	s2i build app/ ${IMAGE_NAME} ${S2I_IMAGE}

buildall: build s2i-build


.PHONY: test
test:
	docker build -t $(IMAGE_NAME)-candidate .
	IMAGE_NAME=$(IMAGE_NAME)-candidate test/run

clean-s2i:
	docker stop ${FLASK_ID}
	docker rmi ${S2I_IMAGE}

clean:
	docker stop ${FLASK_ID}
	docker rm ${FLASK_ID}
	docker rmi -f ${S2I_IMAGE} ${IMAGE_NAME}



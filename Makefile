# Docker Hub account name
HUB_NAMESPACE = "jojees"

MAJOR?=0
MINOR?=1
VERSION=$(MAJOR).$(MINOR)
CUR_DIR = $(shell echo "${PWD}")
TARGET_DIR?=.
DOCKERFILE?=Dockerfile

#################################
# Default targets
#################################
.PHONY: default
default:
	@echo "Hello World!"

#################################
# Docker targets
#################################
.PHONY: clean-image image image-test docker docker-push
clean-image:
	@echo "+ $@"
	@docker rmi ${HUB_NAMESPACE}/${TARGET_DIR}:${DOCKERFILE}  || true

image-build: clean-image
	@echo "+ $@"
	@docker build -t ${HUB_NAMESPACE}/${TARGET_DIR}:${DOCKERFILE} -f ./${TARGET_DIR}/${DOCKERFILE} ${TARGET_DIR}
	@docker images --format '{{.Repository}}:{{.Tag}}\t\t Built: {{.CreatedSince}}\t\tSize: {{.Size}}' | grep ${TARGET_DIR}:${DOCKERFILE}

docker-push:
	@echo "+ $@"
	@chmod +x docker/builder.sh
	@./docker/builder.sh -pd
	@chmod -x docker/builder.sh

docker:
	@chmod +x $@/builder.sh
	@./$@/builder.sh
	@chmod -x $@/builder.sh

hub-push:
	@echo "+ $@"
	@docker push ${HUB_NAMESPACE}/${TARGET_DIR}:${DOCKERFILE}  || true

#################################
# Utilities
#################################

.PHONY: version-check
version-check:
	@echo "+ $@"
	if [ -z "${VERSION}" ]; then \
		echo "VERSION is not set" ; \
		false ; \
	else \
		echo "VERSION is ${VERSION}"; \
	fi

#@echo ${CUR_DIR}
#@docker tag ${HUB_NAMESPACE}/${TARGET_DIR}:${VERSION} ${HUB_NAMESPACE}/${TARGET_DIR}:latest

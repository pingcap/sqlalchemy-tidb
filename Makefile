# Copyright 2021 PingCAP, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# See the License for the specific language governing permissions and
# limitations under the License.
ENV=./.venv

.PHONY: all
all: test lint

.PHONY: bootstrap
bootstrap:
	@mkdir -p ${ENV}
	virtualenv ${ENV}
	pip install -r dev-requirements.txt
	pip install -r test-requirements.txt

.PHONY: update-requirements
update-requirements:
	tox -e pip-compile

.PHONY: test
test:
	tox -e py39

.PHONY: lint
lint:
	tox -e lint

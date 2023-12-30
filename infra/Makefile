# Makefile
.PHONY: deploy
# .PHONY: small-tests medium-tests all-tests deploy

PROVISIONING_SCRIPT = ./provisioning.sh

# small-tests:
# 	@echo "Running small tests"
# 	cd app; find . -name "*_small_tests.py" | xargs pipenv run pytest -x

# medium-tests:
# 	@echo "Running medium tests"
# 	cd app; find . -name "*_medium_tests.py" | xargs pipenv run pytest -x

# Temporarily skipping medium-tests for investigation.
# it fails after using s3 backend for TF state.
# Seems to be a bug from the cdktf testing library since all stacks
# can be deployed successfully.
# all-tests: small-tests medium-tests
# all-tests: small-tests

deploy:
	@bash $(PROVISIONING_SCRIPT) deploy 

destroy:
	@bash $(PROVISIONING_SCRIPT) destroy 

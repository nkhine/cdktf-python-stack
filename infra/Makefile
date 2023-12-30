# Makefile
.PHONY: deploy
# .PHONY: small-tests medium-tests all-tests deploy

PROVISIONING_SCRIPT = ./provisioning.sh

synth:
	@bash $(PROVISIONING_SCRIPT) synth 

deploy:
	@bash $(PROVISIONING_SCRIPT) deploy 

destroy:
	@bash $(PROVISIONING_SCRIPT) destroy 

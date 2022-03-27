-include src/index/Makefile-index
-include src/proto/Makefile-proto

# Coloured text
gprint := printf '\033[32m%s\033[0m'  # green
bprint := printf '\033[36m%s\033[0m'  # blue

checkmark := "  \xE2\x9C\x94\n"

.PHONY += help
help : 
	@$(MAKE) index/help
	@$(MAKE) proto/help

.PHONY += clean/py
clean/py : 
	@$(bprint) "- Cleaning up Python caches"
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '*__pycache__' -delete
	@printf $(checkmark)

.PHONY += clean
clean : clean/py
	@$(gprint) "Cleanup"
	@printf $(checkmark)

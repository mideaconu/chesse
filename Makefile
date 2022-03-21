-include Makefile-index
-include Makefile-proto

.PHONY += help
help : 
	@$(MAKE) index/help
	@$(MAKE) proto/help

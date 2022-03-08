-include Makefile.index
-include Makefile.protobuf

.PHONY += help
help : 
	@$(MAKE) index/help
	@$(MAKE) proto/help

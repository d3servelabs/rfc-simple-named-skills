DRAFT_BASE = draft-zhou-dvs
REVISION   = 01
DRAFT      = $(DRAFT_BASE)-$(REVISION)
SHELL      = /bin/bash
GENDIR     = gen

# Source chruby to find kramdown-rfc installed under ruby 3.3.0
CHRUBY_INIT = source /opt/homebrew/opt/chruby/share/chruby/chruby.sh 2>/dev/null && chruby ruby-3.3.0 2>/dev/null;

.PHONY: all lint clean

all: $(GENDIR)/$(DRAFT).txt

$(GENDIR):
	mkdir -p $(GENDIR)

$(GENDIR)/$(DRAFT).xml: $(DRAFT_BASE).md | $(GENDIR)
	$(CHRUBY_INIT) kramdown-rfc $(DRAFT_BASE).md > $(GENDIR)/$(DRAFT).xml
	sed -i '' 's/$(DRAFT_BASE)-latest/$(DRAFT)/g' $(GENDIR)/$(DRAFT).xml

$(GENDIR)/$(DRAFT).txt: $(GENDIR)/$(DRAFT).xml
	xml2rfc --text $(GENDIR)/$(DRAFT).xml -o $(GENDIR)/$(DRAFT).txt

lint: $(GENDIR)/$(DRAFT).xml
	npx @ietf-tools/idnits $(GENDIR)/$(DRAFT).xml

clean:
	rm -rf $(GENDIR)

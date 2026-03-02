DRAFT = draft-zhou-sns-00
SHELL = /bin/bash

# Source chruby to find kramdown-rfc installed under ruby 3.3.0
CHRUBY_INIT = source /opt/homebrew/opt/chruby/share/chruby/chruby.sh 2>/dev/null && chruby ruby-3.3.0 2>/dev/null;

.PHONY: all clean

all: $(DRAFT).txt

$(DRAFT).xml: $(DRAFT).md
	$(CHRUBY_INIT) kramdown-rfc $(DRAFT).md > $(DRAFT).xml

$(DRAFT).txt: $(DRAFT).xml
	xml2rfc --text $(DRAFT).xml -o $(DRAFT).txt

clean:
	rm -f $(DRAFT).xml $(DRAFT).txt

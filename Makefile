DRAFT_BASE = draft-zzn-dvs
REVISION   = 01
DRAFT      = $(DRAFT_BASE)-$(REVISION)
SHELL      = /bin/bash
GENDIR     = gen

# Source chruby to find kramdown-rfc installed under ruby 3.3.0
CHRUBY_INIT = source /opt/homebrew/opt/chruby/share/chruby/chruby.sh 2>/dev/null && chruby ruby-3.3.0 2>/dev/null;

.PHONY: all lint clean version tag bump submit

all: $(GENDIR)/$(DRAFT).txt

version:
	@echo "$(DRAFT)"

tag:
	@if git rev-parse "$(DRAFT)" >/dev/null 2>&1; then \
		echo "Tag $(DRAFT) already exists"; exit 1; \
	fi
	git tag -a "$(DRAFT)" -m "Release $(DRAFT)"
	@echo "Tagged $(DRAFT)"

bump:
	@NEXT=$$(printf '%02d' $$(( 10#$(REVISION) + 1 ))); \
	echo "Bumping $(DRAFT_BASE)-$(REVISION) → $(DRAFT_BASE)-$$NEXT"; \
	sed -i '' "s/^REVISION   = $(REVISION)/REVISION   = $$NEXT/" Makefile; \
	echo "Updated REVISION to $$NEXT in Makefile"

$(GENDIR):
	mkdir -p $(GENDIR)

$(GENDIR)/$(DRAFT).xml: $(DRAFT_BASE).md | $(GENDIR)
	$(CHRUBY_INIT) kramdown-rfc -3 $(DRAFT_BASE).md > $(GENDIR)/$(DRAFT).xml
	sed -i '' 's/$(DRAFT_BASE)-latest/$(DRAFT)/g' $(GENDIR)/$(DRAFT).xml

$(GENDIR)/$(DRAFT).txt: $(GENDIR)/$(DRAFT).xml
	xml2rfc --text $(GENDIR)/$(DRAFT).xml -o $(GENDIR)/$(DRAFT).txt

lint: $(GENDIR)/$(DRAFT).xml
	npx @ietf-tools/idnits $(GENDIR)/$(DRAFT).xml

submit: $(GENDIR)/$(DRAFT).xml
	@if [ ! -f .env ]; then echo "Error: .env file not found"; exit 1; fi
	@. ./.env && \
	if [ -z "$$IETF_API_KEY" ] || [ -z "$$IETF_AUTHOR_EMAIL" ]; then \
		echo "Error: IETF_API_KEY and IETF_AUTHOR_EMAIL must be set in .env"; exit 1; \
	fi && \
	echo "Submitting $(DRAFT).xml to IETF Datatracker as $$IETF_AUTHOR_EMAIL ..." && \
	curl -v \
		-F "user=$$IETF_AUTHOR_EMAIL" \
		-F "apikey=$$IETF_API_KEY" \
		-F "xml=@$(GENDIR)/$(DRAFT).xml" \
		https://datatracker.ietf.org/api/submission

clean:
	rm -rf $(GENDIR)

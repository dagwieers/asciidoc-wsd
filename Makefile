version = 0.1

bindir = /usr/bin
datadir = /usr/share
sysconfdir = /etc

all:
	@echo "Nothing to do."

install:
	@echo "= Installing wsd filter"
	install -Dp -m0644 wsd-filter.conf $(DESTDIR)$(sysconfdir)/asciidoc/filters/wsd/wsd-filter.conf
	install -Dp -m0755 wsd-filter.py $(DESTDIR)$(sysconfdir)/asciidoc/filters/wsd/wsd-filter.py

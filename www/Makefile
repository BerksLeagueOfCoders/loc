
scss_src_files =$(shell find . -type f -iname \*.scss)
css_files = $(patsubst %.scss,%.css,$(scss_src_files))

tml_src_files = $(shell find . -type f -iname \*.tml)
html_files = $(patsubst %.tml,%.html,$(tml_src_files))
php_src_files = $$(patsubst %.tml,%.php,$(tml_src_files))



all: $(css_files) $(html_files) $(deps)

%.html: %.php
	php -c php.ini $<> $@

%.php: %.tml
	
	python3 htmlTempater.py $<

%.js:

%.inhtml:

%.css: %.scss
	sassc $< $@
	
init:
	touch $(src_files)

clean:
	rm $(src_files)

	
files = style.css
src_files = style.scss

all: $(files)

$(files) :  $(src_files)
	sassc $< $@
	
$(src_files):
	echo "t: " $@ "prereq: " $<
	
init:
	touch $(src_files)

clean:
	rm $(src_files)
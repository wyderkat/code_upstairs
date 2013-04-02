VER=0.3

CORE=code_upstairs_core.py one_line_tree.py 
VIM_SPECIFIC=vim/code_upstairs.py
VIM_STARTER=vim/code_upstairs.vim
README=README.md


vim: cu-vim-$(VER).tgz

cu-vim-$(VER).tgz: $(CORE) $(VIM_STARTER) $(VIM_SPECIFIC)
	mkdir code_upstairs-$(VER)
	mkdir code_upstairs-$(VER)/plugin
	mkdir code_upstairs-$(VER)/plugin/code_upstairs.dir
	cp $(README) code_upstairs-$(VER)
	cp $(VIM_STARTER) code_upstairs-$(VER)/plugin
	cp $(CORE) $(VIM_SPECIFIC) code_upstairs-$(VER)/plugin/code_upstairs.dir
	tar zfc $@ code_upstairs-$(VER)
	rm -r code_upstairs-$(VER)

html: README.html

%.html: %.md
	markdown $^ > $@

.PHONY: vim html

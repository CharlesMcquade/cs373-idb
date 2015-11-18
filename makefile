FILES :=	         \
    .gitignore        \
    makefile          \
    apiary.apid       \
    IDB2.log          \
    model.html        \
    models.py         \
    tests.py          \
    UML.pdf

check:  
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f .coverage
	rm -f *.pyc
	rm -rf __pycache__
	rm -f tests.tmp

config:
	git config -l

scrub:
	make clean

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

test: tests.py
	coverage3 run	--branch tests.py > tests.tmp 2>&1
	coverage3 report -m --include="./*" >> tests.tmp
	cat tests.tmp

idb1.log:
	git log > IDB2.log

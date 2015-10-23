FILES :=	         \
    .gitignore        \
    makefile          \
    apiary.apid       \
    IDB1.log          \
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

test: test.py
	coverage3 run	--branch test.py > test.tmp 2>&1
	coverage3 report -m --include="./*" >> test.tmp
	cat TestNetflix.tmp

idb1.log:
	git log > idb1.log

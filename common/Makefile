.PHONY: clean install all srpm fc31 fc32 fc33 fc34 el6 el7 el8 fc31aarch64 fc32aarch64 fc33aarch64 fc34aarch64 el8aarch64
.SUFFIXES: .spec .rpm
all: build *.src.rpm \
dist/*.el6.i686.rpm dist/*.el6.x86_64.rpm dist/*.el7.x86_64.rpm \
dist/*.el8.x86_64.rpm dist/*.fc31.x86_64.rpm \
dist/*.fc32.x86_64.rpm dist/*.fc33.x86_64.rpm dist/*.fc34.x86_64.rpm

allaarch64: build *.src.rpm \
dist/*fc31.aarch64.rpm dist/*fc32.aarch64.rpm dist/*fc33.aarch64.rpm \
dist/*fc34.aarch64.rpm dist/*.el8.aarch64.rpm

install:
	@echo "Error: Cannot stage these rpms in this Makefile"

build: 
	@echo "Creating empty distributable and buildroot directory."
	mkdir -p ./dist
	touch build

clean:
	@echo "Cleaning distributable and buildroot directory."
	-rm -rf ./dist/
	-rm -rf ./buildroot
	-rm -rf $(wildcard ./*.src.rpm)
	-rm -rf ./build

srpm: *.src.rpm

*.src.rpm: *.spec sources/*
	mkdir -p ./buildroot/SOURCES
	cp -r ./sources/* ./buildroot/SOURCES/
	@echo "Building Source RPM for mock..."
	rpmbuild -bs $(wildcard ./*.spec) --define="_topdir %(pwd)/buildroot"
	cp `find ./buildroot/SRPMS/ -name "*.src.rpm" -type f` ./
	-rm -rf ./buildroot
	
newsrpm = $(shell \ls --color=never *.src.rpm)

el6: dist/*.el6.i686.rpm dist/*.el6.x86_64.rpm

dist/*.el6.i686.rpm: build *.src.rpm
	@echo "Building el6 i686 Binary RPMs for mock..."
	mock --verbose --yum --scrub=all --root=epel-6-i386 --resultdir=./dist --rebuild $(newsrpm)

dist/*.el6.x86_64.rpm: build *.src.rpm
	@echo "Building el6 x86_64 Binary RPMs for mock..."
	mock --verbose --yum --scrub=all --root=epel-6-x86_64 --resultdir=./dist --rebuild $(newsrpm)

el7: dist/*.el7.x86_64.rpm

dist/*.el7.x86_64.rpm: build *.src.rpm
	@echo "Building el7 x86_64 Binary RPMs for mock..."
	mock --verbose --yum --scrub=all --root=epel-7-x86_64 --resultdir=./dist --rebuild $(newsrpm)

el8: dist/*.el8.x86_64.rpm

dist/*.el8.x86_64.rpm: build *.src.rpm
	@echo "Building el8 x86_64 Binary RPMs for mock..."
	mock --verbose --dnf --scrub=all --root=epel-8-x86_64 --resultdir=./dist --rebuild $(newsrpm)

fc31: dist/*.fc31.x86_64.rpm

dist/*.fc31.x86_64.rpm: build *.src.rpm 
	@echo "Building fc31 x86_64 Binary RPMs for mock..."
	mock --verbose --dnf --scrub=all --root=fedora-31-x86_64 --resultdir=./dist --rebuild $(newsrpm)

fc32: dist/*.fc30.x86_64.rpm

dist/*.fc32.x86_64.rpm: build *.src.rpm 
	@echo "Building fc32 x86_64 Binary RPMs for mock..."
	mock --verbose --dnf --scrub=all --root=fedora-32-x86_64 --resultdir=./dist --rebuild $(newsrpm)

fc33: dist/*.fc33.x86_64.rpm

dist/*.fc33.x86_64.rpm: build *.src.rpm 
	@echo "Building fc33 x86_64 Binary RPMs for mock..."
	mock --verbose --dnf --scrub=all --root=fedora-33-x86_64 --resultdir=./dist --rebuild $(newsrpm)

fc34: dist/*.fc34.x86_64.rpm

dist/*.fc34.x86_64.rpm: build *.src.rpm 
	@echo "Building fc34 x86_64 Binary RPMs for mock..."
	mock --verbose --dnf --scrub=all --root=fedora-34-x86_64 --resultdir=./dist --rebuild $(newsrpm)

fc31aarch64: dist/*fc31.aarch64.rpm

dist/*fc31.aarch64.rpm: build *.src.rpm 
	@echo "Building fc31 aarch64 Binary RPMs for mock..."
	mock --verbose --dnf --scrub=all --root=fedora-31-aarch64 --resultdir=./dist --rebuild $(newsrpm)

fc32aarch64: dist/*fc32.aarch64.rpm

dist/*fc32.aarch64.rpm: build *.src.rpm 
	@echo "Building fc32 aarch64 Binary RPMs for mock..."
	mock --verbose --dnf --scrub=all --root=fedora-32-aarch64 --resultdir=./dist --rebuild $(newsrpm)

fc33aarch64: dist/*fc33.aarch64.rpm

dist/*fc33.aarch64.rpm: build *.src.rpm 
	@echo "Building fc33 aarch64 Binary RPMs for mock..."
	mock --verbose --dnf --scrub=all --root=fedora-33-aarch64 --resultdir=./dist --rebuild $(newsrpm)

fc34aarch64: dist/*fc34.aarch64.rpm

dist/*fc34.aarch64.rpm: build *.src.rpm 
	@echo "Building fc34 aarch64 Binary RPMs for mock..."
	mock --verbose --dnf --scrub=all --root=fedora-34-aarch64 --resultdir=./dist --rebuild $(newsrpm)

el8aarch64: dist/*.el8.aarch64.rpm

dist/*.el8.aarch64.rpm: build *.src.rpm
	@echo "Building el8 aarch64 Binary RPMs for mock..."
	mock --verbose --dnf --scrub=all --root=epel-8-aarch64 --resultdir=./dist --rebuild $(newsrpm)
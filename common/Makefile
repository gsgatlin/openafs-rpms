.PHONY: clean install all srpm fc34 fc35 fc36 el7 el8 fc34aarch64 fc35aarch64 fc36aarch64 el8aarch64
.SUFFIXES: .spec .rpm
all: build *.src.rpm \
dist/*.el7.x86_64.rpm dist/*.el8.x86_64.rpm \
dist/*.fc34.x86_64.rpm dist/*.fc35.x86_64.rpm dist/*.fc36.x86_64.rpm \

allaarch64: build *.src.rpm \
dist/*fc34.aarch64.rpm dist/*fc35.aarch64.rpm \
dist/*fc36.aarch64.rpm dist/*.el8.aarch64.rpm

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

el7: dist/*.el7.x86_64.rpm

dist/*.el7.x86_64.rpm: build *.src.rpm
	@echo "Building el7 x86_64 Binary RPMs for mock..."
	mock --verbose --yum --root=epel-7-x86_64 --resultdir=./dist --rebuild $(newsrpm)

el8: dist/*.el8.x86_64.rpm

dist/*.el8.x86_64.rpm: build *.src.rpm
	@echo "Building el8 x86_64 Binary RPMs for mock..."
	mock --verbose --dnf --root=epel-8-x86_64 --resultdir=./dist --rebuild $(newsrpm)

fc34: dist/*.fc34.x86_64.rpm

dist/*.fc34.x86_64.rpm: build *.src.rpm 
	@echo "Building fc34 x86_64 Binary RPMs for mock..."
	mock --verbose --dnf --root=fedora-34-x86_64 --resultdir=./dist --rebuild $(newsrpm)

fc35: dist/*.fc35.x86_64.rpm

dist/*.fc35.x86_64.rpm: build *.src.rpm 
	@echo "Building fc35 x86_64 Binary RPMs for mock..."
	mock --verbose --dnf --root=fedora-35-x86_64 --resultdir=./dist --rebuild $(newsrpm)

fc36: dist/*.fc36.x86_64.rpm

dist/*.fc36.x86_64.rpm: build *.src.rpm 
	@echo "Building fc36 x86_64 Binary RPMs for mock..."
	mock --verbose --dnf --root=fedora-36-x86_64 --resultdir=./dist --rebuild $(newsrpm)

fc34aarch64: dist/*fc34.aarch64.rpm

dist/*fc34.aarch64.rpm: build *.src.rpm 
	@echo "Building fc34 aarch64 Binary RPMs for mock..."
	mock --verbose --dnf --root=fedora-34-aarch64 --resultdir=./dist --rebuild $(newsrpm)

fc35aarch64: dist/*fc35.aarch64.rpm

dist/*fc35.aarch64.rpm: build *.src.rpm 
	@echo "Building fc35 aarch64 Binary RPMs for mock..."
	mock --verbose --dnf --root=fedora-35-aarch64 --resultdir=./dist --rebuild $(newsrpm)

fc36aarch64: dist/*fc36.aarch64.rpm

dist/*fc36.aarch64.rpm: build *.src.rpm 
	@echo "Building fc36 aarch64 Binary RPMs for mock..."
	mock --verbose --dnf --root=fedora-36-aarch64 --resultdir=./dist --rebuild $(newsrpm)

el8aarch64: dist/*.el8.aarch64.rpm

dist/*.el8.aarch64.rpm: build *.src.rpm
	@echo "Building el8 aarch64 Binary RPMs for mock..."
	mock --verbose --dnf --root=epel-8-aarch64 --resultdir=./dist --rebuild $(newsrpm)


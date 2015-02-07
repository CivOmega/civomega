# CivOmega

[![Build Status](https://travis-ci.org/CivOmega/civomega.png?branch=develop)](https://travis-ci.org/CivOmega/civomega)

CivOmega makes it easy for anyone to get answers from open datasets and APIs.  It is powered by "question modules" which are written and contributed by civic minded developers.  These modules are intentionally simple and lightweight, and map question patterns to API calls and queries against datasets.

If you are a developer interested in contributing a question module, we suggest you start by forking our [CivOmega Module Bootstrap](https://github.com/CivOmega/civomega-mod-bootstrap).  Once you are happy with the module, raise an issue in this repository requesting that the module be added to [CivOmega](http://civomega.com).

## Setting Up CivOmega Core
You are going to need [Python](https://www.python.org/downloads/) and [Git](http://git-scm.com/) on your development environment to be able to contribute to CivOmega Core or build a CivOmega Module.


- [OSX Setup Instructions](doc/BOOTSTRAPPING-osx.md)
- [Unix / Linux Setup Instructions](doc/BOOTSTRAPPING-linux.md)


## Contributing
If you are a developer interested in contributing a question module, start by taking a look at our [CivOmega Module Documentation](doc/MODULES.md).  Once you are happy with your module, [raise an issue](https://github.com/CivOmega/civomega/issue) explaining your module, and requesting that it be added to [CivOmega](http://civomega.com).  We will then review the module and respond with any feedback.

If you are a developer interested in contributing to CivOmega Core, there is a small amount of developer-specific documentation available related to the core project. See [CONTRIBUTING.md](CONTRIBUTING.md) and the files in the [doc directory](doc).


## Structure
`civomega.data` represents Django models & functionality related to the
question-answering `Module`s, `DataSource`s, `QuestionPattern`s and the like.

`civomega.cologger` represents Django models & functionality related to
logging of user input, detecting whether answer-generation is taking too long,
etc.

# Contributing to CivOmega

## Contribution Flow

We're a scrappy band of digital vagabonds, and as such we will be using a cheap version [GitHub Flow](http://scottchacon.com/2011/08/31/github-flow.html).  Specifically, we'll have two core branches:

- `develop` -- this branch contains the latest in-progress work.
- `master` -- this branch will ALWAYS be in "good to deploy" condition.

Since civomega is a small operation, core developers should work directly on the CivOmega/civomega repository and use feature branches for all changes.  Branches should always be named using the `username-feature_description` convention.

Once a branch is ready to combine into the main project, issue a pull request from `your-branch_name` into `develop`.  You can do this using the GitHub interfaces, or if that's to complicated just use the url: https://github.com/CivOmega/civomega/compare/FOO...develop Where `FOO` is the name of the feature branch you want ot merge.

## Setting Up

Check the [doc directory](doc) and look for the files named "BOOTSTRAPPING"
(they're OS-dependent) for info on how to check out the repo and
run a local instance of the web app.

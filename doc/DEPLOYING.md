First, acquire the SSH key to the Ubuntu server(s) (usually an AWS instance)
running the app. (The filename will be referred to as `$PATH_TO_SERVER_SSH_KEY`.)

Second, go into the `civomega` directory and copy over `settings_live.py.example`
to `settings_live.py` and edit it to contain the appropriate settings OR
acquire the canonical `settings_live.py` from someone else.

Then, run this command to deploy the `develop` branch to the server. (In the
future, deploys will be from `master`. `master` is assumed to be a "clean"
branch at all times.)

```
fab -i $PATH_TO_SERVER_SSH_KEY deploy
```

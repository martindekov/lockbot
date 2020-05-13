# Lockbot

This repository contains the source code for the `Keep your functions running to schedule with the cron-connector.` blog post.

## What is this bot doing

This bot locks outdated issues in github on a schedule.

### The schedule

The function has annotations:

```yaml
    annotations:
      topic: cron-function
      schedule: "*/1 * * * *"
```

In order to be recognized by the [cron-connector](https://github.com/openfaas-incubator/cron-connector) and to be ran on the cron schedule pointed in the configuration `*/1 * * * *` which means once a minute.

### The locking

The environmental variables:

```yaml
    environment:
      github_repository: push2
      inactive_days: 90
```

define how much days are needed since the last comment in order to consider issue outdated. The repository I chose is my testing ground called [push2](https://github.com/martindekov/push2) which I consider GitHub API playground.

## How to create my own schedule

There is pretty cool site called `crontab guru` you can find it [here](https://crontab.guru/) which translates in a verbose way the schedule you created.

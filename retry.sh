#!/bin/bash
pipenv install

git status

git add .

git commit --amend --no-edit

git push -f

git push -f heroku master

heroku open

heroku logs --tail
#!/usr/bin/env sh

set -e

npm run build

cd dist

git init
git add -A
git commit -m "Automated deployment of the latest version"

git push -f git@github.com:aditya130805/WallPreview.git main:gh-pages

cd -

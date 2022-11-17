#!/bin/sh

repository_name=$(git rev-parse --show-toplevel | xargs basename)

echo "Clone $repository_name..."
git clone https://github.com/calypsonet/$repository_name.git

cd "$repository_name" || exit

echo "Repository name: $repository_name"

echo "Checkout gh-pages branch..."
git checkout -f gh-pages

echo "Delete existing SNAPSHOT directory..."
rm -rf *-SNAPSHOT

echo "Copy diagram folders..."
find .. -type d -regex '\.\./[0-9].*$' -exec cp -rf -t . {} +

echo "Update versions list..."
echo "| Version | Documents |" > list_versions.md
echo "|:---:|---|" >> list_versions.md
for directory in $(ls -rd [0-9]*/ | cut -f1 -d'/')
do
  line="| $directory |"
  cd "$directory" || exit
  for file in  $(ls -r *.svg | cut -f1 -d'/')
  do
    line="$line[$file]($directory/$file)<br/>"
  done
  line="$line|"
  cd ..
  echo "$line" >> ./list_versions.md
done

echo "Local docs update finished."




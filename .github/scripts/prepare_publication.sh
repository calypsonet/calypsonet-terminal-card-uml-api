#!/bin/sh

repository_name=$(git rev-parse --show-toplevel | xargs basename)

echo "Clone $repository_name..."
git clone https://github.com/calypsonet/$repository_name.git

cd "$repository_name" || exit

echo "Repository name: $repository_name"

echo "Checkout doc branch..."
git checkout -f doc

echo "Delete existing SNAPSHOT directory..."
rm -rf *-SNAPSHOT

echo "Copy diagram folders..."
find .. -type d -regex '\.\./[0-9].*$' -exec cp -rf -t . {} +

# Find the latest stable version (first non-SNAPSHOT)
latest_stable=$(ls -d [0-9]*/ | grep -v SNAPSHOT | cut -f1 -d'/' | sort -Vr | head -n1)

# Create latest-stable copy if we have a stable version
if [ ! -z "$latest_stable" ]; then
    echo "Creating latest-stable directory pointing to $latest_stable..."
    rm -rf latest-stable
    mkdir latest-stable
    cp -rf "$latest_stable"/* latest-stable/
fi

echo "Update versions list..."
echo "| Version | Documents |" > list_versions.md
echo "|:---:|---|" >> list_versions.md
for directory in $(ls -rd [0-9]*/ | cut -f1 -d'/')
do
  diagrams=""
  cd "$directory" || exit
  for file in  $(ls -r *.svg 2>/dev/null | cut -f1 -d'/')
  do
    if [ "$directory" = "$latest_stable" ]; then
      diagrams="$diagrams[$file](latest-stable/$file)<br/>"
    else
      diagrams="$diagrams[$file]($directory/$file)<br/>"
    fi
  done
  cd ..
  # If this is the stable version, write latest-stable entry first
  if [ "$directory" = "$latest_stable" ]; then
      echo "| **$directory (latest stable)** | $diagrams |" >> list_versions.md
  else
      echo "| $directory | $diagrams |" >> list_versions.md
  fi
done

echo "Computed all versions:"
cat list_versions.md
cd ..
echo "Local docs update finished."
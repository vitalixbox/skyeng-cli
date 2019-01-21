# Skyeng commanf line tools

This is a command line tool for access to your Skyeng profile.
Originally I needed this tool for sync my words with Anki cards app 
and for convenient way for seeing new words for each lesson.
You can get the following:
1. Your words list with meanings and name of lesson, where this word from.
2. Something else?

# Quickstart

Install:
```sh
cd skyeng-cli
python setup.py install

skyeng-cli --help
```

You can authorize for two ways:
```sh
# 1. With auth token. It's preferable way
skyeng-cli --token=TOKEN wordsets
# Your auth token you can get from browser's cookies "session_global"
#   or from username and password
skyeng-cli --username=USERNAME --password=PASSWORD get-token

# 2. With your username and password
skyeng-cli --username=USERNAME --password=PASSWORD wordsets
```

You can get your profile's data:
```sh
# Wordsets - it's words, which were in lessons
skyeng-cli wordsets

# Show all your words with meanings and wordsets
skyeng-cli words
```

# TODO

1. Sync tool with Anki.
2. Work with Skyeng's dictionary.


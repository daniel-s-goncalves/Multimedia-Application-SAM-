# SAM - Multimedia Application

# Important!!!

You need to install 'Rubberband CLI' and 'ffmpeg' to allow the server to make audio editions.

====================================================================================================
You can install these libraries with 'homebrew' if you are using MAC OS:

```brew install rubberband```
```brew install ffmpeg```
====================================================================================================

If you are using Windows you will need to download these libraries separately and add each of them to the PATH environment library.

# How to run

> Update: Due to some unexpected virtual environment distinctions between Win/Linux distributions (namely environment variables), the system will now run in a global scenario without the need for a Virtual Environment.

**Step 1:** From the main directory (the repository's directory), run the following command:

```
pip install -r requirements.txt
```

**Step 2:** Set up the env variable for flask. This process has two commands, choose the one that fits your OS:

Windows:
```
set FLASK_APP=bin
$env:FLASK_APP = "bin"
```

Linux:
```
export FLASK_APP=bin
```

**Step 3:** Run the flask application using the following commands:

Windows / Linux:
```
python3 -m flask run
```

By default, the website will be available inside ```http://localhost:5000/```

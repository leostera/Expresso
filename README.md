## Expresso: CoffeeScript compiling for Pythonistas.

This is a little continuous builder for CoffeeScript that uses standard Python modules and the excellents PyYAML and PyV8 to perform some little tasks described in *.order files that will make our development hours a joy.
Feel free to fork, report issues, request features, watch, clone and -of course- use it!

### Example of use #1

This really readable YAML file 

```
watch: No
files:
- tests/assets/folder/*.coffee
- tests/assets/file.coffee
deliver: tests/assets/delivery
```

Will compile all .coffee files in the tests/assets/folder folder and file.coffee in tests/assets into their respectives Js files, outputting:

```
tests/assets/folder/*.js
tests/assets/file.js
```

### Example of use #2

This other also really readable YAML file 

```
watch: Yes
files:
- tests/assets/folder/**
join: joint
```

Turns into a watcher that joins all the coffee files in that directory (and subdirectories) into one exported js file named joint in the same directory.


### Order files

So far I have developed the minimal functionality to make it useful right away, it includes:

* watch, boolean Yes or No to watch the file/folder/filepattern
* join, No or string for the name of the file where it all will be joined
* files, list to specify multiple source files
* deliver, string path to output directory

I'm open to suggestions.

## Usage

Create your own .order files into a "orders" folder in your project root, and copy expresso also to your project root. Simply run "python expresso.py" and it will automagically load all the orders in your orders folder.

### Note

It depends on PyYAML and PyV8. Do:

```
pip install PyYAML
```

Install your platforms PyV8 from here http://code.google.com/p/pyv8/downloads/list, and you'll be ready to go.

### Tests

I need to make autodeleting of js files after each test in a tearDown, but so far you can perform the testing and see if everything is working ok in your system by running run_tests.py with "python run_tests.py". After each run delete all the js files under the tests tree if you want to re-run or something.

## NodeJS version

I also included here the first version I used, based on Node.js, for those who already have it installed and running and do not mind using it. For the rest of us, there's Expresso V8.

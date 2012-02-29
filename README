### Expresso

This is a little continuous builder for CoffeeScript that uses standard Python modules and the CoffeeScript ability to "watch" for files to perform some little tasks described in *.order files.

## Example of use #1

This really readable YAML file 

```
watch: No
files:
- tests/assets/folder/*.coffee
- tests/assets/file.coffee
deliver: tests/assets/delivery
```

Turns into a one-time run of the following commands:
```
coffee -l -o tests/assets/delivery -c tests/assets/folder/*.coffee
coffee -l -o tests/assets/delivery -c tests/assets/folder/file.coffee
```

## Example of use #2

This other also really readable YAML file 

```
watch: Yes
files:
- tests/assets/folder/*.coffee
join: joint
```

Turns into a watcher that joins all the coffee files in that directory into one exported js file named joint in the same directory.
```
coffee -lw --join joint -c tests/assets/folder/*.coffee
```

## Order files

So far I just included the minimal necessary stuff for me to use Expresso, that includes:

* watch, boolean Yes or No to watch the file/folder/filepattern
* join, No or string for the name of the file where it all will be joined
* files, list to specify multiple source files
* deliver, string path to output directory

### Usage

Create your own .order files into a "orders" folder in your project root, and copy expresso also to your project root. Simply run "python expresso.py" and it will automagically load all the orders in your orders folder.

## Tests

I need to make autodeleting of js files after each test in a tearDown, but so far you can perform the testing and see if everything is working ok in your system by running run_tests.py with "python run_tests.py". After each run delete all the js files under the tests tree.

### Bakery

This project will be included into Bakery as a continuous building tool.
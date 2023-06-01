# Documentation

## Prerequisites

This project is intended for Linux systems (it has been tested for [Debian](https://www.debian.org/https://www.debian.org/)). 

Here are the dependancies:

 - `sysstat`, a bundle of sytem performance tools,
 - `apache2` or another web server that can run scripts,
 - [Python 3.x](https://www.python.org/downloads/)

!!! note inline end "Naming"
    From now on, it will be refered to as **Directory**.

Before going further, please create a directory for the web interface like `/var/www/html/monitoring`. 
its path will be needend through this process. 

## System data collection

Data collection is done by `script.sh`. 
Give it to a user that can write to the **Directory** and memorize the scripts path.

Open the file and customize the **Directory** to your liking.

```sh title="script.sh" linenums="4"
file="/var/www/html/monitoring/measures"
```

Next, open your crontab (`etc/crontab`) and add the script to be executed every minute.

```title="Crontab example" linenums="22"
* * * * * user /user/script.sh
```

!!! success "Check"
    After a minute, the measures file should appear in the **Directory**.

## Python script

Copy `index.py` and `style.css` into the **Directory** and make `index.py` executeable.

If needed, change the file name in `index.py`:

```py title="index.py" linenums="17"
database = "measures"
```

## Apache configuration

You need to make several changes to Apaches configuration:

 - Allow script execution
 - Add a Python handler
 - Load the CGI module
 - Make `index.py` the index page

Open Apaches configuration file and create a `<Directory>` part for the **Directory**:

```xml title="/etc/apache2/apache2.conf" linenums="170"
<Directory /var/www/>
        Options Indexes FollowSymLinks ExecCGI
        AddHandler cgi-script .cgi .py
        LoadModule cgi_module /usr/lib/apache2/modules/mod_cgi.so
        AllowOverride None
        Require all granted
        DirectoryIndex index.py
</Directory>
```

Reload the server:

```
systemstl reload apache2
```

!!! success "Check"
    The web interface should be availible at https://localhost/**Directory**.



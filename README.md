# changeme

A default credential scanner.

![Basic Scan](https://github.com/user-attachments/assets/ac007c9c-e623-4c0a-b527-1e9d6dedac73)

## About

changeme picks up where commercial scanners leave off. It focuses on detecting default and backdoor credentials and not necessarily common credentials. It's default mode is to scan HTTP default credentials, but has support for other credentials.

changeme is designed to be simple to add new credentials without having to write any code or modules. changeme keeps credential data separate from code. All credentials are stored in [yaml](http://yaml.org/) files so they can be both easily read by humans and processed by changeme. Credential files can be created by using the `./changeme.py --mkcred` tool and answering a few questions.

changeme supports the http/https, mssql, mysql, postgres, ssh, ssh w/key, snmp, mongodb and ftp protocols. Use `./changeme.py --dump` to output all of the currently available credentials.

You can load your targets using a variety of methods, single ip address/host, subnet, list of hosts, nmap xml file and Shodan query. All methods except for Shodan are loaded as a positional argument and the type is inferred.

## Installation

changeme has only been tested on Linux and has known issues on Windows and OS X/macOS. Use Docker to run changeme on unsupported platforms. changeme supports either a redis-backed queue (most stable) or an in-memory backed queue.

### Debian/Ubuntu package

The recommended installation path on Debian or Ubuntu is the packaged release. Stable versions of changeme are published on the [latest release](https://github.com/MakoWish/changeme/releases/latest) page as DEB assets.

Download the newest DEB for your system architecture from the latest release and install it with `apt`:

```
ARCH=$(dpkg --print-architecture)
curl -LO https://github.com/MakoWish/changeme/releases/latest/download/changeme_${ARCH}.deb
sudo apt install ./changeme_${ARCH}.deb
changeme --help
```

The package installs changeme into `/opt/changeme`, creates an isolated Python virtual environment in `/opt/changeme/.venv`, and adds `/usr/bin/changeme` as a symbolic link to the venv-backed launcher. During package configuration, the post-install step runs `pip install -r /opt/changeme/requirements.txt`, so the install host needs access to PyPI or a configured Python package mirror.

For mssql support, `unixodbc-dev` must be installed before `pyodbc` is installed. For postgres support, `libpq-dev` must be installed. These dependencies are included in the DEB package metadata. [PhantomJS](http://phantomjs.org/) is required in your PATH for HTML report screenshots.

### Manual install from source

If you prefer not to use the DEB package, install the system and Python dependencies manually, then run changeme from a virtual environment:

```
sudo apt install python3-venv python3-pip python3-dev build-essential libpq-dev unixodbc-dev libxml2-dev libxslt1-dev zlib1g-dev
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python3 ./changeme.py --help
```

This keeps the Python modules isolated in `.venv`, but it does not create `/usr/bin/changeme` or manage upgrades/removal through the package manager. To upgrade a manual installation, pull or download a newer changeme release and re-run `.venv/bin/pip install -r requirements.txt`.

### Build a local DEB package

Build a local DEB package when you want to test packaging changes or install a package built from your checkout. The package version is read from the repository `VERSION` file.

Install the DEB build requirements first:

```
sudo apt install dpkg-dev python3 python3-venv python3-pip python3-dev build-essential libpq-dev unixodbc-dev libxml2-dev libxslt1-dev zlib1g-dev
```

Build and install the package:

```
./debian/build-deb.sh
sudo apt install ./dist/changeme_$(cat VERSION)_$(dpkg --print-architecture).deb
```

## Usage Examples

Below are some common usage examples.

* Scan a single host: `./changeme.py 192.168.59.100`
* Scan a subnet for default creds: `./changeme.py 192.168.59.0/24`
* Scan using an nmap file `./changeme.py subnet.xml`
* Scan a subnet for Tomcat default creds and set the timeout to 5 seconds: `./changeme.py -n "Apache Tomcat" --timeout 5 192.168.59.0/24`
* Use [Shodan](https://www.shodan.io/) to populate a targets list and check them for default credentials: `./changeme.py --shodan_query "Server: SQ-WEBCAM" --shodan_key keygoeshere -c camera`
* Scan for SSH and known SSH keys: `./changeme.py --protocols ssh,ssh_key 192.168.59.0/24`
* Scan a host for SNMP creds using the protocol syntax: `./changeme.py snmp://192.168.1.20`

See [Wiki Examples](https://github.com/MakoWish/changeme/wiki/Examples) for more detailed examples.

## Known Issues

- [x] The telnet scanner is broken. - FIXED!

Additionally, anything filed under https://github.com/MakoWish/changeme/issues as a bug.

## Bugs and Enhancements

Bugs and enhancements are tracked at [https://github.com/MakoWish/changeme/issues](https://github.com/MakoWish/changeme/issues).

**Request a credential:** Please add an issue to Github and apply the credential label.

**Vote for a credential:** If you would like to help us prioritize which credentials to add, you can add a comment to a credential issue.

Please see the [wiki](https://github.com/MakoWish/changeme/wiki) for more details.

## Contributors

Thanks for code contributions and suggestions.

* @ztgrace
* @AlessandroZ
* @m0ther_
* @GraphX
* @Equinox21_
* https://github.com/MakoWish/changeme/graphs/contributors

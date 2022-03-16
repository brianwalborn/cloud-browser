# cloud-browser
## Set-up
### Prerequisites
- [Git](https://git-scm.com/downloads) (of course!)
- [Python 3.9](https://www.python.org/downloads/release/python-395/) or greater
- [AWS CLI configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config)
___
### Initial set up (Linux, Mac, & Windows)
1. Clone the repository
```sh
git clone https://github.com/brianwalborn/cloud-browser.git
```
2. `cd` into the `cloud-browser` directory
```sh
cd cloud-browser
```
### Running the application (in a bash console)
1. Install the dependecies with `pip`
```sh
pip install -r requirements.txt
```
2. Run the `startup.sh` script with the `-d` flag to initialize the database
```sh
./startup.sh -d
```
3. Navigate to localhost:5000 in a browser

**Note:** To run the application after the database has been initialized, simply run `./startup.sh`
___
### Running the application (in PowerShell)
1. Install the dependecies with `pip`
```powershell
py -m pip install -r .\requirements.txt
```
2. Run the `startup.ps1` script with the `-d` flag to initialize the database
```powershell
.\startup.ps1 -d
```
3. Navigate to localhost:5000 in a browser

**Note:** To run the application after the database has been initialized, simply run `.\startup.ps1`
___
### Initialize settings
1. Enter the desired regions and tags on the settings page. For example:
![alt text](cloud_browser/static/images/settings.png)

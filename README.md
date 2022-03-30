# cloud-browser
## Prerequisites
- [Git](https://git-scm.com/downloads) (of course!)
- [AWS CLI configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config)
- [Python 3.9](https://www.python.org/downloads/release/python-395/) or greater (only when running locally)
- [Docker](https://www.docker.com/get-started/) (only when running with Docker)

---

## Initial set up (Linux, Mac, & Windows)
1. Clone the repository
```sh
git clone https://github.com/brianwalborn/cloud-browser.git
```
2. `cd` into the `cloud-browser` directory
```sh
cd cloud-browser
```

---

## Running the application...
### ...locally in a Mac OS/Linux console
1. Install the dependecies with `pip`
```sh
pip install -r requirements.txt
```
2. Execute the `run_local.sh` script
```sh
./run_local.sh
```
3. Navigate to localhost:5000 in a browser

### ...locally in a PowerShell console
1. Install the dependecies with `pip`
```powershell
py -m pip install -r .\requirements.txt
```
2. Execute the `run_local.ps1` script
```powershell
.\run_local.ps1
```
3. Navigate to localhost:5000 in a browser

### ...with Docker (Mac OS/Linux)
1. Simply execute `./run_docker.sh`
```
./run_docker.sh
```
2. Navigate to localhost:8080 in a browser
- **Note:** If there are errors regarding AWS credentials and/or there are no AWS profiles displaying in settings, the `aws_credentials_path` in `run_docker.sh` may have to be updated to point to the correct AWS credentials file location.
---

## Initialize settings
1. Enter the desired regions and tags on the settings page. For example:
![alt text](cloud_browser/static/images/settings.png)

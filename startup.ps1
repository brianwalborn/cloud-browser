param (
    [switch] $d
)

$env:FLASK_APP="cloud_browser"

if ($d) {
    py -m flask init-database
}

py -m flask run

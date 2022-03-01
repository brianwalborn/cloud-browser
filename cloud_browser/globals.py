# TODO: this is a temporary way to store settings. this needs to be moved to a database

# the regions in which the product exists
regions: list[str] = [ 'ca-central-1', 'eu-west-2', 'us-east-1' ] 

# the resource tags used to look up AWS resources. defaulted to 'Product' but can be changed to any tag that exists on the resources
tags: dict[str, list[str]] = {
    'Product': [ 'example_product', 'another_example_product' ]
}

# ignore any AWS resources with the below tags
tags_to_ignore: dict[str, list[str]] = { 
    'Service': [ 'ignore_this_service', 'ignore_this_service_too' ]
}

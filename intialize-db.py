import datapackage
import pandas as pd

data_json = {'nasdaq':'https://datahub.io/core/nasdaq-listings/datapackage.json',
            's&p500':'https://datahub.io/core/s-and-p-500-companies/datapackage.json',
            'nyse':'https://datahub.io/core/nyse-other-listings/datapackage.json'
            }

data_csv = {'ndx':''}

# to load Data Package into storage
package = datapackage.Package(data_url)

# to load only tabular data
resources = package.resources
for resource in resources:
    if resource.tabular:
        data = pd.read_csv(resource.descriptor['path'])
        print (data)
from flatten_json import flatten
import json
import requests

def queryNVD(url, cveID):
    """ Retrieve CVE details from NVD.
        
        :param url: A string, API URL of NVD.
        :param data: A Dict, containing the CVEs to retrieve details for
        :returns: a dict, JSON object of assets.
        :raises: ConnectionError: if unable to successfully make GET request to NVD API."""
    try:
        params = {'cveId': cveID}
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers, params=params)
        cve_details = json.loads(response.content)
        return cve_details
    except ConnectionError as error:
        content = "No Response"
        raise error
    
def main():
    cveID = 'CVE-2021-44228'
    nvd_url = 'https://services.nvd.nist.gov/rest/json/cves/2.0?'
    result = queryNVD(nvd_url, cveID)
    flattened = flatten(result)
    with open('flattened_nvd.txt', 'w') as w:
        for k, v in flattened.items():
            w.write(k + ': ' + str(v) + '\n')
    
if __name__ == '__main__':
    main()
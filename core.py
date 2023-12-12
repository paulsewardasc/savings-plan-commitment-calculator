# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import requests
import json
import sys

#usage operations dictionary
#ref. mapping https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/billing-info-fields.html
operation_by_platform_dict = {"Linux/UNIX": "RunInstances",
                              "Red Hat BYOL Linux": "RunInstances:00g0",
                              "Red Hat Enterprise Linux": "RunInstances:0010",
                              "Red Hat Enterprise Linux with HA": "RunInstances:1010",
                              "Red Hat Enterprise Linux with SQL Server Standard and HA": "RunInstances:1014",
                              "Red Hat Enterprise Linux with SQL Server Enterprise and HA": "RunInstances:1110",
                              "Red Hat Enterprise Linux with SQL Server Standard": "RunInstances:0014",
                              "Red Hat Enterprise Linux with SQL Server Web": "RunInstances:0210",
                              "Red Hat Enterprise Linux with SQL Server Enterprise": "RunInstances:0110",
                              "SQL Server Enterprise": "RunInstances:0100",
                              "SQL Server Standard": "RunInstances:0004",
                              "SQL Server Web": "RunInstances:0200",
                              "SUSE Linux": "RunInstances:000g",
                              "Ubuntu Pro": "RunInstances:0g00",
                              "Windows": "RunInstances:0002",
                              "Windows BYOL": "RunInstances:0800",
                              "Windows with SQL Server Enterprise": "RunInstances:0102",
                              "Windows with SQL Server Standard": "RunInstances:0006",
                              "Windows with SQL Server Web": "RunInstances:0202"}

#tenancy dictionary
#ref. https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_instances.html
tenancy_dict = {"default":"Shared",
                "dedicated":"Dedicated Instance",
                "host":"Dedicated Host"}


#dict to cache pricing by region
region_price = {};
region_price_ondemand = {};

region_price_index_api_url = "https://pricing.us-east-1.amazonaws.com/savingsPlan/v1.0/aws/AWSComputeSavingsPlan/current/region_index.json"
region_price_index_api_url_ondemand = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/region_index.json"

response_region_price_index = requests.get(region_price_index_api_url, timeout=5)
response_region_price_index_ondemand = requests.get(region_price_index_api_url_ondemand, timeout=5)
region_price_index = response_region_price_index.json()['regions']
region_price_index_ondemand = response_region_price_index_ondemand.json()['regions']

def get_pricing_by_region(region_code):
    print('[+] Getting Costs Savings pricing')
    if (region_code not in region_price): #check if region pricing is already loaded
        for region in region_price_index:
            if (region['regionCode'] == region_code):
                print('[*] Downloading Savings Plan pricing')
                region_price_api_url = "https://pricing.us-east-1.amazonaws.com" + region['versionUrl']
                region_price_response = requests.get(region_price_api_url, timeout=5)
                #save pricing by region
                region_price[region_code] = region_price_response.json()
                break
    return region_price[region_code]

def get_pricing_by_region_ondemand(region_code):
    print('[+] Getting Ondemand pricing')
    if (region_code not in region_price_ondemand): #check if region pricing is already loaded
        for region, region_data in region_price_index_ondemand.items():
            if (region_data['regionCode'] == region_code):
                print('[*] Downloading Ondemand pricing')
                region_price_api_url = "https://pricing.us-east-1.amazonaws.com" + region_data['currentVersionUrl']
                region_price_response_ondemand = requests.get(region_price_api_url, timeout=5)
                #save pricing by region
                region_price_ondemand[region_code] = region_price_response_ondemand.json()
                break
    return region_price_ondemand[region_code]

def get_ondemand_rate(region_code, usage_operation, instance_family, instance_type, tenancy, sp_type, term, purchasing_option):
    region_price = get_pricing_by_region(region_code)
    sku = ''
    sp_rate = 0
    products = region_price['products']
    region_price_ondemand = get_pricing_by_region_ondemand(region_code)
    products_ondemand = region_price_ondemand['products']
    for product,product_item in products_ondemand.items():
        if 'instanceType' in product_item['attributes']:
          if (product_item['attributes']['instanceType'] == instance_type and
            product_item['attributes']['tenancy'] == tenancy and
            product_item['attributes']['operation'] == usage_operation and
            product_item['attributes']['capacitystatus'] == 'Used'):
            sku_ondemand = product

    terms_ondemand = region_price_ondemand['terms']['OnDemand']
    pricePerUnit_ondemand = 0
    for term, term_item in terms_ondemand.items():
      if term == sku_ondemand:
        for i in term_item.keys():
          priceDimensions = term_item[i]['priceDimensions']
          for p in priceDimensions.keys():
            pricePerUnit_ondemand = float(priceDimensions[p]['pricePerUnit']['USD'])
    
    return pricePerUnit_ondemand

def get_savings_plan_rate(region_code, usage_operation, instance_family, instance_type, tenancy, sp_type, term, purchasing_option):
    region_price = get_pricing_by_region(region_code)
    sku = ''
    sp_rate = 0
    products = region_price['products']
    # find correct SKU in the json response
    for product in products:
        if (product['attributes']['purchaseOption'] == purchasing_option and
            product['attributes']['purchaseTerm'] == term and
            product['productFamily'] == sp_type and
            (sp_type == "ComputeSavingsPlans" or product['attributes']['instanceType'] == instance_family)):
            sku = product['sku']

    # find savings plan rate in the json response given the SKU
    terms = region_price['terms']['savingsPlan']
    for term in terms:
        if (term['sku'] == sku):
            rates = term['rates']
            bendsw = "-BoxUsage:"
            if region_code == 'us-east-1':
              bendsw = "BoxUsage:"
            dendsw = "-DedicatedUsage:"
            if region_code == 'us-east-1':
              dendsw = "DedicatedUsage:"
            hendsw = "-HostUsage:"
            if region_code == 'us-east-1':
              hendsw = "HostUsage:"
            for rate in rates:
                if (usage_operation == rate['discountedOperation']):
                    #tenancy SHARED
                    if (tenancy == 'Shared' and rate['discountedUsageType'].endswith(bendsw + instance_type)):
                        sp_rate = float(rate['discountedRate']['price'])
                        break
                    #tenancy DEDICATED INSTANCE
                    elif (tenancy == 'Dedicated Instance' and rate['discountedUsageType'].endswith(dendsw + instance_type)):
                        sp_rate = float(rate['discountedRate']['price'])
                        break
                    #tenancy DEDICATED HOST
                    elif (tenancy == 'Dedicated Host' and rate['discountedUsageType'].endswith(hendsw + instance_family)):
                        sp_rate = float(rate['discountedRate']['price'])
                        break
            break

    return sp_rate


def check_input_parameters(usage_operation, tenancy, sp_type, term, purchasing_option):
    #check usage_operation
    if (usage_operation not in operation_by_platform_dict.values()):
        raise ValueError('Usage operation unknown, check the Operating System input parameter', usage_operation)
    #check tenancy
    if (tenancy not in tenancy_dict.values()):
        raise ValueError('Tenancy unknown, check Tenancy input parameter', tenancy)
    #check sp_type
    if (sp_type != "EC2InstanceSavingsPlans" and sp_type != "ComputeSavingsPlans"):
        raise ValueError('Savings Plan Type unknown, check Savings Plan Type input parameter', sp_type)
    #check term
    if (term != "1yr" and term != "3yr"):
        raise ValueError('Term unknown, check Term input parameter', term)
    #check purchasing_option
    if (purchasing_option != "No Upfront" and purchasing_option != "Partial Upfront" and purchasing_option != "All Upfront"):
        raise ValueError('Purchasing Option unknown, check Purchasing Option input parameter', purchasing_option)


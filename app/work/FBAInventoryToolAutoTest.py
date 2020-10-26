#!/usr/bin/python

import os
import sys
from urllib import urlencode
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from optparse import OptionParser


TOOL_LIST = [
    "ReconciliationTool",
    "GetBoundInventoryBreakdown",
    "GetInventorySupplyTool",
    "GetReservedInventoryBreakdown",
    "InventoryFNSkuLookup",
    "MYIQuantityUpdater",
    "MakeItSellResolver"
    #"ProvenanceQueryTool"
]

TOOL_PARAMETERS = {
    "ReconciliationTool": ["fnsku", "merchant"],
    "GetBoundInventoryBreakdown": ["fnsku", "merchant", "marketplace"],
    "GetInventorySupplyTool": ["fnsku", "merchant"],
    "GetReservedInventoryBreakdown": ["fnsku", "merchant", "marketplace"],
    "InventoryFNSkuLookup": ["fnsku", "iogId"],
    "MYIQuantityUpdater": ["fnsku", "merchant", "marketplace"],
    "MakeItSellResolver": ["fnsku", "merchant", "marketplace"]
    #"ProvenanceQueryTool": ["asin", "merchant"]
}

TOOL_URLS = {
    "USAmazon": "https://fba-inventory-console-na.amazon.com/Tool.jsp?",
    "EUAmazon": "https://fba-inventory-console-eu.dub.amazon.com/Tool.jsp?",
    "JPAmazon": "https://fba-inventory-console-fe.amazon.com/Tool.jsp?",
    "CNAmazon": "https://fba-inventory-console-cn.amazon.com/Tool.jsp"
}

TOOL_COMMON_PARAMETER_REQUEST_TRANSFORM = {
    "merchant" : "Merchant Id",
    "fnsku" : "FNSKU",
    "marketplace" : "MarketplaceId"
}

TOOL_PARAMETER_REQUEST_TRANSFORM = {
    "ReconciliationTool" : {
        "merchant" : "Merchant ID"
    },
    "MakeItSellResolver" : {
        "merchant" : "MerchantId",
        "fnsku": "ItemId"
    }
}


def check_parameters(parser, options, args):
    if not options.region or options.region not in ["USAmazon", "EUAmazon", "JPAmazon", "CNAmazon"]:
        print("[ERROR]: options -r must be set and in [%s,%s,%s,%s]" % ("USAmazon", "EUAmazon", "JPAmazon", "CNAmazon"))
        parser.print_help()
        sys.exit(-1)
    return


def get_tool_list(optionParser, options, args):
    exclude_tool_list = []
    for tool_name, tool_parameters in TOOL_PARAMETERS.items():
        for tool_parameter in tool_parameters:
            if not hasattr(options, tool_parameter):
                print("[WARN] couldn't test %s because parameter %s is not set!" % (tool_name, tool_parameter))
                exclude_tool_list.append(tool_name)
                break
    new_list = [i for i in TOOL_LIST if i not in exclude_tool_list]
    return new_list


def transform_para_key(tool_name, key):
    if tool_name in TOOL_PARAMETER_REQUEST_TRANSFORM and key in TOOL_PARAMETER_REQUEST_TRANSFORM[tool_name]:
        return TOOL_PARAMETER_REQUEST_TRANSFORM[tool_name][key]
    if key in TOOL_COMMON_PARAMETER_REQUEST_TRANSFORM:
        return TOOL_COMMON_PARAMETER_REQUEST_TRANSFORM[key]
    return key


def get_parameter_pair(tool_name, options):
    pair = dict()
    current_parameters = TOOL_PARAMETERS[tool_name]
    for current_parameter in current_parameters:
        pair[transform_para_key(tool_name, current_parameter)] = getattr(options, current_parameter)
    pair["_charset"] = "UTF-8"
    pair["tool"] = tool_name
    return pair


def pick_prefix_for_single(tool_name, options):
    parameter_pair = get_parameter_pair(tool_name, options)
    return [tool_name, TOOL_URLS[options.region] + "#execute=1&" + urlencode(parameter_pair)]


def generate_url_for_toolset(tool_list, options):
    url_list = []
    for tool in tool_list:
        url_list.append(pick_prefix_for_single(tool, options))
    return url_list


# current validate rule is to check exception string in body
def browse_and_validaet_single(driver, url, tool_name):
    driver.get(url)
    try:
        # wait for result
        result = ui.WebDriverWait(driver, 30).until(lambda x: x.find_element_by_class_name('well'))
        body = driver.find_element_by_tag_name('body')
        body_text = body.text
        if "Exception" in body_text:
            driver.get_screenshot_as_file(os.getcwd() + "/%s.png" % (tool_name))
            return "FAILURE"
        if "Required argument" in body_text:
            driver.get_screenshot_as_file(os.getcwd() + "/%s.png" % (tool_name))
            return "PARAMETER ERROR OR PARAMETER MAPPING ERROR"
        return "OK"
    except TimeoutException:
        driver.get_screenshot_as_file(os.getcwd() + "/%s.png" % (tool_name))
        return "TIMEOUT"
    except:
        driver.get_screenshot_as_file(os.getcwd() + "/%s.png" % (tool_name))
        return "UNKNOWN"


def open_browser_and_validate_batch(name2url_list, driver):
    validate_result = dict()
    for tool_name, url in name2url_list:
        cur = browse_and_validaet_single(driver, url, tool_name)
        validate_result[tool_name] = cur
        driver.execute_script("window.open('');")
        driver.switch_to_window(driver.window_handles[-1])
    return validate_result


def print_validate_result(validate_result):
    for k,v in validate_result.items():
        print("%s ======================================= %s" %(k, v))


def handle_all(tool_list, options, driver):
    name2url_list = generate_url_for_toolset(tool_list, options)
    for pair in name2url_list:
        print("%s === %s" %(pair[0], pair[1]))
        print("\n")
    validate_result = open_browser_and_validate_batch(name2url_list, driver)
    driver.close()
    print_validate_result(validate_result)


# usage: python FBAInventoryToolAutoTest.py --fnsku X000ZNCGVV --merchant 9854324825 --region EUAmazon --marketplace 338801
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--fnsku", action="store", type="string", dest='fnsku')
    parser.add_option("-s", "--merchant", action="store", type="string", dest='merchant', help="unencrypted merchant")
    parser.add_option("-m", "--marketplace", action="store", type="string", dest='marketplace', help="valid marketplace")
    parser.add_option("-r", "--region", action="store", type="string", dest='region', help="must be USAmazon, EUAmazon, JPAmazon, CNAmzon")
    options, args = parser.parse_args()
    check_parameters(parser, options, args)
    tool_list = get_tool_list(parser, options, args)

    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    driver.maximize_window()
    handle_all(tool_list, options, driver)


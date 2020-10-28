import boto3
import sys
from boto3.dynamodb.conditions import Key, Attr
import json
from string import Template

# user define lib
sys.path.append('..')
from gim_common.color_log import *
from gim_migration.constants import *

# for merchant level record, integration seller has MERCHANT_LEVEL_RECORD_NUMBER for one table.
MERCHANT_LEVEL_RECORD_NUMBER = 3

META_TABLE_MIGRATION_TABLE_NAME = 'TableMigrationStatus'
META_PA_MIGRATION_TABLE_NAME = 'PAMigrationStatus'


def generate_MSKUInventoryRecords(pa_id, merchantid, size):
    msku_items = []
    record = Template(MSKU_TEMPLATE)
    for i in range(0, size):
        fnsku = "TestFnsku" + str(i)
        mp = 1
        msku = "TestMsku" + str(i)
        cur_record = record.substitute(PAID=pa_id, MERCHANTID=merchantid,
                                       FNSKU=fnsku, MP=mp, MSKU=msku)
        new_item = json.loads(cur_record)
        msku_items.append(new_item)
    return msku_items


def generate_MerchantInStockRate(pa_id, merchantid, length):
    items = []
    record = Template(MerchantInStockRate)
    mps = [1, 7, 77170]
    for mp in mps:
        cur_record = record.substitute(PAID=pa_id, MERCHANTID=merchantid, MP=mp)
        new_item = json.loads(cur_record)
        items.append(new_item)
    return items


def generate_MerchantInventoryAge(pa_id, merchantid, length):
    items = []
    record = Template(MerchantInventoryAge)
    mps = [1, 7, 77170]
    for mp in mps:
        cur_record = record.substitute(PAID=pa_id, MERCHANTID=merchantid, MP=mp)
        new_item = json.loads(cur_record)
        items.append(new_item)
    return items


def generate_MerchantQuantityLimitation(pa_id, merchantid, length):
    items = []
    record = Template(MerchantQuantityLimitation)
    country_code = ["US", "CA", "MX"]
    for cc in country_code:
        cur_record = record.substitute(PAID=pa_id, MERCHANTID=merchantid, CC=cc)
        new_item = json.loads(cur_record)
        items.append(new_item)
    return items


def generate_MerchantSellThrough(pa_id, merchantid, length):
    items = []
    record = Template(MerchantSellThrough)
    mps = [1, 7, 77170]
    for mp in mps:
        cur_record = record.substitute(PAID=pa_id, MERCHANTID=merchantid, MP=mp)
        new_item = json.loads(cur_record)
        items.append(new_item)
    return items


def generate_MerchantStrandedInventory(pa_id, merchantid, length):
    items = []
    record = Template(MerchantStrandedInventory)
    mps = [1, 7, 77170]
    for mp in mps:
        cur_record = record.substitute(PAID=pa_id, MERCHANTID=merchantid, MP=mp)
        new_item = json.loads(cur_record)
        items.append(new_item)
    return items


def generate_MerchantUtilization(pa_id, merchantid, length):
    items = []
    record = Template(MerchantUtilization)
    country_code = ["US", "CA", "MX"]
    for cc in country_code:
        cur_record = record.substitute(PAID=pa_id, MERCHANTID=merchantid, CC=cc)
        new_item = json.loads(cur_record)
        items.append(new_item)
    return items


def generate_MerchantVolumeAllocation(pa_id, merchantid, length):
    items = []
    record = Template(MerchantVolumeAllocation)
    country_code = ["US", "CA", "MX"]
    for cc in country_code:
        cur_record = record.substitute(PAID=pa_id, MERCHANTID=merchantid, CC=cc)
        new_item = json.loads(cur_record)
        items.append(new_item)
    return items


def generate_MerchantConfiguration(pa_id, merchantid, length):
    items = []
    return items


def create_record_for_one_table(dynamodb, pa_id, merchantid, table_name, size):
    table = dynamodb.Table(table_name)
    items = GENERATE_RECORDS_MAP[table_name](pa_id, merchantid, size)
    for item in items:
        table.put_item(Item=item)
    ColorLog.info("created {} records finished".format(table_name))


def create_records_for_all_tables(pa_id, merchantid, size):
    dynamodb = boto3.resource('dynamodb')
    for table_name in GENERATE_RECORDS_MAP:
        ColorLog.info("start to create items for paid - {}, table - {}".format(pa_id, table_name))
        create_record_for_one_table(dynamodb, pa_id, merchantid, table_name, size)
        ColorLog.info("create items for paid - {}, table - {} finish".format(pa_id, table_name))


GENERATE_RECORDS_MAP = {
    'MSKUInventoryRecord': generate_MSKUInventoryRecords,
    'MerchantInStockRate': generate_MerchantInStockRate,
    'MerchantInventoryAge': generate_MerchantInventoryAge,
    'MerchantQuantityLimitation': generate_MerchantQuantityLimitation,
    'MerchantSellThrough': generate_MerchantSellThrough,
    'MerchantStrandedInventory': generate_MerchantStrandedInventory,
    'MerchantUtilization': generate_MerchantUtilization,
    'MerchantVolumeAllocation': generate_MerchantVolumeAllocation,
    'MerchantConfiguration': generate_MerchantConfiguration
}


def generate_MSKUInventoryRecords_delete_key(item):
    return {
        'HashKey': item['HashKey'],
        'RangeKey': item['RangeKey']
    }


def generate_other_delete_key(item):
    return {
        'Id': item['Id'],
        'RangeKey': item['RangeKey']
    }


def generate_MerchantConfiguration_delete_key(item):
    return {
        'PartnerAccountId': item['PartnerAccountId'],
        'ConfigurationType': item['ConfigurationType']
    }


def generate_PAMigrationStatus_delete_key(item):
    return {
        'PAIdPair': item['PAIdPair'],
        'MigrationRole': item['MigrationRole']
    }


def generate_TableMigrationStatus_delete_key(item):
    return {
        'PAIdPair': item['PAIdPair'],
        'TableRole': item['TableRole']
    }


DELETE_MAP = {
    'MSKUInventoryRecord': generate_MSKUInventoryRecords_delete_key,
    'MerchantInStockRate': generate_other_delete_key,
    'MerchantInventoryAge': generate_other_delete_key,
    'MerchantQuantityLimitation': generate_other_delete_key,
    'MerchantSellThrough': generate_other_delete_key,
    'MerchantStrandedInventory': generate_other_delete_key,
    'MerchantUtilization': generate_other_delete_key,
    'MerchantVolumeAllocation': generate_other_delete_key,
    'MerchantConfiguration': generate_MerchantConfiguration_delete_key,
    META_PA_MIGRATION_TABLE_NAME: generate_PAMigrationStatus_delete_key,
    META_TABLE_MIGRATION_TABLE_NAME: generate_TableMigrationStatus_delete_key
}


def delete_msku_items(dynamodb, pa_id, table_name):
    table_handler = dynamodb.Table(table_name)
    done = False
    start_key = None
    scan_kwargs = {
        'FilterExpression': Attr('PartnerAccountId').eq(pa_id)
    }
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table_handler.scan(**scan_kwargs)
        items = response['Items']
        for item in items:
            table_handler.delete_item(Key=DELETE_MAP[table_name](item))
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None


def clean_meta_tables(source_pa_id, destination_pa_id):
    dynamodb = boto3.resource('dynamodb')
    for table_name in [META_PA_MIGRATION_TABLE_NAME, META_TABLE_MIGRATION_TABLE_NAME]:
        ColorLog.info("delete items paid pair {}/{} for table {}".
                      format(source_pa_id, destination_pa_id, table_name))
        table_handler = dynamodb.Table(table_name)
        response = table_handler.query(KeyConditionExpression=Key("PAIdPair").
                                       eq("{}/{}".format(source_pa_id, destination_pa_id)))
        items = response['Items']
        for item in items:
            table_handler.delete_item(Key=DELETE_MAP[table_name](item))
        ColorLog.info("delete items paid pair {}/{} for table {} finish".
                      format(source_pa_id, destination_pa_id, table_name))


def delete_all_items(pa_id):
    ColorLog.info("start to delete items for paid - {}".format(pa_id))
    dynamodb = boto3.resource('dynamodb')
    for table_name in GENERATE_RECORDS_MAP:
        table_handler = dynamodb.Table(table_name)
        if table_name == "MSKUInventoryRecord":
            delete_msku_items(dynamodb, pa_id, table_name)
        else:
            id_key = "PartnerAccountId" if table_name == "MerchantConfiguration" else "Id"
            response = table_handler.query(KeyConditionExpression=Key(id_key).eq(pa_id))
            items = response['Items']
            for item in items:
                table_handler.delete_item(Key=DELETE_MAP[table_name](item))
        ColorLog.info("delete items for table {} finish".format(table_name))
    ColorLog.info("delete all tables finish for paid - {}".format(pa_id))


def check_msku_items_deprecated(dynamodb, paid, table_name, msku_size):
    table_handler = dynamodb.Table(table_name)
    deprecated_total = 0
    done = False
    start_key = None
    scan_kwargs = {
        'FilterExpression': Attr('PartnerAccountId').eq(paid)
    }
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table_handler.scan(**scan_kwargs)
        items = response['Items']
        for item in items:
            if 'RecordStatus' in item and item['RecordStatus'] == 'DEPRECATED':
                deprecated_total += 1
            else:
                ColorLog.error('item not deprecated')
                ColorLog.error(item)
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
    if deprecated_total != msku_size:
        ColorLog.error("msku deprecated number error ! expected - {}, actual - {}"
                       .format(msku_size, deprecated_total))
    else:
        ColorLog.info("check deprecated msku numbers OK!")


def check_old_records_deprecated(app_config, paid, msku_size):
    dynamodb = boto3.resource('dynamodb')
    for table_name in GENERATE_RECORDS_MAP:
        table_handler = dynamodb.Table(table_name)
        if table_name == "MSKUInventoryRecord":
            check_msku_items_deprecated(dynamodb, paid, table_name, msku_size)
        elif table_name == "MerchantConfiguration":
            ColorLog.info("skip MerchantConfiguration deprecated check.")
        else:
            id_key = "PartnerAccountId" if table_name == "MerchantConfiguration" else "Id"
            deprecated_total = 0
            response = table_handler.query(KeyConditionExpression=Key(id_key).eq(paid))
            items = response['Items']
            for item in items:
                if 'RecordStatus' in item and item['RecordStatus'] == 'DEPRECATED':
                    deprecated_total += 1
                else:
                    ColorLog.error('item not deprecated')
                    ColorLog.error(item)
            if deprecated_total != MERCHANT_LEVEL_RECORD_NUMBER:
                ColorLog.error("{} deprecated number error ! expected - {}, actual - {}"
                               .format(table_name, MERCHANT_LEVEL_RECORD_NUMBER, deprecated_total))
            else:
                ColorLog.info("check deprecated for table {} numbers OK!".format(table_name))
    ColorLog.info("check_old_records_deprecated done for paid - {}".format(paid))


def compare_items(expected_items, new_items, table_name):
    all_find = True
    for new_item in new_items:
        find = False
        order_new_item = []
        for i in sorted(new_item):
            order_new_item.append((i, new_item[i]))
        for expected_item in expected_items:
            order_expected_item = []
            for j in sorted(expected_item):
                order_expected_item.append((j, expected_item[j]))
            if new_item == expected_item:
                find = True
        if not find:
            ColorLog.error("can't find new item in expected_items")
            ColorLog.error(new_item)
            all_find = False
    if all_find:
        ColorLog.info("check {} fields OK!".format(table_name))


def compare_items_after_migration(new_items, table_name, pa_id, merchantid1, merchantid2, size):
    expected_items1 = GENERATE_RECORDS_MAP[table_name](pa_id, merchantid1, int(size / 2))
    expected_items2 = GENERATE_RECORDS_MAP[table_name](pa_id, merchantid2, int(size / 2))
    expected_items = expected_items1
    expected_items.extend(expected_items2)
    compare_items(expected_items, new_items, table_name)


def check_msku_items_exists(paid, table_name, size, merchantid1, merchantid2):
    dynamodb = boto3.resource('dynamodb')
    table_handler = dynamodb.Table(table_name)
    done = False
    start_key = None
    scan_kwargs = {
        'FilterExpression': Attr('PartnerAccountId').eq(paid)
    }
    total_size = 0
    new_items = []
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table_handler.scan(**scan_kwargs)
        items = response['Items']
        total_size += len(items)
        new_items.extend(items)
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
    if total_size != size:
        ColorLog.error(
            "check msku number error ! source size - {}, destination size - {}".format(size, total_size))
    else:
        ColorLog.info("check msku total number OK!")
    compare_items_after_migration(new_items, "MSKUInventoryRecord", paid, merchantid1, merchantid2, size)


def check_new_records_exists(app_config, paid, msku_size, source_count, merchantid1, merchantid2):
    dynamodb = boto3.resource('dynamodb')
    for table_name in GENERATE_RECORDS_MAP:
        table_handler = dynamodb.Table(table_name)
        if table_name == "MSKUInventoryRecord":
            check_msku_items_exists(paid, table_name, msku_size * source_count, merchantid1, merchantid2)
        elif table_name == "MerchantConfiguration":
            ColorLog.info("skip MerchantConfiguration new record check.")
        else:
            id_key = "PartnerAccountId" if table_name == "MerchantConfiguration" else "Id"
            total_size = 0
            response = table_handler.query(KeyConditionExpression=Key(id_key).eq(paid))
            new_items = []
            items = response['Items']
            total_size += len(items)
            new_items.extend(items)
            if total_size != source_count * MERCHANT_LEVEL_RECORD_NUMBER:
                ColorLog.error("check {} number error ! expected - {}, acutal - {}".
                               format(table_name, source_count * MERCHANT_LEVEL_RECORD_NUMBER, total_size))
            else:
                ColorLog.info("check {} number OK!".format(table_name))
            compare_items_after_migration(new_items, table_name, paid, merchantid1, merchantid2,
                                          MERCHANT_LEVEL_RECORD_NUMBER)
    ColorLog.info("check all tables finish")


def check_migration_meta_status(app_config, source_paid, destination_paid, role):
    """
    check migration table status update as expected.
    PAMigrationStatus
        sender/receiver entry exists.
        sender/receiver mark to finish
    TableMigrationStatus
        sender/receiver entry exists.
        sender/receiver mark to finish
    :param app_config:
    :param paid:
    :return:
    """
    # check TableMigrationStatus
    ColorLog.info("check TableMigrationStatus start, source paid - {}, destination paid - {}, role - {}"
                  .format(source_paid, destination_paid, role))
    hashkey = "{}/{}".format(source_paid, destination_paid)
    dynamodb = boto3.resource('dynamodb')
    table_handler = dynamodb.Table(META_TABLE_MIGRATION_TABLE_NAME)
    response = table_handler.query(KeyConditionExpression=Key('PAIdPair').eq(hashkey))
    items = response['Items']
    migration_table_number = 0
    expected_number = len(GENERATE_RECORDS_MAP)
    for item in items:
        if item['MigrationRole'] == role:
            migration_table_number += 1
        else:
            continue
        if item['MigrationStatus'] != "FINISH":
            ColorLog.error("TableMigrationStatus MigrationStatus is not correct")
            ColorLog.error(item)
    if migration_table_number != expected_number:
        ColorLog.error("TableMigrationStatus number is not correct, expected - {}, actual - {}"
                       .format(expected_number, migration_table_number))
    # check PAMigrationStatus
    ColorLog.info("check PAMigrationStatus start, source paid - {}, destination paid - {}, role - {}"
                  .format(source_paid, destination_paid, role))
    pa_table_handler = dynamodb.Table(META_PA_MIGRATION_TABLE_NAME)
    response = pa_table_handler.query(KeyConditionExpression=Key('PAIdPair').eq(hashkey))
    pa_items = response['Items']
    for pa_item in pa_items:
        if pa_item['MigrationRole'] != role:
            continue
        if pa_item['MigrationStatus'] != "FINISH":
            ColorLog.error("PAMigrationStatus MigrationStatus is not correct")
            ColorLog.error(item)
    ColorLog.info("check migration meta for source paid - {}, destination paid - {}, role - {} finish"
                  .format(source_paid, destination_paid, role))

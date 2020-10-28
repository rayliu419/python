import sys
import datetime
import time
import json

# user define lib
sys.path.append('..')
from gim_common.app_config import *
from gim_common.color_log import *
from gim_common.door_keeper import *
from gim_migration.ddb_steps import *
from gim_migration.sqs_steps import *


def set_beta_session(app_config, region):
    if region == "na":
        profile = app_config.get_profile_beta_na()
        ColorLog.info("using beta na")
    elif region == "eu":
        profile = app_config.get_profile_beta_eu()
        ColorLog.info("using beta eu")
    else:
        profile = app_config.get_profile_beta_fe()
        ColorLog.info("using beta fe")
    boto3.setup_default_session(profile_name=profile)
    session = boto3.session.Session(profile_name=profile)
    credentials = session.get_credentials().get_frozen_credentials()
    return credentials


def print_section(string):
    ColorLog.info("=" * 80)
    ColorLog.info(string)
    ColorLog.info("=" * 80)


if __name__ == '__main__':
    '''
    1. mock records for source pa id. 
    2. send merge notification to destination pa id.
    3. wait for data migration.
    4. check old records are deprecated.
    5. check new records are migrated.
    6. check migration meta tables are updated correctly. 
    '''
    DoorKeeper.guard()
    app_config = AppConfig()
    paid1 = 'amzn1.pa.o.{}{}'.format('sourcepaid1', datetime.datetime.now().strftime('%Y%m%d'))
    paid2 = 'amzn1.pa.o.{}{}'.format('sourcepaid2', datetime.datetime.now().strftime('%Y%m%d'))
    merchantid1 = 333
    merchantid2 = 666
    paid3 = 'amzn1.pa.o.{}{}'.format('destinationpaid3', datetime.datetime.now().strftime('%Y%m%d'))
    region1 = 'NA'
    region2 = 'NA'
    region3 = 'EU'
    # msku_size must be odd.
    msku_size = 10
    ColorLog.info("integration for merge event - ")
    merge_info = {
        "source paid1:": paid1,
        "source merchantid1:": merchantid1,
        "source region1:": region1,
        "source paid2:": paid2,
        "source merchantid2:": merchantid2,
        "source region2:": region2,
        "destination paid:": paid3,
        "destination region:": region3,
        "mock msku size:": msku_size
    }
    beautiful_format = json.dumps(merge_info, indent=4, ensure_ascii=False)
    ColorLog.info(beautiful_format)
    ColorLog.info(merge_info)

    print_section("clean env")
    set_beta_session(app_config, "na")
    delete_all_items(paid1)
    delete_all_items(paid2)
    clean_meta_tables(paid1, paid3)
    clean_meta_tables(paid2, paid3)
    set_beta_session(app_config, "eu")
    delete_all_items(paid3)
    clean_meta_tables(paid1, paid3)
    clean_meta_tables(paid2, paid3)

    print_section("create records for source pa id")
    # create records for paid1 and paid2
    set_beta_session(app_config, "na")
    create_records_for_all_tables(paid1, merchantid1, msku_size)
    create_records_for_all_tables(paid2, merchantid2, msku_size)

    print_section("send merge event to destination region")
    # send notification to destination
    set_beta_session(app_config, "eu")
    send_merge_notification(app_config, paid1, paid2, paid3, region1, region2, region3)

    # # check result, sleep for 10 mins.
    print_section("wait 10 mins for migration")
    time.sleep(10 * 60)

    print_section("check deprecated records")
    set_beta_session(app_config, "na")
    check_old_records_deprecated(app_config, paid1, msku_size)
    check_old_records_deprecated(app_config, paid2, msku_size)
    # check new result

    print_section("check new records")
    set_beta_session(app_config, "eu")
    check_new_records_exists(app_config, paid3, msku_size, 2, merchantid1, merchantid2)

    print_section("wait 15 mins for migration meta update.")
    time.sleep(20 * 60)
    # check migration meta data.

    print_section("check migration meta tables")
    set_beta_session(app_config, "na")
    check_migration_meta_status(app_config, paid1, paid3, "SENDER")
    check_migration_meta_status(app_config, paid2, paid3, "SENDER")
    set_beta_session(app_config, "eu")
    check_migration_meta_status(app_config, paid1, paid3, "RECEIVER")
    check_migration_meta_status(app_config, paid2, paid3, "RECEIVER")

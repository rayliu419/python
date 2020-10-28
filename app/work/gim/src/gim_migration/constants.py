MSKU_TEMPLATE = '''
{
    "Asin": "B005FTACG8",
    "Bound": 0,
    "BuyableInTransit": 0,
    "CurrentDos": 999,
    "CustomerOrders": 7,
    "CustomerShipDisabled": 0,
    "Encumbered": 21,
    "Fnsku": "${FNSKU}",
    "Fulfillable": 979,
    "FulfillableBound": 0,
    "HashKey": "${PAID}_${FNSKU}",
    "IapFulfillableTimestamp": 1598905447237,
    "IapInboundTimestamp": 1581129333767,
    "IapTimestamp": 1598905447237,
    "IapUnfulfillableTimestamp": 1598905447237,
    "InventorySegmentId": 9001,
    "IsBuyabilityExist": "N",
    "IsListingExisted": "N",
    "MarketplaceId": $MP,
    "MerchantCustomerId": ${MERCHANTID},
    "MerchantSku": "${MSKU}",
    "PartnerAccountId": "${PAID}",
    "PendingCustomerOrderInTransit": 0,
    "PlanningDos": 999,
    "RangeKey": "${MERCHANTID}_${MP}_${MSKU}",
    "Receiving": 0,
    "Shipped": 0,
    "Timestamp": 1598905449012,
    "TransShipmentsTotalQuantity": 14,
    "Unfulfillable": 0,
    "Working": 0
}
'''

MerchantInStockRate = '''
{
    "EstimateLost": "-1.0000000000",
    "Id": "${PAID}",
    "InStockRate": 0,
    "InventorySegmentId": 1,
    "MarketplaceId": ${MP},
    "MerchantCustomerId": ${MERCHANTID},
    "PartnerAccountId": "${PAID}",
    "RangeKey": "${MERCHANTID}_${MP}",
    "SnapshotDatetime": "2020-08-20",
    "Timestamp": 1597881600
}
'''

MerchantInventoryAge = '''
{
    "ActiveListingCount": 0,
    "GvBandGCount": 0,
    "Id": "${PAID}",
    "InventorySegmentId": 1,
    "isRecordDeleted": "N",
    "ListingCountShippedT30": 0,
    "ListingCountShippedT60": 0,
    "ListingCountShippedT7": 0,
    "ListingCountShippedT90": 0,
    "MarketplaceId": ${MP},
    "MerchantCustomerId": ${MERCHANTID},
    "PartnerAccountId": "${PAID}",
    "RangeKey": "${MERCHANTID}_${MP}",
    "SellableQtyAge0To90": 0,
    "SellableQtyAge181To270": 1,
    "SellableQtyAge271To365": 0,
    "SellableQtyAge365Plus": 0,
    "SellableQtyAge91To180": 0,
    "SnapshotDatetime": "2020-07-29",
    "Timestamp": 1595980800,
    "UnitsShippedT30": 0,
    "UnitsShippedT60": 0,
    "UnitsShippedT7": 0,
    "UnitsShippedT90": 0
}
'''

MerchantQuantityLimitation = '''
{
    "CountryCode": "${CC}",
    "EffectiveDate": "2020-07-08",
    "Id": "${PAID}",
    "InventorySegmentId": 5,
    "LimitValue": 18,
    "MerchantCustomerId": ${MERCHANTID},
    "PartnerAccountId": "${PAID}",
    "RangeKey": "${CC}_${MERCHANTID}_SORTABLE",
    "RunDate": "2020-08-19",
    "SnapshotDatetime": "2020-08-20",
    "StorageType": "SORTABLE",
    "Timestamp": 1597881600
}
'''

MerchantSellThrough = '''
{
    "Id": "${PAID}",
    "InventorySegmentId": 1,
    "MarketplaceId": ${MP},
    "MerchantCustomerId": ${MERCHANTID},
    "PartnerAccountId": "${PAID}",
    "RangeKey": "${MERCHANTID}_${MP}",
    "SellThrough": "0.0",
    "SnapshotDatetime": "2020-08-20",
    "Timestamp": 1597881600,
    "UnitShippedT90": 0
}
'''

MerchantStrandedInventory = '''
{
    "Id": "${PAID}",
    "InventorySegmentId": 3,
    "isRecordDeleted": "N",
    "MarketplaceId": ${MP},
    "MerchantCustomerId": ${MERCHANTID},
    "PartnerAccountId": "${PAID}",
    "RangeKey": "${MERCHANTID}_${MP}",
    "SnapshotDatetime": "2020-07-30",
    "StrandedUnit": 3,
    "Timestamp": 1596067200
}
'''

MerchantUtilization = '''
{
    "AllocationNetworkId": 1,
    "countryCode": "${CC}",
    "Id": "${PAID}",
    "InventorySegmentId": 1,
    "MerchantCustomerId": ${MERCHANTID},
    "PartnerAccountId": "${PAID}",
    "Quantity": 3,
    "RangeKey": "${MERCHANTID}_${CC}_SORTABLE",
    "SnapshotDatetime": "2020-08-20",
    "StorageType": "SORTABLE",
    "Timestamp": 1597881600,
    "Volume": 290,
    "VolumeMeasurementUnit": "CUBIC_INCH"
}
'''

MerchantVolumeAllocation = '''
{
    "Allocation": 0,
    "Id": "${PAID}",
    "InventorySegmentId": 1,
    "MerchantCustomerId": ${MERCHANTID},
    "PartnerAccountId": "${PAID}",
    "RangeKey": "${CC}_${MERCHANTID}_APPAREL",
    "ReasonCode": "SMS_PRO",
    "SnapshotDatetime": "2020-08-20",
    "StorageType": "APPAREL",
    "Timestamp": 1597881600,
    "CountryCode": "${CC}"
}
'''
from string import Template
import boto3
import sys
# user define lib
sys.path.append('..')
from gim_common.color_log import *

PARAM_EVENT_QUEUE_NAME = "ParamServiceEventQ"

MERGE_NOTIFICATION_STRING = '''
{
  "Type": "Notification",
  "MessageId": "a86f2753-7ec6-5626-aa69-70fea682a743",
  "TopicArn": "arn:aws:sns:eu-west-1:254997944360:PartnerAccountMerging",
  "Message": "{\\"CreatedFrom\\":[{\\"PartnerAccountId\\":\\"$PAID1\\",\\"HomePod\\":{\\"PodName\\":\\"505328a79e62be65323cadeb8eb7622c\\",\\"Regions\\":[{\\"Name\\":\\"$REGION1\\"}]}},{\\"PartnerAccountId\\":\\"$PAID2\\",\\"HomePod\\":{\\"PodName\\":\\"12dc953c3829885283ec67ed9d209dbd\\",\\"Regions\\":[{\\"Name\\":\\"$REGION2\\"}]}}],\\"MergedTo\\":{\\"PartnerAccountId\\":\\"$PAID3\\",\\"HomePod\\":{\\"PodName\\":\\"12dc953c3829885283ec67ed9d209dbd\\",\\"Regions\\":[{\\"Name\\":\\"$REGION3\\"}]}}}",
  "Timestamp": "2020-09-14T11:44:04.561Z",
  "SignatureVersion": "1",
  "Signature": "XwILqlNMAd8Cnb/2ydbA2fb3kbR660GVGrXSzVeW9pELbTT1UvIXj/Mw9jJMVG0+cDBjrXoCty6S7aNgHymQYsCWWTQNxu5B/luOobsh9/EQ1qnNIu5ZneFm0jWlS08qUc2EcRFKuLOGlvZ3D8woe8qh6YXXmflBD6kTUEN2QvL85lhk50WeYaKZ7ckdsvj6Jp/jgx8m5vncVSt7/tR0VxUJCfpVSjXBYqhBXWJ05kIPG2g8i3rFa2ybMVM9d5DkSidnEThlKOzg+DnOYSXFNz2iyno7xxZvre2f1aeJXhELYRCXPW09/4C16LtzbtmBu0qhESCMH72jpsLxMzZhbg==",
  "SigningCertURL": "https://sns.eu-west-1.amazonaws.com/SimpleNotificationService-a86cb10b4e1f29c941702d737128f7b6.pem",
  "UnsubscribeURL": "https://sns.eu-west-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-1:254997944360:PartnerAccountMerging:640e249c-0e05-4358-8149-7a02bc1f6bb5",
  "MessageAttributes": {
    "NotificationType": {
      "Type": "String",
      "Value": "PARTNER_ACCOUNTS_MERGED"
    },
    "PartnerAccountId": {
      "Type": "String",
      "Value": "$PAID3"
    },
    "TombstonedPartnerAccountIds": {
      "Type": "String.Array",
      "Value": "[\\"$PAID1\\",\\"$PAID2\\"]"
    }
  }
}
'''


def send_merge_notification(app_config, paid1, paid2, paid3, region1, region2, region3):
    doc = Template(MERGE_NOTIFICATION_STRING)
    notification = doc.substitute(PAID1=paid1, PAID2=paid2, PAID3=paid3, REGION1=region1, REGION2=region2, REGION3=region3)
    ColorLog.info(notification)
    sqs_client = boto3.client('sqs')
    queues = sqs_client.list_queues(QueueNamePrefix=PARAM_EVENT_QUEUE_NAME)
    queue_url = queues['QueueUrls'][0]
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=notification
    )
    ColorLog.info(response)
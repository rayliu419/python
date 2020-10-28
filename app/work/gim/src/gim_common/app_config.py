import configparser

CONFIG_PATH = "../../conf/config.ini"


class AppConfig:
    """
    You need have configs in ~/.aws/config and ~/.aws/credentials
    ~/.aws/config like:
    [profile gim-beta-na]
    region = us-east-1
    output = json

    [profile gim-beta-eu]
    region = eu-west-1
    output = json

    [profile gim-beta-fe]
    region = us-west-2
    output = json

    ~/.aws/credentials like:
    [gim-beta-na]
    aws_access_key_id=xxx
    aws_secret_access_key=yyy

    [gim-beta-fe]
    aws_access_key_id=xxx
    aws_secret_access_key=yyy

    [gim-beta-eu]
    aws_access_key_id=xxx
    aws_secret_access_key=yyy
    """
    def __init__(self):
        self.app_config = configparser.ConfigParser()
        self.app_config.read(CONFIG_PATH, encoding="utf-8")
        print(self.app_config.sections())

    def get_profile_beta_na(self):
        return self.app_config["profile"]["gim_beta_na"]

    def get_profile_beta_eu(self):
        return self.app_config["profile"]["gim_beta_eu"]

    def get_profile_beta_fe(self):
        return self.app_config["profile"]["gim_beta_fe"]

    def get_esendpoint_by_profile_name(self, profile_name):
        return self.app_config["esendpoint"][profile_name]
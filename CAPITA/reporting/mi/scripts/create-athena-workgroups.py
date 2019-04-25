import boto3
import yaml
from pathlib import Path
import sys

athena = boto3.client("athena")

"""
Usage:
python create-athena-workgroups.py DEPT ENV

"""


def fill_config(values, conf):
    if isinstance(conf, dict):
        for k, v in conf.items():
            if isinstance(v, str):
                conf[k] = fill_string(values, v)
            if isinstance(v, list):
                new_list = []
                for i in v:
                    new_list.append(fill_config(values, i))
                conf[k] = new_list
            if isinstance(v, dict):
                fill_config(values, v)
    elif isinstance(conf, list):
        for i in conf:
            fill_config(values, i)
    elif isinstance(conf, str):
        return fill_string(values, conf)


def fill_string(values: dict, s: str):
    for k, v in values.items():
        if k in s:
            s = s.replace(k, v)
    return s


def list_workgroups():
    return [wg.get("Name") for wg in athena.list_work_groups().get('WorkGroups')]


def main():
    d = {
        '[department]': sys.argv[1],
        '[env]': sys.argv[2],
        '[env_lower]': sys.argv[2].lower()
    }

    directory = Path(__file__).parents[0]

    with open(directory / "../modules/base-common/conf/athena-workgroups.yml") as f:
        config = yaml.safe_load(f)
        fill_config(d, config)

        existing_wgroups = list_workgroups()

        for workgroupconfig in config:
            wgroupname = [*workgroupconfig][0]
            wconfig = workgroupconfig[wgroupname]

            if wgroupname in existing_wgroups:
                print(f"Updating workgroup '{wgroupname}'")
                try:
                    athena.update_work_group(
                        WorkGroup=wgroupname,
                        ConfigurationUpdates={
                            'ResultConfigurationUpdates': {
                                'OutputLocation': wconfig.get('query-location'),
                                'EncryptionConfiguration': {
                                    'EncryptionOption': wconfig.get('encryption', "SSE_S3")
                                }
                            }
                        },
                        Description=wconfig.get("description")
                    )
                except Exception as e:
                    print(f"Unable to update: {str(e)}")
                    exit(1)
            else:
                print(f"Creating workgroup '{wgroupname}'")
                tags = []
                for tag in wconfig.get("tags"):
                    key = tag[0:tag.rfind(":")]
                    val = tag[tag.rfind(":") + 1:]
                    tags.append({'Key': key, 'Value': val})

                try:
                    athena.create_work_group(
                        Name=wgroupname,
                        Configuration={
                            'ResultConfiguration': {
                                'OutputLocation': wconfig.get('query-location'),
                                'EncryptionConfiguration': {
                                    'EncryptionOption': wconfig.get('encryption')
                                }
                            }
                        },
                        Description=wconfig.get("description"),
                        Tags=tags
                    )
                except Exception as e:
                    print(f"Unable to create: {str(e)}")
                    exit(1)


if __name__ == '__main__':
    sys.exit(main())

import os
import re
import requests
from glob import glob

# 设置仓库地址、用户名和密码
gitea_url = "http://10.3.141.1:3000"

# 要上传的文件目录
directory = "./whl/*"

# 遍历目录中的文件
for filepath in glob(directory):
    filename = os.path.basename(filepath)
    # 从文件名中解析包名和版本号
    match = re.match(r"^(.+)-(.+)-.*\.whl$", filename)
    if match:
        package_name = match.group(1).split('-')[0].replace('_', '-')
        package_version = match.group(1).split('-')[1]
        # 检查文件是否存在
        response = requests.get(f"{gitea_url}/AUO/-/packages/pypi/{package_name}/{package_version}")
        # 如果文件不存在，则上传
        if response.status_code == 404:
            os.system(f"python -m twine upload --repository gitea --config-file ./.pypirc {filepath} --verbose")
        else:
            print(f"Skipping existing file: {filename}")
    else:
        print(f"Invalid filename format: {filename}")

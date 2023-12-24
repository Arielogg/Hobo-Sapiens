from yolk.pypi import CheeseShop

def get_latest_version(package_name):
    shop = CheeseShop()
    versions = shop.package_releases(package_name)
    if not versions:  # No versions found in PyPi
        return None
    return versions[0]  # Return latest version

def update_requirements(file_path):
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            package = line.strip().split('==')[0]
            latest_version = get_latest_version(package)
            if latest_version:
                lines.append(f'{package}=={latest_version}\n')
                print(f'{package}: updated to version {latest_version}')
            else:
                lines.append(line)
                print(f'{package}: not found on PyPi or already at latest version')

    with open(file_path, 'w') as file:
        file.writelines(lines)

update_requirements('src/main/python/crawler_utils/requirements.txt')
update_requirements('src/main/resources/requirements.txt')
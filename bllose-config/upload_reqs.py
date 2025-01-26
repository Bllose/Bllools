import toml

# 读取 requirements.txt 文件
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()

# 读取 pyproject.toml 文件
with open('pyproject.toml', 'r', encoding='utf-8') as f:
    pyproject = toml.load(f)

# 添加依赖到 pyproject.toml
dependencies = pyproject['tool']['poetry']['dependencies']
for req in requirements:
    package, version = req.split('==')
    dependencies[package] = f"=={version}"

# 将修改后的内容写回 pyproject.toml
with open('pyproject.toml', 'w', encoding='utf-8') as f:
    toml.dump(pyproject, f)
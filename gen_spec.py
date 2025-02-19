import os
import ast
import sys


class ImportFinder(ast.NodeVisitor):
    def __init__(self):
        self.imports = set()

    def visit_Import(self, node):
        for name in node.names:
            self.imports.add(name.name.split('.')[0])

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module.split('.')[0])


def analyze_file_imports(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())
    finder = ImportFinder()
    finder.visit(tree)
    return finder.imports


def is_stdlib_module(module_name):
    if module_name in sys.stdlib_module_names:
        return True
    try:
        spec = __import__(module_name).__spec__
        return spec and 'site-packages' not in spec.origin
    except (ImportError, AttributeError):
        return False


def get_project_imports():

    base_imports = [
        'cn', 'config', 'en', 'loguru', 'rich',
        'win32api', 'win32con', 'yaml'
    ]

    exclude_modules = {
        'matplotlib', 'tkinter', 'cv2', 'numpy',
        'PIL', 'PIL._imagingtk', 'PIL._tkinter_finder',
        'scipy', 'pandas', 'pyautogui'
    }

    imports = set()
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                file_imports = analyze_file_imports(file_path)
                imports.update(file_imports)

    # 过滤掉标准库和排除的模块
    project_imports = {imp for imp in imports if not is_stdlib_module(imp) and imp not in exclude_modules}

    # 添加基础导入
    project_imports.update(base_imports)

    return sorted(list(project_imports))


def get_project_data_files():
    data_files = []
    directories = ['core', 'utils', 'logs', 'lang', 'score', 'trans']

    for directory in directories:
        if os.path.exists(directory):
            data_files.append((directory, directory))

    if os.path.exists('config.yaml'):
        data_files.append(('config.yaml', '.'))

    return data_files


def generate_spec_file():
    imports = get_project_imports()
    data_files = get_project_data_files()

    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas={data_files},
    hiddenimports={imports},
    excludes=[
        'matplotlib', 'tkinter', 'cv2', 'numpy',
        'PIL', 'PIL._imagingtk', 'PIL._tkinter_finder',
        'scipy', 'pandas', 'pyautogui'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NikkiAutoPlayer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='asset/violin.ico'
    version_info={
    'fileversion': (1, 0, 0, 0),
    'productversion': (1, 0, 0, 0),
    'CompanyName': 'SleepFox',
    'FileDescription': 'Infinity Nikki Auto Player for Musical Instrument',
    'ProductName': 'NikkiAutoPlayer',
    'OriginalFilename': 'NikkiAutoPlayer.exe'
    },
    options={
        'encoding': 'utf-8'
    }
)
"""
    with open('build.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)


if __name__ == '__main__':
    generate_spec_file()

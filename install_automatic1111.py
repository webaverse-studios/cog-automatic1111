# Wrapper for AUTOMATIC1111's launch.py
import git
import os
import wget
import shutil

# Stable Diffusion checkpoints
S3_URL = 'https://webaverse-sd-models.s3.amazonaws.com/models/'
S3_MODEL_CHECKPOINTS = ['sd-v1-4.ckpt',
                        'wd-v1-3-float16.ckpt']

# AUTOMATIC1111 git constants
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
AUTOMATIC1111_REPO = 'https://github.com/AUTOMATIC1111/stable-diffusion-webui.git'
AUTOMATIC1111_LOCAL_PATH = os.path.join(ROOT_DIR, 'stable_diffusion_webui')
AUTOMATIC1111_COMMIT_ID = '6c36fe5719a824fa18f6ad3e02727783f095bc5f'

# Everything to be kept from the AUTOMATIC1111 repo
AUTOMATIC1111_PATHS = ['models', 'modules', 'repositories', 'scripts',
                       'textual_inversion_templates', 'embeddings', '.gitignore']

# move gitignore to gitignore.bak
os.rename(os.path.join(ROOT_DIR, '.gitignore'),
          os.path.join(ROOT_DIR, '.gitignore.bak'))

repo = git.Repo.clone_from(AUTOMATIC1111_REPO, AUTOMATIC1111_LOCAL_PATH, no_checkout=True)
repo.git.checkout(AUTOMATIC1111_COMMIT_ID)

# Import AUTOMATIC1111 install script, now that it's cloned
# Note: environment is misspelled "enviroment" in AUTOMATIC1111's install script
from stable_diffusion_webui.launch import prepare_enviroment

# Run AUTOMATIC1111's own install scripts
os.chdir(AUTOMATIC1111_LOCAL_PATH)

# prepare_enviroment [sic]
prepare_enviroment()

# Move desired files/folders from AUTOMATIC1111 repo to current directory
for item in os.listdir(AUTOMATIC1111_LOCAL_PATH):
    if item in AUTOMATIC1111_PATHS:
        shutil.move(os.path.join(AUTOMATIC1111_LOCAL_PATH, item),
                    os.path.join(ROOT_DIR, item))

"""# Merge gitignores
with open(os.path.join(ROOT_DIR, '.gitignore.bak'), 'r') as f:
    gitignore_bak = f.read()
with open(os.path.join(ROOT_DIR, '.gitignore'), 'r+') as f:
    gitignore = f.read()
    gitignore_string = gitignore_bak + "\n" + gitignore + "\n"
    # Add the AUTOMATIC1111 paths
    for path in AUTOMATIC1111_PATHS:
        gitignore_string += "\n" + path
    f.write(gitignore_string)
os.remove(os.path.join(ROOT_DIR, '.gitignore.bak'))"""

# Change back to project root
os.chdir(ROOT_DIR)

# Delete AUTOMATIC1111 repo folder
shutil.rmtree(AUTOMATIC1111_LOCAL_PATH)

# Get models from S3
for model in S3_MODEL_CHECKPOINTS:
    wget.download(S3_URL + model, out='models/Stable-diffusion')

# Run webui for testing
#os.chdir(AUTOMATIC1111_LOCAL_PATH)
#os.system('python3 launch.py --share')
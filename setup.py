# Wrapper for AUTOMATIC1111's launch.py
import git
import os
import wget

# Stable Diffusion checkpoints
S3_URL = 'https://webaverse-sd-models.s3.amazonaws.com/models/'
S3_MODEL_CHECKPOINTS = ['sd-v1-4.ckpt',
                        'wd-v1-3-float16.ckpt']

# Install AUTOMATIC1111
AUTOMATIC1111_REPO = 'https://github.com/AUTOMATIC1111/stable-diffusion-webui.git'
AUTOMATIC1111_LOCAL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stable_diffusion_webui')
AUTOMATIC1111_COMMIT_ID = '6c36fe5719a824fa18f6ad3e02727783f095bc5f'

if not os.path.exists(AUTOMATIC1111_LOCAL_PATH):
    repo = git.Repo.clone_from(AUTOMATIC1111_REPO, AUTOMATIC1111_LOCAL_PATH, no_checkout=True)
    repo.git.checkout(AUTOMATIC1111_COMMIT_ID)

# Import AUTOMATIC1111 install script, now that it's cloned
# Note: environment is misspelled "enviroment" in AUTOMATIC1111's install script
from stable_diffusion_webui.launch import prepare_enviroment

# Run AUTOMATIC1111's own install scripts
os.chdir(AUTOMATIC1111_LOCAL_PATH)

# prepare_enviroment [sic]
prepare_enviroment()

# Get models from S3
for model in S3_MODEL_CHECKPOINTS:
    wget.download(S3_URL + model, out=os.path.join(AUTOMATIC1111_LOCAL_PATH, 'models/Stable-diffusion'))

# Run webui for testing
os.chdir(AUTOMATIC1111_LOCAL_PATH)
#os.system('python3 launch.py --share')
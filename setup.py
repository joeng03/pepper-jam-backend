import os
import subprocess

def setup_wav2lip():
    # Clone the Wav2Lip repository
    if not os.path.exists('Wav2Lip'):
        subprocess.run(['git', 'clone', 'https://github.com/justinjohn0306/Wav2Lip'], check=True)
    
    # Change to the Wav2Lip directory
    os.chdir('Wav2Lip')
    
    # Download the pretrained models
    os.makedirs('checkpoints', exist_ok=True)
    model_urls = {
        'wav2lip.pth': 'https://github.com/justinjohn0306/Wav2Lip/releases/download/models/wav2lip.pth',
        'wav2lip_gan.pth': 'https://github.com/justinjohn0306/Wav2Lip/releases/download/models/wav2lip_gan.pth',
        'resnet50.pth': 'https://github.com/justinjohn0306/Wav2Lip/releases/download/models/resnet50.pth',
        'mobilenet.pth': 'https://github.com/justinjohn0306/Wav2Lip/releases/download/models/mobilenet.pth'
    }
    
    for filename, url in model_urls.items():
        subprocess.run(['wget', url, '-O', f'checkpoints/{filename}'], check=True)


if __name__ == "__main__":
    setup_wav2lip()
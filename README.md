## Setting up Google Translate API
1. Create a new Google Cloud project called `pepper-jam`
2. Enable Service Usage API
3. Enable Google Translate API
4. `gcloud auth application-default login`
5. `gcloud auth application-default set-quota-project pepper-jam`

## Setting up wav2lip
1. `cd wav2lip`
2. `pip install -r requirements.txt` - Unless you're on windows, you may run into an issue saying that torch==2.3.0+cu118 was not found. This is because CUDA-enabled versions for pytorch is not yet supported for mac

import os
import sys
if not os.path.isdir('colab_utils'):
  !git clone https://github.com/mixuala/colab_utils.git
  sys.path.append('colab_utils')
  !pip install --upgrade google-cloud-storage
import colab_utils.gcloud

# Mount Google Cloud Storage
def mount_cloud(project_name, bucket_name):
  # authorize access to Google Cloud SDK from `colaboratory` VM
  colab_utils.gcloud.gcloud_auth(project_name)
  
  # mount gcs bucket to local fs using the `gcsfuse` package, installs automatically
  bucket_dir = "/tmp/gcs-bucket/" + bucket_name
  if not os.path.isdir(bucket_dir):
    local_path = colab_utils.gcloud.gcsfuse(bucket=bucket_name)  
    bucket_dir = local_path
  
  return bucket_dir
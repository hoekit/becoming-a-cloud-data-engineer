# Notes on Cloud Data Engineering

----
### Digital Badges
__

- List of credential earned:
    - <img src="img/notes-credentials.png" alt="" width="60%"/>
    - See: [Current Credentials](https://www.cloudskillsboost.google/public_profiles/70c3e8fe-77a0-45d9-a627-fa64f50ddafa)
..


----
### HDD vs SSD
__

- Read performance of SSD is 10-20x faster than HDD
..


----
### Firebase Web
__ Add Firebase SDK: npm

npm install firebase

// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBTcvPbOGcRjNNFgoLb-atLzAhWSQKRUes",
  authDomain: "qwiklabs-gcp-04-baa9a18ae125.firebaseapp.com",
  projectId: "qwiklabs-gcp-04-baa9a18ae125",
  storageBucket: "qwiklabs-gcp-04-baa9a18ae125.appspot.com",
  messagingSenderId: "304827617045",
  appId: "1:304827617045:web:c4d919b5877b6a099a631c",
  measurementId: "G-NF5S38Q158"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
..
__ Add Firebase SDK: script tag

<script type="module">
  // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-app.js";
  import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-analytics.js";
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  const firebaseConfig = {
    apiKey: "AIzaSyBTcvPbOGcRjNNFgoLb-atLzAhWSQKRUes",
    authDomain: "qwiklabs-gcp-04-baa9a18ae125.firebaseapp.com",
    projectId: "qwiklabs-gcp-04-baa9a18ae125",
    storageBucket: "qwiklabs-gcp-04-baa9a18ae125.appspot.com",
    messagingSenderId: "304827617045",
    appId: "1:304827617045:web:c4d919b5877b6a099a631c",
    measurementId: "G-NF5S38Q158"
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const analytics = getAnalytics(app);
</script>
..
__ Install Firebase CLI

npm install -g firebase-tools

See: https://firebase.google.com/docs/cli/?authuser=0&hl=en
..
__ Deploy to Firebase Hosting

firebase login

firebase init

firebase deploy
..
__ Web: https://qwiklabs-gcp-04-baa9a18ae125.web.app/
..


----
### Google APIs
__ Enable APIs

- Enable the Cloud Run API
    - gcloud services enable run.googleapis.com

```
    Name            API
    ------------    -----------------------------------
    Cloud Build     cloudbuild.googleapis.com
    Cloud Storage   storage-component.googleapis.com
    Cloud Run       run.googleapis.com
```
..


----
### Google Firestore
__
..


----
### Google Cloud Run
__ Steps to use Cloud Run to run LibreOffice to convert PDF

- Lab: Build a Server App with Cloud Run that Creates PDF Files
    - https://www.cloudskillsboost.google/focuses/8390?parent=catalog

- Enable the Cloud Run API
    - gcloud services enable run.googleapis.com

- Deploy the Cloud Run prototype
    - git clone https://github.com/rosera/pet-theory.git
    - See: lab03

gcloud run deploy pdf-converter --image gcr.io/$GOOGLE_CLOUD_PROJECT/pdf-converter --platform managed --region us-central1 --no-allow-unauthenticated --max-instances=1

    - Deploys container from GCR image


SERVICE_URL=$(gcloud beta run services describe pdf-converter --platform managed --region us-central1 --format="value(status.url)")

    - Store service URL in a variable

curl -X POST -H "Authorization: Bearer $(gcloud auth print-identity-token)" $SERVICE_URL

    - Send authenticated request


gcloud iam service-accounts create pubsub-cloud-run-invoker --display-name "PubSub Cloud Run Invoker"

    - Create a service account that can Pub/Sub can run


gcloud beta run services add-iam-policy-binding pdf-converter --member=serviceAccount:pubsub-cloud-run-invoker@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com --role=roles/run.invoker --platform managed --region us-central1

    - Give the service account named `pubsub-cloud-run-invoker` permission to invoke the Cloud Run service


gcloud projects list

    - Show projects with corresponding project number


PROJECT_NUMBER=

    - Store project number of current project in a variable


gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT --member=serviceAccount:service-$PROJECT_NUMBER@gcp-sa-pubsub-iam.gserviceaccount.com --role=roles/iam.serviceAccountTokenCreator

    - Add an IAM policy to the current project to be able to create Pub/Sub authentication tokens


gcloud beta pubsub subscriptions create pdf-conv-sub --topic new-doc --push-endpoint=$SERVICE_URL --push-auth-service-account=pubsub-cloud-run-invoker@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com

    - Create a Pub/Sub subscription that invokes a HTTP endpoint whenever a message is publised on the topic "new-doc"


FROM node:12
RUN apt-get update -y \
    && apt-get install -y libreoffice \
    && apt-get clean
WORKDIR /usr/src/app
COPY package.json package*.json ./
RUN npm install --only=production
COPY . .
CMD [ "npm", "start" ]

    - Update contents of Dockerfirle to instll libreoffice

..
__ Check logs

- Go to Logging
    - Filter by: resource_type="cloud_run_revision"

..
__ Resources

- Cloud Run at Next '19
    - https://youtu.be/16vANkKxoAU?t=1317
..

__ gcloud run with 2GB memory

gcloud run deploy pdf-converter \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/pdf-converter \
  --platform managed \
  --region us-central1 \
  --memory=2Gi \
  --no-allow-unauthenticated \
  --max-instances=1 \
  --set-env-vars PDF_BUCKET=$GOOGLE_CLOUD_PROJECT-processed
..
__ Example index.js file

const {promisify} = require('util');
const {Storage}   = require('@google-cloud/storage');
const exec        = promisify(require('child_process').exec);
const storage     = new Storage();
const express     = require('express');
const bodyParser  = require('body-parser');
const app         = express();
app.use(bodyParser.json());
const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log('Listening on port', port);
});
app.post('/', async (req, res) => {
  try {
    const file = decodeBase64Json(req.body.message.data);
    await downloadFile(file.bucket, file.name);
    const pdfFileName = await convertFile(file.name);
    await uploadFile(process.env.PDF_BUCKET, pdfFileName);
    await deleteFile(file.bucket, file.name);
  }
  catch (ex) {
    console.log(`Error: ${ex}`);
  }
  res.set('Content-Type', 'text/plain');
  res.send('\n\nOK\n\n');
})
function decodeBase64Json(data) {
  return JSON.parse(Buffer.from(data, 'base64').toString());
}
async function downloadFile(bucketName, fileName) {
  const options = {destination: `/tmp/${fileName}`};
  await storage.bucket(bucketName).file(fileName).download(options);
}
async function convertFile(fileName) {
  const cmd = 'libreoffice --headless --convert-to pdf --outdir /tmp ' +
              `"/tmp/${fileName}"`;
  console.log(cmd);
  const { stdout, stderr } = await exec(cmd);
  if (stderr) {
    throw stderr;
  }
  console.log(stdout);
  pdfFileName = fileName.replace(/\.\w+$/, '.pdf');
  return pdfFileName;
}
async function deleteFile(bucketName, fileName) {
  await storage.bucket(bucketName).file(fileName).delete();
}
async function uploadFile(bucketName, fileName) {
  await storage.bucket(bucketName).upload(`/tmp/${fileName}`);
}
..
__ Pattern



..


----
### Google Cloud Build
__

gcloud services enable cloudbuild.googleapis.com

    - Enable the Cloud Run API


gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/pdf-converter

    - Builds a container and puts it in GCR
    - Uses the Dockerfile in the current directory
..


----
### Google Cloud Storage
__ gsutil

gsutil mb gs://$GOOGLE_CLOUD_PROJECT-upload
    - Create the receiving bucket

gsutil mb gs://$GOOGLE_CLOUD_PROJECT-processed
    - Create the done bucket

gsutil notification create -t new-doc -f json -r OBJECT_FINALIZE gs://$GOOGLE_CLOUD_PROJECT-upload
    - Tells Cloud Storage to send a Pub/Sub notification whenever a new file lands on the upload bucket
    - Topic is 'new-doc'
..


----
### Google IAM
__ gcloud iam

gcloud iam service-accounts create pubsub-cloud-run-invoker --display-name "PubSub Cloud Run Invoker"

    - Create a service account that can Pub/Sub can run


gcloud projects list

    - Show projects with corresponding project number


PROJECT_NUMBER=408692058566

    - Store project number of current project in a variable


gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT --member=serviceAccount:service-$PROJECT_NUMBER@gcp-sa-pubsub.iam.gserviceaccount.com --role=roles/iam.serviceAccountTokenCreator

    - Add an IAM policy to the current project to be able to create Pub/Sub authentication tokens


gcloud projects add-iam-policy-binding $PROJECT_ID --member=user:student-02-2545ad7ce1ab@qwiklabs.net --role=roles/logging.viewer

    - Assigns `logging.viewer` role to `student-02-2545ad7ce1ab@qwiklabs.net`
    - Able to view logs across the entire project
    - See list of roles: https://cloud.google.com/iam/docs/understanding-roles#predefined_roles


gcloud projects add-iam-policy-binding $PROJECT_ID --member=user:student-02-2545ad7ce1ab@qwiklabs.net --role=roles/source.writer

    - Assigns `source.writer` role to `student-02-2545ad7ce1ab@qwiklabs.net`
    - Able to read write to source control repository


..


----
### Google Pub

----
### Speech Accuracy
__ Concepts

- Word Error Rate (WER)
    - percentage of incorrect transcriptions in the set
    - lower error rate means higher accuracy

- Ground truth
    - refers to 100% accurate (usually human) transcription to compare
      against to measure accuracy

- Types of error
    - Insertion Errors (I)
        - Words present in transcript but not in ground truth
    - Deletion Errors (D)
        - Words in ground truth but not in transcript
    - Substitution Errors (S)
        - Words present in both but transcribed incorrectly

- WER = (I + D + S) / N
    - Note WER can be > 100% if num errors > num words

- Jaccard Index
    - Measures correctness (broadly speaking)
    - number of words that are the same same over total number of words

- F1 Score
    - Measure precision vs recall
    - Precision almost 1  ⇒  Very few false positives
    - Recall almost 1     ⇒  Very few false negatives
..
__ Practice

- Need 30 mins to 3 hours of audio with ground truth for sampling

- Use the same equipment to get the input as used in transcription

..


----
### Firebase
__

- Lab
    - https://www.cloudskillsboost.google/focuses/660?parent=catalog

- Sample code
    - git clone https://github.com/firebase/friendlychat-web

- Firebase Console: https://console.firebase.google.com/
    - Add project
    - Add a Firebase Web App
    - Enable Google sign-in for Firebase Authentication
    - Enable Cloud Firestore
..
__ firebase commands

npm init --yes
npm install -g firebase-tools

    - Install firebase CLI into Cloud Shell


firebase login --no-localhost

    - Authorize Cloud Shell to access firebase
    - Similar to kubectl container clusters get-credentials


- firebase --version
    - Check that firebase CLI is installed

- firebase login --no-localhost
    - Authorize the Firebase CLI
    - `--no-localhost` cos we are in a remote shell

- firebase use --add
    - Tell firebase CLI which project to use, like use database
    - Give project an alias like `staging`

- firebase use staging
    - Use the staging project

- firebase serve --only hosting
    - Serve app locally

- npm install
    - Downloads the Firebase SDK. See the package.json file

- npm run start &
    - Run Webpack continuously

- Edit the file: src/firebase-config.js
    - Get the config from Firebase Console

- firebase deploy --except functions --token $(gcloud auth application-default print-access-token)
    - Redeploy app
..

----
### ASP.NET Core
__ dotnet

- dotnet --version
    - Check that .NET Core is installed

- export DOTNET_CLI_TELEMETRY_OPTOUT=1
    - Disable app telemetry

- dotnet new razor -o HelloWorldAspNetCore
    - Create a skeleton app

- dotnet run --urls=http://localhost:8080
    - Run the app in the current folder

- dotnet publish -c Release
    - Publish the app to get a self-contained DLL
    - Published into: bin/Release/netcoreapp3.1/publish/
..
__ Dockerfile

FROM gcr.io/google-appengine/aspnetcore:3.1
ADD ./ /app
# Tells .NET Core which port to listen to
ENV ASPNETCORE_URLS=http://*:${PORT}
WORKDIR /app
ENTRYPOINT [ "dotnet", "HelloWorldAspNetCore.dll" ]
..

----
### Cloud Ops
__ Github repo: https://github.com/GoogleCloudPlatform/cloud-ops-sandbox.git
..


----
### Challenge Lab: Deploy to Kubernetes in Google Cloud
__ Lab: https://www.cloudskillsboost.google/focuses/10457?parent=catalog
..
__ Team Standards

Team Standards:
    - Region: us-east1
    - Zone: use-east1-b
    - Use project VPCs
    - Use n1-standard-1

Naming Standards:
    - team-resource e.g. kraken-webserver
..
__ Task 0: Setup

- Setup project region and zone
    - gcloud config set compute/region us-east1
    - gcloud config set compute/zone us-east1-b

- Setup project ID
    - export PROJECT_ID=qwiklabs-gcp-04-de61d1b485e8

..
__ Task 1: Create a Docker image and store the Dockerfile

- Install marking script:
    - source < $(gsutil cat gs://cloud-training/gsp318/marking/setup_marking_v2.sh)

- Cloud source repo: valkyrie-app
    - gcloud source repos clone valkyrie-app

- Create valkyrie-app/Dockerfile:
    ```
        FROM golang:1.0
        WORKDIR /go/src/app
        COPY source .
        RUN go install -v
        ENTRYPOINT ["app", "-single=true"."-port=8080"]
    ```

- Create a docker image:
    - docker build -t valkyrie-prod:v0.0.2 .
    - image: FIXME
    - tag: FIXME

- Check progress:
    - ./step1_v2.sh
..
__ Task 2: Test the created Docker image

- Launch container, mapping port 8080 of Cloud Shell to image
    - docker run -p 8080:8080 --name valkyrie-image valkyrie-prod:v0.0.2 &

- Check progress:
    - ./step2_v2.sh

- Stop the container when done
    - docker stop valkyrie-image
..
__ Task 3: Push the Docker image in the Container Registry

- Retag image for GCR:
    - docker tag valkyrie-prod:v0.0.2 gcr.io/$PROJECT_ID/valkyrie-prod:v0.0.2

- Push to GCR:
    - docker push gcr.io/$PROJECT_ID/valkyrie-prod:v0.0.2
..
__ Task 4: Create and expose a deployment in Kubernetes

- Check the deployment and service, understand what's being deployed,
  probably some simple go-app behind a service:
    - vim valkyrie-app/k8s/deployment.yaml
    - vim valkyrie-app/k8s/service.yaml
    - IMAGE_HERE: gcr.io/qwiklabs-gcp-04-de61d1b485e8/valkyrie-prod:v0.0.2

- Fix any issues found in the yaml files
    - FIXME

- Use the provided Kubernetes cluster: valkyrie-dev
    - gcloud container clusters list

- Get kubectl credentials:
    - gcloud container clusters get-credentials valkyrie-dev

- Deploy the pods and check that it's working
    - kubectl apply -f valkyrie-app/k8s/deployment.yaml
    - kubectl deployments
    - kubectl pods

- Deploy the service and check that it's working
    - kubectl apply -f valkyrie-app/k8s/service.yaml
    - kubectl svc
    - Access the External IP to see if it's working nicely
..
__ Task 5: Update the deployment with a new version of valkyrie-app

- Get the deployment name
    - kubectl get deployments

- Scale the deployment
    - kubectl scale deployment DEPLOYMENT --replicas=N
    - kubectl scale deployment valkyrie-dev --replicas=3

- Merge in Kurt's changes:
    - git checkout master
    - git merge origin/kurt-dev

- Rebuild the valkyrie app if all is good
    - docker build -t valkyrie-prod:v0.0.3  

- Run the app to see what it does:
    - docker run -p 8080:8080 --name valkyrie-image3 valkyrie-prod:v0.0.3

- Retag and push to GCR
    - docker tag IMAGE:TAG2 gcr.io/$PROJECT_ID/IMAGE:TAG2
    - docker tag valkyrie-prod:v0.0.3 gcr.io/$PROJECT_ID/valkyrie-prod:v0.0.3
    - docker push gcr.io/$PROJECT_ID/valkyrie-prod:v0.0.3

- Update the deployment and apply:
    - vim valkyrie-app/k8s/deployment.yaml
        - Use the updated version TAG2
    - kubectl get pods
    - kubectl apply -f valkyrie-app/k8s/deployment.yaml
    - kubectl get pods

- Service is unaffected so no need to redeploy
    - kubectl svc
    - Access the External IP to see if it's working like the local Docker image
..
__ Task 6: Create a pipeline in Jenkins to deploy your app

- There is a Jenkins deployment in valkyrie-dev cluster already
    - Use it

- Get the Jenkins admin password:
    - printf $(kubectl get secret cd-jenkins -o jsonpath="{.data.jenkins-admin-password}" | base64 --decode);echo

- Get the Jenkins pod name and port forward from Cloud Shell to pod:
    - kubectl get pods
    - export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/component=jenkins-master" -l "app.kubernetes.io/instance=cd" -o jsonpath="{.items[0].metadata.name}")
    - kubectl port-forward $POD_NAME 8080:8080 >> /dev/null &

- Login to Jenkins
    - See: https://www.cloudskillsboost.google/focuses/1104?parent=catalog

- Jenkins: Add a Google Service Account

- Jenkins: Create a Multibranch Pipeline
    - git repo: FIXME
        - https://source.developers.google.com/p/[PROJECT_ID]/r/default
        - Or `git remote -v` in the repo to see the remote

- Cloud Shell: Edit `valkyrie-app/Jenkinsfile` and `valkyrie-app/source/html.go`
    - git add and push changes to repo
    - manually trigger the build


..


----
### Terraform
__ What is it:

- Terraform is:
    - a tool for provisioning infrastructure
    - open-source
    - more importantly: declarative
    - automatic changes to infrastructure is easy
    - replicating infrastructure is easy e.g. staging, dev
..
__ Compared to Ansible

- Both
    - Infrastructure as code

- Differences
    - Ansible:
        - Mainly a configuration tool
        - more mature
    - Teraform:
        - Mainly infrastructure tool
        - relatively new
        - more advanced in orchestration
..
__ Terraform Architecture

- Terraform Core
    - Terraform configuration TF-Config i.e. the target state
    - Core creates plan: a function of config and state
        - Plan of what needs to do and the sequence
        - Execute plan with Providers

- Terraform State
    - Is the Current state of the infrastructure

- Providers
    - Connectors to providers:
        - IaaS: AWS | Azure
        - PaaS: Kubernetes
        - SaaS: Fastly
..
__ Terraform commands

- refresh
    - query infrastructure provider to get current State

- plan
    - create an execution plan

- apply
    - execute the plan

- destry
    - destroy the resources/infrastructure
..


----
### Engineer Data in Google Cloud: Challenge Lab
__ Lab:

- Lab: https://www.cloudskillsboost.google/focuses/12379?parent=catalog
- Dataset: taxirides
- Source Table: historical_taxi_rides_raw
- Target Table: taxi_training_data_499
..
__ Task 1: Clean your training data

- Clean the data:
    ```
    #standardSQL
    SELECT
        Fare_amount                                 -- FIXME
        FIXME
    - WHERE
        - trip_distance > Number                    -- FIXME
        - fare_amount >= Value                      -- FIXME
        - latitude  is reasonable                   -- FIXME NOT NULL??
            - Need to look at the values
        - longitude is reasonable                   -- FIXME NOT NULL??
            - Need to look at the values
        - passenger_count > Number                  -- FIXME
        - sampling 1 million rows from > 1Billion   -- FIXME

    ```

- Look at latitude longitude distribution:

    SELECT
      COUNTIF(pickup_latitude IS NULL) AS null_pickup_latitude,
      COUNT(pickup_latitude) AS num_pickup_latitude,
      MIN(pickup_latitude) AS low_pickup_latitude,
      MAX(pickup_latitude) AS high_pickup_latitude,
      AVG(pickup_latitude) AS avg_pickup_latitude,
      STDDEV(pickup_latitude) AS stddev
    FROM `qwiklabs-gcp-04-2230a17d031d.taxirides.historical_taxi_rides_raw`

    SELECT
      COUNTIF(dropoff_latitude IS NULL) AS null_dropoff_latitude,
      COUNT(dropoff_latitude) AS num_dropoff_latitude,
      MIN(dropoff_latitude) AS low_dropoff_latitude,
      MAX(dropoff_latitude) AS high_dropoff_latitude,
      AVG(dropoff_latitude) AS avg_dropoff_latitude,
      STDDEV(dropoff_latitude) AS stddev
    FROM `qwiklabs-gcp-04-2230a17d031d.taxirides.historical_taxi_rides_raw`

    SELECT
      COUNTIF(pickup_longitude IS NULL) AS null_pickup_longitude,
      COUNT(pickup_longitude) AS num_pickup_longitude,
      MIN(pickup_longitude) AS low_pickup_longitude,
      MAX(pickup_longitude) AS high_pickup_longitude,
      AVG(pickup_longitude) AS avg_pickup_longitude,
      STDDEV(pickup_longitude) AS stddev
    FROM `qwiklabs-gcp-04-2230a17d031d.taxirides.historical_taxi_rides_raw`

    SELECT
      COUNTIF(dropoff_longitude IS NULL) AS null_dropoff_longitude,
      COUNT(dropoff_longitude) AS num_dropoff_longitude,
      MIN(dropoff_longitude) AS low_dropoff_longitude,
      MAX(dropoff_longitude) AS high_dropoff_longitude,
      AVG(dropoff_longitude) AS avg_dropoff_longitude,
      STDDEV(dropoff_longitude) AS stddev
    FROM `qwiklabs-gcp-04-2230a17d031d.taxirides.historical_taxi_rides_raw`

    SELECT
      COUNTIF(longitude IS NULL) AS null_longitude,
      COUNT(longitude) AS num_longitude,
      MIN(longitude) AS low_longitude,
      MAX(longitude) AS high_longitude,
      AVG(longitude) AS avg_longitude,
      STDDEV(longitude) AS stddev
    FROM `nyc-tlc.yellow.trips`

    SELECT
        # Technique to sample 1 out of 1000 rows
        MOD(ABS(FARM_FINGERPRINT(CAST(pickup_datetime AS STRING))),1000) = 1

See https://cloud.google.com/bigquery/docs/writing-results
    - On saving query results to tables

..
__ Task 2: Create a BQML model

- First create/train a model
- Then run ML.EVALUATE() on the model
- Need to do feature engineering by enriching the data with euclidean distance
..
__   Task 2.1: Create the model with TRANSFORM clause

See: https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-create#transform
    - All preprocessing in TRANSFORM clause is automatically applied
      during prediction and evaluation!

CREATE OR REPLACE MODEL m
TRANSFORM (
    * EXCEPT(...),                                  -- FIXME
    ST_Distance(
      ST_GeogPoint(pickuplon, pickuplat),           -- FIXME
      ST_GeogPoint(dropofflon, dropofflat)          -- FIXME
    ) AS euclidean,
    label_col                                       -- FIXME
)
OPTIONS (
    model_type=’linear_reg’,
    input_label_cols=['label_col'])                 -- FIXME
)
AS SELECT * FROM t              -- Use the same columns in evaluate and predict
..
__   Task 2.2 Evaluate the model

See: https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-evaluate

#standardSQL
SELECT
  SQRT(mean_squared_error) AS rmse
FROM
  ML.EVALUATE(MODEL m, TABLE t)

- To get RMSE below 10, try:
    - feature engineering to put in more relevant features
    - change the sampling
..
__ Task 3: Perform batch prediction

See: https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-predict

- Source table: report_prediction_data
- Target table: 2015_fare_amount_predictions

#standardSQL
SELECT
  *
FROM
  ML.PREDICT(MODEL m, TABLE t)

..
__ Resource:

- The TRANSFORM Clause
    - https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-create#transform

- The ML.EVALUATE Function
    - https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-evaluate

- The ML.PREDICT function
    - https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-predict

- Standard SQL Functions and Operators
    - https://cloud.google.com/bigquery/docs/reference/standard-sql/functions-and-operators

- Writing BigQuery output to tables
    - https://cloud.google.com/bigquery/docs/writing-results
    - Easier to use the UI

: https://www.cloudskillsboost.google/focuses/1797?parent=catalog
..


----
### Google Cloud IoT Core
__ What is it

- Cloud IoT Core is:
    - fully managed services
    - securely connect devices via MQTT protocol
        - MQTT: Message Queue Telemetry Transport
    - ingest data from devices
    - manage devices

- Cloud IoT Core works with:
    - Cloud PubSub: by sending data to PubSub
..
__ Concepts:

- Device:
    - a processing unit
    - capable of connecting to the internet and send data
    - send two types of data: telemetry and state

- Telemetry:
    - event data monitored by the device
        - e.g. measurements about the environment
    - `device telemetry event`: refers to telemetry data sent from
      device to cloud

- Device state
    - an arbitrary, user-defined blob of data
    - describes the current status of the device
    - can be structured or unstructured
    - flows only in the device-to-cloud direction

- Device configuration
    - an arbitrary, user-defined blob of data
    - used to control or change a device's state
    - can be structured or unstructured
    - flows only in the cloud-to-device direction

- Device registry
    - A container of devices with shared properties
    - devices are `registered` to a device service like Cloud IoT Core

Device Manager
    - The service used to:
        - monitor device health and activity
        - update device configurations
        - manage credentials and authentication

MQTT:
    - an industry-standard IoT protocol
    - a publish/subscrib messaging protocol

..
__ Cloud IoT Components

- Main components:
    - one device manager
        - to register, monitor and configure devices
    - two protocol bridges (MQTT and HTTP)
        - for devices to connect to Google Cloud
..
__ Reference Architecture

- Device telemetry data sent to Cloud IoT Core
- Events sent to Cloud Pub/Sub

..

__ Lab: https://www.cloudskillsboost.google/focuses/1771?parent=catalog
..
__ Cloud IoT Core to PubSub

- A PubSub topic must be created first
- Then create an IoT Core registry

..
__ Device to Cloud IoT Core

- An IoT Core registry must be created first

- A Device must also be registered

- An RS256 public key must be created:
    ```
        openssl req -x509 -newkey rsa:2048 -keyout rsa_private.pem -nodes \
            -out rsa_cert.pem -subj "/CN=unused"
    ```
- The public key in rsa_cert.pem must be added as a public key in the
  device created
    - Input method: Enter manually
    - Public key format: RS256_X509

- Install Google Cloud root cert
    - `curl -O https://pki.goog/roots.pem`

- A NodeJS sample to simulate a device:
    - git clone https://github.com/googleapis/nodejs-iot
    - Needs the private key generated above to work

- Generate events from simulator
    ```
    node cloudiot_mqtt_example_nodejs.js \
        mqttDeviceDemo \
        --projectId=$PROJECT_ID \
        --cloudRegion=us-central1 \
        --registryId=my-registry \
        --deviceId=my-device \
        --privateKeyFile=rsa_private.pem \
        --numMessages=25 \
        --algorithm=RS256 \
        --serverCertFile=roots.pem \
        --mqttBridgePort=443
    ```
..

__ References:

- Easily Build an IoT Analytics Pipeline
    - https://youtu.be/r_4BVf2x2Yo

- Quest: IoT in the Google Cloud
    - https://google.qwiklabs.com/quests/49

- Read: Getting Started guide for Cloud IoT Core
    - https://cloud.google.com/iot/docs/how-tos/getting-started

- Read Overview of Internet of Things
    - https://cloud.google.com/solutions/iot-overview
..


----
### gcloud service accounts
__

- Export env variables
    ```
        export PROJECT_ID=$(gcloud config get-value project)
    ```

- Create service account e.g. SQL Server to Data Catalog Connector
    ```
        gcloud iam service-accounts create sqlserver2dc-credentials \
          --display-name  "Service Account for SQLServer to Data Catalog connector" \
          --project $PROJECT_ID
    ```

- Create and Download Service Account Key:
    ```
        gcloud iam service-accounts keys create "sqlserver2dc-credentials.json" \
          --iam-account "sqlserver2dc-credentials@$PROJECT_ID.iam.gserviceaccount.com"
    ```

- Add Data Catalog admin role to Service Account:
    ```
        gcloud projects add-iam-policy-binding $PROJECT_ID \
          --member "serviceAccount:sqlserver2dc-credentials@$PROJECT_ID.iam.gserviceaccount.com" \
          --quiet \
          --project $PROJECT_ID \
          --role "roles/datacatalog.admin"
    ```

..


----
### Data Catalog
__

- Automatic metadata update
- Search with ACL
- Structured tags
..
__ References

- GitHub repo for SQLServer to Data Catalog connector
    - https://github.com/GoogleCloudPlatform/datacatalog-connectors-rdbms/tree/master/google-datacatalog-sqlserver-connector

- Introduction to Data Catalog, 2020
    - https://www.youtube.com/watch?v=eUKqXZDXj78
    - Includes how BlackRock is using Data Catalog

- Data Catalog roles
    - https://cloud.google.com/data-catalog/docs/concepts/iam#attaching_tags_to_resources

- IAM roles for Data Catalog
    - https://cloud.google.com/iam/docs/understanding-roles#datacatalog

- Data Catalog docs
    - https://cloud.google.com/data-catalog/docs/concepts/introduction-data-catalog
..


----
### Readiness Probe
__ What is it

- A readiness probe is a way for Kubernetes to ask your app if if it
  should send traffic to it

- It's where the application and infrastructure meet

- Typically implemented as an endpoint at tcp:81

- See: https://youtu.be/IDoRWieTcMc?t=1527
..


----
### Jenkins
__



..
__ Lab: [`Setting up Jenkins on Kubernetes Engine`](https://www.cloudskillsboost.google/focuses/1776?parent=catalog)
..
__ gcloud commands

gcloud config set compute/zone us-east1-d

    - Set default zone


gcloud container clusters create SOME-CLUSTER \
    --num-nodes 2 \
    --machine-type n1-standard-2 \
    --scopes "https://www.googleapis.com/auth/projecthosting,cloud-platform"

    - Create a Kubernetes cluster named `SOME-CLUSTER`, has two (2)
      nodes and scoped to access to Google Cloud Repositories and Google
      Container Registry


gcloud container clusters list

    - Check cluster


gcloud container clusters get-credentials SOME-CLUSTER

    - Get credentials to be able to run `kubectl`


..
__ kubectl


- export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/component=jenkins-master" -l "app.kubernetes.io/instance=cd" -o jsonpath="{.items[0].metadata.name}")

    - Assuming jenkins was installed on the cluster via Helm
    - Get pod name of the jenkins-master


kubectl port-forward $POD_NAME 8080:8080 >> /dev/null &

    - Map Cloud Shell port to port on POD


kubectl create ns production

    - Creates a production namespace. Namespaces help to logically
      isolate deployments


kubectl apply -f k8s/production -n production

    - Apply all the definitions in the `k8s/production` folder
    - To the production namespace (`-n production`) 


kubectl get deployments -n production

    - view deployments in production namespace


export FRONTEND_SERVICE_IP=$(kubectl get -o jsonpath="{.status.loadBalancer.ingress[0].ip}" --namespace=production services gceme-frontend)

    - Get the External IP address of a service by name, in this case `gceme-frontend`
..
__ See: ### Helm

- On how to install Jenkins using Helm
..
__ Resources

- Continuous Delivery Best Practices with Jenkins and GKE, 2018
    - https://www.youtube.com/watch?v=IDoRWieTcMc

- More about Jenkins
    - https://cloud.google.com/solutions/jenkins-on-kubernetes-engine

- How to configure Jenkins for Kubernetes Engine
    - https://cloud.google.com/solutions/configuring-jenkins-kubernetes-engine

- Setting up Continuous Deployment (CD) to Kubernetes Engine using Jenkins
    - https://cloud.google.com/solutions/continuous-delivery-jenkins-kubernetes-engine
..



----
### Helm
__ What is it

- Helm is:
    - a package manager for Kubernetes
    - packages are called `charts`
    - Helm has a Jenkins Helm chart

..
__ helm commands

- helm repo add stable https://charts.helm.sh/stable
    - Add the stable repo. Like adding a ppa to ubuntu:

- helm repo add jenkins https://charts.jenkins.io
    - Add just the jenkins repo

- helm repo update
    - Update the repo, like `apt-get update`:

- helm install cd stable/jenkins -f jenkins/values.yaml --version 1.2.2 --wait
    - Deploy the chart
    - `jenkins/values.yaml` contains service account credentials to
      access Google Cloud Source Repository
..
__ jenkins/values.yaml

controller:
  installPlugins:
    - kubernetes:latest
    - workflow-job:latest
    - workflow-aggregator:latest
    - credentials-binding:latest
    - git:latest
    - google-oauth-plugin:latest
    - google-source-plugin:latest
    - google-kubernetes-engine:latest
    - google-storage-plugin:latest
  resources:
    requests:
      cpu: "50m"
      memory: "1024Mi"
    limits:
      cpu: "1"
      memory: "3500Mi"
  javaOpts: "-Xms3500m -Xmx3500m"
  serviceType: ClusterIP
agent:
  resources:
    requests:
      cpu: "500m"
      memory: "256Mi"
    limits:
      cpu: "1"
      memory: "512Mi"
persistence:
  size: 100Gi
serviceAccount:
  name: cd-jenkins

..
__ About jenkins/values.yaml

- Deploys a jenkins pod containing:
    - a jenkins controller
        - a host of plugins are installed
        - these plugins allow Jenkins to connect to the K8S cluster and
          GCP project
    - a jenkins agent
    - a service account
..
__ On completion of the `helm install command` above:

    NAME: cd
    LAST DEPLOYED: Tue Apr  5 12:37:52 2022
    NAMESPACE: default
    STATUS: deployed
    REVISION: 1
    NOTES:

    1. Get your 'admin' user password by running:
      printf $(kubectl get secret --namespace default cd-jenkins -o jsonpath="{.data.jenkins-admin-password}" | base64 --decode);echo

    2. Get the Jenkins URL to visit by running these commands in the same shell:
      NOTE: It may take a few minutes for the LoadBalancer IP to be available.
            You can watch the status of by running 'kubectl get svc --namespace default -w cd-jenkins'
      export SERVICE_IP=$(kubectl get svc --namespace default cd-jenkins --template "{{ range (index .status.loadBalancer.ingress 0) }}{{ . }}{{ end }}")
      echo http://$SERVICE_IP:8080/login

    3. Login with the password from step 1 and the username: admin


    For more information on running Jenkins on Kubernetes, visit:
    https://cloud.google.com/solutions/jenkins-on-container-engine

..
__ gcloud, kubectl and bash commands

export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/component=jenkins-master" -l "app.kubernetes.io/instance=cd" -o jsonpath="{.items[0].metadata.name}")

    - Extract the pod name of the jenkins master pod


kubectl port-forward $POD_NAME 8080:8080 >> /dev/null &

    - Setup port mapping of Cloud Shell to pod


kubectl get svc

    - Check Jenkins service is running


printf $(kubectl get secret cd-jenkins -o jsonpath="{.data.jenkins-admin-password}" | base64 --decode);echo

    - View the jenkins admin password
    - Login as `admin` with that password at the mapped port
..

__ Default jenkins/values.yaml file

# Default values for jenkins.
# This is a YAML-formatted file.
# Declare name/value pairs to be passed into your templates.
# name: value

## Overrides for generated resource names
# See templates/_helpers.tpl
# nameOverride:
# fullnameOverride:
# namespaceOverride:

# For FQDN resolving of the controller service. Change this value to match your existing configuration.
# ref: https://github.com/kubernetes/dns/blob/master/docs/specification.md
clusterZone: "cluster.local"

renderHelmLabels: true

controller:
  # Used for label app.kubernetes.io/component
  componentName: "jenkins-controller"
  image: "jenkins/jenkins"
  tag: "2.289.1-jdk11"
  imagePullPolicy: "Always"
  imagePullSecretName:
  # Optionally configure lifetime for controller-container
  lifecycle:
  #  postStart:
  #    exec:
  #      command:
  #      - "uname"
  #      - "-a"
  disableRememberMe: false
  numExecutors: 0
  # configures the executor mode of the Jenkins node. Possible values are: NORMAL or EXCLUSIVE
  executorMode: "NORMAL"
  # This is ignored if enableRawHtmlMarkupFormatter is true
  markupFormatter: plainText
  customJenkinsLabels: []
  # The default configuration uses this secret to configure an admin user
  # If you don't need that user or use a different security realm then you can disable it
  adminSecret: true

  hostNetworking: false
  # When enabling LDAP or another non-Jenkins identity source, the built-in admin account will no longer exist.
  # If you disable the non-Jenkins identity store and instead use the Jenkins internal one,
  # you should revert controller.adminUser to your preferred admin user:
  adminUser: "admin"
  # adminPassword: <defaults to random>
  admin:
    existingSecret: ""
    userKey: jenkins-admin-user
    passwordKey: jenkins-admin-password
  # This values should not be changed unless you use your custom image of jenkins or any devired from. If you want to use
  # Cloudbees Jenkins Distribution docker, you should set jenkinsHome: "/var/cloudbees-jenkins-distribution"
  jenkinsHome: "/var/jenkins_home"
  # This values should not be changed unless you use your custom image of jenkins or any devired from. If you want to use
  # Cloudbees Jenkins Distribution docker, you should set jenkinsRef: "/usr/share/cloudbees-jenkins-distribution/ref"
  jenkinsRef: "/usr/share/jenkins/ref"
  # Path to the jenkins war file which is used by jenkins-plugin-cli.
  jenkinsWar: "/usr/share/jenkins/jenkins.war"
  # Overrides the default arguments passed to the war
  # overrideArgs:
  #   - --httpPort=8080
  resources:
    requests:
      cpu: "50m"
      memory: "256Mi"
    limits:
      cpu: "2000m"
      memory: "4096Mi"
  # Environment variables that get added to the init container (useful for e.g. http_proxy)
  # initContainerEnv:
  #   - name: http_proxy
  #     value: "http://192.168.64.1:3128"
  # containerEnv:
  #   - name: http_proxy
  #     value: "http://192.168.64.1:3128"
  # Set min/max heap here if needed with:
  # javaOpts: "-Xms512m -Xmx512m"
  # jenkinsOpts: ""
  # If you are using the ingress definitions provided by this chart via the `controller.ingress` block the configured hostname will be the ingress hostname starting with `https://` or `http://` depending on the `tls` configuration.
  # The Protocol can be overwritten by specifying `controller.jenkinsUrlProtocol`.
  # jenkinsUrlProtocol: "https"
  # If you are not using the provided ingress you can specify `controller.jenkinsUrl` to change the url definition.
  # jenkinsUrl: ""
  # If you set this prefix and use ingress controller then you might want to set the ingress path below
  # jenkinsUriPrefix: "/jenkins"
  # Enable pod security context (must be `true` if podSecurityContextOverride, runAsUser or fsGroup are set)
  usePodSecurityContext: true
  # Note that `runAsUser`, `fsGroup`, and `securityContextCapabilities` are
  # being deprecated and replaced by `podSecurityContextOverride`.
  # Set runAsUser to 1000 to let Jenkins run as non-root user 'jenkins' which exists in 'jenkins/jenkins' docker image.
  # When setting runAsUser to a different value than 0 also set fsGroup to the same value:
  runAsUser: 1000
  fsGroup: 1000
  # If you have PodSecurityPolicies that require dropping of capabilities as suggested by CIS K8s benchmark, put them here
  securityContextCapabilities: {}
  #  drop:
  #    - NET_RAW
  # Completely overwrites the contents of the `securityContext`, ignoring the
  # values provided for the deprecated fields: `runAsUser`, `fsGroup`, and
  # `securityContextCapabilities`.  In the case of mounting an ext4 filesystem,
  # it might be desirable to use `supplementalGroups` instead of `fsGroup` in
  # the `securityContext` block: https://github.com/kubernetes/kubernetes/issues/67014#issuecomment-589915496
  # podSecurityContextOverride:
  #   runAsUser: 1000
  #   runAsNonRoot: true
  #   supplementalGroups: [1000]
  #   # capabilities: {}
  servicePort: 8080
  targetPort: 8080
  # For minikube, set this to NodePort, elsewhere use LoadBalancer
  # Use ClusterIP if your setup includes ingress controller
  serviceType: ClusterIP
  # Jenkins controller service annotations
  serviceAnnotations: {}
  # Jenkins controller custom labels
  statefulSetLabels: {}
  #   foo: bar
  #   bar: foo
  # Jenkins controller service labels
  serviceLabels: {}
  #   service.beta.kubernetes.io/aws-load-balancer-backend-protocol: https
  # Put labels on Jenkins controller pod
  podLabels: {}
  # Used to create Ingress record (should used with ServiceType: ClusterIP)
  # nodePort: <to set explicitly, choose port between 30000-32767
  # Enable Kubernetes Liveness and Readiness Probes
  # if Startup Probe is supported, enable it too
  # ~ 2 minutes to allow Jenkins to restart when upgrading plugins. Set ReadinessTimeout to be shorter than LivenessTimeout.
  healthProbes: true
  probes:
    startupProbe:
      httpGet:
        path: '{{ default "" .Values.controller.jenkinsUriPrefix }}/login'
        port: http
      periodSeconds: 10
      timeoutSeconds: 5
      failureThreshold: 12
    livenessProbe:
      failureThreshold: 5
      httpGet:
        path: '{{ default "" .Values.controller.jenkinsUriPrefix }}/login'
        port: http
      periodSeconds: 10
      timeoutSeconds: 5
      # If Startup Probe is not supported on your Kubernetes cluster, you might want to use "initialDelaySeconds" instead.
      # It delays the initial liveness probe while Jenkins is starting
      # initialDelaySeconds: 60
    readinessProbe:
      failureThreshold: 3
      httpGet:
        path: '{{ default "" .Values.controller.jenkinsUriPrefix }}/login'
        port: http
      periodSeconds: 10
      timeoutSeconds: 5
      # If Startup Probe is not supported on your Kubernetes cluster, you might want to use "initialDelaySeconds" instead.
      # It delays the initial readyness probe while Jenkins is starting
      # initialDelaySeconds: 60

  agentListenerEnabled: true
  agentListenerPort: 50000
  agentListenerHostPort:
  agentListenerNodePort:
  disabledAgentProtocols:
    - JNLP-connect
    - JNLP2-connect
  csrf:
    defaultCrumbIssuer:
      enabled: true
      proxyCompatability: true
  # Kubernetes service type for the JNLP agent service
  # agentListenerServiceType is the Kubernetes Service type for the JNLP agent service,
  # either 'LoadBalancer', 'NodePort', or 'ClusterIP'
  # Note if you set this to 'LoadBalancer', you *must* define annotations to secure it. By default
  # this will be an external load balancer and allowing inbound 0.0.0.0/0, a HUGE
  # security risk:  https://github.com/kubernetes/charts/issues/1341
  agentListenerServiceType: "ClusterIP"
  # Optionally assign an IP to the LoadBalancer agentListenerService LoadBalancer
  # GKE users: only regional static IPs will work for Service Load balancer.
  agentListenerLoadBalancerIP:
  agentListenerServiceAnnotations: {}

  # Example of 'LoadBalancer' type of agent listener with annotations securing it
  # agentListenerServiceType: LoadBalancer
  # agentListenerServiceAnnotations:
  #   service.beta.kubernetes.io/aws-load-balancer-internal: "True"
  #   service.beta.kubernetes.io/load-balancer-source-ranges: "172.0.0.0/8, 10.0.0.0/8"

  # LoadBalancerSourcesRange is a list of allowed CIDR values, which are combined with ServicePort to
  # set allowed inbound rules on the security group assigned to the controller load balancer
  loadBalancerSourceRanges:
  - 0.0.0.0/0
  # Optionally assign a known public LB IP
  # loadBalancerIP: 1.2.3.4
  # Optionally configure a JMX port
  # requires additional javaOpts, ie
  # javaOpts: >
  #   -Dcom.sun.management.jmxremote.port=4000
  #   -Dcom.sun.management.jmxremote.authenticate=false
  #   -Dcom.sun.management.jmxremote.ssl=false
  # jmxPort: 4000
  # Optionally configure other ports to expose in the controller container
  extraPorts: []
  # - name: BuildInfoProxy
  #   port: 9000

  # List of plugins to be install during Jenkins controller start
  installPlugins:
    - kubernetes:1.29.4
    - workflow-multibranch:latest
    - workflow-aggregator:latest
    - pipeline-model-definition:latest
    - pipeline-model-extensions:latest
    - git:4.7.1
    - configuration-as-code:1.51
    - google-oauth-plugin:latest
    - google-source-plugin:latest
    - google-kubernetes-engine:latest
    - google-storage-plugin:latest
  resources:

  # Set to false to download the minimum required version of all dependencies.
  installLatestPlugins: false

  # List of plugins to install in addition to those listed in controller.installPlugins
  additionalPlugins: []

  # Enable to initialize the Jenkins controller only once on initial installation.
  # Without this, whenever the controller gets restarted (Evicted, etc.) it will fetch plugin updates which has the potential to cause breakage.
  # Note that for this to work, `persistence.enabled` needs to be set to `true`
  initializeOnce: false

  # Enable to always override the installed plugins with the values of 'controller.installPlugins' on upgrade or redeployment.
  # overwritePlugins: true

  # Configures if plugins bundled with `controller.image` should be overwritten with the values of 'controller.installPlugins' on upgrade or redeployment.
  overwritePluginsFromImage: true

  # Enable HTML parsing using OWASP Markup Formatter Plugin (antisamy-markup-formatter), useful with ghprb plugin.
  # The plugin is not installed by default, please update controller.installPlugins.
  enableRawHtmlMarkupFormatter: false
  # Used to approve a list of groovy functions in pipelines used the script-security plugin. Can be viewed under /scriptApproval
  scriptApproval: []
  #  - "method groovy.json.JsonSlurperClassic parseText java.lang.String"
  #  - "new groovy.json.JsonSlurperClassic"
  # List of groovy init scripts to be executed during Jenkins controller start
  initScripts: []
  #  - |
  #    print 'adding global pipeline libraries, register properties, bootstrap jobs...'

  # 'name' is a name of an existing secret in same namespace as jenkins,
  # 'keyName' is the name of one of the keys inside current secret.
  # the 'name' and 'keyName' are concatenated with a '-' in between, so for example:
  # an existing secret "secret-credentials" and a key inside it named "github-password" should be used in Jcasc as ${secret-credentials-github-password}
  # 'name' and 'keyName' must be lowercase RFC 1123 label must consist of lower case alphanumeric characters or '-',
  # and must start and end with an alphanumeric character (e.g. 'my-name',  or '123-abc')
  additionalExistingSecrets: []
  #  - name: secret-name-1
  #    keyName: username
  #  - name: secret-name-1
  #    keyName: password

  additionalSecrets: []
  #  - name: nameOfSecret
  #    value: secretText

  # Generate SecretClaim resources in order to create Kubernetes secrets from HashiCorp Vault using kube-vault-controller.
  # 'name' is name of the secret that will be created in Kubernetes. The Jenkins fullname is prepended to this value.
  # 'path' is the fully qualified path to the secret in Vault
  # 'type' is an optional Kubernetes secret type. Defaults to 'Opaque'
  # 'renew' is an optional secret renewal time in seconds
  secretClaims: []
  # - name: secretName        # required
  #   path: testPath          # required
  #   type: kubernetes.io/tls # optional
  #   renew: 60               # optional

  # Name of default cloud configuration.
  cloudName: "kubernetes"

  # Below is the implementation of Jenkins Configuration as Code.  Add a key under configScripts for each configuration area,
  # where each corresponds to a plugin or section of the UI.  Each key (prior to | character) is just a label, and can be any value.
  # Keys are only used to give the section a meaningful name.  The only restriction is they may only contain RFC 1123 \ DNS label
  # characters: lowercase letters, numbers, and hyphens.  The keys become the name of a configuration yaml file on the controller in
  # /var/jenkins_home/casc_configs (by default) and will be processed by the Configuration as Code Plugin.  The lines after each |
  # become the content of the configuration yaml file.  The first line after this is a JCasC root element, eg jenkins, credentials,
  # etc.  Best reference is https://<jenkins_url>/configuration-as-code/reference.  The example below creates a welcome message:
  JCasC:
    defaultConfig: true
    configScripts: {}
    #  welcome-message: |
    #    jenkins:
    #      systemMessage: Welcome to our CI\CD server.  This Jenkins is configured and managed 'as code'.
    # Ignored if securityRealm is defined in controller.JCasC.configScripts and
    # ignored if controller.enableXmlConfig=true as controller.securityRealm takes precedence
    securityRealm: |-
      local:
        allowsSignup: false
        enableCaptcha: false
        users:
        - id: "${chart-admin-username}"
          name: "Jenkins Admin"
          password: "${chart-admin-password}"
    # Ignored if authorizationStrategy is defined in controller.JCasC.configScripts
    authorizationStrategy: |-
      loggedInUsersCanDoAnything:
        allowAnonymousRead: false
  # Optionally specify additional init-containers
  customInitContainers: []
  # - name: custom-init
  #   image: "alpine:3.7"
  #   imagePullPolicy: Always
  #   command: [ "uname", "-a" ]

  sidecars:
    configAutoReload:
      # If enabled: true, Jenkins Configuration as Code will be reloaded on-the-fly without a reboot.  If false or not-specified,
      # jcasc changes will cause a reboot and will only be applied at the subsequent start-up.  Auto-reload uses the
      # http://<jenkins_url>/reload-configuration-as-code endpoint to reapply config when changes to the configScripts are detected.
      enabled: true
      image: kiwigrid/k8s-sidecar:1.12.2
      imagePullPolicy: IfNotPresent
      resources: {}
        #   limits:
        #     cpu: 100m
        #     memory: 100Mi
        #   requests:
        #     cpu: 50m
        #     memory: 50Mi
      # How many connection-related errors to retry on
      reqRetryConnect: 10
      # env:
      #   - name: REQ_TIMEOUT
      #     value: "30"
      # SSH port value can be set to any unused TCP port.  The default, 1044, is a non-standard SSH port that has been chosen at random.
      # Is only used to reload jcasc config from the sidecar container running in the Jenkins controller pod.
      # This TCP port will not be open in the pod (unless you specifically configure this), so Jenkins will not be
      # accessible via SSH from outside of the pod.  Note if you use non-root pod privileges (runAsUser & fsGroup),
      # this must be > 1024:
      sshTcpPort: 1044
      # folder in the pod that should hold the collected dashboards:
      folder: "/var/jenkins_home/casc_configs"
      # If specified, the sidecar will search for JCasC config-maps inside this namespace.
      # Otherwise the namespace in which the sidecar is running will be used.
      # It's also possible to specify ALL to search in all namespaces:
      # searchNamespace:

    # Allows you to inject additional/other sidecars
    other: []
    ## The example below runs the client for https://smee.io as sidecar container next to Jenkins,
    ## that allows to trigger build behind a secure firewall.
    ## https://jenkins.io/blog/2019/01/07/webhook-firewalls/#triggering-builds-with-webhooks-behind-a-secure-firewall
    ##
    ## Note: To use it you should go to https://smee.io/new and update the url to the generete one.
    # - name: smee
    #   image: docker.io/twalter/smee-client:1.0.2
    #   args: ["--port", "{{ .Values.controller.servicePort }}", "--path", "/github-webhook/", "--url", "https://smee.io/new"]
    #   resources:
    #     limits:
    #       cpu: 50m
    #       memory: 128Mi
    #     requests:
    #       cpu: 10m
    #       memory: 32Mi
  # Name of the Kubernetes scheduler to use
  schedulerName: ""
  # Node labels and tolerations for pod assignment
  # ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#nodeselector
  # ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#taints-and-tolerations-beta-feature
  nodeSelector: {}

  terminationGracePeriodSeconds:

  tolerations: []

  affinity: {}
  # Leverage a priorityClass to ensure your pods survive resource shortages
  # ref: https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/
  priorityClassName:

  podAnnotations: {}
  # Add StatefulSet annotations
  statefulSetAnnotations: {}

  # StatefulSet updateStrategy
  # ref: https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#update-strategies
  updateStrategy: {}

  ingress:
    enabled: false
    # Override for the default paths that map requests to the backend
    paths: []
    # - backend:
    #     serviceName: ssl-redirect
    #     servicePort: use-annotation
    # - backend:
    #     serviceName: >-
    #       {{ template "jenkins.fullname" . }}
    #     # Don't use string here, use only integer value!
    #     servicePort: 8080
    # For Kubernetes v1.14+, use 'networking.k8s.io/v1beta1'
    # For Kubernetes v1.19+, use 'networking.k8s.io/v1'
    apiVersion: "extensions/v1beta1"
    labels: {}
    annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
    # For Kubernetes >= 1.18 you should specify the ingress-controller via the field ingressClassName
    # See https://kubernetes.io/blog/2020/04/02/improvements-to-the-ingress-api-in-kubernetes-1.18/#specifying-the-class-of-an-ingress
    # ingressClassName: nginx
    # Set this path to jenkinsUriPrefix above or use annotations to rewrite path
    # path: "/jenkins"
    # configures the hostname e.g. jenkins.example.com
    hostName:
    tls:
    # - secretName: jenkins.cluster.local
    #   hosts:
    #     - jenkins.cluster.local

  # often you want to have your controller all locked down and private
  # but you still want to get webhooks from your SCM
  # A secondary ingress will let you expose different urls
  # with a differnt configuration
  secondaryingress:
    enabled: false
    # paths you want forwarded to the backend
    # ex /github-webhook
    paths: []
    # For Kubernetes v1.14+, use 'networking.k8s.io/v1beta1'
    # For Kubernetes v1.19+, use 'networking.k8s.io/v1'
    apiVersion: "extensions/v1beta1"
    labels: {}
    annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
    # For Kubernetes >= 1.18 you should specify the ingress-controller via the field ingressClassName
    # See https://kubernetes.io/blog/2020/04/02/improvements-to-the-ingress-api-in-kubernetes-1.18/#specifying-the-class-of-an-ingress
    # ingressClassName: nginx
    # configures the hostname e.g. jenkins-external.example.com
    hostName:
    tls:
    # - secretName: jenkins-external.example.com
    #   hosts:
    #     - jenkins-external.example.com

  # If you're running on GKE and need to configure a backendconfig
  # to finish ingress setup, use the following values.
  # Docs: https://cloud.google.com/kubernetes-engine/docs/concepts/backendconfig
  backendconfig:
    enabled: false
    apiVersion: "extensions/v1beta1"
    name:
    labels: {}
    annotations: {}
    spec: {}

  # Openshift route
  route:
    enabled: false
    labels: {}
    annotations: {}
    # path: "/jenkins"

  # controller.hostAliases allows for adding entries to Pod /etc/hosts:
  # https://kubernetes.io/docs/concepts/services-networking/add-entries-to-pod-etc-hosts-with-host-aliases/
  hostAliases: []
  # - ip: 192.168.50.50
  #   hostnames:
  #     - something.local
  # - ip: 10.0.50.50
  #   hostnames:
  #     - other.local

  # Expose Prometheus metrics
  prometheus:
    # If enabled, add the prometheus plugin to the list of plugins to install
    # https://plugins.jenkins.io/prometheus
    enabled: false
    # Additional labels to add to the ServiceMonitor object
    serviceMonitorAdditionalLabels: {}
    # Set a custom namespace where to deploy ServiceMonitor resource
    # serviceMonitorNamespace: monitoring
    scrapeInterval: 60s
    # This is the default endpoint used by the prometheus plugin
    scrapeEndpoint: /prometheus
    # Additional labels to add to the PrometheusRule object
    alertingRulesAdditionalLabels: {}
    # An array of prometheus alerting rules
    # See here: https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/
    # The `groups` root object is added by default, simply add the rule entries
    alertingrules: []
    # Set a custom namespace where to deploy PrometheusRule resource
    prometheusRuleNamespace: ""

  # Can be used to disable rendering controller test resources when using helm template
  testEnabled: true

  httpsKeyStore:
    jenkinsHttpsJksSecretName: ''
    enable: false
    httpPort: 8081
    path: "/var/jenkins_keystore"
    fileName: "keystore.jks"
    password: "password"
    # Convert keystore.jks files content to base64 ( cat keystore.jks | base64 ) and put the output here
    jenkinsKeyStoreBase64Encoded: |
        /u3+7QAAAAIAAAABAAAAAQANamVua2luc2NpLmNvbQAAAW2r/b1ZAAAFATCCBP0wDgYKKwYBBAEq
        AhEBAQUABIIE6QbCqasvoHS0pSwYqSvdydMCB9t+VNfwhFIiiuAelJfO5sSe2SebJbtwHgLcRz1Z
        gMtWgOSFdl3bWSzA7vrW2LED52h+jXLYSWvZzuDuh8hYO85m10ikF6QR+dTi4jra0whIFDvq3pxe
        TnESxEsN+DvbZM3jA3qsjQJSeISNpDjO099dqQvHpnCn18lyk7J4TWJ8sOQQb1EM2zDAfAOSqA/x
        QuPEFl74DlY+5DIk6EBvpmWhaMSvXzWZACGA0sYqa157dq7O0AqmuLG/EI5EkHETO4CrtBW+yLcy
        2dUCXOMA+j+NjM1BjrQkYE5vtSfNO6lFZcISyKo5pTFlcA7ut0Fx2nZ8GhHTn32CpeWwNcZBn1gR
        pZVt6DxVVkhTAkMLhR4rL2wGIi/1WRs23ZOLGKtyDNvDHnQyDiQEoJGy9nAthA8aNHa3cfdF10vB
        Drb19vtpFHmpvKEEhpk2EBRF4fTi644Fuhu2Ied6118AlaPvEea+n6G4vBz+8RWuVCmZjLU+7h8l
        Hy3/WdUPoIL5eW7Kz+hS+sRTFzfu9C48dMkQH3a6f3wSY+mufizNF9U298r98TnYy+PfDJK0bstG
        Ph6yPWx8DGXKQBwrhWJWXI6JwZDeC5Ny+l8p1SypTmAjpIaSW3ge+KgcL6Wtt1R5hUV1ajVwVSUi
        HF/FachKqPqyLJFZTGjNrxnmNYpt8P1d5JTvJfmfr55Su/P9n7kcyWp7zMcb2Q5nlXt4tWogOHLI
        OzEWKCacbFfVHE+PpdrcvCVZMDzFogIq5EqGTOZe2poPpBVE+1y9mf5+TXBegy5HToLWvmfmJNTO
        NCDuBjgLs2tdw2yMPm4YEr57PnMX5gGTC3f2ZihXCIJDCRCdQ9sVBOjIQbOCzxFXkVITo0BAZhCi
        Yz61wt3Ud8e//zhXWCkCsSV+IZCxxPzhEFd+RFVjW0Nm9hsb2FgAhkXCjsGROgoleYgaZJWvQaAg
        UyBzMmKDPKTllBHyE3Gy1ehBNGPgEBChf17/9M+j8pcm1OmlM434ctWQ4qW7RU56//yq1soFY0Te
        fu2ei03a6m68fYuW6s7XEEK58QisJWRAvEbpwu/eyqfs7PsQ+zSgJHyk2rO95IxdMtEESb2GRuoi
        Bs+AHNdYFTAi+GBWw9dvEgqQ0Mpv0//6bBE/Fb4d7b7f56uUNnnE7mFnjGmGQN+MvC62pfwfvJTT
        EkT1iZ9kjM9FprTFWXT4UmO3XTvesGeE50sV9YPm71X4DCQwc4KE8vyuwj0s6oMNAUACW2ClU9QQ
        y0tRpaF1tzs4N42Q5zl0TzWxbCCjAtC3u6xf+c8MCGrr7DzNhm42LOQiHTa4MwX4x96q7235oiAU
        iQqSI/hyF5yLpWw4etyUvsx2/0/0wkuTU1FozbLoCWJEWcPS7QadMrRRISxHf0YobIeQyz34regl
        t1qSQ3dCU9D6AHLgX6kqllx4X0fnFq7LtfN7fA2itW26v+kAT2QFZ3qZhINGfofCja/pITC1uNAZ
        gsJaTMcQ600krj/ynoxnjT+n1gmeqThac6/Mi3YlVeRtaxI2InL82ZuD+w/dfY9OpPssQjy3xiQa
        jPuaMWXRxz/sS9syOoGVH7XBwKrWpQcpchozWJt40QV5DslJkclcr8aC2AGlzuJMTdEgz1eqV0+H
        bAXG9HRHN/0eJTn1/QAAAAEABVguNTA5AAADjzCCA4swggJzAhRGqVxH4HTLYPGO4rzHcCPeGDKn
        xTANBgkqhkiG9w0BAQsFADCBgTELMAkGA1UEBhMCY2ExEDAOBgNVBAgMB29udGFyaW8xEDAOBgNV
        BAcMB3Rvcm9udG8xFDASBgNVBAoMC2plbmtpbnN0ZXN0MRkwFwYDVQQDDBBqZW5raW5zdGVzdC5p
        bmZvMR0wGwYJKoZIhvcNAQkBFg50ZXN0QHRlc3QuaW5mbzAeFw0xOTEwMDgxNTI5NTVaFw0xOTEx
        MDcxNTI5NTVaMIGBMQswCQYDVQQGEwJjYTEQMA4GA1UECAwHb250YXJpbzEQMA4GA1UEBwwHdG9y
        b250bzEUMBIGA1UECgwLamVua2luc3Rlc3QxGTAXBgNVBAMMEGplbmtpbnN0ZXN0LmluZm8xHTAb
        BgkqhkiG9w0BCQEWDnRlc3RAdGVzdC5pbmZvMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKC
        AQEA02q352JTHGvROMBhSHvSv+vnoOTDKSTz2aLQn0tYrIRqRo+8bfmMjXuhkwZPSnCpvUGNAJ+w
        Jrt/dqMoYUjCBkjylD/qHmnXN5EwS1cMg1Djh65gi5JJLFJ7eNcoSsr/0AJ+TweIal1jJSP3t3PF
        9Uv21gm6xdm7HnNK66WpUUXLDTKaIs/jtagVY1bLOo9oEVeLN4nT2CYWztpMvdCyEDUzgEdDbmrP
        F5nKUPK5hrFqo1Dc5rUI4ZshL3Lpv398aMxv6n2adQvuL++URMEbXXBhxOrT6rCtYzbcR5fkwS9i
        d3Br45CoWOQro02JAepoU0MQKY5+xQ4Bq9Q7tB9BAwIDAQABMA0GCSqGSIb3DQEBCwUAA4IBAQAe
        4xc+mSvKkrKBHg9/zpkWgZUiOp4ENJCi8H4tea/PCM439v6y/kfjT/okOokFvX8N5aa1OSz2Vsrl
        m8kjIc6hiA7bKzT6lb0EyjUShFFZ5jmGVP4S7/hviDvgB5yEQxOPpumkdRP513YnEGj/o9Pazi5h
        /MwpRxxazoda9r45kqQpyG+XoM4pB+Fd3JzMc4FUGxfVPxJU4jLawnJJiZ3vqiSyaB0YyUL+Er1Q
        6NnqtR4gEBF0ZVlQmkycFvD4EC2boP943dLqNUvop+4R3SM1QMM6P5u8iTXtHd/VN4MwMyy1wtog
        hYAzODo1Jt59pcqqKJEas0C/lFJEB3frw4ImNx5fNlJYOpx+ijfQs9m39CevDq0=

agent:
  enabled: true
  defaultsProviderTemplate: ""
  # URL for connecting to the Jenkins contoller
  jenkinsUrl:
  # connect to the specified host and port, instead of connecting directly to the Jenkins controller
  jenkinsTunnel:
  kubernetesConnectTimeout: 5
  kubernetesReadTimeout: 15
  maxRequestsPerHostStr: "32"
  namespace:
  image: "jenkins/inbound-agent"
  tag: "4.6-1"
  workingDir: "/home/jenkins"
  customJenkinsLabels: []
  # name of the secret to be used for image pulling
  imagePullSecretName:
  componentName: "jenkins-agent"
  websocket: false
  privileged: false
  runAsUser:
  runAsGroup:
  resources:
    requests:
      cpu: "512m"
      memory: "512Mi"
    limits:
      cpu: "512m"
      memory: "512Mi"
  # You may want to change this to true while testing a new image
  alwaysPullImage: false
  # Controls how agent pods are retained after the Jenkins build completes
  # Possible values: Always, Never, OnFailure
  podRetention: "Never"
  # Disable if you do not want the Yaml the agent pod template to show up
  # in the job Console Output. This can be helpful for either security reasons
  # or simply to clean up the output to make it easier to read.
  showRawYaml: true
  # You can define the volumes that you want to mount for this container
  # Allowed types are: ConfigMap, EmptyDir, HostPath, Nfs, PVC, Secret
  # Configure the attributes as they appear in the corresponding Java class for that type
  # https://github.com/jenkinsci/kubernetes-plugin/tree/master/src/main/java/org/csanchez/jenkins/plugins/kubernetes/volumes
  volumes: []
  # - type: ConfigMap
  #   configMapName: myconfigmap
  #   mountPath: /var/myapp/myconfigmap
  # - type: EmptyDir
  #   mountPath: /var/myapp/myemptydir
  #   memory: false
  # - type: HostPath
  #   hostPath: /var/lib/containers
  #   mountPath: /var/myapp/myhostpath
  # - type: Nfs
  #   mountPath: /var/myapp/mynfs
  #   readOnly: false
  #   serverAddress: "192.0.2.0"
  #   serverPath: /var/lib/containers
  # - type: PVC
  #   claimName: mypvc
  #   mountPath: /var/myapp/mypvc
  #   readOnly: false
  # - type: Secret
  #   defaultMode: "600"
  #   mountPath: /var/myapp/mysecret
  #   secretName: mysecret
  # Pod-wide environment, these vars are visible to any container in the agent pod

  # You can define the workspaceVolume that you want to mount for this container
  # Allowed types are: DynamicPVC, EmptyDir, HostPath, Nfs, PVC
  # Configure the attributes as they appear in the corresponding Java class for that type
  # https://github.com/jenkinsci/kubernetes-plugin/tree/master/src/main/java/org/csanchez/jenkins/plugins/kubernetes/volumes/workspace
  workspaceVolume: {}
  # - type: DynamicPVC
  #   configMapName: myconfigmap
  # - type: EmptyDir
  #   memory: false
  # - type: HostPath
  #   hostPath: /var/lib/containers
  # - type: Nfs
  #   readOnly: false
  #   serverAddress: "192.0.2.0"
  #   serverPath: /var/lib/containers
  # - type: PVC
  #   claimName: mypvc
  #   readOnly: false
  # Pod-wide environment, these vars are visible to any container in the agent pod
  envVars: []
  # - name: PATH
  #   value: /usr/local/bin
  nodeSelector: {}
  # Key Value selectors. Ex:
  # jenkins-agent: v1

  # Executed command when side container gets started
  command:
  args: "${computer.jnlpmac} ${computer.name}"
  # Side container name
  sideContainerName: "jnlp"
  # Doesn't allocate pseudo TTY by default
  TTYEnabled: false
  # Max number of spawned agent
  containerCap: 10
  # Pod name
  podName: "default"
  # Allows the Pod to remain active for reuse until the configured number of
  # minutes has passed since the last step was executed on it.
  idleMinutes: 0
  # Raw yaml template for the Pod. For example this allows usage of toleration for agent pods.
  # https://github.com/jenkinsci/kubernetes-plugin#using-yaml-to-define-pod-templates
  # https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/
  yamlTemplate: ""
  # yamlTemplate: |-
  #   apiVersion: v1
  #   kind: Pod
  #   spec:
  #     tolerations:
  #     - key: "key"
  #       operator: "Equal"
  #       value: "value"
  # Defines how the raw yaml field gets merged with yaml definitions from inherited pod templates: merge or override
  yamlMergeStrategy: "override"
  # Timeout in seconds for an agent to be online
  connectTimeout: 100
  # Annotations to apply to the pod.
  annotations: {}

  # Below is the implementation of custom pod templates for the default configured kubernetes cloud.
  # Add a key under podTemplates for each pod template. Each key (prior to | character) is just a label, and can be any value.
  # Keys are only used to give the pod template a meaningful name.  The only restriction is they may only contain RFC 1123 \ DNS label
  # characters: lowercase letters, numbers, and hyphens. Each pod template can contain multiple containers.
  # For this pod templates configuration to be loaded the following values must be set:
  # controller.JCasC.defaultConfig: true
  # Best reference is https://<jenkins_url>/configuration-as-code/reference#Cloud-kubernetes. The example below creates a python pod template.
  podTemplates: {}
  #  python: |
  #    - name: python
  #      label: jenkins-python
  #      serviceAccount: jenkins
  #      containers:
  #        - name: python
  #          image: python:3
  #          command: "/bin/sh -c"
  #          args: "cat"
  #          ttyEnabled: true
  #          privileged: true
  #          resourceRequestCpu: "400m"
  #          resourceRequestMemory: "512Mi"
  #          resourceLimitCpu: "1"
  #          resourceLimitMemory: "1024Mi"

# Here you can add additional agents
# They inherit all values from `agent` so you only need to specify values which differ
additionalAgents: {}
#  maven:
#    podName: maven
#    customJenkinsLabels: maven
#    # An example of overriding the jnlp container
#    # sideContainerName: jnlp
#    image: jenkins/jnlp-agent-maven
#    tag: latest
#  python:
#    podName: python
#    customJenkinsLabels: python
#    sideContainerName: python
#    image: python
#    tag: "3"
#    command: "/bin/sh -c"
#    args: "cat"
#    TTYEnabled: true

persistence:
  enabled: true
  ## A manually managed Persistent Volume and Claim
  ## Requires persistence.enabled: true
  ## If defined, PVC must be created manually before volume will be bound
  existingClaim:
  ## jenkins data Persistent Volume Storage Class
  ## If defined, storageClassName: <storageClass>
  ## If set to "-", storageClassName: "", which disables dynamic provisioning
  ## If undefined (the default) or set to null, no storageClassName spec is
  ##   set, choosing the default provisioner.  (gp2 on AWS, standard on
  ##   GKE, AWS & OpenStack)
  ##
  storageClass:
  annotations: {}
  accessMode: "ReadWriteOnce"
  size: "8Gi"
  volumes:
  #  - name: nothing
  #    emptyDir: {}
  mounts:
  #  - mountPath: /var/nothing
  #    name: nothing
  #    readOnly: true

networkPolicy:
  # Enable creation of NetworkPolicy resources.
  enabled: false
  # For Kubernetes v1.4, v1.5 and v1.6, use 'extensions/v1beta1'
  # For Kubernetes v1.7, use 'networking.k8s.io/v1'
  apiVersion: networking.k8s.io/v1
  # You can allow agents to connect from both within the cluster (from within specific/all namespaces) AND/OR from a given external IP range
  internalAgents:
    allowed: true
    podLabels: {}
    namespaceLabels: {}
      # project: myproject
  externalAgents: {}
  #   ipCIDR: 172.17.0.0/16
  #   except:
  #     - 172.17.1.0/24

## Install Default RBAC roles and bindings
rbac:
  create: true
  readSecrets: false

serviceAccount:
  create: true
  # The name of the service account is autogenerated by default
  name:
  annotations: {}
  imagePullSecretName:


serviceAccountAgent:
  # Specifies whether a ServiceAccount should be created
  create: false
  # The name of the ServiceAccount to use.
  # If not set and create is true, a name is generated using the fullname template
  name:
  annotations: {}
  imagePullSecretName:

## Backup cronjob configuration
## Ref: https://github.com/maorfr/kube-tasks
backup:
  # Backup must use RBAC
  # So by enabling backup you are enabling RBAC specific for backup
  enabled: false
  # Used for label app.kubernetes.io/component
  componentName: "backup"
  # Schedule to run jobs. Must be in cron time format
  # Ref: https://crontab.guru/
  schedule: "0 2 * * *"
  labels: {}
  annotations: {}
    # Example for authorization to AWS S3 using kube2iam or IRSA
    # Can also be done using environment variables
    # iam.amazonaws.com/role: "jenkins"
    # "eks.amazonaws.com/role-arn": "arn:aws:iam::123456789012:role/jenkins-backup"
  # Set this to terminate the job that is running/failing continously and set the job status to "Failed"
  activeDeadlineSeconds: ""
  image:
    repository: "maorfr/kube-tasks"
    tag: "0.2.0"
  # Additional arguments for kube-tasks
  # Ref: https://github.com/maorfr/kube-tasks#simple-backup
  extraArgs: []
  # Add existingSecret for AWS credentials
  existingSecret: {}
  ## Example for using an existing secret
   # jenkinsaws:
  ## Use this key for AWS access key ID
     # awsaccesskey: jenkins_aws_access_key
  ## Use this key for AWS secret access key
     # awssecretkey: jenkins_aws_secret_key
  # Add additional environment variables
   # jenkinsgcp:
  ## Use this key for GCP credentials
     # gcpcredentials: credentials.json
  env: []
  # Example environment variable required for AWS credentials chain
  # - name: "AWS_REGION"
  #   value: "us-east-1"
  resources:
    requests:
      memory: 1Gi
      cpu: 1
    limits:
      memory: 1Gi
      cpu: 1
  # Destination to store the backup artifacts
  # Supported cloud storage services: AWS S3, Minio S3, Azure Blob Storage, Google Cloud Storage
  # Additional support can added. Visit this repository for details
  # Ref: https://github.com/maorfr/skbn
  destination: "s3://jenkins-data/backup"
  # By enabling only the jenkins_home/jobs folder gets backed up, not the whole jenkins instance
  onlyJobs: false
  # Enable backup pod security context (must be `true` if runAsUser or fsGroup are set)
  usePodSecurityContext: true
  # When setting runAsUser to a different value than 0 also set fsGroup to the same value:
  runAsUser: 1000
  fsGroup: 1000
  securityContextCapabilities: {}
  #  drop:
  #    - NET_RAW
checkDeprecation: true
..
__ About the default jenkins/values.yaml file

- It creates:
    - a pod named cd-jenkin-0
    - two services:
        - cd-jenkins at tcp:8080
        - cd-jenkins-agent at tcp:50000

- Need to configure a service account like so:
    - kubectl create clusterrolebinding jenkins-deploy --clusterrole=cluster-admin --serviceaccount=default:cd-jenkins
..


----
### Heterogenous Deployments
__

- Common scenarios:
    - Multi-cloud deployments
    - Fronting on-premises data
    - CI/CD processes

- Nice lab on managing canary, blue-green deployments on GKE
    - https://www.cloudskillsboost.google/focuses/639?parent=catalog
    - Canary Deployments and rollbacks are made easy
    - Blue-Green Deployments and rollbacks are made easy
..

----
### Google Cloud Endpoints
__

- What is it?
    - A set of tools to generate APIs from within an App Engine application

- The steps:
    - git clone https://github.com/GoogleCloudPlatform/endpoints-quickstart.git
    - Create an OpenAPI configuration file
        - See example: openapi.yaml
    - Deploy the API:
        - See example: cd scripts && ./deploy_api.sh

    - Create the app
        - See example: app/airports.py
    - Deploy the app:
        - See example: cd scripts && ./deploy_app.sh

    - See also other scripts in the `scripts` directory

- If Google Cloud Endpoints is used with App Engine
    - Updating the endpoints will also need to redeploy the app

- The nice thing is that Google Cloud Endpoints provides rate-limiting
..


----
### Google Actions
__

- Actions on Google Developer Console
    - http://console.actions.google.com/

- Actions Glossary
    - https://developers.google.com/actions/glossary

- Glossary:
    - `Action`: an interaction built for Google Assistant that performs
      specific tasks based on user input.
    - `Intent`: the goal of the Action (e.g. generate quotes). An intent
      takes user input and channels it to trigger an event.
    - `Agent (Dialogflow)`: a module that uses NLU and ML to transform
      user input into actionable data to be used by an Assistant
      application.

- So basically the flow is this:
    - Google Assistant receives some input e.g. user speech or some text
    - That's passed on to DialogFlow parses it and matches it to an intent
        - It then triggers an intent
        - An intent is like an endpoint within an Android app
..


----
### Google Cloud Functions
__

- Great Google Cloud Functions demo, 2017
    - https://www.youtube.com/watch?v=kXk78ihBpiQ
..


----
### DevOps
__ Overview

- Talk on DORA's Report 2019
    - https://www.youtube.com/watch?v=y0M9Z_zSmPo

- Why you should read DORA's 2019 Accelerate State of DevOps Report
    - https://www.youtube.com/watch?v=8M3WibXvC84
..


----
### Google Cloud Source Repositories
__ What is it

- Provide a managed Git version control remote
..
__ gcloud commands

- Create a a repo in Google Cloud Source Repositories
    - gcloud source repos create REPO_DEMO

- Clone Cloud repo to local
    - gcloud source repos clone REPO_DEMO

- Configure git
    - git config --global user.email "you@example.com"
    - git config --global user.name "Your Name"

- The usual git commands:
    - git push origin master
..
__ Integration with Kubernetes

- Create a Kubernetes cluster that has access to Cloud Source
  Repositories and Google Container Registry
    - The `--scopes` argument lets the cluster access Google Cloud Repo
      and Google Container Registry
    ```
        gcloud container clusters create jenkins-cd \
        --num-nodes 2 \
        --machine-type n1-standard-2 \
        --scopes "https://www.googleapis.com/auth/projecthosting,cloud-platform"
    ```

..


----
### Kubernetes
__ Kubernetes pods

- A Docker container is:
    - typically for a single microservice
    - a microservice typically talks to other microservices

- A Kubernetes pod is:
    - a group of containers tied together
    - with shared storage and network resources
        - shared namespace
        - One IP per pod
    - to simplify admin and networking
    - also have volumes

- A Pod Volume is
    - a set of data disks that live as long as the pods live
    - can be used by containers in that pod
    - shared by containers in the pod
..
__ Kubernetes Services

- A Kubernetes service:
    - provides stable endpoints for pods
        - Pods can be restarted anytime, resulting in changed IP
    - uses labels to determine what Pods to operate on
        - if they have the corect labels, they are exposed

- Types of Service:
    - ClusterIP (default):
        - means service only visible inside K8s cluster
    - LoadBalancer:
        - adds a load balancer, forwards traffic from service to nodes
    - NodePort:
        - Each node gets an externally accessible IP
..
__ Kubernetes Cluster Info

- View cluster configuration
    - `kubectl cluster-info`
    - `kubectl config view`

- View events and logs
    - `kubectl get events`
    - `kubectl logs POD_NAME`
..
__ Exposing Kubernetes pods

- Expose a deployment
    - `kubectl expose deployment hello-server --type=LoadBalancer --port 8080`
        - The cluster is exposed using a load-balancer
            - A Compute Engine load balancer [web](https://cloud.google.com/compute/docs/load-balancing/)

- Get public IP Address of service:
    - `kubectl get services`
        - CLUSTER-IP is internal IP of cluster
        - EXTERNAL-IP is public IP of cluster
..
__ Scale up a Kubernetes (K8s) cluster

- Scale up cluster to four (4) pods
    - `kubectl scale deployment $DEPLOYMENT --replicas=4`
        - Number of pods is now four (4) i.e. four containers
    - `kubectl get deployment`
        - View deployment to check number of pods
    - `kubectl get pods`
        - List pods. There should be four (4)
..
__ Update Deployments

- Steps
    - Update code
    - Build a docker image with updated tag
    - Push docker image to GCR
    - Update the deployment to use updated deployment
        - `kubectl edit deployment $DEPLOYMENT`
            - Update Spec > containers > image
..
__ gcloud commands

- Create a Kubernetes cluster
    - Cluster name is `some-cluster`
    - Has two (2) nodes
    - Scoped to access to Google Cloud Repositories and Google Container Registry
    ```
        gcloud container clusters create some-cluster \
            --num-nodes 2 \
            --machine-type n1-standard-2 \
            --scopes "https://www.googleapis.com/auth/projecthosting,cloud-platform"
    ```
- Check cluster
    - gcloud container clusters list

- Get credentials to be able to run `kubectl`
    - Cluster name is `some-cluster`
    - gcloud container clusters get-credentials some-cluster

..
__ kubectl commands

- kubectl explain deployment
- kubectl explain deployment --recursive
- kubectl explain deployment.metadata.name

- kubectl cluster-info
    - Get cluster info:

- kubectl get svc frontend -o=jsonpath="{.status.loadBalancer.ingress[0].ip}"
    - Get External IP of a service named `frontend`:

- kubectl scale deployment hello --replicas=5
    - Scale a deployment named `hello`

- `kubectl get pods -o jsonpath --template='{range .items[*]}{.metadata.name}{"\t"}{"\t"}{.spec.containers[0].image}{"\n"}{end}'`
    - Get pod versions

- kubectl run -it --rm python --image=python:3.6-alpine --restart=Never sh
    - Run a minimal container with python 3.6 installed

..
__ References:

- Kubernetes for Sysadmins
    - https://www.youtube.com/watch?v=HlAXp0-M6SY

- kubectl commands
    - https://cloud.google.com/container-engine/docs/kubectl/

- A Compute Engine load balancer
    - https://cloud.google.com/compute/docs/load-balancing/

- Rolling Updates
    - https://cloud.google.com/container-engine/docs/rolling-updates

- Minikube, a simple setup of a single node kubernetes cluster for dev
    - http://kubernetes.io/docs/getting-started-guides/minikube/.

- Kubernetes Blog
    - http://blog.kubernetes.io/

- Video on difference between K8s Deployments and Pods
    - https://www.youtube.com/watch?v=t-y3PpuBadA
..

__ Notes from Kubernetes for Sysadmins, 2016

- https://www.youtube.com/watch?v=HlAXp0-M6SY

- Kubernetes is declarative
    - A contract between developer and sysadmin
    - Kubernetes expects a container
        - Like Fedex expects a Fedex box

- Think of containers in two parts
    - Building the container
    - Running the container

- Configuration for apps:
    - Handled by Secrets and ConfigMaps
        - kubectl create secret generic ngins --from-file nginx.conf

- The problem with containers @20:10
    - Most people are not used to explicitly listing the filepaths that
      the app need
..

----
### Docker
__ What is Docker, what's in it, how it helps:

- Docker is for:
    - separating application from infrastructure

- Docker combines:
    - kernel containerization features
    - workflows and
    - tooling

- Docker helps with:
    - testing
    - deployment
    - shorten time between writing code and running code

- Docker works with:
    - Kubernetes
..
__ Naming in Docker:

- Naming:
    - `Container ID` is a UUID generated by Docker e.g. 73bc1674ee1b
    - `Container Name` is human-readable string e.g. epic_ishizaka
    - `Image` is the docker image e.g. hello-world
    - `Command` is the image command to execute e.g. /hello or bash
..
__ Build a Docker image using a Dockerfile

- Sample dockerfile
    ```
        # Use an official Node runtime as the parent image
        FROM node:6

        # Set the working directory in the container to /app
        WORKDIR /app

        # Copy the current directory contents into the container at /app
        ADD . /app

        # Make the container's port 80 available to the outside world
        EXPOSE 80

        # Run app.js using node when the container launches
        CMD ["node", "app.js"]
    ```

- Notes:
    - All different apps such as NodeJS, etc may have parent Docker Images
        - This simplifies development
    - The /app dir must already exist in the NodeJS image
    - Keywords:
        - FROM, WORKDIR, ADD, EXPOSE, CMD
    - [Dockerfile command reference](https://docs.docker.com/engine/reference/builder/)

- Sample app.js file
    ```
        const http = require('http');
        const hostname = '0.0.0.0';
        const port = 80;
        const server = http.createServer((req, res) => {
            res.statusCode = 200;
              res.setHeader('Content-Type', 'text/plain');
                res.end('Hello World\n');
        });
        server.listen(port, hostname, () => {
            console.log('Server running at http://%s:%s/', hostname, port);
        });
        process.on('SIGINT', function() {
            console.log('Caught interrupt signal and will exit');
            process.exit();
        });
    ```

- Command to build the image (takes under a minute):
    - `docker build -t node-app:0.1 .
        - `-t`: names and tags an image with the name:tag syntax e.g.
          name is `node-app` and tag is `0.1`
    - Creates two docker images:
        - `node` which is the parent image
        - `node-app` which is based on `node
    - Both images are at about 884MB

- List of official node versions
    - https://hub.docker.com/_/node
..
__ Running and stopping a Docker image with port mapping

- Command:
    - `docker run -p 4000:80 --name my-app node-app:0.1`
        - `-p 4000:80` maps local port 4000 to container port 80
        - `--name my-app` specifies the container name
    - `docker run -d ...`
        - `-d` will run in background as daemon
    - `docker stop NAME`
        - stops a running container
    - `docker rm NAME`
        - removes execution history from `docker ps -a` output
..
__ Viewing and tailing outputs:

- Command:
    - `docker logs CONTAINER_ID`
        - tail the STDOUT of CMD
        - For CONTAINER_ID, just type enough to disambiguate the
          different container IDs
    - `docker logs -f CONTAINER_ID`
        - tail -f the STDOUT of CMD
..
__ Debugging containers

- Start an interactive Bash session inside a running container:
    - `docker exec -it CONTAINER_ID bash`
        - `-it` allows interaction with container
            - does this by allocating a pseudo-tty and keeping stdin open
        - bash will run in WORKDIR specified in the Dockerfile

- Inspect container metadata
    - `docker inspect CONTAINER_ID`
    - `docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' CONTAINER_ID`
        - Inspect specific fields
..
__ Publishing to Google Container Registry

- Naming images:
    - hostname for Google Container Registry (gcr) is `gcr.io`
    - project-id is the GCP Project-ID e.g. qwiklabs-gcp-00-98d3951b3b64
    - image is the image name e.g. node-app
    - tag is string of choice e.g. 0.1. Default to "latest" if unspecified

- Tag an image:
    - `docker tag node-app:0.2 gcr.io/$PROJECT_ID/node-app:0.2`
        - `tag` creates a tag, something like an alias

- Publish to GCR
    - `docker push gcr.io/$PROJECT_ID/node-app:0.2`
        - Note that the full name is specified
        - Apparently the target is something like a git repo?
..
__ Clean up Docker environment

- Stop and remove all containers
    - `docker stop $(docker ps -q)`
    - `docker rm $(docker ps -aq)`

- Remove all images
    - `docker rmi node-app:0.2 gcr.io/$PROJECT_ID/node-app node-app:0.1`
    - `docker rmi node:6`
    - `docker rmi $(docker images -aq) # remove remaining images`
    - `docker images`
..
__ Pull an image from gcr.io

- Pull an image:
    - `docker pull gcr.io/[project-id]/node-app:0.2`
        - fetch image from gcr.io
    - `docker run -p 4000:80 -d gcr.io/$PROJECT_ID/node-app:0.2`
        - run image in background
    - `curl http://localhost:4000`
        - Check output
..
__ References:

- Dockerfile command reference:
    - https://docs.docker.com/engine/reference/builder/#known-issues-run

- List of Official Node Images:
    - https://hub.docker.com/_/node

- Docker inspect reference:
    - https://docs.docker.com/engine/reference/commandline/inspect/#examples

- Docker exec reference:
    - https://docs.docker.com/engine/reference/commandline/exec/

- Docker run reference:
    - https://docs.docker.com/engine/reference/run/

- Google Container Registry:
    - https://cloud.google.com/container-registry/

- Specifying zones and buckets for GCR:
    - https://cloud.google.com/container-registry/docs/#pushing_to_the_registry
..

__ Best Practices

- Use small containers
    - Default node image: 670MB
    - node-alpine image: 65MB (10 times smaller)
    - https://www.youtube.com/watch?v=wGz_cbtCiEA

..

__ Dockerfile: node + libreoffice

FROM node:12
RUN apt-get update -y \
    && apt-get install -y libreoffice \
    && apt-get clean
WORKDIR /usr/src/app
COPY package.json package*.json ./
RUN npm install --only=production
COPY . .
CMD [ "npm", "start" ]
..



----
### Google Apps Script
__

- Server-side JS similar to Node.js, focused on tight integration with
  Workspace and other Google services
- To automate work across Google products and third party services
..


----
### Experimenting with Big Datasets
__

- To generate streaming data, one way is to simulate it. [github](https://github.com/GoogleCloudPlatform/training-data-analyst/courses/streaming/publish/send_sensor_data.py)
    - The notion of speedup factor in the code is interesting

- Sources of public datasets:
    - UCI ML Repository
        - Online Retail Data Set [uci](https://archive.ics.uci.edu/ml/datasets/online+retail)

- GCP:
    - data-to-insights ecommerce dataset [gcp](https://console.cloud.google.com/bigquery?project=data-to-insights&page=ecommerce)
..


----
### On Managing Change
__ Intro

- The notion that everything that we are doing is some form or other of
  managing and coping with change
    - This section of the notes try to note the changes and point to
      solutions
..
__ From Batch to Stream Processing

- The truth is business have always wanted stream processing however the
  computing technologies of the past have only been capable of batch
  processing.

..
__ From Flat Workloads to Seasonal Workloads

- Retailers, Movie industries have seasonal workloads
- Food on the other hand has rather flat workload
..


----
### Google Pub/Sub (PubSub)
__

- Pub/Sub
    - 100s of miliseconds latency
    - API: C#, Go, Java, Node, Python, Ruby
    - Save messages for 7 days
    - HIPAA compliance
    - Encrypted in-motion and at-rest
    - At least once semantics
    - Publisher: Pub/Sub Client that creates a Topic
        - Multiple, decoupled Publishers to the same topic
    - Subscriber: Pub/Sub Client that creates a Subscription (to a Topic)
        - A Subscription is only to a single topic
        - Muliple, decoupled Subscriptions to the same topic
    - Pub/Sub is essentially a decoupled enterprise message bus at scale
    - Pull subscriptions for manual pulls by any in a pool of workers
        - This is an interesting pattern

- Subscription
    - Can setup Filters on message attributes

- Patterns:
    - Pass-through:
        - 1 Publisher  -> 1 Topic -> 1 Subscription -> 1 Subscriber
    - Fan-in:
        - N Publishers -> 1 Topic -> 1 Subscription -> M Subscribers
        - All Publisher messages goes to the same Subscription
        - Each subscriber can filter on messages of interest
    - Fan-out:
        - 1 Publisher  -> 1 Topic -> 1 Subscription -> M Subscribers
            - All subscribers get all messages from Publisher
            - i.e. replicate publisher messages to all subscribers

- Push vs Pull deliveries
    - Pull Subscribers must send ACK after getting the Msg
    - Push Subscribers assumed to send ACK on a HTTP 200 OK status
        - Push Subscribers are web-hooks

- Message Replays
    - Allows Pub/Sub to send older messages to new subscribers

- Subcriber Worker Pools
    - Only one worker needs to send an ACK
    - A good pattern for autoscaling workers

- Messages
    - Limit: 10 MB
    - Can send binary data
    - Message attributes are stored separately as metadata to facilliate
      filtering to avoid deserializing

- Publishing
    - Send messages in batches
    - Pub/Sub waits till batch is full
    - Even with batch publishing, it is delivered one at a time to
      subscribers

- Subscribing
    - Message ordering supported if in the same region
    - Configured when creating a Subscription
    - Prevents Denial-of-Service on the push subscriber

- Subscription Delivery
    - Data is held/buffered until application is ready
    - Delivery failures should end-up in a Dead Letter Queue (DLQ)
    - Exponential Backoff implemented for delivery failures for better
      flow control
    - Data may be delivered out-of-order (not a queue)
    - Duplication will happen
    - Dataflow will dedup messages and also handle late data to mitigate
      out-of-order messages

- Write-ups
    - Differences between Google Pub/Sub and Apache Kafka, 2016
      [web](https://www.jesse-anderson.com/2016/07/apache-kafka-and-google-cloud-pubsub/)

..
__ gcloud pubsub

gcloud beta pubsub subscriptions create pdf-conv-sub --topic new-doc --push-endpoint=$SERVICE_URL --push-auth-service-account=pubsub-cloud-run-invoker@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com

    - Create a Pub/Sub subscription that invokes a HTTP endpoint whenever a message is publised on the topic "new-doc"


gcloud pubsub topics create new-lab-report

    - Create a new pubsub topic named `new-lab-report`
..


----
### Dead Letter Queues (DLQ)
__

- A placeholder to DLQ
    - https://developer.confluent.io/learn-kafka/kafka-connect/error-handling-and-dead-letter-queues/

..


----
### Stream Processing
__

- Google Reference Architecture
    - Ingestion: Pub/Sub
    - Stream Processing:
        - Dataflow
            - (ELT|ETL: mostly aggregates & transforms)
            - Also enrichment
    - Storage: BigQuery, Cloud Bigtable
    - Analytics & Visualization: BigQuery

- Unbounded data
    - Characteristics:
        - Infinite dataset
        - Time of data element matters
        - Typically in-motion / held in temporaty storage
    - Contrast with bounded data:
        - Finite dataset
        - Time element usually disregarded
        - Typically at-rest / persisted in durable storage

- Stream Processing Systems
    - Low Latency
    - Speculative results
    - Controls for correctness
..
__ Use Cases

- Online/Real-time decisions (100 ms - 10 s)
    - Real-time recommendations
    - Fraud detection
    - Stock trading
    - ML applications

- Data Integration (10 sec - 10 min)
    - Real-time Data Warehouse Dashboards
    - ML applications:
        - Sentiment analysis
..
__ Challenge: Volume

- The challenge here is that the size of data has increased

- Google proposes autoscaling as a solution here
    - I think that's only if the data increase is seasonal or unpredictable
    - Pub/Sub can autoscale to handle changing volumes of data

..
__ Challenge: Velocity

- The challenge here is that time between each data element is shorter
    - Or more data elements in the same time span
    - Think of Black Friday or online sales days

- Google proposes streaming processing here
    - to handle variability of data arrivals
    - Dataflow handles streaming data
..
__ Challenge: Variety

- Voice data and images is one form of unstructured data

- Google proposes using AI to handle unstructured data

..
__ Solution Architectures

- Google Cloud Platform Solution
    - <img src="img/stream-processing-gcp-solution.png" alt="" width="80%"/>
..
__ Challenge: Late arriving data

- The challenge here is that data could arrive out of order
    - Google Pub/Sub does not guarantee ordering across regions
..
__ Windows in Stream Processing

- Motivation:
    - Aggregation functions typically occurs over a finite window
    - Streams are unbounded
    - Streams are divided into a series of finite windows
        - Think modulus, or the second hand of the clod
        - Making the infinite, finite

- Terms & Abbreviations:
    - DTS: Datetime Stamp
..


----
### Google Dataflow
__

- Dataflow for stream processing
    - Dedups by:
        - Maintaining a list of unique ids seen in the last 10 minutes
    - Supports streaming windows by:
        - Automatically windowing on date-time-stamp (DTS)
        - If there is a significant delay between the timestamp of an
          event and the time the message is actually received, able to
          use a PTransform to update the DTS in the message's metadata
          (which is used for windowing) to use the original event
          timestamp
..
__ Types of Windows

- 

..
__ Watermarks

- The watermark
- A nice talk on streaming processing, watermarks, 2016 [youtube](https://www.youtube.com/watch?v=TWxSLmkWPm4)
    - Motivates the need for stream processing and windows
    - Introduces the notion of low watermarks
    - Benefits of watermarks:
        - Visibility: Knows how much backlog there is
        - Actionability: Once passed the watermark, window is bounded,
          aggregates flushed
    - Formalizes notion of watermarks in a DAG pipeline
    - Inferring Source (PubSub) watermarks from metadata
    - Notion of data watermarks vs system watermarks
    - System watermarks to distinguish between data and system delays
    - Source matermarks are critical
..
__ Custom triggers

- Dataflow triggers window flush in several ways
    - AfterWatermark (Default)
        - Trigger after watermark
    - AfterProcessing
        - Trigger after processing for some time duration
    - AfterCount
        - Trigger after processing N elements

- Can be combined e.g.
    - While batching, trigger several releases using `AfterProcessing`
    - Then on watermark, trigger using `AfterWatermark`
    - And finally, trigger using `AfterCount` for late arriving elements
..


----
### Dimensions of a Solution
__

- Scalability
    - How does the solution handle larger input volumes

- Fault Tolerance
    - How does the solution handle component failures

- Latency
    - How long does it take the solution to convert input into output
..


----
### Change Data Capture
__

- Change data capture (CDC) provides historical change information for a
  user table by capturing both the fact that Data Manipulation Language
  (DML) changes (insert / update / delete) were made and the changed
  data. Changes are captured in real time by using a capture process
  that reads changes from the transaction log and places them in
  corresponding change tables. These change tables provide a historical
  view of the changes made over time to source tables. CDC functions
  enable the change data to be consumed easily and systematically.
    - From [microsoft](https://techcommunity.microsoft.com/t5/azure-sql-blog/stream-data-changes-from-a-cdc-enabled-azure-sql-database-to-an/ba-p/2570907)

- Me: It's making the database transaction log accessible to other
  processes.

..

----
### Good Blogs & Articles & Videos
__

- Stream Processing
    - A nice talk on streaming processing, watermarks, 2016 [youtube](https://www.youtube.com/watch?v=TWxSLmkWPm4)
    - Another talk on Apache Beam, 2016 [youtube](https://www.youtube.com/watch?v=E1k0B9LN46M)
    - Tyler Akidau on Data Processing at Google, 2016 [youtube](https://www.youtube.com/watch?v=9J_cWustI-A)

- Data Quality
    - Wikipedia on Data Quality [web](https://en.wikipedia.org/wiki/Data_quality)
    - Liliendahl on Data Quality [web](https://liliendahl.com/data-quality-3-0)
    - Has a good list of references at the bottom [web](https://profisee.com/data-quality-what-why-how-who/)

- Data Analytics
    - In Government: https://gcn.com/data-analytics/

- Reinforcement Learning
    - Google just gave control over data center cooling to an AI, 2018 [mit](https://www.technologyreview.com/2018/08/17/140987/google-just-gave-control-over-data-center-cooling-to-an-ai/)
    - Grandmaster level in StarCraft II using multi-agent reinforcement learning, 2019 [paper](https://storage.googleapis.com/deepmind-media/research/alphastar/AlphaStar_unformatted.pdf)
..


----
### Kubernetes
__

- Kubernetes
    - For deploying containerized applications
    - Runs on a cluster composed of a master node and worker nodes

- Kubernetes Deployment object
    - An object for deploying stateless applications like web servers

- Kubernetes Service object
    - Defined rules and load balancing for accessing applications from
      the internet
    - No Service means no access from internet
..


----
### Security Credentials
__

- How security credentials typically designed:
    - First, there are credentials, usually made up of a username and
      password
    - Credentials represent an identity
    - An identity may have one or more roles
    - These roles have access permissions
..


----
### Cloud Resources
__

- Naming
    - Use the format `team-resource` e.g. an instance `jupiter-webserver1`

- Compute sizes:
    - f1-micro for small Linux VMS
    - n1-standard-1 for Windows or other applications, such as Kubernetes nodes

..


----
### ETL Design Patterns
__

- Ingest data:
    - On success, move source data to "Archive"
    - On error, flag error, move source data to "Archive"

- Rolling Windows:
    - Make data windows an input parameter
    - Start and end date of the rolling window can be derived from
      job schedule date. Run dates are not suitable because re-runs will
      then not be idempotent.

- Workflow Scheduling
    - Also known as triggering jobs
    - It could be periodic (Pull)
        - This is named Pull cos periodically look into a folder then "Pull"
    - It could be event-driven (Push): e.g. triggered by new file in a folder
        - This is Push because file if Pushed to folder and that triggers

- Articles to research:
    - https://www.leapfrogbi.com/etl-design-patterns-the-foundation/
    - https://www.timmitchell.net/etl-best-practices/
    - https://aws.amazon.com/blogs/big-data/etl-and-elt-design-patterns-for-lake-house-architecture-using-amazon-redshift-part-1/
    - https://docs.microsoft.com/en-us/azure/architecture/data-guide/relational-data/etl
    - https://www.codeproject.com/Articles/5324207/Making-a-Simple-Data-Pipeline-Part-1-The-ETL-Patte
    - https://davewentzel.com/content/performant-etl-and-ssis-patterns/


..


----
### Google Cloud Composer
__

- Managed Apache Airflow as a Service

- What is it: An Orchestrator
    - Orchestrates: Google Cloud Services

- Contrast with: Google Cloud Data Fusion
    - Orchestrates: ETL Steps
..


----
### Google Cloud Functions
__

The function is written in Javascript. Mostly boilerplate code.

..


----
### GCP Billing
__

- Google Cloud Platform Billing is done by projects:
    - A Google Cloud project is an organizing entity for your Google
      Cloud resources. It often contains resources and services; for
      example, it may hold a pool of virtual machines, a set of
      databases, and a network that connects them together. Projects
      also contain settings and permissions, which specify security
      rules and who has access to what resources.
      [web](https://cloud.google.com/docs/overview/#projects)


..


----
### Apache Airflow
__

- Airflow [web](https://airflow.apache.org/)

- Executes tasks on an array of workers e.g.
    - Google Kubernetes engine workers

- DAG [web](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html)
    - A Directed Acyclic Graph is a collection of all the tasks you want
      to run, organized in a way that reflects their relationships and
      dependencies.

- Operator [web](https://airflow.apache.org/docs/apache-airflow/stable/concepts/operators.html)
    - The description of a single task, it is usually atomic. For
      example, the BashOperator is used to execute bash command.

- Task [web](https://airflow.apache.org/docs/apache-airflow/stable/concepts/tasks.html)
    - A parameterised instance of an Operator; a node in the DAG.

- Task Instance [web](https://airflow.apache.org/docs/apache-airflow/stable/concepts/tasks.html#task-instances)
    - A specific run of a task; characterized as: a DAG, a Task, and a
      point in time. It has an indicative state: running, success,
      failed, skipped, ...

- More concepts [web](https://airflow.apache.org/concepts.html#)

- Relies on 'Operators' to invoke services
    - See: https://airflow.apache.org/integration.html

- Airflow workflows are written in Python using 'Operators'
    - Parameterization can be done using macros

- Airflow visually represents the workflow in a Directed Acyclic Graph (DAG)

- Allows multi-cloud integration
    - Unlikely in practice due to egress charges

- Why AirFlow?
    - Visualization of workflow?
    - Visualization has job-completion-status indicators: Green|Pink|Red|etc
    - A simple dashboard of success|failed jobs
        - How to specify window?
    - Easily access logs of failed steps

- Support triggers via POST requests

- Auto retry N times supported
..
__ Resources

- Newcomer's Guide to Airflow's Architecture, 2021
    - https://www.youtube.com/watch?v=oLTMN-4Rvj8
    - Airflow does scheduling of DAGs
    - Airflow runs TaskInstances and records the results
    - DAGs is like a template, when it runs, it's a DagRun
    - An Operator is a Task Template
    - A Task is a parameterized operator in a DAG
    - A TaskInstance is a Task running in a DagRun

- References:
    - Airflow concepts: https://airflow.apache.org/concepts.html#

- Cloud Composer: Good development practices, 2020
    - https://www.youtube.com/watch?v=RrKXZcKOz4A
    - Full compatibility with Apache Airflow
    - Practices
        - Have tasks retry
        - Tasks should be idempotent else retry may not work
        - All work should be in Tasks
        - Use existing operators first
        - Modules: Use PyPi and Composer allows specifying packages
        - Use DAG Run Operator to compose Tasks instead of SubDags
..


----
### Vertex AI
__

- Formerly called Cloud ML Engine

..


----
### Google Cloud Data Fusion
__

- Managed CDAP as a Service

- What is it: An Orchestrator
    - Orchestrates: ETL Steps

..


----
### Azure Data Explorer
__

- Source: Sent from Websites, Application, IoT

- Scales quickly
    - Uses Kusto Query Language, read-only
    - NoSQL under the hood

- Data Collection
    - IoT Hubs
    - Event Hubs
- Ingestion
- Storage
- Indexing structured and non-structured
- Querying
- Visualization: Power BI

- Workflow
    - Create storage: A cluster i.e. an instance of Azure Data Explorer
    - Create database: within cluster
    - Ingest data: loading data into the database
        - Setup automatic ingestion
        - Data is never deleted or updated
    - Query database
..


----
### Batch Data Processing
__

- Google Cloud Data Fusion handles only Batch Processing

..


----
### Cask, CDP, Cloud Data Fusion
__

- Curt Monash on Cask and CDAP 2015 [dbms2](http://www.dbms2.com/2015/03/05/cask-and-cdap/#more-9534)
..


----
### On Maven
__ Naming

- Maven projects are named using Maven UIDs:
    - groupID e.g. com.firexis.com
    - artifactID e.g. someApp
    - version e.g. 0.0.1-SNAPSHOT
..
__

- What is Maven:
    - A build tool that helps in project management
        - Generate source code
        - Generates docs
        - Compiles source code
        - Downloads libraries
        - Packages compiled codes into JAR files
        - Installing packaged code in local repo or central repo
    - Based on Project Object Model (POM)
        - An XML file that contains info regarding project and configuration
          details
        - Essential file is pom.xml
    - Used to build and manage Java-based project. Simplifies daya to
      day work of Java developers

- Maven solves the following problems:
    - Ensure needed JAR files are available
    - Downloads dependencies from mvnrepository.com
    - Creates the right project structure
    - Builds and deploys the project

- Understanding pom.xml
    - https://www.youtube.com/watch?v=KNGQ9JBQWhQ
    - A Project is defined uniquely by:
        - groupID
        - artifactID
        - version
    - Maven UIDs = groupID + artifactID + version
    - Depencies are also refered to via Maven UIDs
    - project
        - The root element in pom.xml
    - parent
        - to inherit from another pom.xml file
    - dependencies
        - container for dependency
    - dependency
        - a Maven UID that the current project depends on
    - build.plugins
        - container for plugins
    - build.plugins.plugin
        - A Maven UID of plugins needed during the build process

- Understanding Maven Archetypes
    - https://www.youtube.com/watch?v=U3AvNVT5j8w
    - A maven template built using Quarkus
        - A repeatedly usable archetype
        - Jackson for serailization
        - Panache for DB access
        - SmallRye OpenAI documentation
        - sonar-maven for Static Code analysis
        - pitest-junit5-plugin for mutation modification tests
..


---
### Google BigQuery
__ Naming

- BigQuery tables are named using:
    - Project ID e.g. qwiklabs-123
    - Dataset ID e.g. Marketing
    - Table Name e.g. Campaign
..
__ Concepts

- Arrays: Vertically compresses several rows into a single field
- Struct: Horizonally compresses several fields into a single field
- Arrays of Struct: Compresses a table into a single field

..
__ Links

- bq CLI [gcp](https://cloud.google.com/bigquery/docs/reference/bq-cli-reference)
- Standard SQL [gcp](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax)
- Interactive SQL translator for Teradata SQL [gcp](https://cloud.google.com/bigquery/docs/interactive-sql-translator)
..
__ Arrays

- finding the number of elements with ARRAY_LENGTH(<array>)
- deduplicating elements with ARRAY_AGG(DISTINCT <field>)
- ordering elements with ARRAY_AGG(<field> ORDER BY <field>)
- limiting ARRAY_AGG(<field> LIMIT 5)
..
__ Example Query:

# Deduplicate the pages and products so you can see how many unique
# products were viewed by adding DISTINCT to ARRAY_AGG()

SELECT
  fullVisitorId,
  date,
  ARRAY_AGG(DISTINCT v2ProductName) AS products_viewed,
  ARRAY_LENGTH(ARRAY_AGG(DISTINCT v2ProductName)) AS distinct_products_viewed,
  ARRAY_AGG(DISTINCT pageTitle) AS pages_viewed,
  ARRAY_LENGTH(ARRAY_AGG(DISTINCT pageTitle)) AS distinct_pages_viewed
  FROM `data-to-insights.ecommerce.all_sessions`
WHERE visitId = 1501570398
GROUP BY fullVisitorId, date
ORDER BY date
..

----
### Compare and contrast technologies
__

- Apache Spark vs Apache Beam
    - allegro.tech experience report, 2021 [web](https://blog.allegro.tech/2021/06/1-task-2-solutions-spark-or-beam.html)
        - A good write-up
        - Conclusion: Dataflow is more expensive, Dataproc is cheaper.
          So, essentially trading Dataflow cost for developer cost
    - A blog article circa 2016 [web](https://mpouttuclarke.wordpress.com/2016/02/06/apache-beam-vs-apache-spark-comparison/)
    - An SO question circa May 2017 [so](https://stackoverflow.com/questions/43581127)
..

----
### Notion of Component Gateway
__

- In Google Cloud Dataproc, there is the notion of a `Component
  Gateway`. It allows tools commonly associated with Apache Spark to be
  connected to the cluster.
- This is interesting in the sense that the backend setup and
  configuration is automated.
..


----
### List of Compatible OS, Hadoop, Spark
__

```
- Debian 10         , Hadoop 3.2, Spark 3.1
- RockyLinux 8      , Hadoop 3.2, Spark 3.1
- Ubuntu 18.04 LTS  , Hadoop 3.2, Spark 3.1

- CentOS 8          , Hadoop 2.10, Spark 2.4
- Debian 10         , Hadoop 2.10, Spark 2.4
- Ubuntu 18.04 LTS  , Hadoop 2.10, Spark 2.4

- Debian 10         , Hadoop 2.9, Spark 2.4
- Ubuntu 18.04 LTS  , Hadoop 2.9, Spark 2.4

- Debian 10         , Hadoop 2.9, Spark 2.3
- Ubuntu 18.04 LTS  , Hadoop 2.9, Spark 2.3
```


..


----
### Other Quick Bites
__

- Hadoop Cluster Size Calculation [web](https://www.youtube.com/watch?v=0ni6i8XkG88)
    - Key items:
        - Est. Overhead: 20% per node
        - Replication Factor contributes 3X
        - Intermediate contributes 1X
        - Est. Compression Factor: 2.3X
        - Est. Utilization Rate: 65%
        - Est. Data Growth Rate
- It's amazing what you can quickly learn online

- Spark Tutorial
    - A great Spark 2.0 demo at Spark SUMMIT 2016 [web](https://www.youtube.com/watch?v=2Qj1b4TruKA)
    - Data Engineering on databricks Demo, 2021 [web](https://www.youtube.com/watch?v=6Q8qPZ7c1O0)
        - Databricks is at v3.4.7 in 2021
    - Contrasts Spark and Hadoop [web](https://www.youtube.com/watch?v=QaoJNXW6SQo)
        - Databricks is a private company by the core developers of Spark
        - RDD: Resilient Distributed Datasets

- Delta Lakes [web](https://delta.io/) | [azure](https://docs.microsoft.com/en-us/azure/databricks/delta/delta-intro)
    - Evolution of Data Lakes and Data Warehouses into Lakehouses

..


----
### Some books on Skillsoft
__

- Snowflake Security: Security Your Snowflake Data Cloud, 2021 [web](https://orange.hosting.lsoft.com/trk/click?ref=znwrbbrs9_6-2e46bx332778x036174&)

..


----
### Columnar Databases
__

- VLDB 2009 Tutorial on Column-Oriented Database Systems [web](http://nms.csail.mit.edu/~stavros/pubs/tutorial2009-column_stores.pdf) | [local](tutorial2009-column_stores.pdf)
    - Interesting slides on what goes on under the hood in columnar databases.

- Inside Capacitor, BigQuery's next generation columnar storage format, 2016 [web](https://cloud.google.com/blog/products/bigquery/inside-capacitor-bigquerys-next-generation-columnar-storage-format)
    - Covers the storage system used in BigQuery
    - Storage system is one major component, the other is the execution engine

- Azure has Columnstore Indexes within SQL Server, 2021 [web](https://web.archive.org/web/20211214211514/https://docs.microsoft.com/en-us/sql/relational-databases/indexes/get-started-with-columnstore-for-real-time-operational-analytics?view=sql-server-ver15)
..


----
### Fun, short intros to Google Cloud offerings
__

- https://github.com/priyankavergadia/google-cloud-4-words
- https://github.com/priyankavergadia/GCPSketchnote
- https://www.youtube.com/playlist?list=PLIivdWyY5sqIQ4_5PwyyXZVdsXr3wYhip
..

----
### Serverless vs Managed Service
__

- Managed Service
    - Means: No setup, no management e.g. backup, replication, scaling
    - Examples:
        - DataProc

- Serverless
    - Means: Managed-Service + Event-driven/API endpoints
    - Examples:
        - BigQuery
        - DataFlow
        - Pub/Sub
        - Cloud Storage
..

----
### On Pseudo Benefits
__

- Pseudo benefits are things that sound like benefits but may not be.
    - An example is the availability of many choices to do something
    - Choices introduces complexity and the need to manage that
      complexity
    - If one selects the simplest option in a bevy of choices and simply
      stick to that, then it may help simplify the entire architecture

- In contrast, the ability to auto-scale is a true benefit
    - But only if you have lots of compute/storage and don't know what
      to do with them
..

----
### On Data Lineage
__

- In a recent development project, one of the things I find nice-to-have
  is the ability to know the call dependency graph.
    - A call stack is the list of function calls leading to the current
      function call. A call dependency graph would be a DAG going
      backwards from the current function to all the functions that can
      possibly call this function.
    - Why is this useful? When there is a problem with a function, the
      function will get modified as part of the fix. Knowing the
      dependency graph is useful because I'll know who will may get
      impacted upstream.
    - Another use of the call dependency graph is to work backwards to
      find impacted services and only restart those services to use the
      updated version of the function.

- How is that related to data lineage?
    - It's analogous. When there is a problem with data downstream. I'd
      like to be able to trace back to how that problem data was
      processed upstream.

..

----
### Roles, Responsiblities, Tasks
__ Types of Roles

- Taking all the different labs highlights a kind of separation:
    - Data Engineers
        - Tools: BigQuery, Data Ingestion, Output
    - Developers
        - Develop apps, website tools, etc
    - Infrastructure
        - Tools: Kubernetes, Jenkins
..
__ Roles and Responsibilities

- Role: Data Engineer
- Responsibilities:
    - Analyze, Explore a dataset
    - Ingest
    - Design Schema
    - Physical Data Design
    - Design and Implement Batch Data Pipelines
    - Design and Implement Streaming Data Pipelines
    - Design and Implement Data Quality Transforms
    - Design and Implement Data Enrichment Transforms
    - Monitoring: Capacity, Performance
    - Modify: ML team wants more data
    - Data access and governance
    - Metadata management
        - Tool: Cloud Data Catalog

- Role: Data Warehouse Engineer
    - Responsiblities:
        - Develop batch data pipelines
        - Develop streaming data pipelines
        - Support adhoc queries, visualization, reporting
        - Support machine learning
        - Manage security and governance

- Role: DBA
    - Responsibilities:
        - Backup & Recovery
            - Design Snapshots for quick recoveries
        - Scaling
        - Managing replicas
        - Encryption
        - Security & Patches
        - Vertical Scaling
        - Horizontal scaling (replicas)
        - Replication and Failover

- Role: ETL Engineer
    - Responsibilities
        - Logging: Log metadata, monitor logs
        - Documentation
        - Develop Load Processes
            - Capture Load Process logs and metadata
    - References:
        - https://www.timmitchell.net/post/2020/12/21/etl-antipattern-ignore-the-logging
..
__ Responsibilities and Tasks

- Physical Data Design
    - Partition
    - Denormalization (1NF?)

- Metadata management
    - Data lineage management
        - Start with adding labels
            - A label is a key, value pair
            - To datasets, tables, views

- Design and Implement Data Quality Transforms (DQT)
    - Roles: Data Engineer
    - Guildeline: Implement DQTs only when poor data quality interferes
      with data analysis and leads to poor business decisions.
    - Types of DQ Issues:
        - Not Valid
            - Problem: Data does not conform to your business rules
            - Example: $7 dollar transaction for standard movie ticket
              price of $10
            - Examples: Out of range, Empty/Null fields
        - Not Accurate
            - Problem: Data does not conform to an objective true value
            - Examples: Lookup issues, Datasets do not exist
        - Not Complete
            - Problem: Unable to analyze full dataset
            - Example: Failed to create, save and store whole datasets
            - Causes: Corrupted Data
        - Not Consistent
            - Problem: Two different computations from data ought to be
              the same but are not, so unable to proceed because do not
              know which to trust
            - Duplicate records
        - Not Uniform
            - Problem: When values in the same column but different rows
              mean different things
            - Example: Value of 10 in one row has the unit meters and the
              other has the unit of feett
    - Common DQ Problems:
        - Invalid data
            - Tools: Filter rows/aggregates invalid data
        - Duplication
        - Uniform
            - SQL CAST()
            - SQL FORMAT() [web](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions#format_string)
    - Common DQ Tasks:
        - Cleanse
        - Match
        - De-dupe
        - Standardize

- Design and Implement Batch Data Pipelines
    - Roles: Data Engineer, Data Warehouse Engineer
    - Choose EL, ELT or ETL
        - Key consideration is how much transformation is needed
    - Design pipeline
    - Design execution triggers
        - Google Tools: Cloud Composer, Cloud Functions, Scheduled queries

- Analyze, Explore a dataset (Data Engineer)
    - Use SQL to quickly analyze, explore a dataset
        - How many tables
        - How many columns
        - Any columns partitioned or clustered
        - What's the data size
        - When was table last updated
        - Unique values per column
        - Null values per column

- Detect and handle late-arriving data
    - Data backfills

- Manage Security (Data Warehouse Engineer)
    - Encryption
    - Authentication
        - Configure accounts
    - Access control
        - Setup roles
            - Configure Read Permissions
            - Configure Write/Update Permissions
        - Assign access to roles
        - Row-level access policy
    - Audit logs (immutable logging)
        - Admin activity, System event, Data access
    - Log Monitoring

- Data access and governance
    - Define roles and authorization
    - Setup IAM roles and permissions
    - Setup Row-level security
    - Setup Authorized Views
    - Setup Access to Dataset, Columns, Rows
    - Restrict columns
    - Sharing Datasets

- Logging (ETL Engineer)
    - Things to log: Admin activity, System Event, Data Access
    - Logging needs to be [immutable](https://towardsdatascience.com/data-mesh-patterns-immutable-change-audit-log-aec93da33648)

- Design Schema (Data Engineer)
    - 

..
__ Case Studies

- You are building data pipelines. Some steps require call an API such
  as the Translate APi to augment/transform data. Another part of the
  pipeline requires processing more suited for procedural programming.
  What do you do:
    - Since the transformations cannot be expressed in SQL or are too
      complex to do in SQL, these transformations should be done in an
      ETL fashion.
    - Build an ETL pipeline
    - Implement the transforms in Dataflow, Dataproc, or use Data Fusion
      GUI to build pipelines

- There are some gaps in historical data. What are you going to do?
    - Discuss with the business users
    - Backfill with augmented data with the same distribution generated
      from the previous three years of data

- Need to batch load historical data. Data is clean and correct:
    - Since data is clean and correct, no further transformation needed
    - Use EL data pipeline
        - File hits Cloud Storage
        - Cloud Function invokes BigQuery load
        - Table appended to
    - To expose loaded file for use:
        - Table stored in private dataset
        - Public view that performs integrity checks
        - SQL query transforms and creates destination public table

- You create an image service. Users upload lots of images. The Vision
  API is used to identify objects in the image. How would you store this
  data for unknown future analysis?
    - The Vision API returns JSON data.
    - Since future use cases is unknown, the raw JSON data and a pointer
      to the original image should be stored.
    - This is an ELT pipeline
    - EL the image and JSON
    - Later, transforms may be applied to query the JSON to extract
      required data
..


----
### Lab: Vertex AI: Predicting Loan Risk with AutoML
__

Sun, 20 Mar 2022 (2h30m / 5 Credits)
- Course: [Google Cloud Big Data and Machine Learning Fundamentals](https://www.cloudskillsboost.google/course_templates/3)

- Goals:
    - Use AutoML to build a machine learning model to predict loan risk
    - 2,050 data points from financial institution
    - AutoML requires minimum 1,000 data points

- Tasks:
    - Task 1: Prepare the training data
    - Task 2: Train your model
    - Task 3: Evaluate the model performance 
    - Task 4: Deploy the model
    - Task 5: Shared Machine Learning (SML) Bearer Token
    - Task 6: Get predictions

- Notes:
    - [Vertex Pricing](https://cloud.google.com/vertex-ai/pricing?_ga=2.181173863.-1790764198.1647754986)
    - [Vertex AI documentation](https://cloud.google.com/ai-platform-unified/docs)
    - [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc)

- Task 1: Prepare the training data
    - Navigation menu > Vertex AI
    - Create dataset name: LoanRisk
    - Upload data options:
        - Upload a local file from your computer.
        - Select files from Cloud Storage.
        - Select data from BigQuery.
    - Import from Cloud Storage:
        - spls/cbl455/loan_risk.csv
    - Generate statistics
        - To see statistics of loans data
            - Total rows: 2,050
            - Age: 2048 distinct values
            - ClientID: 2,050 distinct values
            - Default: 2 distinct values
            - Income: 2050 distinct values
            - Loan: 2050 distinct values

- Task 2: Train your model
    - Strangely, the dataset name expected is "LoanRisk"
    - Set Objective = Classification
    - Model Details:
        - Model name: LoanRisk
        - Target column: Default
        - Advanced Model Options:
            - To determine training vs testing data & setup encryption
    - Training options
        - Specify columns (features) to include in training model
        - Exclude: ClientID
        - Advanced Training Options:
            - Can select different optimization objectives
            - See: https://cloud.google.com/vertex-ai/docs/training/tabular-opt-obj
    - Compute & Pricing
        - Set Budget: 1 (node hours)
            - 1 compute hour is a good start
        - Early Stopping: Enabled
        - Click: Start training

- Task 3: Evaluate the model performance (demo only)
    - This task is demo-only, no real hands-on cos the training takes an hour
    - On [ROC Curve and AUC](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc)
    - Navigate > Vertex AI > Models
    - Click on model trained > Evaluate
    - Possible to manually adjust the confidence threshold
        - <img src="img/notes-confidence-threshold.png" alt="" width="80%"/>
        - In image above, looking at the Precision-recall by threhold
          graph on the right, I'd raise the threshold to about 0.72
          because higher values result in lower recall. But the actual
          change will depend on the business case

- Task 4: Deploy the model (demo only)
    - This task is demo-only, no real hands-on cos the training takes an hour
    - Create and define an endpoint
        - Navigate to model page > Deploy and test
        - Click: Deploy to endpoint
        - Endpoint name: LoanRisk
        - Click: Continue
    - Model settings and monitoring
        - Traffic splitting settings: Unchanged
        - Machine type: n1-standard-8, 8 vCPUs, 30 GiB memory
        - All other settings: Unchanged
        - Click: Deploy

- Task 5: Shared Machine Learning (SML) Bearer Token
    - This is to get a token to use the ML model for prediction
    - Prepare Task 6 before doing the below:
        - Log in to https://gsp-auth-kjyo252taq-uc.a.run.app/
        - Copy token to clipboard
            - Token is available for about 60secs.

- Task 6: Get predictions
    - Setup environment variables needed:
    - AUTH_TOKEN: To access the endpoint
    - ENDPOINT: The ML predict endpoint
    - INPUT_DATA_FILE: Input file containing features as JSON

```
# Download files used
gsutil cp gs://spls/cbl455/cbl455.tar.gz .
tar -xvf cbl455.tar.gz

# Setup environment variables:
AUTH_TOKEN="INSERT_SML_BEARER_TOKEN"
ENDPOINT="https://sml-api-vertex-kjyo252taq-uc.a.run.app/vertex/predict/tabular_classification"
INPUT_DATA_FILE="INPUT-JSON"

# Make request using smlproxy
# smlproxy is a binary executable to communicate with the backend
./smlproxy tabular \
  -a $AUTH_TOKEN \
  -e $ENDPOINT \
  -d $INPUT_DATA_FILE
```
..


----
### Confusion Matrix, Recall and Precision
__

- Confusion Matrix defines the following:
    - True Positive   TP   Predicted 🐈 Cat / Turned out to be 🐈 Cat   ✔️
    - True Negative   TN   Predicted 🐕 Dog / Turned out to be 🐕 Dog   ✔️
    - False Positive  FP   Predicted 🐈 Cat / Turned out to be 🐕 Dog   ❌
    - False Negative  FP   Predicted 🐕 Dog / Turned out to be 🐈 Cat   ❌

- Helps to think of the confusion matrix as follows:
    - Predictions come first, the actual values come later and compared
      to prediction
    - We are typically interested in Positive predictions
    - Hence the Recall and Precision are useful metrics
    - Negative predictions can easily be turned into positive
      predictions

- Recall almost 1     ⇒  Very few false negatives
    - Missed some which were actually positive, hence imperfect recall
    - Like having to recall a list of 16 items, and of the 16 items
      remembered, some were not in the original list. Imperfect recall.
    - TP / (TP + FN)
    - Question: Did you get all of them right?

- Precision almost 1  ⇒  Very few false positives
    - Lots of positive predictions but some turned out to be false
    - Like shooting at real and fake ducks, some ducks turned out to be
      fake, hence imperfect precision
    - TP / (TP + FP)
    - Of all the ones you shot, how many were what you aimed for?
..


----
### First Class Objects
__

- Google Feature Store
    - The Feature Store in Vertex AI has the result of making features
      [first class
      objects](https://www.cs.iusb.edu/~danav/teach/c311/c311_2_firstclass.html)
      in AI. This is just fancy speak for making features the priority.
    - And making it a priority means make it easy to work with, to
      organize, to store, to aggregate, to share, to reuse, etc.
    - This leads to the interesting question:
        - What are the priority objects in different stages of the Data
          Engineering workflow?

- Data Warehouses
    - The first class objects in Data Warehouses should to be schema?
    - Schema should be easy to work with, to organize, to manage
    - Schema should be fluid, composable and all the nice buzzwords
    - Maybe..

..


----
### Lab: [Predicting Visitor Purchases with a Classification Model with BigQuery ML](https://www.cloudskillsboost.google/course_sessions/887252/labs/198828)
__ Tasks

Sat, 19 Mar 2022 (1hr20m 5 Credits)

- Tasks:
    - Task 1. Explore ecommerce data
    - Task 2. Select features and create your training dataset
    - Task 3. Create a BigQuery dataset to store models
    - Task 4. Select a BigQuery ML model type and specify options
    - Task 5. Evaluate classification model performance
    - Task 6. Improve model performance with feature engineering
    - Task 7. Predict which new visitors will come back and purchase
..
__ Notes

- Notes:
    - [Course dataset](https://console.cloud.google.com/bigquery?p=data-to-insights&d=ecommerce&t=web_analytics&page=table)
    - [Field Definitions](https://support.google.com/analytics/answer/3437719?hl=en)
    - [Preview Demo Dataset](https://bigquery.cloud.google.com/table/data-to-insights:ecommerce.web_analytics?tab=preview)
    - Other Models:
        - [Deep Neural Networks](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models)
        - [Boosted Decision Trees (XGBoost)](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree)
        - [AutoML Tables Models](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-create-automl)
        - [Importing Custom TensorFlow Models](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-create-tensorflow)
..
__   Task 1. Explore ecommerce data

- Task 1. Explore ecommerce data
    - Data is already in BigQuery
    - Ask: Out of the total visitors who visited our website, what % made a purchase?

```
-- 1. What % of visitors made a purchase?

#standardSQL
WITH visitors AS(
SELECT
COUNT(DISTINCT fullVisitorId) AS total_visitors
FROM `data-to-insights.ecommerce.web_analytics`
),
purchasers AS(
SELECT
COUNT(DISTINCT fullVisitorId) AS total_purchasers
FROM `data-to-insights.ecommerce.web_analytics`
WHERE totals.transactions IS NOT NULL
)
SELECT
  total_visitors,
  total_purchasers,
  total_purchasers / total_visitors AS conversion_rate
FROM visitors, purchasers


-- 2. What are the top 5 selling products?
SELECT
  p.v2ProductName,
  p.v2ProductCategory,
  SUM(p.productQuantity) AS units_sold,
  ROUND(SUM(p.localProductRevenue/1000000),2) AS revenue
FROM `data-to-insights.ecommerce.web_analytics`,
UNNEST(hits) AS h,
UNNEST(h.product) AS p
GROUP BY 1, 2
ORDER BY revenue DESC
LIMIT 5;

-- 3. How many visitors bought on subsequent visits to the website?
# visitors who bought on a return visit (could have bought on first as well
WITH all_visitor_stats AS (
SELECT
  fullvisitorid, # 741,721 unique visitors
  IF(COUNTIF(totals.transactions > 0 AND totals.newVisits IS NULL) > 0, 1, 0) AS will_buy_on_return_visit
  FROM `data-to-insights.ecommerce.web_analytics`
  GROUP BY fullvisitorid
)
SELECT
  COUNT(DISTINCT fullvisitorid) AS total_visitors,
  will_buy_on_return_visit
FROM all_visitor_stats
GROUP BY will_buy_on_return_visit
```
..
__   Task 2. Select features and create your training dataset

- Task 2. Select features and create your training dataset

```
SELECT
  * EXCEPT(fullVisitorId)
FROM
  # features
  (SELECT
    fullVisitorId,
    IFNULL(totals.bounces, 0) AS bounces,
    IFNULL(totals.timeOnSite, 0) AS time_on_site
  FROM
    `data-to-insights.ecommerce.web_analytics`
  WHERE
    totals.newVisits = 1)
  JOIN
  (SELECT
    fullvisitorid,
    IF(COUNTIF(totals.transactions > 0 AND totals.newVisits IS NULL) > 0, 1, 0) AS will_buy_on_return_visit
  FROM
      `data-to-insights.ecommerce.web_analytics`
  GROUP BY fullvisitorid)
  USING (fullVisitorId)
ORDER BY time_on_site DESC
LIMIT 10;
```
..
__   Task 3. Create a BigQuery dataset to store models

- Task 3. Create a BigQuery dataset to store models
    - Need a dataset to store models
    - Dataset ID: ecommerce
..
__   Task 4. Select a BigQuery ML model type and specify options

- Task 4. Select a BigQuery ML model type and specify options
    - Create a logistic regression model
    - Notice the WHERE clause that splits data into training and evaluation
    - Training takes 5-10 minutes

```
CREATE OR REPLACE MODEL `ecommerce.classification_model`
OPTIONS
(
model_type='logistic_reg',
labels = ['will_buy_on_return_visit']
)
AS
#standardSQL
SELECT
  * EXCEPT(fullVisitorId)
FROM
  # features
  (SELECT
    fullVisitorId,
    IFNULL(totals.bounces, 0) AS bounces,
    IFNULL(totals.timeOnSite, 0) AS time_on_site
  FROM
    `data-to-insights.ecommerce.web_analytics`
  WHERE
    totals.newVisits = 1
    AND date BETWEEN '20160801' AND '20170430') # train on first 9 months
  JOIN
  (SELECT
    fullvisitorid,
    IF(COUNTIF(totals.transactions > 0 AND totals.newVisits IS NULL) > 0, 1, 0) AS will_buy_on_return_visit
  FROM
      `data-to-insights.ecommerce.web_analytics`
  GROUP BY fullvisitorid)
  USING (fullVisitorId)
;
```
..
__   Task 5. Evaluate classification model performance

- Task 5. Evaluate classification model performance
    - Use Receiver Operating Characteristics (ROC) to evaluate
    - Maximize are under the curve (AUC)
    - Notice the WHERE clause now evaluates on two (2) months of data

```
SELECT
  roc_auc,
  CASE
    WHEN roc_auc > .9 THEN 'good'
    WHEN roc_auc > .8 THEN 'fair'
    WHEN roc_auc > .7 THEN 'not great'
  ELSE 'poor' END AS model_quality
FROM
  ML.EVALUATE(MODEL ecommerce.classification_model,  (
SELECT
  * EXCEPT(fullVisitorId)
FROM
  # features
  (SELECT
    fullVisitorId,
    IFNULL(totals.bounces, 0) AS bounces,
    IFNULL(totals.timeOnSite, 0) AS time_on_site
  FROM
    `data-to-insights.ecommerce.web_analytics`
  WHERE
    totals.newVisits = 1
    AND date BETWEEN '20170501' AND '20170630') # eval on 2 months
  JOIN
  (SELECT
    fullvisitorid,
    IF(COUNTIF(totals.transactions > 0 AND totals.newVisits IS NULL) > 0, 1, 0) AS will_buy_on_return_visit
  FROM
      `data-to-insights.ecommerce.web_analytics`
  GROUP BY fullvisitorid)
  USING (fullVisitorId)
));
```
..
__   Task 6. Improve model performance with feature engineering

- Task 6. Improve model performance with feature engineering
    - Add more features:
        - How far the visitor got in the checkout process on their first visit
        - Where visitors came from (traffic source: organic search, referring site etc.)
        - Device category (mobile, tablet, desktop)
        - Geographic information (country)
    - UNNEST() function
        - To break apart ARRAYS into separate rows. Making the table in 1NF (First Normal Form)

```
# Create second model
CREATE OR REPLACE MODEL `ecommerce.classification_model_2`
OPTIONS
  (model_type='logistic_reg', labels = ['will_buy_on_return_visit']) AS
WITH all_visitor_stats AS (
SELECT
  fullvisitorid,
  IF(COUNTIF(totals.transactions > 0 AND totals.newVisits IS NULL) > 0, 1, 0) AS will_buy_on_return_visit
  FROM `data-to-insights.ecommerce.web_analytics`
  GROUP BY fullvisitorid
)
# add in new features
SELECT * EXCEPT(unique_session_id) FROM (
  SELECT
      CONCAT(fullvisitorid, CAST(visitId AS STRING)) AS unique_session_id,
      # labels
      will_buy_on_return_visit,
      MAX(CAST(h.eCommerceAction.action_type AS INT64)) AS latest_ecommerce_progress,
      # behavior on the site
      IFNULL(totals.bounces, 0) AS bounces,
      IFNULL(totals.timeOnSite, 0) AS time_on_site,
      totals.pageviews,
      # where the visitor came from
      trafficSource.source,
      trafficSource.medium,
      channelGrouping,
      # mobile or desktop
      device.deviceCategory,
      # geographic
      IFNULL(geoNetwork.country, "") AS country
  FROM `data-to-insights.ecommerce.web_analytics`,
     UNNEST(hits) AS h
    JOIN all_visitor_stats USING(fullvisitorid)
  WHERE 1=1
    # only predict for new visits
    AND totals.newVisits = 1
    AND date BETWEEN '20160801' AND '20170430' # train 9 months
  GROUP BY
  unique_session_id,
  will_buy_on_return_visit,
  bounces,
  time_on_site,
  totals.pageviews,
  trafficSource.source,
  trafficSource.medium,
  channelGrouping,
  device.deviceCategory,
  country
);


# Evaluate the second model
#standardSQL
SELECT
  roc_auc,
  CASE
    WHEN roc_auc > .9 THEN 'good'
    WHEN roc_auc > .8 THEN 'fair'
    WHEN roc_auc > .7 THEN 'not great'
  ELSE 'poor' END AS model_quality
FROM
  ML.EVALUATE(MODEL ecommerce.classification_model_2,  (
WITH all_visitor_stats AS (
SELECT
  fullvisitorid,
  IF(COUNTIF(totals.transactions > 0 AND totals.newVisits IS NULL) > 0, 1, 0) AS will_buy_on_return_visit
  FROM `data-to-insights.ecommerce.web_analytics`
  GROUP BY fullvisitorid
)
# add in new features
SELECT * EXCEPT(unique_session_id) FROM (
  SELECT
      CONCAT(fullvisitorid, CAST(visitId AS STRING)) AS unique_session_id,
      # labels
      will_buy_on_return_visit,
      MAX(CAST(h.eCommerceAction.action_type AS INT64)) AS latest_ecommerce_progress,
      # behavior on the site
      IFNULL(totals.bounces, 0) AS bounces,
      IFNULL(totals.timeOnSite, 0) AS time_on_site,
      totals.pageviews,
      # where the visitor came from
      trafficSource.source,
      trafficSource.medium,
      channelGrouping,
      # mobile or desktop
      device.deviceCategory,
      # geographic
      IFNULL(geoNetwork.country, "") AS country
  FROM `data-to-insights.ecommerce.web_analytics`,
     UNNEST(hits) AS h
    JOIN all_visitor_stats USING(fullvisitorid)
  WHERE 1=1
    # only predict for new visits
    AND totals.newVisits = 1
    AND date BETWEEN '20170501' AND '20170630' # eval 2 months
  GROUP BY
  unique_session_id,
  will_buy_on_return_visit,
  bounces,
  time_on_site,
  totals.pageviews,
  trafficSource.source,
  trafficSource.medium,
  channelGrouping,
  device.deviceCategory,
  country
)
));
```
..
__   Task 7. Predict which new visitors will come back and purchase

- Task 7. Predict which new visitors will come back and purchase

```
SELECT
*
FROM
  ml.PREDICT(MODEL `ecommerce.classification_model_2`,
   (
WITH all_visitor_stats AS (
SELECT
  fullvisitorid,
  IF(COUNTIF(totals.transactions > 0 AND totals.newVisits IS NULL) > 0, 1, 0) AS will_buy_on_return_visit
  FROM `data-to-insights.ecommerce.web_analytics`
  GROUP BY fullvisitorid
)
  SELECT
      CONCAT(fullvisitorid, '-',CAST(visitId AS STRING)) AS unique_session_id,
      # labels
      will_buy_on_return_visit,
      MAX(CAST(h.eCommerceAction.action_type AS INT64)) AS latest_ecommerce_progress,
      # behavior on the site
      IFNULL(totals.bounces, 0) AS bounces,
      IFNULL(totals.timeOnSite, 0) AS time_on_site,
      totals.pageviews,
      # where the visitor came from
      trafficSource.source,
      trafficSource.medium,
      channelGrouping,
      # mobile or desktop
      device.deviceCategory,
      # geographic
      IFNULL(geoNetwork.country, "") AS country
  FROM `data-to-insights.ecommerce.web_analytics`,
     UNNEST(hits) AS h
    JOIN all_visitor_stats USING(fullvisitorid)
  WHERE
    # only predict for new visits
    totals.newVisits = 1
    AND date BETWEEN '20170701' AND '20170801' # test 1 month
  GROUP BY
  unique_session_id,
  will_buy_on_return_visit,
  bounces,
  time_on_site,
  totals.pageviews,
  trafficSource.source,
  trafficSource.medium,
  channelGrouping,
  device.deviceCategory,
  country
)
)
ORDER BY
  predicted_will_buy_on_return_visit DESC;
```

- Challenge:
    - Use the XGBoost Classifier:
        - Use options/hyperparameters:
            - L2_reg = 0.1
            - num_parallel_tree = 8
            - max_tree-depth = 10
    - Change only one line of SQL
    - See: [Boosted Decision Trees (XGBoost)](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree)

```
# 1. Train the model
CREATE OR REPLACE MODEL `ecommerce.classification_model_3`
        OPTIONS
          (model_type='BOOSTED_TREE_CLASSIFIER' , l2_reg = 0.1, num_parallel_tree = 8, max_tree_depth = 10,
              labels = ['will_buy_on_return_visit']) AS
        WITH all_visitor_stats AS (
        SELECT
          fullvisitorid,
          IF(COUNTIF(totals.transactions > 0 AND totals.newVisits IS NULL) > 0, 1, 0) AS will_buy_on_return_visit
          FROM `data-to-insights.ecommerce.web_analytics`
          GROUP BY fullvisitorid
        )
        # add in new features
        SELECT * EXCEPT(unique_session_id) FROM (
          SELECT
              CONCAT(fullvisitorid, CAST(visitId AS STRING)) AS unique_session_id,
              # labels
              will_buy_on_return_visit,
              MAX(CAST(h.eCommerceAction.action_type AS INT64)) AS latest_ecommerce_progress,
              # behavior on the site
              IFNULL(totals.bounces, 0) AS bounces,
              IFNULL(totals.timeOnSite, 0) AS time_on_site,
              totals.pageviews,
              # where the visitor came from
              trafficSource.source,
              trafficSource.medium,
              channelGrouping,
              # mobile or desktop
              device.deviceCategory,
              # geographic
              IFNULL(geoNetwork.country, "") AS country
          FROM `data-to-insights.ecommerce.web_analytics`,
             UNNEST(hits) AS h
            JOIN all_visitor_stats USING(fullvisitorid)
          WHERE 1=1
            # only predict for new visits
            AND totals.newVisits = 1
            AND date BETWEEN '20160801' AND '20170430' # train 9 months
          GROUP BY
          unique_session_id,
          will_buy_on_return_visit,
          bounces,
          time_on_site,
          totals.pageviews,
          trafficSource.source,
          trafficSource.medium,
          channelGrouping,
          device.deviceCategory,
          country
        );


# 2. Evaluate the model
#standardSQL
SELECT
  roc_auc,
  CASE
    WHEN roc_auc > .9 THEN 'good'
    WHEN roc_auc > .8 THEN 'fair'
    WHEN roc_auc > .7 THEN 'not great'
  ELSE 'poor' END AS model_quality
FROM
  ML.EVALUATE(MODEL ecommerce.classification_model_3,  (
WITH all_visitor_stats AS (
SELECT
  fullvisitorid,
  IF(COUNTIF(totals.transactions > 0 AND totals.newVisits IS NULL) > 0, 1, 0) AS will_buy_on_return_visit
  FROM `data-to-insights.ecommerce.web_analytics`
  GROUP BY fullvisitorid
)
# add in new features
SELECT * EXCEPT(unique_session_id) FROM (
  SELECT
      CONCAT(fullvisitorid, CAST(visitId AS STRING)) AS unique_session_id,
      # labels
      will_buy_on_return_visit,
      MAX(CAST(h.eCommerceAction.action_type AS INT64)) AS latest_ecommerce_progress,
      # behavior on the site
      IFNULL(totals.bounces, 0) AS bounces,
      IFNULL(totals.timeOnSite, 0) AS time_on_site,
      totals.pageviews,
      # where the visitor came from
      trafficSource.source,
      trafficSource.medium,
      channelGrouping,
      # mobile or desktop
      device.deviceCategory,
      # geographic
      IFNULL(geoNetwork.country, "") AS country
  FROM `data-to-insights.ecommerce.web_analytics`,
     UNNEST(hits) AS h
    JOIN all_visitor_stats USING(fullvisitorid)
  WHERE 1=1
    # only predict for new visits
    AND totals.newVisits = 1
    AND date BETWEEN '20170501' AND '20170630' # eval 2 months
  GROUP BY
  unique_session_id,
  will_buy_on_return_visit,
  bounces,
  time_on_site,
  totals.pageviews,
  trafficSource.source,
  trafficSource.medium,
  channelGrouping,
  device.deviceCategory,
  country
)
));


# 3. Make Predictions
SELECT
*
FROM
  ml.PREDICT(MODEL `ecommerce.classification_model_3`,
   (
WITH all_visitor_stats AS (
SELECT
  fullvisitorid,
  IF(COUNTIF(totals.transactions > 0 AND totals.newVisits IS NULL) > 0, 1, 0) AS will_buy_on_return_visit
  FROM `data-to-insights.ecommerce.web_analytics`
  GROUP BY fullvisitorid
)
  SELECT
      CONCAT(fullvisitorid, '-',CAST(visitId AS STRING)) AS unique_session_id,
      # labels
      will_buy_on_return_visit,
      MAX(CAST(h.eCommerceAction.action_type AS INT64)) AS latest_ecommerce_progress,
      # behavior on the site
      IFNULL(totals.bounces, 0) AS bounces,
      IFNULL(totals.timeOnSite, 0) AS time_on_site,
      totals.pageviews,
      # where the visitor came from
      trafficSource.source,
      trafficSource.medium,
      channelGrouping,
      # mobile or desktop
      device.deviceCategory,
      # geographic
      IFNULL(geoNetwork.country, "") AS country
  FROM `data-to-insights.ecommerce.web_analytics`,
     UNNEST(hits) AS h
    JOIN all_visitor_stats USING(fullvisitorid)
  WHERE
    # only predict for new visits
    totals.newVisits = 1
    AND date BETWEEN '20170701' AND '20170801' # test 1 month
  GROUP BY
  unique_session_id,
  will_buy_on_return_visit,
  bounces,
  time_on_site,
  totals.pageviews,
  trafficSource.source,
  trafficSource.medium,
  channelGrouping,
  device.deviceCategory,
  country
)
)
ORDER BY
  predicted_will_buy_on_return_visit DESC;
```
..


----
### Lab: [Set Up Network and HTTP Load Balancers](https://www.cloudskillsboost.google/focuses/12007?parent=catalog)
__

Sat, 19 Mar 2022

- Tasks:
    - Task 1: Set the default region and zone for all resources
    - Task 2: Create multiple web server instances
    - Task 3: Configure the load balancing service
    - Task 4: Sending traffic to your instances
    - Task 5: Create an HTTP load balancer
    - Task 6: Testing traffic sent to your instances

- Notes:
    - The gcloud create instance is quite powerful, allowing arbitrary
      startup scripts e.g. installing apache and customizing the default
      home page
    - `gcloud compute ... create` commands:
        - addresses: Static, public IP address
        - http-health-checks: Health check resource (Legacy)
        - target-pools: Targets for IP Forwarding
        - forwarding-rules: IP Forwarding rule
        - firewall rules: Firewall rule
        - instance-templates: Templates for instances
        - instance-groups managed: Managed instance groups
        - health-checks: Health check resource
        - backend-services: A grouping of instances like target pools
        - url-maps: URL rules to map requests to backend services. This
          is a load balancer!
        - target-http-proxies: HTTP proxy to route requests to url map
    - The step in Task 3 differs from Task 5:
        - Task 3: Load balancing results from using a combination of
          forwarding rules and target pool
        - Task 5: Load balancing results from grouping the instances in
          a `backend service`
        - The target-pool + forwarding-rule in Task 3 maps to
          backend-service + url-map + target-http-proxy in Task 5. One
          more level of indirection
    - Task 5 takes awhile to come up to wait a bit before clicking on
      the `Check my progress` button
    - [YouTube video](https://youtu.be/1ZW59HrRUzw)

- Task 1: Set the default region and zone for all resources
    ```
    gcloud config set compute/zone us-central1-a
    gcloud config set compute/region us-central1
    ```

- Task 2: Create multiple web server instances
    - The `tags` attribute is used to group resources
    - Below, the `network-lb-tag` is common to all three instances
    ```
    # Create web server "www1"
    gcloud compute instances create www1 \
      --image-family debian-9 \
      --image-project debian-cloud \
      --zone us-central1-a \
      --tags network-lb-tag \
      --metadata startup-script="#! /bin/bash
        sudo apt-get update
        sudo apt-get install apache2 -y
        sudo service apache2 restart
        echo '<!doctype html><html><body><h1>www1</h1></body></html>' | tee /var/www/html/index.html"

    # Create web server "www2"
    gcloud compute instances create www2 \
      --image-family debian-9 \
      --image-project debian-cloud \
      --zone us-central1-a \
      --tags network-lb-tag \
      --metadata startup-script="#! /bin/bash
        sudo apt-get update
        sudo apt-get install apache2 -y
        sudo service apache2 restart
        echo '<!doctype html><html><body><h1>www2</h1></body></html>' | tee /var/www/html/index.html"

    # Create web server "www3"
    gcloud compute instances create www3 \
      --image-family debian-9 \
      --image-project debian-cloud \
      --zone us-central1-a \
      --tags network-lb-tag \
      --metadata startup-script="#! /bin/bash
        sudo apt-get update
        sudo apt-get install apache2 -y
        sudo service apache2 restart
        echo '<!doctype html><html><body><h1>www3</h1></body></html>' | tee /var/www/html/index.html"

    # Create firewall rule:
    - Note the value of `target-tags`
    gcloud compute firewall-rules create www-firewall-network-lb \
        --target-tags network-lb-tag --allow tcp:80

    # List each instance to see external IP
    gcloud compute instances list

    # Run curl to check each instance
    curl http://35.224.73.148
    curl http://34.67.240.70
    curl http://35.184.186.55
    ```

- Task 3: Configure the load balancing service
    ```
    # Create a static, public IP for load balancer
    gcloud compute addresses create network-lb-ip-1 \
        --region us-central1

    # Create a legacy HTTP health check resource
    gcloud compute http-health-checks create basic-check

    # Create an empty target pool in the same region and use the
    #   health-check above.
    gcloud compute target-pools create www-pool \
        --region us-central1 --http-health-check basic-check

    # Add compute instances to the pool
    gcloud compute target-pools add-instances www-pool \
        --instances www1,www2,www3

    # Add a forwarding rule. Forwarding requests to the static, public
    # IP to the target pool containing the three web server instances
    gcloud compute forwarding-rules create www-rule \
        --region us-central1 \
        --ports 80 \
        --address network-lb-ip-1 \
        --target-pool www-pool
    ```

- Task 4: Sending traffic to your instances
    ```
    # View the forwarding rule
    gcloud compute forwarding-rules describe www-rule --region us-central1

    # Access the external IP address continuously
    while true; do curl -m1 34.68.108.146; done
    ```

- Task 5: Create an HTTP load balancer
    ```
    # 1. Create an instance template
    gcloud compute instance-templates create lb-backend-template \
       --region=us-central1 \
       --network=default \
       --subnet=default \
       --tags=allow-health-check \
       --image-family=debian-9 \
       --image-project=debian-cloud \
       --metadata=startup-script='#! /bin/bash
         apt-get update
         apt-get install apache2 -y
         a2ensite default-ssl
         a2enmod ssl
         vm_hostname="$(curl -H "Metadata-Flavor:Google" \
         http://169.254.169.254/computeMetadata/v1/instance/name)"
         echo "Page served from: $vm_hostname" | \
         tee /var/www/html/index.html
         systemctl restart apache2'

    # 2. Create a managed instance group using above template:
    gcloud compute instance-groups managed create lb-backend-group \
       --template=lb-backend-template --size=2 --zone=us-central1-a

    # 3. Create a firewall rule. The `target-tags` identify the affected instances
    gcloud compute firewall-rules create fw-allow-health-check \
        --network=default \
        --action=allow \
        --direction=ingress \
        --source-ranges=130.211.0.0/22,35.191.0.0/16 \
        --target-tags=allow-health-check \
        --rules=tcp:80

    # 4a. Create a static, external IP address
    gcloud compute addresses create lb-ipv4-1 \
        --ip-version=IPV4 \
        --global

    # 4b. Note the IP address reserved
    gcloud compute addresses describe lb-ipv4-1 \
        --format="get(address)" \
        --global
        # 34.120.130.89 (xxx)

    # 5. Create a health check for the load balancer
    gcloud compute health-checks create http http-basic-check \
        --port 80

    # 6. Create a backend service
    gcloud compute backend-services create web-backend-service \
        --protocol=HTTP \
        --port-name=http \
        --health-checks=http-basic-check \
        --global

    # 7. Add instance group to backend service
    gcloud compute backend-services add-backend web-backend-service \
        --instance-group=lb-backend-group \
        --instance-group-zone=us-central1-a \
        --global

    # 8. Create a URL map to send requests to backend service. This is
    #    the load balancer!
    gcloud compute url-maps create web-map-http \
        --default-service web-backend-service

    # 9. Create a target HTTP proxy to route requests to URL map
    gcloud compute target-http-proxies create http-lb-proxy \
        --url-map web-map-http

    # 10. Create forwarding rule to send requests to proxy
    gcloud compute forwarding-rules create http-content-rule \
        --address=lb-ipv4-1\
        --global \
        --target-http-proxy=http-lb-proxy \
        --ports=80
    ```

- Task 6: Testing traffic sent to your instances


..

----
### Lab: [Kubernetes Engine: Qwik Start](https://www.cloudskillsboost.google/focuses/878?parent=catalog)
__

Sat, 19 Mar 2022

- Tasks
    - Task 1: Set a default compute zone
    - Task 2: Create a GKE cluster
    - Task 3: Get authentication credentials for the cluster

- Notes:
    - Creating and deleting the cluster takes awhile so best to read
      through the lab in its entirety before starting the lab
    - [`Manage Containerized Apps with Kubernetes Engine`](https://youtu.be/u9nsngvmMK4)

- Task 1: Set a default compute zone
    ```
    # Set default zone
    gcloud config set compute/zone us-central1-a
    ```

- Task 2: Create a GKE cluster
    - A cluster has a cluster master and several workers called nodes
    - Note: Cluster names must start with a letter and end with an
      alphanumeric, and cannot be longer than 40 characters.
    ```
    # Create a cluster
    # gcloud container clusters create [CLUSTER-NAME]
    gcloud container clusters create my-cluster
    ```

- Task 3: Get authentication credentials for the cluster
    - Auth credentials needed to interact with cluster
    ```
    # Get cluster credentials
    # gcloud container clusters get-credentials [CLUSTER-NAME]
    gcloud container clusters get-credentials my-cluster
    ```

- Task 4: Deploy an application to the cluster
    - Lab deploys a hello-app
    - `Deployment` objects are for stateless applications like web servers
    - `Service` objects define rules and load balancing for accessing
      app from the net
    ```
    # Create a new Deployment of 'hello-server' from a pre-defined container image
    kubectl create deployment hello-server --image=gcr.io/google-samples/hello-app:1.0
    # Expect: deployment.apps/hello-server created

    # Create a Service, which exposes app to external traffic
    kubectl expose deployment hello-server --type=LoadBalancer --port 8080
    # Expect: service/hello-server exposed

    # Inspect service:
    kubectl get service
    # Expect: NAME  TYPE    CLUSTER-IP  EXTERNAL-IP    PORT(S)    AGE
    ```

- Task 5: Deleting the cluster
    ```
    # gcloud container clusters delete [CLUSTER-NAME]
    gcloud container clusters delete my-cluster

    ```
- Resources:
..

----
### Lab: [Create a Virtual Machine](https://www.cloudskillsboost.google/focuses/3563?parent=catalog)
__

Sat, 19 Mar 2022

- Tasks
    - Create a virtual machine with the Cloud Console.
    - Create a virtual machine with the gcloud command line.
    - Deploy a web server and connect it to a virtual machine.

- `gcloud`:
    ```
    # List active account name
    gcloud auth list

    # List project ID
    gcloud config list project
    ```

- Typical VM parameters:
    - <img src="img/notes-typical-vm-parameters.png" alt="" width="80%"/>

- Install NGINX web server on a fresh VM
    ```
    sudo su -
    apt-get update
    apt-get install nginx -y

    # Check that nginx is running
    ps auwx | grep nginx
    ```

- Create a VM via cloud shell:
    ```
    gcloud compute instances create gcelab2 --machine-type n1-standard-2 --zone us-central1-f

    # Get help on CLI
    gcloud compute instances create --help

    # Set default zone and region
    gcloud config set compute/zone ...
    gcloud config set compute/region ...

    # SSH connect
    gcloud compute ssh gcelab2 --zone us-central1-f
    ```
..


----
### Lab: [Getting Started with Cloud Shell and gcloud](https://www.cloudskillsboost.google/focuses/563?parent=catalog)
__

Sat, 19 Mar 2022

- Task 1: Configure your environment
    ```
    # See default region and zone
    gcloud config get-value compute/zone
    gcloud config get-value compute/region

    # Describe project
    # gcloud compute project-info describe --project <your_project_ID>
    gcloud compute project-info describe --project qwiklabs-gcp-02-b02d242a3d87

    # Set environment variables:
    # export PROJECT_ID=<your_project_ID>
    export PROJECT_ID=qwiklabs-gcp-02-b02d242a3d87

    # export ZONE=<your_zone>
    export ZONE=us-central1-a

    # Create a VM
    gcloud compute instances create gcelab2 --machine-type n1-standard-2 --zone $ZONE

    - gcloud compute allows you to manage your Compute Engine resources in a format that's simpler than the Compute Engine API.
    - instances create creates a new instance.
    - gcelab2 is the name of the VM.
    - The --machine-type flag specifies the machine type as n1-standard-2.
    - The --zone flag specifies where the VM is created.

    If you omit the --zone flag, the gcloud tool can infer your desired zone based on your default properties. Other required instance settings, such as machine type and image, are set to default values if not specified in the create command.

    # To get help
    gcloud compute instances create --help

    # gcloud help
    gcloud -h
    gcloud config --help

    # List gcloud config
    gcloud config list                  # common user config
    gcloud config list --all            # all config

    # List gcloud components
    gcloud components list
    ```

- Task 2: Install a new component
    ```
    # Install beta components:
    sudo apt-get install google-cloud-sdk

    # Enable gcloud interactive mode:
    gcloud beta interactive

    ```

- Task 3: Connect to VM via SSH
    ```
    gcloud compute ssh gcelab2 --zone $ZONE

    ```
..


----
### A Completion Badge vs A Skill Badge in Quests
__

- A completion badge is given upon completion

- A skill badge is given after an ability is tested

- <img src="img/notes-completion-vs-skill-badge.png" alt="" width="50%"/>
..


----
### Apache Beam and Google DataFlow
__

- How are they related?

- Apache Beam is the program, DataFlow is the engine

- If they were database technologies, Apache Beam would be SQL programs
  and DataFlow would be the database engine running those SQL programs

- There other pipeline runners other than Google DataFlow. But the key
  feature of DataFlow is autoscaling

- See also: https://medium.com/swlh/dataflow-and-apache-beam-the-result-of-a-learning-process-since-mapreduce-c591b2ab180e (TODO)
- Apache Beam video analytics for Football games (28:57m)
    - https://www.youtube.com/watch?v=dPuE30kY6-c
    - Design and create a platform that can handle auto-production and
      broadcasting, for up to hundreds of games per weekend with as
      little time delay as possible
..


----
### Google Cloud Offerings Group
__

- IAM & Admin (Security)
- APIs & Services
- Cloud Offerings e.g. Compute, Storage, Network, BigQuery etc..
..


----
### GSP001 - Creating a Virtual Machine
__

- Course Link:
    - https://www.cloudskillsboost.google/focuses/3563?parent=catalog
    - 40 minutes 1 Credit

- Goals
    - Create a VM on GCP
    - Create a VM using gcloud CLI
    - Deploy an NGinx web server

- Notes on Cloud Shell:
    - A VM loaded with development tools
    - 5GB persistence home directory on Google Cloud
    - In Cloud Console, click on `Activate Cloud Shell` button
    - <img src="img/GSP001_1-cloud-shell.png" alt="" width="80%"/>

- `gcloud`:
    - Docs: https://cloud.google.com/sdk/gcloud
    ```
    List active account names
        gcloud auth list

    List project ID
        gcloud config list project
    ```

- Regions and zones
    - One region has many zones
    - Naming convention: REGION-ZONE
        - Region: us-west1, Zone: a  -->  us-west1-a
        - Region: us-west1, Zone: b  -->  us-west1-b
        - Region: asia-east1, Zone: a  -->  asia-east1-a
        - etc
    - Zones are like data centers (I think)
    - Resources such as VM, Storage, etc live in zones aka data centers
..


----
### List of Google Cloud Quests
__

- BigQuery for Data Warehousing
    - https://www.cloudskillsboost.google/quests/68
    - Fundamental, 6 hours, 5 Credits

- BigQuery Basics for Data Analysts
    - https://www.cloudskillsboost.google/quests/69
    - Fundamental, 5 hours, 2 Credits

- Courses, Quests and Labs for Data Engineer Role:
    - https://www.cloudskillsboost.google/catalog?keywords=&locale=&solution%5B%5D=any&role%5B%5D=data-engineer&skill-badge%5B%5D=any&format%5B%5D=any&level%5B%5D=any&duration%5B%5D=any&language%5B%5D=any

..


----
### Google API Design Guide for Cloud APIs
__

- A good read to understand Google Cloud Design principles
    - https://cloud.google.com/apis/design/
..


----
### Google APIs Explorer
__

- A useful tool to try out Google Cloud APIs
    - https://developers.google.com/apis-explorer/#p/

- A lab to try APIs Explorer
    - https://google.qwiklabs.com/catalog_lab/1241
..


----
### Data Engineer Learning Path

__ Articles on online training

- https://solutionsreview.com/data-management/the-best-data-warehousing-courses-and-online-training/
..
__

- Link:
    - https://www.cloudskillsboost.google/paths/16

- Why take this path
    - To obtain the Google Cloud Data Engineer certification

- Costs:
    - https://www.cloudskillsboost.google/payments/new
    - Buy Advantage Subscription for USD 29 (~ 1000 THB) for a monthly
      subscription and get unlimited credits
    - Possible to get a 1-month free promotion by going to 
        - https://go.qwiklabs.com/qwiklabs-free
        - Click on `Accept the challenge!`
    - <img src="img/labs-accept-the-challenge.png" alt="" width="80%"/>

- Courses and Quests:
    - Estimated Total:
        - 14 Days / 299 Credits
    - A Tour of Google Cloud Hands-On Labs
        - https://www.cloudskillsboost.google/focuses/2794?parent=catalog
        - 45 mins / Free
    - Google Cloud Big Data and Machine Learning Fundamentals
        - https://www.cloudskillsboost.google/course_templates/3
        - 1 day / Introductory / 20 Credits
    - Modernizing Data Lakes and Data Warehouses with Google Cloud
        - https://www.cloudskillsboost.google/course_templates/54
        - 1 day / Advanced / 20 Credits
    - Building Batch Data Pipelines on Google Cloud
        - https://www.cloudskillsboost.google/course_templates/53
        - 1 day / Advanced / 45 Credits
    - Building Resilient Streaming Analytics Systems on Google Cloud
        - https://www.cloudskillsboost.google/course_templates/52
        - 1 day / Advanced / 30 Credits
    - Smart Analytics, Machine Learning, and AI on Google Cloud
        - https://www.cloudskillsboost.google/course_templates/55
        - 1 day / Advanced / 25 Credits
    - Serverless Data Processing with Dataflow: Foundations
        - https://www.cloudskillsboost.google/course_templates/218
        - Advanced / 5 Credits
    - Serverless Data Processing with Dataflow: Develop Pipelines
        - https://www.cloudskillsboost.google/course_templates/229
        - Expert / 70 Credits
    - Serverless Data Processing with Dataflow: Operations
        - https://www.cloudskillsboost.google/course_templates/264
        - Expert / 30 Credits
    - Create and Manage Cloud Resources
        - https://www.cloudskillsboost.google/quests/120
        - 5 hours / Introductory / 6 Credits
    - Perform Foundational Data, ML, and AI Tasks in Google Cloud
        - https://www.cloudskillsboost.google/quests/117
        - 6 hours / Introductory / 16 Credits
    - Engineer Data in Google Cloud
        - https://www.cloudskillsboost.google/quests/132
        - 6 hours / Advanced / 27 Credits
    - Preparing for the Google Cloud Professional Data Engineer Exam
        - Expert / 10 Credits

- Other Relevant Courses and Quests:
    - Google Cloud Essentials
        - https://www.cloudskillsboost.google/quests/23
        - 4 hours / Introductory / 5 Credits
..

__ Microsoft Certifications

- Azure Data Fundamentals DP-900 [skillport](https://acm.skillport.com/skillportfe/main.action?path=summary/BOOKS/157587#browse/12aea111-8721-4ba8-9ceb-c8d382043faf)

- Azure Data Engineer Associate [DP-203] [skillport](https://acm.skillport.com/skillportfe/main.action?path=summary/BOOKS/157587#browse/425ca390-aa45-4de4-b9cd-f746020f076a)

- MCSE: Data Management and Analytics [skillport](https://acm.skillport.com/skillportfe/main.action?path=summary/BOOKS/157587#browse/fd1727c3-3cf1-4b18-9583-7ca5eb852f3b)

- SSIS Design Patterns: https://www.pluralsight.com/courses/ssis-design-patterns-data-warehousing

..

__ AWS

- Data Engineer nano degree
    - https://www.udacity.com/course/data-engineer-nanodegree--nd027
..

__ Databricks Training
..

__ Google

- Google Data Engineer [skillport](https://acm.skillport.com/skillportfe/main.action?path=summary/BOOKS/157587#browse/7bcdd429-959d-4f02-baf8-78edb874b6b5)

..

__ Coursera

- Design and Build a Data Warehouse for Business Intelligence Implementation
    - https://www.coursera.org/learn/data-warehouse-bi-building
- Relational Database Support for Data Warehouses
    - https://www.coursera.org/learn/dwrelational
- Design and Build a Data Warehouse for Business Intelligence Implementation
    - https://www.coursera.org/learn/data-warehouse-bi-building
- Data Warehouse Concepts, Design, and Data Integration
    - https://www.coursera.org/learn/dwdesign
- Data Warehousing for Business Intelligence Specialization
    - https://www.coursera.org/specializations/data-warehousing
..

__ Teradata

- Citizen Data Scientist
    - https://www.teradata.com/University/Citizen-Data-Scientist

- Teradata Certification
    - https://www.teradata.com/University/Certification

..

__ Python

- Faust: Getting Started with Stream Processing
    - https://acm.skillport.com/skillportfe/main.action#summary/COURSES/CDE$110302:_ss_cca:it_pyspwfdj_01_enus

..

__ Apache Flink

- https://flink.apache.org/training.html
- https://data-flair.training/blogs/flink-tutorials-home/

- Introduction to Stateful Stream Processing with Apache Flink
    - https://www.youtube.com/watch?v=DkNeyCW-eH0

..


----
### Unsorted notes from Azure DP-900
__

Notions of:
    - Data Workloads
    - Workload SLAs
    - Workload Classification, Importance and Isolation

- A Graph Database
    - Could be useful for dependency graphs
..


----
### Thailand Data Sources
__

- https://www.dataforthai.com
..

----
### Other Data Sources
__

- NYPD Motor Vehicle Collisions Dataset
    - https://data.cityofnewyork.us/Public-Safety/NYPD-Motor-Vehicle-Collisions/h9gi-nx95

- Twitter API
    - https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api

- London Datastore:
    - https://data.london.gov.uk/dataset/
    - Reports/Dashboards are driven by Tableau
        - https://www.met.police.uk/sd/stats-and-data/met/stop-and-search-dashboard/
        - https://data.london.gov.uk/dataset/mps-stop-and-search-public-dashboard-data

- See also:
    - https://careerfoundry.com/en/blog/data-analytics/where-to-find-free-datasets/
    - https://careerfoundry.com/en/blog/data-analytics/data-analyst-portfolio/
        - Something similar but for data-engineering
..


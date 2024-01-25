from time import sleep
import os
import requests
# import github_action_utils as gha_utils

# with gha_utils.group("My Group"):
#     gha_utils.set_output("test_var", "test_value")
#     gha_utils.save_state("state", "val")

#     gha_utils.debug("Debug message")

#     gha_utils.warning(
#         "Warning message", title="Warning Title", file="example.py",
#         col=1, end_column=2, line=5, end_line=6,
#     )
#     gha_utils.warning("Another warning message")

#     gha_utils.error(
#         "Error message", title="Error Title", file="example.py",
#         col=1, end_column=2, line=1, end_line=2,
#     )
#     gha_utils.notice("Another notice message")

#     gha_utils.append_job_summary("# Hello World")
#     gha_utils.append_job_summary("- Point 1")
#     gha_utils.append_job_summary("- Point 2")

ENDPOINT = 'https://public-api.wordpress.com/wpcom/v2/code-deployment'
WPCOM_CONNECTION_TOKEN = os.environ.get('WPCOM_CONNECTION_TOKEN')
ARTIFACT_URL = os.environ.get('ARTIFACT_URL')
COMMIT_SHA = os.environ.get('COMMIT_SHA')

create_deployment = requests.post(
    ENDPOINT,
    json={
        'commit_sha': COMMIT_SHA,
        'zip_url': ARTIFACT_URL,
    },
    headers={
        'X-WPCOM-Connection-Token': WPCOM_CONNECTION_TOKEN
    }).json()

if create_deployment['code'] != 'deployment_started':
    print("Error starting the deployment", create_deployment['message'])
    exit(1)

while True:
    print("\033c", end="")
    deployment = requests.get(
        ENDPOINT,
        headers={
            'X-WPCOM-Connection-Token': WPCOM_CONNECTION_TOKEN
        }).json()

    for site in deployment['report']:
        print('Deployment for site', site)

        for line in deployment['report'][site]:
            print(line['timestamp'], line['description'])

    if len(deployment['status']['queued']) == 0:
        exit(1 if len(deployment['status']['failed']) > 0 else 0)

    sleep(5)

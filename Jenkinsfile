pipeline {
    agent any

    parameters {
        string(name: 'MAIL_TO', description: 'To recipients')
        string(name: 'MAIL_CC', description: 'CC recipients')
        string(name: 'TITLE', defaultValue: 'MY PROD | Unable to login')
        string(name: 'START_TIME')
        string(name: 'END_TIME', defaultValue: 'N/A')
        string(name: 'CASE_ID')
        string(name: 'DESCRIPTION')
        string(name: 'PRIORITY', defaultValue: '1')
        string(name: 'SEVERITY', defaultValue: 'Critical')
        string(name: 'STATUS', defaultValue: 'In Analysis')
        string(name: 'REPORTED_BY', defaultValue: 'BizTech')
        string(name: 'TEAMS', defaultValue: 'ITSM, Cloud, BizTech')
        string(name: 'LATEST_UPDATE')
        string(name: 'RCA', defaultValue: 'Under investigation')
        string(name: 'RESOLUTION', defaultValue: 'In progress')
    }

    environment {
        SMTP_PASSWORD = credentials('itsm-smtp-password')
    }

    stages {
        stage('Setup') {
            steps {
                sh '''
                  python3 -m venv venv
                  ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Send Incident Notification') {
            steps {
                sh """
                ./venv/bin/python send_incident_mail.py \
                  --to "${MAIL_TO}" \
                  --cc "${MAIL_CC}" \
                  --title "${TITLE}" \
                  --start_time "${START_TIME}" \
                  --end_time "${END_TIME}" \
                  --case_id "${CASE_ID}" \
                  --description "${DESCRIPTION}" \
                  --priority "${PRIORITY}" \
                  --severity "${SEVERITY}" \
                  --status "${STATUS}" \
                  --reported_by "${REPORTED_BY}" \
                  --teams "${TEAMS}" \
                  --latest_update "${LATEST_UPDATE}" \
                  --rca "${RCA}" \
                  --resolution "${RESOLUTION}"
                """
            }
        }
    }
}

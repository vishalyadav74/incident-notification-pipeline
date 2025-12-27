pipeline {
    agent any

    parameters {
        string(name: 'MAIL_TO', description: 'To recipients (comma separated)')
        string(name: 'MAIL_CC', description: 'CC recipients (comma separated)')

        string(name: 'TITLE', defaultValue: 'MY PROD | Unable to login')
        string(name: 'START_TIME')
        string(name: 'END_TIME', defaultValue: 'N/A')
        string(name: 'CASE_ID')
        string(name: 'DESCRIPTION')

        choice(name: 'PRIORITY', choices: ['P1', 'P2', 'P3'])
        choice(name: 'SEVERITY', choices: ['Critical', 'High', 'Medium', 'Low'])
        choice(name: 'STATUS', choices: ['In Analysis', 'Identified', 'Monitoring', 'Resolved'])

        string(name: 'REPORTED_BY', defaultValue: 'BizTech')
        string(name: 'TEAMS', defaultValue: 'ITSM, Cloud, BizTech')

        text(name: 'LATEST_UPDATE')
        text(name: 'RCA', defaultValue: 'Under investigation')
        text(name: 'RESOLUTION', defaultValue: 'In progress')
    }

    stages {

        stage('Send Incident Notification') {
            steps {
                script {
                    // 📄 Load HTML template from repo
                    def htmlTemplate = readFile 'incident_mail.html'

                    // 🔁 Replace placeholders manually
                    htmlTemplate = htmlTemplate
                        .replace('{{ title }}', TITLE)
                        .replace('{{ start_time }}', START_TIME)
                        .replace('{{ end_time }}', END_TIME)
                        .replace('{{ case_id }}', CASE_ID)
                        .replace('{{ description }}', DESCRIPTION)
                        .replace('{{ priority }}', PRIORITY)
                        .replace('{{ severity }}', SEVERITY)
                        .replace('{{ status }}', STATUS)
                        .replace('{{ reported_by }}', REPORTED_BY)
                        .replace('{{ teams }}', TEAMS)
                        .replace('{{ latest_update }}', LATEST_UPDATE)
                        .replace('{{ rca }}', RCA)
                        .replace('{{ resolution }}', RESOLUTION)

                    // ✉️ Send mail using Jenkins Email Extension
                    emailext(
                        subject: "${PRIORITY} Incident | ${TITLE}",
                        body: htmlTemplate,
                        to: MAIL_TO,
                        cc: MAIL_CC,
                        mimeType: 'text/html'
                    )
                }
            }
        }
    }
}

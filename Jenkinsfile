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

                    // ---------- Empty-safe helper ----------
                    def v = { val, defVal = '—' ->
                        (val != null && val.trim()) ? val : defVal
                    }

                    // ---------- Priority based UI ----------
                    def priorityClass = 'p3'
                    def priorityEmoji = '🟢'

                    if (PRIORITY == 'P1') {
                        priorityClass = 'p1'
                        priorityEmoji = '🔴'
                    } else if (PRIORITY == 'P2') {
                        priorityClass = 'p2'
                        priorityEmoji = '🟠'
                    }

                    // ---------- Load & populate HTML ----------
                    def htmlTemplate = readFile 'incident_mail.html'

                    htmlTemplate = htmlTemplate
                        .replace('{{ title }}', v(TITLE))
                        .replace('{{ start_time }}', v(START_TIME))
                        .replace('{{ end_time }}', v(END_TIME, 'N/A'))
                        .replace('{{ case_id }}', v(CASE_ID))
                        .replace('{{ description }}', v(DESCRIPTION))
                        .replace('{{ priority }}', PRIORITY)
                        .replace('{{ severity }}', SEVERITY)
                        .replace('{{ status }}', STATUS)
                        .replace('{{ reported_by }}', v(REPORTED_BY))
                        .replace('{{ teams }}', v(TEAMS))
                        .replace('{{ latest_update }}', v(LATEST_UPDATE))
                        .replace('{{ rca }}', v(RCA))
                        .replace('{{ resolution }}', v(RESOLUTION))
                        .replace('{{ priority_class }}', priorityClass)
                        .replace('{{ priority_emoji }}', priorityEmoji)

                    // ---------- Send Mail ----------
                    emailext(
                        subject: "${priorityEmoji} ${PRIORITY} Incident | ${TITLE}",
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

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

                    // ---------- Safe value helper ----------
                    def safe = { val, defVal = '—' ->
                        (val != null && val.toString().trim()) ? val.toString() : defVal
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

                    def htmlTemplate = readFile 'incident_mail.html'

                    htmlTemplate = htmlTemplate
                        .replace('{{ title }}', safe(TITLE))
                        .replace('{{ start_time }}', safe(START_TIME))
                        .replace('{{ end_time }}', safe(END_TIME, 'N/A'))
                        .replace('{{ case_id }}', safe(CASE_ID))
                        .replace('{{ description }}', safe(DESCRIPTION))
                        .replace('{{ priority }}', safe(PRIORITY))
                        .replace('{{ severity }}', safe(SEVERITY))
                        .replace('{{ status }}', safe(STATUS))
                        .replace('{{ reported_by }}', safe(REPORTED_BY))
                        .replace('{{ teams }}', safe(TEAMS))
                        .replace('{{ latest_update }}', safe(LATEST_UPDATE))
                        .replace('{{ rca }}', safe(RCA))
                        .replace('{{ resolution }}', safe(RESOLUTION))
                        .replace('{{ priority_class }}', safe(priorityClass))
                        .replace('{{ priority_emoji }}', safe(priorityEmoji))

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

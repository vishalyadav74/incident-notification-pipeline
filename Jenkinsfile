pipeline {
    agent any

    parameters {
        string(name: 'MAIL_TO', description: 'To recipients (comma separated)')
        string(name: 'MAIL_CC', description: 'CC recipients (comma separated)')
        string(name: 'BRIDGE_CALL_URL', description: 'Bridge call / Teams / Zoom link')
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

                    // ---------- Priority UI ----------
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

                    // ---------- SAFE replace (NO NULL POSSIBLE) ----------
                    def replaceSafe = { key, val ->
                        htmlTemplate = htmlTemplate.replace(
                            key,
                            (val == null || val.toString().trim() == '') ? '—' : val.toString()
                        )
                    }

                    replaceSafe('{{ title }}', TITLE)
                    replaceSafe('{{ start_time }}', START_TIME)
                    replaceSafe('{{ end_time }}', END_TIME ?: 'N/A')
                    replaceSafe('{{ case_id }}', CASE_ID)
                    replaceSafe('{{ description }}', DESCRIPTION)
                    replaceSafe('{{ priority }}', PRIORITY)
                    replaceSafe('{{ severity }}', SEVERITY)
                    replaceSafe('{{ status }}', STATUS)
                    replaceSafe('{{ reported_by }}', REPORTED_BY)
                    replaceSafe('{{ teams }}', TEAMS)
                    replaceSafe('{{ latest_update }}', LATEST_UPDATE)
                    replaceSafe('{{ rca }}', RCA)
                    replaceSafe('{{ resolution }}', RESOLUTION)
                    replaceSafe('{{ priority_class }}', priorityClass)
                    replaceSafe('{{ priority_emoji }}', priorityEmoji)
                    replaceSafe('{{ bridge_call_url }}', BRIDGE_CALL_URL)

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

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

        // 🔥 WAR ROOM ADDONS
        string(name: 'BRIDGE_CALL_URL', description: 'Teams / Zoom / Bridge call link')
        string(name: 'SLA_REMAINING', description: 'SLA Remaining (e.g. 00:45)')
        choice(name: 'SLA_STATUS', choices: ['GREEN', 'AMBER', 'RED'])
    }

    stages {
        stage('Send Incident Notification') {
            steps {
                script {

                    // ---------- NULL SAFE REPLACER ----------
                    def replaceSafe = { html, key, val, defVal = '—' ->
                        html.replace(
                            key,
                            (val == null || val.toString().trim() == '') ? defVal : val.toString()
                        )
                    }

                    // ---------- LOAD HTML ----------
                    def htmlTemplate = readFile 'incident_mail.html'

                    // ---------- APPLY REPLACEMENTS ----------
                    htmlTemplate = replaceSafe(htmlTemplate, '{{ title }}', TITLE)
                    htmlTemplate = replaceSafe(htmlTemplate, '{{ start_time }}', START_TIME)
                    htmlTemplate = replaceSafe(htmlTemplate, '{{ end_time }}', END_TIME, 'N/A')
                    htmlTemplate = replaceSafe(htmlTemplate, '{{ case_id }}', CASE_ID)
                    htmlTemplate = replaceSafe(htmlTemplate, '{{ description }}', DESCRIPTION)

                    htmlTemplate = replaceSafe(htmlTemplate, '{{ priority }}', PRIORITY)
                    htmlTemplate = replaceSafe(htmlTemplate, '{{ severity }}', SEVERITY)
                    htmlTemplate = replaceSafe(htmlTemplate, '{{ status }}', STATUS)

                    htmlTemplate = replaceSafe(htmlTemplate, '{{ reported_by }}', REPORTED_BY)
                    htmlTemplate = replaceSafe(htmlTemplate, '{{ teams }}', TEAMS)

                    htmlTemplate = replaceSafe(htmlTemplate, '{{ latest_update }}', LATEST_UPDATE)
                    htmlTemplate = replaceSafe(htmlTemplate, '{{ rca }}', RCA)
                    htmlTemplate = replaceSafe(htmlTemplate, '{{ resolution }}', RESOLUTION)

                    // 🔥 WAR ROOM FIELDS
                    htmlTemplate = replaceSafe(htmlTemplate, '{{ bridge_call_url }}', BRIDGE_CALL_URL)
                    htmlTemplate = replaceSafe(htmlTemplate, '{{ sla_remaining }}', SLA_REMAINING)
                    htmlTemplate = replaceSafe(htmlTemplate, '{{ sla_status }}', SLA_STATUS)

                    // ---------- SEND EMAIL ----------
                    emailext(
                        subject: "🚨 ${PRIORITY} INCIDENT | ${TITLE}",
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

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

                    // ---------- Helper: null-safe string ----------
                    def safe = { val, defVal = '—' ->
                        return (val == null || val.toString().trim() == '') ? defVal : val.toString()
                    }

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

                    // ---------- Load HTML ----------
                    def htmlTemplate = readFile 'incident_mail.html'

                    // ---------- Replacement map (NO NULL VALUES) ----------
                    def replacements = [
                        '{{ title }}'          : safe(TITLE),
                        '{{ start_time }}'     : safe(START_TIME),
                        '{{ end_time }}'       : safe(END_TIME, 'N/A'),
                        '{{ case_id }}'        : safe(CASE_ID),
                        '{{ description }}'    : safe(DESCRIPTION),
                        '{{ priority }}'       : safe(PRIORITY),
                        '{{ severity }}'       : safe(SEVERITY),
                        '{{ status }}'         : safe(STATUS),
                        '{{ reported_by }}'    : safe(REPORTED_BY),
                        '{{ teams }}'          : safe(TEAMS),
                        '{{ latest_update }}'  : safe(LATEST_UPDATE),
                        '{{ rca }}'            : safe(RCA),
                        '{{ resolution }}'     : safe(RESOLUTION),
                        '{{ priority_class }}' : priorityClass,
                        '{{ priority_emoji }}' : priorityEmoji
                    ]

                    // ---------- Apply replacements safely ----------
                    replacements.each { key, value ->
                        htmlTemplate = htmlTemplate.replace(key, value)
                    }

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

pipeline {
    agent any

    parameters {
        string(name: 'MAIL_TO')
        string(name: 'MAIL_CC')

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

        string(name: 'BRIDGE_CALL_URL')
    }

    stages {
        stage('Send Incident Notification') {
            steps {
                script {

                    // ---------- SAFE VALUE ----------
                    def safe = { v ->
                        (v == null || v.toString().trim() == '') ? '—' : v.toString()
                    }

                    // ---------- STATUS BADGE ----------
                    def statusBadge = '<span class="badge open">OPEN</span>'
                    if (STATUS == 'Resolved') {
                        statusBadge = '<span class="badge resolved">RESOLVED</span>'
                    }

                    // ---------- BRIDGE / RESOLVED SECTION ----------
                    def bridgeSection = '''
                        <a href="''' + safe(BRIDGE_CALL_URL) + '''" class="bridge-btn">
                            📞 JOIN BRIDGE CALL
                        </a>
                    '''

                    if (STATUS == 'Resolved') {
                        bridgeSection = '''
                        <div class="resolved-box">
                            ✅ Incident has been resolved. Please review the resolution summary above.
                        </div>
                        '''
                    }

                    def html = readFile 'incident_mail.html'

                    // ---------- REPLACEMENTS ----------
                    def values = [
                        '{{ title }}'          : safe(TITLE),
                        '{{ start_time }}'     : safe(START_TIME),
                        '{{ end_time }}'       : safe(END_TIME),
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

                        '{{ bridge_section }}' : bridgeSection,
                        '{{ status_badge }}'   : statusBadge
                    ]

                    values.each { k, v ->
                        html = html.replace(k, v)
                    }

                    emailext(
                        subject: "🚨 ${PRIORITY} INCIDENT | ${TITLE}",
                        body: html,
                        to: MAIL_TO,
                        cc: MAIL_CC,
                        mimeType: 'text/html'
                    )
                }
            }
        }
    }
}

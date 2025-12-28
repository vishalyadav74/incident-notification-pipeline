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

                    def safe = { v ->
                        (v == null || v.toString().trim() == '') ? '—' : v.toString()
                    }

                    // STATUS BADGE
                    def statusBadge = (STATUS == 'Resolved')
                        ? '<span style="background:#22c55e;color:#fff;padding:4px 10px;border-radius:999px;font-size:11px;font-weight:700">RESOLVED</span>'
                        : '<span style="background:#E01E7E;color:#fff;padding:4px 10px;border-radius:999px;font-size:11px;font-weight:700">OPEN</span>'

                    // 👉 JOIN BRIDGE BUTTON ONLY IF NOT RESOLVED
                    def bridgeSection = ''
                    if (STATUS != 'Resolved') {
                        bridgeSection = '''
                          <a href="''' + safe(BRIDGE_CALL_URL) + '''"
                             class="pill-btn pill-danger"
                             target="_blank">
                             📞 JOIN BRIDGE CALL
                          </a>
                        '''
                    }

                    def html = readFile 'incident_mail.html'

                    def values = [
                        '{{ title }}'        : safe(TITLE),
                        '{{ start_time }}'   : safe(START_TIME),
                        '{{ end_time }}'     : safe(END_TIME),
                        '{{ case_id }}'      : safe(CASE_ID),
                        '{{ description }}'  : safe(DESCRIPTION),

                        '{{ priority }}'     : safe(PRIORITY),
                        '{{ severity }}'     : safe(SEVERITY),
                        '{{ status }}'       : safe(STATUS),

                        '{{ reported_by }}'  : safe(REPORTED_BY),
                        '{{ teams }}'        : safe(TEAMS),
                        '{{ latest_update }}': safe(LATEST_UPDATE),
                        '{{ rca }}'          : safe(RCA),
                        '{{ resolution }}'   : safe(RESOLUTION),

                        '{{ bridge_section }}': bridgeSection,
                        '{{ status_badge }}' : statusBadge
                    ]

                    values.each { k, v -> html = html.replace(k, v) }

                    emailext(
                        subject: " ${PRIORITY} INCIDENT | ${TITLE}",
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

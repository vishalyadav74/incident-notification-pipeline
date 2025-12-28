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

                    def safe = { v -> (v == null || v.toString().trim() == '') ? '—' : v.toString() }

                    /* ---------- INTRO MESSAGE ---------- */
                    def introMessage = """
                    Hi All,<br><br>
                    This is to inform you that we are experiencing a <b>${PRIORITY}</b> issue with
                    <b>${TITLE}</b> in the Production environment. Please find the incident details below.
                    """

                    if (STATUS == 'Resolved') {
                        introMessage = """
                        Hi All,<br><br>
                        This is to bring to your kind attention that the <b>${PRIORITY}</b> issue for
                        <b>${TITLE}</b> in the Production environment has been <b>resolved</b> now.
                        Please find the incident details below.
                        """
                    }

                    /* ---------- STATUS BADGE ---------- */
                    def statusBadge = (STATUS == 'Resolved')
                        ? '<span class="status-pill status-resolved">RESOLVED</span>'
                        : '<span class="status-pill status-open">OPEN</span>'

                    /* ---------- JOIN BRIDGE BUTTON (INLINE STYLE) ---------- */
                    def bridgeSection = ''
                    if (STATUS != 'Resolved' && BRIDGE_CALL_URL?.trim()) {
                        bridgeSection = """
                        <div style="margin-top:20px;">
                          <a href="${safe(BRIDGE_CALL_URL)}"
                             target="_blank"
                             style="
                               display:inline-block;
                               background:#b91c1c;
                               color:#ffffff;
                               padding:12px 28px;
                               border-radius:999px;
                               font-size:14px;
                               font-weight:700;
                               text-decoration:none;
                               box-shadow:0 6px 14px rgba(185,28,28,0.45);
                             ">
                             📞 JOIN BRIDGE CALL
                          </a>
                        </div>
                        """
                    }

                    def mailSubject = (STATUS == 'Resolved')
                        ? "RESOLVED | ${PRIORITY} | ${TITLE}"
                        : "INCIDENT | ${PRIORITY} | ${TITLE}"

                    def html = readFile 'incident_mail.html'

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

                        '{{ status_badge }}'   : statusBadge,
                        '{{ intro_message }}'  : introMessage,
                        '{{ bridge_section }}' : bridgeSection
                    ]

                    values.each { k, v -> html = html.replace(k, v) }

                    emailext(
                        subject: mailSubject,
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

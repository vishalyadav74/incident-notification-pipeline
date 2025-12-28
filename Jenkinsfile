stage('Send Incident Notification') {
    steps {
        script {

            def safe = { v -> (v == null || v.toString().trim() == '') ? '—' : v.toString() }

            /* INTRO MESSAGE */
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

            /* STATUS BADGE */
            def statusBadge = (STATUS == 'Resolved')
                ? '<span class="status-pill status-resolved">RESOLVED</span>'
                : '<span class="status-pill status-open">OPEN</span>'

            /* JOIN BRIDGE BUTTON – ONLY WHEN NOT RESOLVED */
            def bridgeSection = ''
            if (STATUS != 'Resolved' && BRIDGE_CALL_URL?.trim()) {
                bridgeSection = """
                <div style="margin-top:20px;">
                  <a href="${safe(BRIDGE_CALL_URL)}"
                     style="display:inline-block;
                            background:#b91c1c;
                            color:#ffffff;
                            padding:12px 28px;
                            border-radius:999px;
                            font-weight:700;
                            text-decoration:none;">
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
                '{{ title }}'         : safe(TITLE),
                '{{ start_time }}'    : safe(START_TIME),
                '{{ end_time }}'      : safe(END_TIME),
                '{{ case_id }}'       : safe(CASE_ID),
                '{{ description }}'   : safe(DESCRIPTION),
                '{{ priority }}'      : safe(PRIORITY),
                '{{ severity }}'      : safe(SEVERITY),
                '{{ status }}'        : safe(STATUS),
                '{{ reported_by }}'   : safe(REPORTED_BY),
                '{{ teams }}'         : safe(TEAMS),
                '{{ latest_update }}' : safe(LATEST_UPDATE),
                '{{ rca }}'           : safe(RCA),
                '{{ resolution }}'    : safe(RESOLUTION),
                '{{ status_badge }}'  : statusBadge,
                '{{ intro_message }}' : introMessage,
                '{{ bridge_section }}': bridgeSection
            ]

            values.each { k, v -> html = html.replace(k, v) }

            writeFile file: 'final_mail.html', text: html

            sh """
              python3 send.py \
                "${mailSubject}" \
                "\$(cat final_mail.html)" \
                "${MAIL_TO}" \
                "${MAIL_CC}"
            """
        }
    }
}

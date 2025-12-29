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

    choice(name: 'PRIORITY', choices: ['P1','P2','P3'])
    choice(name: 'SEVERITY', choices: ['Critical','High','Medium','Low'])
    choice(name: 'STATUS', choices: ['In Analysis','Identified','Monitoring','Resolved'])

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

          def safe = { v -> (v == null || v.toString().trim() == '') ? '' : v.toString() }

          /* INTRO MESSAGE */
          def introMessage = (STATUS == 'Resolved') ?
          """
          Hi All,<br><br>
          This is to bring to your kind attention that the <b>${PRIORITY}</b> issue for
          <b>${TITLE}</b> in the Production environment has been <b>resolved</b>.
          Please find the incident details below.
          """
          :
          """
          Hi All,<br><br>
          This is to inform you that we are experiencing a <b>${PRIORITY}</b> issue with
          <b>${TITLE}</b> in the Production environment.
          """

          /* STATUS BADGE */
          def statusBadge = (STATUS == 'Resolved') ?
          '''
          <span style="display:inline-block;background:#16a34a;color:#fff;
                       padding:6px 14px;border-radius:999px;
                       font-size:12px;font-weight:700;">
            RESOLVED
          </span>
          '''
          :
          '''
          <span style="display:inline-block;background:#b91c1c;color:#fff;
                       padding:6px 14px;border-radius:999px;
                       font-size:12px;font-weight:700;">
            OPEN
          </span>
          '''

          /* ✅ FINAL BRIDGE SECTION LOGIC */
          def bridgeSection = ''

          if (STATUS == 'Resolved') {
            bridgeSection = '''
            <div style="margin-top:16px;
                        font-size:13px;
                        color:#475569;
                        font-style:italic;">
              Check case for complete detail.
            </div>
            '''
          }
          else if (BRIDGE_CALL_URL?.trim()) {
            bridgeSection = """
            <div style="margin-top:20px;">
              <a href="${BRIDGE_CALL_URL}" target="_blank"
                 style="display:inline-block;
                        background:#b91c1c;
                        color:#ffffff;
                        padding:12px 28px;
                        border-radius:999px;
                        font-size:14px;
                        font-weight:700;
                        text-decoration:none;">
                 📞 JOIN BRIDGE CALL
              </a>
            </div>
            """
          }

          def subject = (STATUS == 'Resolved')
            ? "RESOLVED | ${PRIORITY} | ${TITLE}"
            : "INCIDENT | ${PRIORITY} | ${TITLE}"

          def html = readFile 'incident_mail.html'

          [
            '{{ title }}':TITLE,
            '{{ start_time }}':START_TIME,
            '{{ end_time }}':END_TIME,
            '{{ case_id }}':CASE_ID,
            '{{ description }}':DESCRIPTION,
            '{{ priority }}':PRIORITY,
            '{{ severity }}':SEVERITY,
            '{{ status }}':STATUS,
            '{{ reported_by }}':REPORTED_BY,
            '{{ teams }}':TEAMS,
            '{{ latest_update }}':LATEST_UPDATE,
            '{{ rca }}':RCA,
            '{{ resolution }}':RESOLUTION,
            '{{ status_badge }}':statusBadge,
            '{{ intro_message }}':introMessage,
            '{{ bridge_section }}':bridgeSection
          ].each { k,v -> html = html.replace(k, safe(v)) }

          writeFile file: 'final_mail.html', text: html

          sh """
            python3 send.py \
              --subject "${subject}" \
              --to "${MAIL_TO}" \
              --cc "${MAIL_CC}" \
              --body final_mail.html
          """
        }
      }
    }
  }
}

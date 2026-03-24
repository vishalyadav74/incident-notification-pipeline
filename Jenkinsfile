pipeline {
  agent any

  parameters {
    string(name: 'MAIL_TO',   description: 'Recipient email(s), comma-separated')
    string(name: 'MAIL_CC',   description: 'CC email(s), comma-separated')

    string(name: 'TITLE',       defaultValue: 'MY PROD | Unable to login',  description: 'Incident title')
    string(name: 'START_TIME',  description: 'Incident start time')
    string(name: 'END_TIME',    defaultValue: 'N/A',                        description: 'Incident end time (N/A if ongoing)')
    string(name: 'CASE_ID',     description: 'Unique case/ticket ID')
    string(name: 'DESCRIPTION', description: 'Brief description of the incident')

    choice(name: 'PRIORITY',  choices: ['P1', 'P2', 'P3'],                             description: 'Incident priority level')
    choice(name: 'SEVERITY',  choices: ['Critical', 'High', 'Medium', 'Low'],           description: 'Incident severity level')
    choice(name: 'STATUS',    choices: ['In Analysis', 'Identified', 'Monitoring', 'Resolved'], description: 'Current incident status')

    string(name: 'REPORTED_BY', defaultValue: 'BizTech',           description: 'Who reported the incident')
    string(name: 'TEAMS',       defaultValue: 'ITSM, Cloud, BizTech', description: 'Teams involved in resolution')

    text(name: 'LATEST_UPDATE', description: 'Most recent update on the incident')
    text(name: 'RCA',           defaultValue: 'Under investigation', description: 'Root cause analysis')
    text(name: 'RESOLUTION',    defaultValue: 'In progress',         description: 'Resolution details')

    string(name: 'BRIDGE_CALL_URL', description: 'Bridge call URL (leave blank if none)')
  }

  stages {

    stage('Validate Inputs') {
      steps {
        script {
          if (!params.MAIL_TO?.trim()) {
            error("MAIL_TO is required.")
          }
          if (!params.TITLE?.trim()) {
            error("TITLE is required.")
          }
          if (!params.START_TIME?.trim()) {
            error("START_TIME is required.")
          }
          echo "✅ Inputs validated. Preparing incident notification..."
        }
      }
    }

    stage('Send Incident Notification') {
      steps {
        script {

          /* ─── Helper: safely coerce null/empty to '' ─── */
          def safe = { v -> (v == null || v.toString().trim() == '') ? '' : v.toString().trim() }

          def isResolved = (safe(params.STATUS) == 'Resolved')

          /* ─── INTRO MESSAGE ─── */
          def introMessage = isResolved
            ? """Hi All,<br><br>
                 This is to bring to your kind attention that the <b>${safe(params.PRIORITY)}</b> incident
                 <b>${safe(params.TITLE)}</b> in the Production environment has been <b>resolved</b>.
                 Please find the complete incident details below."""
            : """Hi All,<br><br>
                 This is to inform you that we are currently experiencing a <b>${safe(params.PRIORITY)}</b>
                 incident with <b>${safe(params.TITLE)}</b> in the Production environment.
                 Our teams are actively working on resolution. Please find the details below."""

          /* ─── STATUS BADGE ─── */
          def statusBadge = isResolved
            ? """<span style="display:inline-block;background:#16a34a;color:#fff;
                              padding:6px 18px;border-radius:999px;font-size:12px;font-weight:800;
                              letter-spacing:1px;text-transform:uppercase;">
                   ✅ &nbsp;RESOLVED
                 </span>"""
            : """<span style="display:inline-block;background:#dc2626;color:#fff;
                              padding:6px 18px;border-radius:999px;font-size:12px;font-weight:800;
                              letter-spacing:1px;text-transform:uppercase;">
                   🔴 &nbsp;OPEN — ${safe(params.STATUS)}
                 </span>"""

          /* ─── BRIDGE CALL SECTION ─── */
          def bridgeSection = ''
          if (isResolved) {
            bridgeSection = """
              <div style="background:#f0fdf4;border:1px solid #86efac;border-radius:14px;
                          padding:16px 20px;font-size:13px;color:#166534;">
                ✅ &nbsp;<b>Incident has been resolved.</b> Please refer to the case for complete RCA and resolution details.
              </div>"""
          } else if (safe(params.BRIDGE_CALL_URL)) {
            bridgeSection = """
              <div style="background:#fef2f2;border:1px solid #fca5a5;border-radius:14px;padding:20px 24px;text-align:center;">
                <div style="font-size:13px;color:#991b1b;font-weight:600;margin-bottom:14px;">
                  🔴 &nbsp;Active bridge call in progress — join immediately if you are part of the resolution team.
                </div>
                <a href="${safe(params.BRIDGE_CALL_URL)}" target="_blank"
                   style="display:inline-block;background:#dc2626;color:#ffffff;
                          padding:13px 32px;border-radius:999px;font-size:14px;
                          font-weight:800;text-decoration:none;letter-spacing:0.5px;">
                  📞 &nbsp;JOIN BRIDGE CALL
                </a>
              </div>"""
          } else {
            bridgeSection = """
              <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:14px;
                          padding:16px 20px;font-size:13px;color:#64748b;">
                ℹ️ &nbsp;No active bridge call at this time.
              </div>"""
          }

          /* ─── EMAIL SUBJECT ─── */
          def subject = isResolved
            ? "[RESOLVED] ${safe(params.PRIORITY)} | ${safe(params.TITLE)}"
            : "[INCIDENT] ${safe(params.PRIORITY)} | ${safe(params.TITLE)}"

          /* ─── TEMPLATE REPLACEMENT ─── */
          def html = readFile('incident_mail.html')

          def replacements = [
            '{{ title }}'          : safe(params.TITLE),
            '{{ start_time }}'     : safe(params.START_TIME),
            '{{ end_time }}'       : safe(params.END_TIME),
            '{{ case_id }}'        : safe(params.CASE_ID),
            '{{ description }}'    : safe(params.DESCRIPTION),
            '{{ priority }}'       : safe(params.PRIORITY),
            '{{ severity }}'       : safe(params.SEVERITY),
            '{{ status }}'         : safe(params.STATUS),
            '{{ reported_by }}'    : safe(params.REPORTED_BY),
            '{{ teams }}'          : safe(params.TEAMS),
            '{{ latest_update }}'  : safe(params.LATEST_UPDATE),
            '{{ rca }}'            : safe(params.RCA),
            '{{ resolution }}'     : safe(params.RESOLUTION),
            '{{ status_badge }}'   : statusBadge,
            '{{ intro_message }}'  : introMessage,
            '{{ bridge_section }}' : bridgeSection
          ]

          replacements.each { k, v -> html = html.replace(k, v) }

          writeFile(file: 'final_mail.html', text: html)

          echo "📧 Sending notification to: ${params.MAIL_TO}"

          sh """
            python3 send.py \
              --subject "${subject}" \
              --to "${safe(params.MAIL_TO)}" \
              --cc "${safe(params.MAIL_CC)}" \
              --body final_mail.html
          """

          echo "✅ Incident notification dispatched successfully."
        }
      }
    }
  }

  post {
    success {
      echo "🚀 Pipeline completed — notification sent."
    }
    failure {
      echo "❌ Pipeline failed — check logs for details."
    }
  }
}

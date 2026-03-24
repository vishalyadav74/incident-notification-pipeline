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

    choice(name: 'PRIORITY',  choices: ['P1', 'P2', 'P3'],                                       description: 'Incident priority level')
    choice(name: 'SEVERITY',  choices: ['Critical', 'High', 'Medium', 'Low'],                     description: 'Incident severity level')
    choice(name: 'STATUS',    choices: ['In Analysis', 'Identified', 'Monitoring', 'Resolved'],   description: 'Current incident status')

    string(name: 'REPORTED_BY', defaultValue: 'BizTech',              description: 'Who reported the incident')
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
          if (!params.MAIL_TO?.trim())    { error("MAIL_TO is required.")    }
          if (!params.TITLE?.trim())      { error("TITLE is required.")      }
          if (!params.START_TIME?.trim()) { error("START_TIME is required.") }
          echo "Inputs validated. Building incident notification..."
        }
      }
    }

    stage('Send Incident Notification') {
      steps {
        script {

          /* ── Safe coerce: null / blank → empty string ── */
          def safe = { v -> (v == null || v.toString().trim() == '') ? '' : v.toString().trim() }

          def isResolved = (safe(params.STATUS) == 'Resolved')

          /* ════════════════════════════════════
             INTRO MESSAGE
          ════════════════════════════════════ */
          def introMessage = isResolved
            ? """Hi All,<br><br>
This is to inform you that the <b>${safe(params.PRIORITY)}</b> incident
<b>${safe(params.TITLE)}</b> in the Production environment has been <b>resolved</b>.
Please find the complete incident details below."""
            : """Hi All,<br><br>
This is to inform you that we are currently experiencing a <b>${safe(params.PRIORITY)}</b>
incident with <b>${safe(params.TITLE)}</b> in the Production environment.
Our teams are actively working on resolution. Please find the details below."""

          /* ════════════════════════════════════
             STATUS BADGE  (table-based, Outlook-safe)
          ════════════════════════════════════ */
          def statusBadge = isResolved
            ? """<table border="0" cellpadding="0" cellspacing="0">
  <tr>
    <td bgcolor="#16a34a" style="padding:5px 16px;">
      <span style="font-family:Arial,Helvetica,sans-serif;font-size:10px;font-weight:700;
                   color:#ffffff;letter-spacing:2.5px;text-transform:uppercase;">
        RESOLVED
      </span>
    </td>
  </tr>
</table>"""
            : """<table border="0" cellpadding="0" cellspacing="0">
  <tr>
    <td bgcolor="#dc2626" style="padding:5px 16px;">
      <span style="font-family:Arial,Helvetica,sans-serif;font-size:10px;font-weight:700;
                   color:#ffffff;letter-spacing:2.5px;text-transform:uppercase;">
        OPEN &mdash; ${safe(params.STATUS)}
      </span>
    </td>
  </tr>
</table>"""

          /* ════════════════════════════════════
             BRIDGE CALL SECTION  (table-based)
          ════════════════════════════════════ */
          def bridgeSection = ''

          if (isResolved) {
            bridgeSection = """
<table width="100%" border="0" cellpadding="0" cellspacing="0">
  <tr>
    <td bgcolor="#f0fdf4" style="border-left:4px solid #22c55e;padding:13px 18px;">
      <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#166534;">
        <b>Incident resolved.</b> Refer to the case for complete RCA and resolution details.
      </p>
    </td>
  </tr>
</table>"""

          } else if (safe(params.BRIDGE_CALL_URL)) {
            bridgeSection = """
<table width="100%" border="0" cellpadding="0" cellspacing="0">
  <tr>
    <td bgcolor="#fef2f2" style="border-left:4px solid #dc2626;padding:16px 20px;">

      <p style="margin:0 0 14px 0;font-family:Arial,Helvetica,sans-serif;
                font-size:12px;font-weight:700;color:#991b1b;text-align:center;">
        Active bridge call in progress &mdash; join immediately if you are part of the resolution team.
      </p>

      <table border="0" cellpadding="0" cellspacing="0" align="center">
        <tr>
          <td bgcolor="#dc2626" style="padding:11px 28px;">
            <a href="${safe(params.BRIDGE_CALL_URL)}" target="_blank"
               style="font-family:Arial,Helvetica,sans-serif;font-size:13px;font-weight:700;
                      color:#ffffff;text-decoration:none;letter-spacing:0.5px;">
              JOIN BRIDGE CALL
            </a>
          </td>
        </tr>
      </table>

    </td>
  </tr>
</table>"""

          } else {
            bridgeSection = """
<table width="100%" border="0" cellpadding="0" cellspacing="0">
  <tr>
    <td bgcolor="#f8fafc" style="border-left:4px solid #cbd5e1;padding:13px 18px;">
      <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#64748b;">
        No active bridge call at this time.
      </p>
    </td>
  </tr>
</table>"""
          }

          /* ════════════════════════════════════
             EMAIL SUBJECT
          ════════════════════════════════════ */
          def subject = isResolved
            ? "[RESOLVED] ${safe(params.PRIORITY)} | ${safe(params.TITLE)}"
            : "[INCIDENT] ${safe(params.PRIORITY)} | ${safe(params.TITLE)}"

          /* ════════════════════════════════════
             TEMPLATE REPLACEMENT
          ════════════════════════════════════ */
          def html = readFile('incident_mail.html')

          [
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
          ].each { k, v -> html = html.replace(k, v) }

          writeFile(file: 'final_mail.html', text: html)

          echo "Sending notification to: ${params.MAIL_TO}"

          sh """
            python3 send.py \
              --subject "${subject}" \
              --to "${safe(params.MAIL_TO)}" \
              --cc "${safe(params.MAIL_CC)}" \
              --body final_mail.html
          """

          echo "Incident notification dispatched successfully."
        }
      }
    }
  }

  post {
    success { echo "Pipeline completed — notification sent." }
    failure { echo "Pipeline failed — check logs above for details." }
  }
}

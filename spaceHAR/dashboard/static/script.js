let running = false;


/* =================================
   CLOCK
================================= */

function updateClock() {

    const now = new Date();

    const time =
        now.toLocaleTimeString(
            "en-GB",
            {
                hour12: false
            }
        );

    document.getElementById(
        "clock"
    ).textContent = time;
}

setInterval(
    updateClock,
    1000
);

updateClock();



/* =================================
   START
================================= */

async function startExperiment() {

    try {

        const response =
            await fetch(
                "/api/experiment/start",
                {
                    method: "POST"
                }
            );

        const data =
            await response.json();

        if (!data.success) {

            alert(
                data.message
            );

            return;
        }

        document.getElementById(
            "missionState"
        ).textContent =
            "Mission Active";

        updateStatus();

    } catch (error) {

        console.error(error);

        alert(
            "Unable to start mission."
        );
    }
}



/* =================================
   STOP
================================= */

async function stopExperiment() {

    try {

        const response =
            await fetch(
                "/api/experiment/stop",
                {
                    method: "POST"
                }
            );

        const data =
            await response.json();

        if (!data.success) {

            alert(
                data.message
            );
        }

        document.getElementById(
            "missionState"
        ).textContent =
            "Mission Stopped";

        updateStatus();

    } catch (error) {

        console.error(error);
    }
}



/* =================================
   RESET
================================= */

async function resetExperiment() {

    try {

        await fetch(
            "/api/experiment/reset",
            {
                method: "POST"
            }
        );

        document.getElementById(
            "missionState"
        ).textContent =
            "System Ready";

        updateStatus();
        updateEvents();
        updateAlerts();

    } catch (error) {

        console.error(error);
    }
}



/* =================================
   CLEAR ALERTS
================================= */

async function clearAlerts() {

    try {

        await fetch(
            "/api/alerts/clear",
            {
                method: "POST"
            }
        );

        updateAlerts();

    } catch (error) {

        console.error(error);
    }
}



/* =================================
   PROCESS AI
================================= */

async function processActivity() {

    if (!running) {
        return;
    }

    try {

        await fetch(
            "/api/process_activity",
            {
                method: "POST"
            }
        );

    } catch (error) {

        console.error(error);
    }
}



/* =================================
   STATUS
================================= */

async function updateStatus() {

    try {

        const response =
            await fetch(
                "/api/status"
            );

        const data =
            await response.json();


        running =
            data.experiment.running;


        /* Camera */

        const cameraOnline =
            data.camera.running;


        document.getElementById(
            "cameraTelemetry"
        ).textContent =
            cameraOnline
                ? "ONLINE"
                : "OFFLINE";


        document.getElementById(
            "recordingTelemetry"
        ).textContent =
            data.recording.running
                ? "REC"
                : "OFF";


        /* Sidebar */

        document.getElementById(
            "sideStatus"
        ).textContent =
            cameraOnline
                ? "ONLINE"
                : "OFFLINE";


        /* Activity */

        document.getElementById(
            "activity"
        ).textContent =
            data.ai.activity;


        const confidence =
            Math.round(
                data.ai.confidence * 100
            );


        document.getElementById(
            "confidence"
        ).textContent =
            confidence + "%";


        document.getElementById(
            "confidenceBar"
        ).style.width =
            confidence + "%";


        /* Detection */

        document.getElementById(
            "detections"
        ).textContent =
            data.ai.detections.length;


        document.getElementById(
            "tracked"
        ).textContent =
            data.ai.tracks.length;


        /* Experiment */

        document.getElementById(
            "experimentName"
        ).textContent =
            data.experiment.name;


        const progress =
            data.experiment.progress || 0;


        document.getElementById(
            "progress"
        ).textContent =
            progress + "%";


        document.getElementById(
            "progressBar"
        ).style.width =
            progress + "%";


        /* Steps */

        const current =
            data.experiment.current_step;


        const next =
            data.experiment.next_step;


        document.getElementById(
            "currentStep"
        ).textContent =
            current
                ? current.name
                : "Complete";


        document.getElementById(
            "nextStep"
        ).textContent =
            next
                ? next.name
                : "Final Step";


        /* Experiment badge */

        const badge =
            document.getElementById(
                "experimentBadge"
            );


        if (data.experiment.finished) {

            badge.textContent =
                "COMPLETED";

        } else if (running) {

            badge.textContent =
                "RUNNING";

        } else {

            badge.textContent =
                "STANDBY";
        }


        /* Mission state */

        if (running) {

            document.getElementById(
                "missionState"
            ).textContent =
                "Mission Active";

        } else {

            document.getElementById(
                "missionState"
            ).textContent =
                "System Ready";
        }


        /* Alerts count */

        document.getElementById(
            "alertCount"
        ).textContent =
            data.alerts;


    } catch (error) {

        console.error(
            "Status error:",
            error
        );
    }
}



/* =================================
   EVENTS
================================= */

async function updateEvents() {

    try {

        const response =
            await fetch(
                "/api/events"
            );

        const events =
            await response.json();


        const table =
            document.getElementById(
                "events"
            );


        table.innerHTML = "";


        const reversed =
            [...events].reverse();


        if (reversed.length === 0) {

            table.innerHTML = `
                <tr>
                    <td colspan="4">
                        No mission events recorded.
                    </td>
                </tr>
            `;

            return;
        }


        reversed.forEach(
            event => {

                const row =
                    document.createElement(
                        "tr"
                    );


                const time =
                    document.createElement(
                        "td"
                    );

                time.textContent =
                    event.timestamp || "-";


                const type =
                    document.createElement(
                        "td"
                    );

                type.textContent =
                    event.event_type || "-";


                const activity =
                    document.createElement(
                        "td"
                    );

                activity.textContent =
                    event.activity || "-";


                const confidence =
                    document.createElement(
                        "td"
                    );

                confidence.textContent =
                    Math.round(
                        (event.confidence || 0)
                        * 100
                    ) + "%";


                row.appendChild(time);
                row.appendChild(type);
                row.appendChild(activity);
                row.appendChild(confidence);


                table.appendChild(row);

            }
        );


    } catch (error) {

        console.error(
            "Events error:",
            error
        );
    }
}



/* =================================
   ALERTS
================================= */

async function updateAlerts() {

    try {

        const response =
            await fetch(
                "/api/alerts"
            );

        const alerts =
            await response.json();


        const container =
            document.getElementById(
                "alerts"
            );


        container.innerHTML = "";


        if (
            !alerts ||
            alerts.length === 0
        ) {

            container.innerHTML = `
                <div class="empty-state">

                    <span>✓</span>

                    <div>

                        <strong>
                            No active alerts
                        </strong>

                        <small>
                            Mission systems operating normally
                        </small>

                    </div>

                </div>
            `;

            return;
        }


        alerts.slice(0, 10)
            .forEach(
                alert => {

                    const div =
                        document.createElement(
                            "div"
                        );


                    div.className =
                        "alert " +
                        (
                            alert.level ||
                            "warning"
                        );


                    div.innerHTML = `

                        <strong>
                            ${alert.level || "NOTICE"}
                        </strong>

                        <span>
                            ${alert.message}
                        </span>

                        <small>
                            ${alert.timestamp}
                        </small>

                    `;


                    container.appendChild(
                        div
                    );

                }
            );


    } catch (error) {

        console.error(
            "Alerts error:",
            error
        );
    }
}



/* =================================
   AUTO REFRESH
================================= */

setInterval(
    updateStatus,
    1000
);


setInterval(
    updateEvents,
    2000
);


setInterval(
    updateAlerts,
    2000
);


setInterval(
    processActivity,
    1000
);


/* Initial */

updateStatus();
updateEvents();
updateAlerts();